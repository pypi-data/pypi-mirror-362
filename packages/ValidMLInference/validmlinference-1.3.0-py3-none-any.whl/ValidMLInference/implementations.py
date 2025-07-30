import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize
from scipy import stats
import numdifftools as nd
import jax
import jax.numpy as jnp
from jax import grad, jit, hessian
from jaxopt import LBFGS
from functools import partial
import math
import jax.random as jr
import patsy
from patsy import dmatrices
import pandas as pd
from dataclasses import dataclass, field


@dataclass
class RegressionResult:
    coef: np.ndarray
    vcov: np.ndarray
    names: list[str] | None = None

    def summary(self, alpha: float = 0.05) -> pd.DataFrame:
        b = np.asarray(self.coef).ravel()
        V = np.asarray(self.vcov)
        d = b.size


        if self.names is None or len(self.names) != d:
            names = [f"x{i}" for i in range(1, d+1)]
        else:
            names = self.names

        se    = np.sqrt(np.diag(V))
        z     = b / se
        pval  = 2 * (1 - stats.norm.cdf(np.abs(z)))
        lo    = b + stats.norm.ppf(alpha/2)   * se
        hi    = b + stats.norm.ppf(1 - alpha/2) * se

        ci_low_label  = f"{100*(alpha/2):.1f}%"
        ci_high_label = f"{100*(1-alpha/2):.1f}%"

        return pd.DataFrame({
            "Estimate":    b,
            "Std. Error":  se,
            "z value":     z,
            "P>|z|":       pval,
            ci_low_label:  lo,
            ci_high_label: hi
        }, index=names)


def _ols_bca_core(Y, Xhat, fpr, m, target_idx: int = 0):

    Y = np.asarray(Y).ravel()
    X = np.asarray(Xhat)
    if X.ndim == 1:
        X = X.reshape(-1, 1)


    b0, V0, sXX = _ols_core(Y, X, se=True, intercept=False)


    d = X.shape[1]
    A = np.zeros((d, d))
    A[target_idx, target_idx] = 1.0
    Gamma = np.linalg.solve(sXX, A)


    b_corr = b0 + fpr * (Gamma @ b0)
    I = np.eye(d)
    V_corr = (
        (I + fpr * Gamma) @ V0 @ (I + fpr * Gamma).T
        + fpr * (1.0 - fpr) * (Gamma @ (V0 + np.outer(b_corr, b_corr)) @ Gamma.T) / m
    )
    return b_corr, V_corr

def _ols_bcm_core(Y, Xhat, fpr, m, target_idx: int = 0):
    Y = np.asarray(Y).ravel()
    X = np.asarray(Xhat)
    if X.ndim == 1:
        X = X.reshape(-1, 1)


    b0, V0, sXX = _ols_core(Y, X, se=True, intercept=False)


    d = X.shape[1]
    A = np.zeros((d, d))
    A[target_idx, target_idx] = 1.0
    Gamma = np.linalg.solve(sXX, A)


    I = np.eye(d)
    b_corr = np.linalg.inv(I - fpr * Gamma) @ b0
    V_corr = (
        np.linalg.inv(I - fpr * Gamma) @ V0 @ np.linalg.inv(I - fpr * Gamma).T
        + fpr * (1.0 - fpr) * (Gamma @ (V0 + np.outer(b_corr, b_corr)) @ Gamma.T) / m
    )
    return b_corr, V_corr


def ols_bcm_topic(Y, Q, W, S, B, k):
    _b, Gamma, V, d = ols_bc_topic_internal(Y, Q, W, S, B, k)

    eigvals = np.linalg.eigvals(Gamma)
    rho     = np.max(np.abs(eigvals))

    if rho < 1:
        b = np.linalg.solve(np.eye(d) - Gamma, _b)
    else:
        b = (np.eye(d) + Gamma) @ _b

    return b, V

def ols_bca_topic(Y, Q, W, S, B, k):
    _b, Gamma, V, d = ols_bc_topic_internal(Y, Q, W, S, B, k)

    b = (np.eye(d) + Gamma) @ _b

    return b, V

