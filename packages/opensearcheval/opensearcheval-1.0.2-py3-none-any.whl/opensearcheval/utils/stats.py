from typing import List, Dict, Any, Tuple
import numpy as np
from scipy import stats
import logging

logger = logging.getLogger(__name__)

def t_test(control_data: List[float], treatment_data: List[float], 
           alpha: float = 0.05) -> Dict[str, Any]:
    """
    Perform a t-test to compare two groups
    
    Args:
        control_data: List of metric values for control group
        treatment_data: List of metric values for treatment group
        alpha: Significance level
        
    Returns:
        Dictionary with test results
    """
    try:
        t_stat, p_value = stats.ttest_ind(control_data, treatment_data, equal_var=False)
        
        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        percent_change = ((treatment_mean - control_mean) / control_mean) * 100 if control_mean != 0 else 0
        
        significant = p_value < alpha
        
        return {
            "test": "t_test",
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "control_mean": float(control_mean),
            "treatment_mean": float(treatment_mean),
            "percent_change": float(percent_change),
            "significant": significant,
            "confidence_level": 1 - alpha,
            "sample_sizes": {
                "control": len(control_data),
                "treatment": len(treatment_data)
            }
        }
    except Exception as e:
        logger.error(f"Error in t_test: {str(e)}")
        return {
            "test": "t_test",
            "error": str(e)
        }

def mann_whitney_u_test(control_data: List[float], treatment_data: List[float], 
                       alpha: float = 0.05) -> Dict[str, Any]:
    """
    Perform a Mann-Whitney U test (non-parametric test)
    
    Args:
        control_data: List of metric values for control group
        treatment_data: List of metric values for treatment group
        alpha: Significance level
        
    Returns:
        Dictionary with test results
    """
    try:
        u_stat, p_value = stats.mannwhitneyu(control_data, treatment_data, alternative='two-sided')
        
        control_median = np.median(control_data)
        treatment_median = np.median(treatment_data)
        percent_change = ((treatment_median - control_median) / control_median) * 100 if control_median != 0 else 0
        
        significant = p_value < alpha
        
        return {
            "test": "mann_whitney_u_test",
            "u_statistic": float(u_stat),
            "p_value": float(p_value),
            "control_median": float(control_median),
            "treatment_median": float(treatment_median),
            "percent_change": float(percent_change),
            "significant": significant,
            "confidence_level": 1 - alpha,
            "sample_sizes": {
                "control": len(control_data),
                "treatment": len(treatment_data)
            }
        }
    except Exception as e:
        logger.error(f"Error in mann_whitney_u_test: {str(e)}")
        return {
            "test": "mann_whitney_u_test",
            "error": str(e)
        }

def bootstrap_test(control_data: List[float], treatment_data: List[float], 
                  alpha: float = 0.05, n_resamples: int = 10000) -> Dict[str, Any]:
    """
    Perform a bootstrap hypothesis test
    
    Args:
        control_data: List of metric values for control group
        treatment_data: List of metric values for treatment group
        alpha: Significance level
        n_resamples: Number of bootstrap resamples
        
    Returns:
        Dictionary with test results
    """
    try:
        # Calculate observed difference in means
        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        observed_diff = treatment_mean - control_mean
        
        # Combine data for bootstrap
        combined = np.concatenate([control_data, treatment_data])
        n_control = len(control_data)
        n_treatment = len(treatment_data)
        
        # Bootstrap resampling
        diffs = []
        for _ in range(n_resamples):
            # Resample from combined data
            resampled = np.random.choice(combined, size=n_control + n_treatment, replace=True)
            
            # Split into control and treatment
            resample_control = resampled[:n_control]
            resample_treatment = resampled[n_control:]
            
            # Calculate difference in means
            diff = np.mean(resample_treatment) - np.mean(resample_control)
            diffs.append(diff)
        
        # Calculate p-value
        p_value = np.mean([abs(diff) >= abs(observed_diff) for diff in diffs])
        
        # Calculate confidence interval
        lower_percentile = alpha / 2 * 100
        upper_percentile = (1 - alpha / 2) * 100
        confidence_interval = np.percentile(diffs, [lower_percentile, upper_percentile])
        
        percent_change = (observed_diff / control_mean) * 100 if control_mean != 0 else 0
        significant = p_value < alpha
        
        return {
            "test": "bootstrap_test",
            "observed_difference": float(observed_diff),
            "p_value": float(p_value),
            "control_mean": float(control_mean),
            "treatment_mean": float(treatment_mean),
            "percent_change": float(percent_change),
            "confidence_interval": [float(confidence_interval[0]), float(confidence_interval[1])],
            "significant": significant,
            "confidence_level": 1 - alpha,
            "n_resamples": n_resamples,
            "sample_sizes": {
                "control": n_control,
                "treatment": n_treatment
            }
        }
    except Exception as e:
        logger.error(f"Error in bootstrap_test: {str(e)}")
        return {
            "test": "bootstrap_test",
            "error": str(e)
        }

def power_analysis(control_mean: float, control_std: float, 
                  min_detectable_effect: float, alpha: float = 0.05, 
                  power: float = 0.8) -> Dict[str, Any]:
    """
    Calculate sample size required for desired statistical power
    
    Args:
        control_mean: Mean of the control group
        control_std: Standard deviation of the control group
        min_detectable_effect: Minimum effect size to detect (as percentage)
        alpha: Significance level
        power: Desired statistical power
        
    Returns:
        Dictionary with power analysis results
    """
    try:
        # Calculate effect size
        effect_size = (control_mean * min_detectable_effect / 100) / control_std
        
        # Calculate required sample size
        required_n = stats.norm.ppf(1 - alpha/2) + stats.norm.ppf(power)
        required_n = required_n**2 / effect_size**2
        required_n = int(np.ceil(required_n))
        
        return {
            "analysis": "power_analysis",
            "required_sample_size": required_n,
            "effect_size": float(effect_size),
            "min_detectable_effect_percent": float(min_detectable_effect),
            "significance_level": alpha,
            "power": power,
            "control_mean": float(control_mean),
            "control_std": float(control_std)
        }
    except Exception as e:
        logger.error(f"Error in power_analysis: {str(e)}")
        return {
            "analysis": "power_analysis",
            "error": str(e)
        }