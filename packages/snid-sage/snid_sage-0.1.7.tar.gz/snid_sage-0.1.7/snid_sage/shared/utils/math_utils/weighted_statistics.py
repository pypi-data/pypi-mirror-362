"""
Statistically rigorous weighted calculations for redshift estimation in SNID SAGE.

This module implements both pure inverse variance weighting and hybrid methods that
include cluster-level scatter, following improved statistical recommendations for optimal
redshift and age estimation in the winning cluster.

The weighting schemes supported:
- Pure inverse variance weighting: Weight = 1 / (redshift_uncertainty^2)  
- Hybrid weighting: Weight = 1 / (redshift_uncertainty^2 + τ^2) where τ^2 is cluster scatter
- RLAP weighting for age estimates with optional cluster scatter addition
"""

import numpy as np
from typing import Union, List, Tuple, Optional
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

def calculate_hybrid_weighted_redshift(
    redshifts: Union[np.ndarray, List[float]], 
    redshift_errors: Union[np.ndarray, List[float]],
    include_cluster_scatter: bool = True,
    min_error: float = 1e-6,
    default_error: float = 0.01
) -> Tuple[float, float, float]:
    """
    Calculate hybrid weighted redshift estimate using inverse variance weighting with cluster scatter.
    
    This implements the statistically rigorous two-step approach:
    1. Pure inverse variance weighting using individual template uncertainties
    2. Hybrid method that incorporates cluster-level scatter (τ²) in quadrature
    
    Parameters
    ----------
    redshifts : array-like
        Redshift values from winning cluster
    redshift_errors : array-like  
        Individual redshift uncertainties from correlation peak fits
    include_cluster_scatter : bool, default=True
        Whether to include cluster-level scatter (τ²) term
    min_error : float, default=1e-6
        Minimum allowed error to prevent division by zero
    default_error : float, default=0.01
        Default error for missing/invalid uncertainties
        
    Returns
    -------
    Tuple[float, float, float]
        (final_redshift, final_uncertainty, cluster_scatter)
        
    Notes
    -----
    Statistical Method:
    - Calculate preliminary unweighted mean for cluster scatter estimation
    - Estimate excess variance: τ² = max(0, S² - σ̄²)
    - Apply hybrid weighting: w_i = 1/(σ_i² + τ²)
    """
    redshifts = np.asarray(redshifts, dtype=float)
    redshift_errors = np.asarray(redshift_errors, dtype=float)
    
    if len(redshifts) == 0:
        return np.nan, np.nan, np.nan
        
    if len(redshifts) == 1:
        error = float(redshift_errors[0]) if len(redshift_errors) > 0 else default_error
        return float(redshifts[0]), error, 0.0
    
    # Handle missing or invalid errors
    if len(redshift_errors) != len(redshifts):
        logger.warning(f"Redshift errors length ({len(redshift_errors)}) != redshifts length ({len(redshifts)}). Using default errors.")
        redshift_errors = np.full(len(redshifts), default_error)
    
    # Ensure minimum error to prevent division by zero
    redshift_errors = np.maximum(redshift_errors, min_error)
    
    # Remove any invalid data
    valid_mask = np.isfinite(redshifts) & np.isfinite(redshift_errors) & (redshift_errors > 0)
    
    if not np.any(valid_mask):
        logger.warning("No valid redshift/error pairs found")
        return np.nan, np.nan, np.nan
        
    valid_redshifts = redshifts[valid_mask]
    valid_errors = redshift_errors[valid_mask]
    N = len(valid_redshifts)
    
    if N == 1:
        return float(valid_redshifts[0]), float(valid_errors[0]), 0.0
    
    # Method 1: Pure inverse variance weighting (baseline)
    weights_iv = 1.0 / (valid_errors ** 2)
    z_iv = np.sum(weights_iv * valid_redshifts) / np.sum(weights_iv)
    sigma_iv = 1.0 / np.sqrt(np.sum(weights_iv))
    
    if not include_cluster_scatter:
        return float(z_iv), float(sigma_iv), 0.0
    
    # Method 2: Hybrid method with cluster scatter
    
    # Step 1: Preliminary unweighted mean for scatter estimation
    z_tilde = np.mean(valid_redshifts)
    
    # Step 2: Sample variance of the cluster  
    S_squared = np.var(valid_redshifts, ddof=1) if N > 1 else 0.0
    
    # Step 3: Mean individual variance
    sigma_bar_squared = np.mean(valid_errors ** 2)
    
    # Step 4: Excess (between-template) variance
    tau_squared = max(0.0, S_squared - sigma_bar_squared)
    
    # Step 5: Total variance and new weights
    total_variances = valid_errors ** 2 + tau_squared
    weights_hybrid = 1.0 / total_variances
    
    # Step 6: Final combined redshift and uncertainty
    z_final = np.sum(weights_hybrid * valid_redshifts) / np.sum(weights_hybrid)
    sigma_final = 1.0 / np.sqrt(np.sum(weights_hybrid))
    
    logger.info(f"Enhanced redshift estimate: pure IV: {z_iv:.6f}±{sigma_iv:.6f}, "
                f"hybrid: {z_final:.6f}±{sigma_final:.6f}, τ={np.sqrt(tau_squared):.6f}")
    
    return float(z_final), float(sigma_final), float(np.sqrt(tau_squared))