def ols_bc_topic_internal(Y, Q, W, S, B, k):
    Theta = W @ S.T

    Xhat  = np.hstack([Theta, Q])

    d = Xhat.shape[1]

    _b, V, sXX = _ols_core(Y, Xhat)

    n = Y.shape[0] if Y.ndim > 1 else Y.size

    mW = W.mean(axis=0) 
    Bt = B.T                 
    M  = Bt * (Bt @ mW)[:, None]  

    Omega = (
        S @ np.linalg.inv(B @ Bt) @ B
          @ M
          @ np.linalg.inv(B @ Bt)
          @ S.T
        - (Theta.T @ Theta) / n
    )

    A = np.zeros((d, d))
    r = S.shape[0]
    A[:r, :r] = Omega

    Gamma = (k / math.sqrt(n)) * np.linalg.solve(sXX, A)

    return _b, Gamma, V, d


def _one_step_core(Y, Xhat, homoskedastic=False, distribution=None):
    Yj = jnp.asarray(Y).ravel()
    Xj = jnp.asarray(Xhat)
    b_jax, V_jax = _one_step_jax_core(Yj, Xj, homoskedastic, distribution)
    return np.array(b_jax), np.array(V_jax)

@partial(jit, static_argnames=('homoskedastic','distribution'))
def _one_step_jax_core(Y, Xhat, homoskedastic=False, distribution=None):

    def objective(theta):
        return likelihood_unlabeled_jax(Y, Xhat, theta, homoskedastic, distribution)

    theta0 = get_starting_values_unlabeled_jax(Y, Xhat, homoskedastic)
    solver = LBFGS(fun=objective, tol=1e-12, maxiter=500)
    sol = solver.run(theta0)
    th_opt = sol.params

    H = hessian(objective)(th_opt)
    d = Xhat.shape[1]
    b = th_opt[:d]
    V = jnp.linalg.pinv(H)[:d, :d]
    return b, V


def likelihood_unlabeled_jax(Y, Xhat, theta, homoskedastic, distribution=None):

    Y = jnp.ravel(Y)
    d = Xhat.shape[1]
    b, w00, w01, w10, sigma0, sigma1 = theta_to_pars_jax(theta, d, homoskedastic)

    w11 = 1.0 / (1.0 + jnp.exp(theta[d]) + jnp.exp(theta[d+1]) + jnp.exp(theta[d+2]))
    mu = Xhat @ b  # (n,)
    

    pdf = normal_pdf if distribution is None else distribution

    term1_1 = w11 * pdf(Y, mu, sigma1)
    term2_1 = w10 * pdf(Y, mu - b[0], sigma0)

    term1_0 = w01 * pdf(Y, mu + b[0], sigma1)
    term2_0 = w00 * pdf(Y, mu, sigma0)
    indicator = Xhat[:, 0]

    log_term = jnp.where(indicator == 1.0,
                         jnp.log(term1_1 + term2_1),
                         jnp.log(term1_0 + term2_0))
    return -jnp.sum(log_term)

def theta_to_pars_jax(theta, d, homoskedastic):
    b = theta[:d]
    v = theta[d:d+3]
    exp_v = jnp.exp(v)
    w = exp_v / (1.0 + jnp.sum(exp_v))
    sigma0 = jnp.exp(theta[d+3])
    sigma1 = sigma0 if homoskedastic else jnp.exp(theta[d+4])
    return b, w[0], w[1], w[2], sigma0, sigma1

