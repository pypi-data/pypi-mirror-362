import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
import io
import base64
import logging
from matplotlib.figure import Figure
import matplotlib.dates as mdates

logger = logging.getLogger(__name__)

# Set style
sns.set(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['figure.figsize'] = (10, 6)

def metrics_time_series(
    data: pd.DataFrame,
    metric_col: str,
    time_col: str = 'date',
    group_col: Optional[str] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> Figure:
    """
    Create a time series plot of metrics
    
    Args:
        data: DataFrame with metrics data
        metric_col: Column name for metric values
        time_col: Column name for timestamps
        group_col: Optional column name for grouping (e.g., experiment group)
        title: Optional plot title
        figsize: Figure size as (width, height)
    
    Returns:
        Matplotlib Figure object
    """
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Convert time column to datetime if it's not already
        if not pd.api.types.is_datetime64_dtype(data[time_col]):
            data[time_col] = pd.to_datetime(data[time_col])
        
        # Create the plot
        if group_col and group_col in data.columns:
            # Plot by group
            for group, group_data in data.groupby(group_col):
                ax.plot(
                    group_data[time_col],
                    group_data[metric_col],
                    marker='o',
                    linewidth=2,
                    label=group
                )
            ax.legend(title=group_col.replace('_', ' ').title())
        else:
            # Single line plot
            ax.plot(
                data[time_col],
                data[metric_col],
                marker='o',
                linewidth=2,
                color='#007AFF'
            )
        
        # Set title and labels
        if title:
            ax.set_title(title, fontsize=14, pad=20)
        
        ax.set_xlabel('Date', fontsize=12, labelpad=10)
        ax.set_ylabel(metric_col.replace('_', ' ').title(), fontsize=12, labelpad=10)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        
        # Grid and spines
        ax.grid(True, linestyle='--', alpha=0.7)
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Tight layout
        fig.tight_layout()
        
        return fig
    
    except Exception as e:
        logger.error(f"Error creating metrics time series plot: {str(e)}")
        # Return a simple error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', fontsize=12)
        ax.axis('off')
        return fig

def ab_test_results_plot(
    control_data: List[float],
    treatment_data: List[float],
    metric_name: str = 'Metric',
    p_value: float = 0.05,
    confidence_level: float = 0.95,
    figsize: Tuple[int, int] = (12, 6)
) -> Figure:
    """
    Create a visualization of A/B test results
    
    Args:
        control_data: List of metric values for control group
        treatment_data: List of metric values for treatment group
        metric_name: Name of the metric
        p_value: p-value from statistical test
        confidence_level: Confidence level (0-1)
        figsize: Figure size as (width, height)
    
    Returns:
        Matplotlib Figure object
    """
    try:
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Prepare data
        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        control_std = np.std(control_data)
        treatment_std = np.std(treatment_data)
        
        # Calculate percent change
        percent_change = ((treatment_mean - control_mean) / control_mean) * 100 if control_mean != 0 else 0
        
        # Calculate confidence intervals
        from scipy import stats
        
        control_ci = stats.norm.interval(
            confidence_level, 
            loc=control_mean, 
            scale=control_std/np.sqrt(len(control_data))
        )
        
        treatment_ci = stats.norm.interval(
            confidence_level, 
            loc=treatment_mean, 
            scale=treatment_std/np.sqrt(len(treatment_data))
        )
        
        # Plot 1: Bar chart with confidence intervals
        bar_width = 0.35
        positions = [0, 1]
        
        bars = ax1.bar(
            positions, 
            [control_mean, treatment_mean],
            bar_width,
            yerr=[
                [control_mean - control_ci[0], treatment_mean - treatment_ci[0]],
                [control_ci[1] - control_mean, treatment_ci[1] - treatment_mean]
            ],
            capsize=10,
            color=['#5856D6', '#007AFF'],
            alpha=0.8
        )
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.02 * max(control_mean, treatment_mean),
                f'{height:.3f}',
                ha='center', 
                va='bottom',
                fontsize=10
            )
        
        # Add significance indicator
        if p_value < 0.05:
            max_height = max(control_ci[1], treatment_ci[1])
            ax1.plot([0, 1], [max_height * 1.1, max_height * 1.1], 'k-', linewidth=1)
            ax1.text(
                0.5, 
                max_height * 1.15,
                f'p = {p_value:.4f} (significant)',
                ha='center',
                va='bottom',
                fontsize=10
            )
            ax1.plot([0, 0, 1, 1], [max_height * 1.05, max_height * 1.1, max_height * 1.1, max_height * 1.05], 'k-', linewidth=1)
        
        # Set labels and title
        ax1.set_ylabel(metric_name, fontsize=12)
        ax1.set_title('Comparison of Means', fontsize=14)
        ax1.set_xticks(positions)
        ax1.set_xticklabels(['Control', 'Treatment'])
        
        # Remove spines
        for spine in ax1.spines.values():
            spine.set_visible(False)
        
        # Plot 2: Distribution comparison
        sns.kdeplot(control_data, ax=ax2, label='Control', color='#5856D6', fill=True, alpha=0.3)
        sns.kdeplot(treatment_data, ax=ax2, label='Treatment', color='#007AFF', fill=True, alpha=0.3)
        
        # Add mean lines
        ax2.axvline(control_mean, color='#5856D6', linestyle='--', linewidth=1.5, label=f'Control Mean: {control_mean:.3f}')
        ax2.axvline(treatment_mean, color='#007AFF', linestyle='--', linewidth=1.5, label=f'Treatment Mean: {treatment_mean:.3f}')
        
        # Set labels and title
        ax2.set_xlabel(metric_name, fontsize=12)
        ax2.set_ylabel('Density', fontsize=12)
        ax2.set_title('Distribution Comparison', fontsize=14)
        ax2.legend(fontsize=10)
        
        # Remove spines
        for spine in ax2.spines.values():
            spine.set_visible(False)
        
        # Add summary text
        fig.text(
            0.5, 
            0.01, 
            f"Summary: {percent_change:.2f}% {'increase' if percent_change >= 0 else 'decrease'} in {metric_name}\n"
            f"Control: n={len(control_data)}, Treatment: n={len(treatment_data)}, "
            f"p-value: {p_value:.4f} ({'significant' if p_value < 0.05 else 'not significant'})",
            ha='center',
            fontsize=12
        )
        
        # Tight layout
        fig.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        return fig
    
    except Exception as e:
        logger.error(f"Error creating A/B test results plot: {str(e)}")
        # Return a simple error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', fontsize=12)
        ax.axis('off')
        return fig

def user_behavior_heatmap(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 8)
) -> Figure:
    """
    Create a heatmap of user behavior data
    
    Args:
        data: DataFrame with user behavior data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        value_col: Column name for values
        title: Optional plot title
        figsize: Figure size as (width, height)
    
    Returns:
        Matplotlib Figure object
    """
    try:
        # Create pivot table
        pivot_data = data.pivot_table(
            index=y_col,
            columns=x_col,
            values=value_col,
            aggfunc='mean'
        )
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create heatmap
        sns.heatmap(
            pivot_data,
            cmap='YlGnBu',
            annot=True,
            fmt='.2f',
            linewidths=0.5,
            ax=ax,
            cbar_kws={'label': value_col.replace('_', ' ').title()}
        )
        
        # Set title and labels
        if title:
            ax.set_title(title, fontsize=14, pad=20)
        else:
            ax.set_title(f'{value_col.replace("_", " ").title()} by {x_col.replace("_", " ").title()} and {y_col.replace("_", " ").title()}', fontsize=14, pad=20)
        
        ax.set_xlabel(x_col.replace('_', ' ').title(), fontsize=12, labelpad=10)
        ax.set_ylabel(y_col.replace('_', ' ').title(), fontsize=12, labelpad=10)
        
        # Rotate x-axis labels if there are many
        if len(pivot_data.columns) > 10:
            plt.xticks(rotation=45, ha='right')
        
        # Tight layout
        fig.tight_layout()
        
        return fig
    
    except Exception as e:
        logger.error(f"Error creating user behavior heatmap: {str(e)}")
        # Return a simple error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', fontsize=12)
        ax.axis('off')
        return fig