def calculate_metric_weighted_age(
    ages: Union[np.ndarray, List[float]], 
    metric_weights: Union[np.ndarray, List[float]],
    include_cluster_scatter: bool = True
) -> Tuple[float, float, float, float]:
    """
    Calculate metric-weighted age estimate with optional cluster scatter modeling.
    
    This function uses the best available metric (RLAP-cos if available, otherwise RLAP)
    for weighting age estimates. This implements statistical age estimation methods:
    1. Metric-weighted mean age with effective sample size uncertainty
    2. Hybrid error that incorporates cluster scatter in quadrature
    
    Parameters
    ----------
    ages : array-like
        Age values in days (already filtered for valid ages)
    metric_weights : array-like
        Metric values (RLAP-cos or RLAP) to use as weights
    include_cluster_scatter : bool, default=True
        Whether to include cluster scatter term
        
    Returns
    -------
    Tuple[float, float, float, float]
        (final_age, metric_only_error, total_error_with_scatter, cluster_scatter)
        
    Notes
    -----
    Statistical Methods:
    - Metric-weighted mean with effective sample size uncertainty
    - Cluster scatter added in quadrature for total error
    """
    ages = np.asarray(ages, dtype=float)
    metric_weights = np.asarray(metric_weights, dtype=float)
    
    if len(ages) == 0:
        return np.nan, np.nan, np.nan, np.nan
        
    if len(ages) == 1:
        return float(ages[0]), 0.0, 0.0, 0.0
    
    # Remove invalid data
    valid_mask = np.isfinite(ages) & np.isfinite(metric_weights) & (metric_weights > 0)
    
    if not np.any(valid_mask):
        logger.warning("No valid age/metric pairs found")
        return np.nan, np.nan, np.nan, np.nan
        
    valid_ages = ages[valid_mask]
    valid_weights = metric_weights[valid_mask]
    N = len(valid_ages)
    
    if N == 1:
        return float(valid_ages[0]), 0.0, 0.0, 0.0
    
    # Method 1: Metric-weighted mean age
    w_i = valid_weights  # Metric weights (RLAP-cos or RLAP)
    t_bar_metric = np.sum(w_i * valid_ages) / np.sum(w_i)
    
    # Metric-weighted uncertainty
    N_eff = (np.sum(w_i) ** 2) / np.sum(w_i ** 2)  # Effective number of templates
    
    # Weighted variance
    weighted_variance = np.sum(w_i * (valid_ages - t_bar_metric) ** 2) / np.sum(w_i)
    
    # Statistical uncertainty (metric-only)
    sigma_metric = np.sqrt(weighted_variance / N_eff)
    
    if not include_cluster_scatter:
        return float(t_bar_metric), float(sigma_metric), float(sigma_metric), 0.0
    
    # Method 2: Hybrid error with cluster scatter
    
    # Cluster scatter in age space
    s_tc_squared = weighted_variance  # This is the metric-weighted scatter
    s_tc = np.sqrt(s_tc_squared)
    
    # Total error combining statistical and systematic components
    sigma_total = np.sqrt(sigma_metric ** 2 + s_tc_squared)
    
    logger.info(f"Enhanced age estimate: {t_bar_metric:.1f} days, "
                f"metric-only error: ±{sigma_metric:.1f}, "
                f"total error: ±{sigma_total:.1f}, cluster scatter: {s_tc:.1f}")
    
    return float(t_bar_metric), float(sigma_metric), float(sigma_total), float(s_tc)


# Keep the old function name for backward compatibility
def calculate_rlap_weighted_age(
    ages: Union[np.ndarray, List[float]], 
    rlaps: Union[np.ndarray, List[float]],
    include_cluster_scatter: bool = True
) -> Tuple[float, float, float, float]:
    """
    DEPRECATED: Use calculate_metric_weighted_age instead.
    
    This function is kept for backward compatibility but now internally
    uses the new calculate_metric_weighted_age function.
    """
    return calculate_metric_weighted_age(ages, rlaps, include_cluster_scatter)


def calculate_inverse_variance_weighted_redshift(
    redshifts: Union[np.ndarray, List[float]], 
    redshift_errors: Union[np.ndarray, List[float]],
    min_error: float = 1e-6,
    default_error: float = 0.01
) -> Tuple[float, float]:
    """
    LEGACY: Calculate inverse variance weighted redshift using only redshift uncertainties.
    
    This is maintained for backwards compatibility. New code should use
    calculate_hybrid_weighted_redshift() for better statistical accuracy.
    """
    result = calculate_hybrid_weighted_redshift(
        redshifts, redshift_errors, include_cluster_scatter=False, 
        min_error=min_error, default_error=default_error
    )
    return result[0], result[1]  # Return only redshift and uncertainty