def get_starting_values_unlabeled_jax(Y, Xhat, homoskedastic):
    Y = jnp.ravel(Y)
    Xhat = jnp.asarray(Xhat)

    b = ols_jax(Y, Xhat, se=False)
    u = Y - Xhat @ b
    sigma = jnp.std(u)

    def pdf_func(y, loc, scale):
        return jnp.exp(-0.5 * jnp.square((y - loc) / scale)) / (jnp.sqrt(2 * jnp.pi) * scale)
    mu = Xhat @ b

    cond1 = pdf_func(Y, mu, sigma) > pdf_func(Y, mu - b[0], sigma)
    cond2 = pdf_func(Y, mu + b[0], sigma) > pdf_func(Y, mu, sigma)
    X_imputed = jnp.where(Xhat[:, 0] == 1.0,
                          cond1.astype(jnp.float32),
                          cond2.astype(jnp.float32))
    freq00 = jnp.mean(((Xhat[:, 0] == 0.0) & (X_imputed == 0.0)).astype(jnp.float32))
    freq01 = jnp.mean(((Xhat[:, 0] == 0.0) & (X_imputed == 1.0)).astype(jnp.float32))
    freq10 = jnp.mean(((Xhat[:, 0] == 1.0) & (X_imputed == 0.0)).astype(jnp.float32))
    freq11 = jnp.mean(((Xhat[:, 0] == 1.0) & (X_imputed == 1.0)).astype(jnp.float32))
    w00 = jnp.maximum(freq00, 0.001)
    w01 = jnp.maximum(freq01, 0.001)
    w10 = jnp.maximum(freq10, 0.001)
    w11 = jnp.maximum(freq11, 0.001)
    w = jnp.array([w00, w01, w10, w11])
    w = w / jnp.sum(w)
    v = jnp.log(w[:3] / w[3])

    mask0 = (X_imputed == 0.0)
    mask1 = (X_imputed == 1.0)
    sigma0 = subset_std(u, mask0)
    sigma1 = subset_std(u, mask1)
    sigma0 = jnp.where(jnp.isnan(sigma0), sigma1, sigma0)
    sigma1 = jnp.where(jnp.isnan(sigma1), sigma0, sigma1)
    if homoskedastic:
        p_val = jnp.mean(X_imputed)
        sigma_comb = sigma1 * p_val + sigma0 * (1.0 - p_val)
        return jnp.concatenate([b, v, jnp.array([jnp.log(sigma_comb)])])
    else:
        return jnp.concatenate([b, v, jnp.array([jnp.log(sigma0), jnp.log(sigma1)])])

def _ols_core(Y, X, se=True, intercept=False):  

    Y = np.asarray(Y).flatten()
    X = np.asarray(X)


    if X.ndim == 1:
        X = X.reshape(-1, 1)

    if intercept:
        ones = np.ones((X.shape[0], 1))
        X = np.concatenate([X, ones], axis=1)

    n, d = X.shape
    sXX  = (1.0 / n) * (X.T @ X)
    sXY  = (1.0 / n) * (X.T @ Y)
    b    = np.linalg.solve(sXX, sXY)

    if not se:

        if intercept:
            b = np.concatenate(([b[-1]], b[:-1]))
        return b


    Omega = np.zeros((d, d))
    for i in range(n):
        x_i = X[i]
        u   = Y[i] - x_i @ b
        Omega += (u**2) * np.outer(x_i, x_i)

    inv_sXX = np.linalg.inv(sXX)
    V       = inv_sXX @ Omega @ inv_sXX / (n**2)


    if intercept:
        b, V = _reorder_intercept_first(b, V, True)

    return b, V, sXX
    
def ols_jax(Y, X, se=True):

    Y = jnp.ravel(Y)
    X = jnp.asarray(X)
    n, d = X.shape
    sXX = (1.0 / n) * (X.T @ X)
    sXY = (1.0 / n) * (X.T @ Y)
    b = jnp.linalg.solve(sXX, sXY)
    if se:

        residuals = Y - X @ b
        # Compute Omega = sum_i [u_i^2 * (x_i x_i^T)]
        Omega = jnp.sum(jnp.einsum('ni,nj->nij', X, X) * (residuals**2)[:, None, None], axis=0)
        inv_sXX = jnp.linalg.inv(sXX)
        V = inv_sXX @ Omega @ inv_sXX / (n**2)
        return b, V, sXX
    else:
        return b


def log_normal_pdf(x, loc, scale):
    return -0.5 * jnp.log(2 * jnp.pi) - jnp.log(scale) - 0.5 * jnp.square((x - loc) / scale)

def normal_pdf(x, loc, scale):
    return jnp.exp(log_normal_pdf(x, loc, scale))

def subset_std(x, mask):

    mask = mask.astype(jnp.float32)
    mean_val = jnp.sum(x * mask) / jnp.sum(mask)
    var = jnp.sum(mask * jnp.square(x - mean_val)) / jnp.sum(mask)
    return jnp.sqrt(var)

def one_step_unlabeled(Y, Xhat, homoskedastic=False, distribution=None, intercept =True):
    print("one_step_unlabeled is deprecated, instead, call the one_step function.")