def metric_comparison_radar(
    metrics: Dict[str, Dict[str, float]],
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> Figure:
    """
    Create a radar chart (spider plot) to compare metrics across groups
    
    Args:
        metrics: Dictionary with group names as keys and dictionaries of metrics as values
        title: Optional title for the plot
        figsize: Figure size as (width, height)
        
    Returns:
        Matplotlib Figure object
    """
    try:
        # Get all metric names
        all_metrics = set()
        for group_metrics in metrics.values():
            all_metrics.update(group_metrics.keys())
        
        all_metrics = sorted(list(all_metrics))
        num_metrics = len(all_metrics)
        
        # Set up the figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, polar=True)
        
        # Set the angles for each metric
        angles = np.linspace(0, 2*np.pi, num_metrics, endpoint=False).tolist()
        angles += angles[:1]  # Close the loop
        
        # Set the labels for each metric
        labels = [m.replace('_', ' ').title() for m in all_metrics]
        labels += labels[:1]  # Close the loop
        
        # Plot each group
        colors = ['#007AFF', '#5856D6', '#34C759', '#FF9500', '#FF3B30']
        
        for i, (group_name, group_metrics) in enumerate(metrics.items()):
            # Get values for each metric
            values = [group_metrics.get(metric, 0) for metric in all_metrics]
            values += values[:1]  # Close the loop
            
            # Plot the group
            color = colors[i % len(colors)]
            ax.plot(angles, values, 'o-', linewidth=2, label=group_name, color=color)
            ax.fill(angles, values, alpha=0.1, color=color)
        
        # Set the labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels[:-1])
        
        # Set title
        if title:
            ax.set_title(title, y=1.1)
        else:
            ax.set_title("Metric Comparison", y=1.1)
        
        # Add legend
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        return fig
    except Exception as e:
        logger.error(f"Error creating metric comparison radar chart: {str(e)}")
        # Return a simple error figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', fontsize=12)
        ax.axis('off')
        return fig

def figure_to_base64(fig: Figure) -> str:
    """
    Convert a Matplotlib figure to a base64-encoded string
    
    Args:
        fig: Matplotlib Figure object
        
    Returns:
        Base64-encoded string
    """
    try:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return img_str
    except Exception as e:
        logger.error(f"Error converting figure to base64: {str(e)}")
        return ""

def save_figure(fig: Figure, path: str, dpi: int = 300) -> bool:
    """
    Save a Matplotlib figure to a file
    
    Args:
        fig: Matplotlib Figure object
        path: Output file path
        dpi: Resolution in dots per inch
        
    Returns:
        True if successful, False otherwise
    """
    try:
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
        logger.info(f"Saved figure to {path}")
        return True
    except Exception as e:
        logger.error(f"Error saving figure to {path}: {str(e)}")
        return False