def calculate_weighted_redshift_with_uncertainty(
    redshifts: Union[np.ndarray, List[float]], 
    weights: Union[np.ndarray, List[float]],
    redshift_errors: Optional[Union[np.ndarray, List[float]]] = None
) -> Tuple[float, float]:
    """
    DEPRECATED: This function is obsolete. Use calculate_hybrid_weighted_redshift() instead.
    
    This legacy function is maintained only for backwards compatibility.
    All new code should use the enhanced methods that implement improved
    statistical recommendations.
    """
    logger.warning("Using deprecated function. Switch to calculate_hybrid_weighted_redshift()")
    
    if redshift_errors is not None:
        result = calculate_hybrid_weighted_redshift(redshifts, redshift_errors, include_cluster_scatter=False)
        return result[0], result[1]
    
    # Legacy RLAP-only fallback 
    redshifts = np.asarray(redshifts, dtype=float)
    weights = np.asarray(weights, dtype=float)
    
    if len(redshifts) == 0:
        return np.nan, np.nan
        
    valid_mask = np.isfinite(redshifts) & np.isfinite(weights) & (weights > 0)
    if not np.any(valid_mask):
        return np.nan, np.nan
        
    valid_redshifts = redshifts[valid_mask]
    valid_weights = weights[valid_mask]
    
    if len(valid_redshifts) <= 1:
        return float(valid_redshifts[0]) if len(valid_redshifts) == 1 else np.nan, 0.0
    
    # Simple weighted calculation for legacy compatibility
    normalized_weights = valid_weights / np.sum(valid_weights)
    weighted_mean = np.sum(normalized_weights * valid_redshifts)
    weighted_variance = np.sum(normalized_weights * (valid_redshifts - weighted_mean)**2)
    N_eff = (np.sum(valid_weights))**2 / np.sum(valid_weights**2)
    weighted_uncertainty = np.sqrt(weighted_variance / N_eff)
    
    return float(weighted_mean), float(weighted_uncertainty)


def calculate_weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted median."""
    if len(values) == 0:
        return np.nan
        
    if len(values) == 1:
        return float(values[0])
    
    # Remove invalid data
    valid_mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not np.any(valid_mask):
        return np.nan
        
    valid_values = values[valid_mask]
    valid_weights = weights[valid_mask]
    
    if len(valid_values) == 1:
        return float(valid_values[0])
    
    # Sort by values
    sorted_indices = np.argsort(valid_values)
    sorted_values = valid_values[sorted_indices]
    sorted_weights = valid_weights[sorted_indices]
    
    # Calculate cumulative weights
    cumsum_weights = np.cumsum(sorted_weights)
    total_weight = cumsum_weights[-1]
    
    # Find median position
    median_weight = total_weight / 2.0
    
    # Find the value(s) at median position
    idx = np.searchsorted(cumsum_weights, median_weight)
    
    if idx == 0:
        return float(sorted_values[0])
    elif idx >= len(sorted_values):
        return float(sorted_values[-1])
    else:
        # Linear interpolation between adjacent values
        w1 = cumsum_weights[idx-1]
        w2 = cumsum_weights[idx]
        if w1 == median_weight:
            return float(sorted_values[idx-1])
        elif w2 == median_weight:
            return float((sorted_values[idx-1] + sorted_values[idx]) / 2.0)
        else:
            # Interpolate
            alpha = (median_weight - w1) / (w2 - w1)
            return float(sorted_values[idx-1] + alpha * (sorted_values[idx] - sorted_values[idx-1]))


def validate_weighted_calculation(
    redshifts: np.ndarray, 
    weights: np.ndarray, 
    result: Tuple[float, float]
) -> bool:
    """Validate a weighted calculation result."""
    weighted_mean, uncertainty = result
    
    if not np.isfinite(weighted_mean) or not np.isfinite(uncertainty):
        return False
        
    if len(redshifts) == 0:
        return np.isnan(weighted_mean) and np.isnan(uncertainty)
        
    # Check if result is within reasonable bounds
    min_z, max_z = np.min(redshifts), np.max(redshifts)
    if not (min_z <= weighted_mean <= max_z):
        return False
        
    # Check if uncertainty is positive and reasonable
    if uncertainty < 0 or uncertainty > (max_z - min_z):
        return False
        
    return True


# Backwards compatibility exports
__all__ = [
    'calculate_hybrid_weighted_redshift',
    'calculate_metric_weighted_age',
    'calculate_rlap_weighted_age',
    'calculate_inverse_variance_weighted_redshift',
    'calculate_weighted_redshift_with_uncertainty',
    'calculate_weighted_median',
    'validate_weighted_calculation'
] 