def mixture_pdf(x, weights, means, sigmas):

    diffs = (x[..., None] - means) / sigmas
    comp = jnp.exp(-0.5 * diffs**2) / (jnp.sqrt(2*jnp.pi) * sigmas)
    return jnp.sum(weights * comp, axis=-1)

def unpack_theta(θ, d, k, homosked):

    i = 0
    b = θ[i:i+d]; i += d


    v = θ[i:i+3]; i += 3
    w_all = jax.nn.softmax(jnp.concatenate([v, jnp.zeros(1)]))
    w00, w01, w10, w11 = w_all


    v0 = θ[i:i+(k-1)]; i += (k-1)
    ω0 = jax.nn.softmax(jnp.concatenate([v0, jnp.zeros(1)]))


    v1 = θ[i:i+(k-1)]; i += (k-1)
    ω1 = jax.nn.softmax(jnp.concatenate([v1, jnp.zeros(1)]))


    m0p = θ[i:i+(k-1)]; i += (k-1)
    μ0  = jnp.concatenate([jnp.cumsum(m0p), jnp.zeros(1)])
    μ0  = μ0 - jnp.dot(ω0, μ0)

    m1p = θ[i:i+(k-1)]; i += (k-1)
    μ1  = jnp.concatenate([jnp.cumsum(m1p), jnp.zeros(1)])
    μ1  = μ1 - jnp.dot(ω1, μ1)


    logs0 = θ[i:i+k]; i += k
    σ0    = jnp.exp(logs0)
    if homosked:
        σ1 = σ0
    else:
        logs1 = θ[i:i+k]; i += k
        σ1    = jnp.exp(logs1)

    return (b, (w00,w01,w10,w11), ω0, ω1, μ0, μ1, σ0, σ1)

def get_starting_values_unlabeled_gaussian_mixture(Y, Xhat, k, homosked):
    Y = jnp.asarray(Y).ravel()
    Xhat = jnp.asarray(Xhat)
    if Xhat.ndim == 1:
        Xhat = Xhat[:, None]
    n, d = Xhat.shape

    b = ols_jax(Y, Xhat, se=False)
    
    u = Y - Xhat @ b
    sigma = jnp.std(u)
    
    μ = Xhat @ b
    treatment_effect = b[0]  
    
    p11 = jnp.exp(-0.5 * jnp.square((Y - μ) / sigma)) / (jnp.sqrt(2 * jnp.pi) * sigma)
    p10 = jnp.exp(-0.5 * jnp.square((Y - (μ - treatment_effect)) / sigma)) / (jnp.sqrt(2 * jnp.pi) * sigma)
    p01 = jnp.exp(-0.5 * jnp.square((Y - (μ + treatment_effect)) / sigma)) / (jnp.sqrt(2 * jnp.pi) * sigma)
    p00 = jnp.exp(-0.5 * jnp.square((Y - μ) / sigma)) / (jnp.sqrt(2 * jnp.pi) * sigma)
    
    is_treated = (Xhat[:, 0] == 1.0)
    X_imputed = jnp.where(is_treated, 
                         (p11 > p10).astype(jnp.float32),
                         (p01 > p00).astype(jnp.float32))
    
    mask00 = (Xhat[:, 0] == 0) & (X_imputed == 0)
    mask01 = (Xhat[:, 0] == 0) & (X_imputed == 1)
    mask10 = (Xhat[:, 0] == 1) & (X_imputed == 0)
    mask11 = (Xhat[:, 0] == 1) & (X_imputed == 1)
    
    w00 = jnp.maximum(mask00.mean(), 1e-3)
    w01 = jnp.maximum(mask01.mean(), 1e-3)
    w10 = jnp.maximum(mask10.mean(), 1e-3)
    w11 = jnp.maximum(mask11.mean(), 1e-3)
    
    w = jnp.array([w00, w01, w10, w11])
    w = w / jnp.sum(w)
    
    v = jnp.log(w[:3] / w[3])
    
    u0 = u[X_imputed == 0]
    u1 = u[X_imputed == 1]
    σ0_base = jnp.where(u0.size > 0, jnp.std(u0), sigma)
    σ1_base = jnp.where(u1.size > 0, jnp.std(u1), sigma)
    

    σ0_base = jnp.where(jnp.isnan(σ0_base), σ1_base, σ0_base)
    σ1_base = jnp.where(jnp.isnan(σ1_base), σ0_base, σ1_base)
    
    if homosked:

        v0 = jnp.zeros(k-1) + 0.01 * jnp.arange(k-1)  
        
        mean_increments = 0.1 * jnp.arange(k-1)  
        μ0 = mean_increments
        
        p_val = jnp.mean(X_imputed)
        σ_combined = σ1_base * p_val + σ0_base * (1.0 - p_val)
        σ0_log = jnp.log(σ_combined) * jnp.ones(k)
        
        return jnp.concatenate([
            b,                    
            v,                    
            v0,                   
            μ0,                   
            σ0_log               
        ])
    
    else:
        v0 = jnp.zeros(k-1) + 0.01 * jnp.arange(k-1)
        v1 = jnp.zeros(k-1) + 0.01 * jnp.arange(k-1) * 0.5 
        mean_increments_0 = 0.1 * jnp.arange(k-1)
        mean_increments_1 = 0.15 * jnp.arange(k-1)  
        μ0 = mean_increments_0
        μ1 = mean_increments_1
        
        σ0_log = jnp.log(σ0_base) * jnp.ones(k)
        σ1_log = jnp.log(σ1_base) * jnp.ones(k)
        
        return jnp.concatenate([
            b,                    
            v,
            v0,                   
            v1,                   
            μ0,                   
            μ1,                   
            σ0_log,              
            σ1_log               
        ])



def likelihood_unlabeled_gaussian_mixture(θ, Y, Xhat, k, homosked):
    n, d = Xhat.shape
    b, (w00,w01,w10,w11), ω0, ω1, μ0, μ1, σ0, σ1 = unpack_theta(θ, d, k, homosked)
    μ = Xhat @ b                          

    is1 = (Xhat[:,0] == 1.0)

    pdf1_g1 = mixture_pdf(Y - μ,                    ω1, μ1, σ1)
    pdf0_g1 = mixture_pdf(Y - (μ - b[0]),           ω0, μ0, σ0)
    mix1    = w11 * pdf1_g1 + w10 * pdf0_g1 + 1e-12

    pdf1_g0 = mixture_pdf(Y - (μ + b[0]),           ω1, μ1, σ1)
    pdf0_g0 = mixture_pdf(Y - μ,                    ω0, μ0, σ0)
    mix0    = w01 * pdf1_g0 + w00 * pdf0_g0 + 1e-12

    ll = jnp.where(is1, jnp.log(mix1), jnp.log(mix0))
    return -jnp.sum(ll)


def _one_step_gaussian_mixture_core(Y, Xhat, k=2, homosked=False,
                                   nguess=20, maxiter=100, seed=0):
    Yj = jnp.asarray(Y).ravel()
    Xj = jnp.asarray(Xhat)

    θ0 = get_starting_values_unlabeled_gaussian_mixture(Yj, Xj, k, homosked)
    
    solver = LBFGS(fun=lambda th: likelihood_unlabeled_gaussian_mixture(th, Yj, Xj, k, homosked),
                   maxiter=maxiter, tol=1e-12)
    
    key = jr.PRNGKey(seed)
    subkeys = jr.split(key, nguess)
    
    best_loss, best_θ = jnp.inf, θ0
    
    for i, sk in enumerate(subkeys):
        if i == 0:
            θ_try = θ0
        else:
            noise_scale = 0.05 + 0.02 * (i / nguess)  
            noise = jr.normal(sk, θ0.shape) * noise_scale
            
            d = Xj.shape[1]
            noise = noise.at[:d].multiply(0.5)  
            noise = noise.at[d:d+3].multiply(0.3)  
            
            θ_try = θ0 + noise
        
        try:
            out = solver.run(θ_try)
            if out.state.value < best_loss and jnp.isfinite(out.state.value):
                best_loss, best_θ = out.state.value, out.params
        except:
            continue
    
    H = hessian(lambda th: likelihood_unlabeled_gaussian_mixture(th, Yj, Xj, k, homosked))(best_θ)
    cov = jnp.linalg.pinv(H)
    
    b_jax = best_θ[:Xj.shape[1]]
    V_jax = cov[:Xj.shape[1], :Xj.shape[1]]
    
    return np.array(b_jax), np.array(V_jax)

def _reorder_intercept_first(b, V, intercept):
    if not intercept:
        return b, V

    d = b.shape[0]
    order = jnp.array([d-1] + list(range(d-1)), dtype=jnp.int32)
    b_new = jnp.take(b, order)
    V_new = jnp.take(jnp.take(V, order, axis=0), order, axis=1)
    return b_new, V_new

def _standardize_coefficient_order(b, V, names):
    """
    Standardize coefficient ordering: intercept first, then alphabetical.
    
    Parameters
    ----------
    b : array-like
        Coefficients
    V : array-like
        Covariance matrix
    names : list[str] or None
        Variable names
        
    Returns
    -------
    tuple
        Reordered (coefficients, covariance_matrix, names)
    """
    b = np.asarray(b)
    V = np.asarray(V)
    
    if names is None:
        return b, V, names
    
    # Standardize intercept name and identify intercept position
    intercept_names = ['Intercept', '(Intercept)']
    intercept_idx = None
    standardized_names = []
    
    for i, name in enumerate(names):
        if name in intercept_names:
            intercept_idx = i
            standardized_names.append('Intercept')
        else:
            standardized_names.append(name)
    
    # Create ordering: intercept first, then alphabetical
    if intercept_idx is not None:
        # Get non-intercept names with their indices
        non_intercept_items = [(i, name) for i, name in enumerate(standardized_names) if name != 'Intercept']
        # Sort by name alphabetically
        non_intercept_items.sort(key=lambda x: x[1])
        
        # Create new ordering: intercept first, then alphabetical
        order = [intercept_idx] + [item[0] for item in non_intercept_items]
        new_names = ['Intercept'] + [item[1] for item in non_intercept_items]
    else:
        # No intercept, just sort alphabetically
        name_index_pairs = [(i, name) for i, name in enumerate(standardized_names)]
        name_index_pairs.sort(key=lambda x: x[1])
        order = [item[0] for item in name_index_pairs]
        new_names = [item[1] for item in name_index_pairs]
    
    # Reorder coefficients and covariance matrix
    b_new = b[order]
    V_new = V[np.ix_(order, order)]
    
    return b_new, V_new, new_names

def summarize_coefs(b, V, names=None, alpha=0.05):

    b = np.asarray(b).ravel()
    V = np.asarray(V)
    d = b.size

    if names is None:
        names = [f"x{i}" for i in range(1, d+1)]
    elif len(names) != d:
        names = [f"x{i}" for i in range(1, d+1)]

    se    = np.sqrt(np.diag(V))
    z     = b / se
    pval  = 2 * (1 - stats.norm.cdf(np.abs(z)))
    lo    = b + stats.norm.ppf(alpha/2) * se
    hi    = b + stats.norm.ppf(1 - alpha/2) * se

    ci_low_label  = f"{100*(alpha/2):.1f}%"
    ci_high_label = f"{100*(1-alpha/2):.1f}%"

    df = pd.DataFrame({
        "Estimate":    b,
        "Std. Error":  se,
        "z value":     z,
        "P>|z|":       pval,
        ci_low_label:  lo,
        ci_high_label: hi
    }, index=names)

    return df

@partial(jit, static_argnames=('treatment_idx', 'homoskedastic','distribution'))
def _one_step_jax_core_with_treatment_idx(Y, Xhat, treatment_idx, homoskedastic=False, distribution=None):

    def objective(theta):
        return likelihood_unlabeled_jax_with_treatment_idx(Y, Xhat, theta, treatment_idx, homoskedastic, distribution)

    theta0 = get_starting_values_unlabeled_jax_with_treatment_idx(Y, Xhat, treatment_idx, homoskedastic)
    solver = LBFGS(fun=objective, tol=1e-12, maxiter=500)
    sol = solver.run(theta0)
    th_opt = sol.params

    H = hessian(objective)(th_opt)
    d = Xhat.shape[1]
    b = th_opt[:d]
    V = jnp.linalg.pinv(H)[:d, :d]
    
    return b, V

def _one_step_core_with_treatment_idx(Y, Xhat, treatment_idx=0, homoskedastic=False, distribution=None):

    Yj = jnp.asarray(Y).ravel()
    Xj = jnp.asarray(Xhat)
    b_jax, V_jax = _one_step_jax_core_with_treatment_idx(Yj, Xj, treatment_idx, homoskedastic, distribution)

    return np.array(b_jax), np.array(V_jax)

def likelihood_unlabeled_jax_with_treatment_idx(Y, Xhat, theta, treatment_idx, homoskedastic, distribution=None):

    Y = jnp.ravel(Y)
    d = Xhat.shape[1]
    b, w00, w01, w10, sigma0, sigma1 = theta_to_pars_jax(theta, d, homoskedastic)
    w11 = 1.0 / (1.0 + jnp.exp(theta[d]) + jnp.exp(theta[d+1]) + jnp.exp(theta[d+2]))
    mu = Xhat @ b
    
    pdf = normal_pdf if distribution is None else distribution

    treatment_effect = b[treatment_idx]
    
    term1_1 = w11 * pdf(Y, mu, sigma1)
    term2_1 = w10 * pdf(Y, mu - treatment_effect, sigma0)
    
    term1_0 = w01 * pdf(Y, mu + treatment_effect, sigma1)
    term2_0 = w00 * pdf(Y, mu, sigma0)
    
    indicator = Xhat[:, treatment_idx]
    log_term = jnp.where(indicator == 1.0,
                         jnp.log(term1_1 + term2_1),
                         jnp.log(term1_0 + term2_0))
    return -jnp.sum(log_term)

def get_starting_values_unlabeled_jax_with_treatment_idx(Y, Xhat, treatment_idx, homoskedastic):

    Y = jnp.ravel(Y)
    Xhat = jnp.asarray(Xhat)
    b = ols_jax(Y, Xhat, se=False)
    u = Y - Xhat @ b
    sigma = jnp.std(u)
    
    def pdf_func(y, loc, scale):
        return jnp.exp(-0.5 * jnp.square((y - loc) / scale)) / (jnp.sqrt(2 * jnp.pi) * scale)
    
    mu = Xhat @ b
    treatment_effect = b[treatment_idx]
    
    cond1 = pdf_func(Y, mu, sigma) > pdf_func(Y, mu - treatment_effect, sigma)
    cond2 = pdf_func(Y, mu + treatment_effect, sigma) > pdf_func(Y, mu, sigma)
    
    X_imputed = jnp.where(Xhat[:, treatment_idx] == 1.0,
                          cond1.astype(jnp.float32),
                          cond2.astype(jnp.float32))
    
    freq00 = jnp.mean(((Xhat[:, treatment_idx] == 0.0) & (X_imputed == 0.0)).astype(jnp.float32))
    freq01 = jnp.mean(((Xhat[:, treatment_idx] == 0.0) & (X_imputed == 1.0)).astype(jnp.float32))
    freq10 = jnp.mean(((Xhat[:, treatment_idx] == 1.0) & (X_imputed == 0.0)).astype(jnp.float32))
    freq11 = jnp.mean(((Xhat[:, treatment_idx] == 1.0) & (X_imputed == 1.0)).astype(jnp.float32))
    
    w00 = jnp.maximum(freq00, 0.001)
    w01 = jnp.maximum(freq01, 0.001)
    w10 = jnp.maximum(freq10, 0.001)
    w11 = jnp.maximum(freq11, 0.001)
    w = jnp.array([w00, w01, w10, w11])
    w = w / jnp.sum(w)
    v = jnp.log(w[:3] / w[3])
    
    mask0 = (X_imputed == 0.0)
    mask1 = (X_imputed == 1.0)
    sigma0 = subset_std(u, mask0)
    sigma1 = subset_std(u, mask1)
    sigma0 = jnp.where(jnp.isnan(sigma0), sigma1, sigma0)
    sigma1 = jnp.where(jnp.isnan(sigma1), sigma0, sigma1)
    
    if homoskedastic:
        p_val = jnp.mean(X_imputed)
        sigma_comb = sigma1 * p_val + sigma0 * (1.0 - p_val)
        return jnp.concatenate([b, v, jnp.array([jnp.log(sigma_comb)])])
    else:
        return jnp.concatenate([b, v, jnp.array([jnp.log(sigma0), jnp.log(sigma1)])])