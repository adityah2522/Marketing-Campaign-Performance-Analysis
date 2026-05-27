# src/stats_utils.py

import pandas as pd
import scipy.stats as stats
import itertools
from statsmodels.stats.multitest import multipletests

def run_kruskal_wallis(df, group_col, metric_col):
    """
    Executes a Kruskal-Wallis H-test (non-parametric One-Way ANOVA) to determine 
    if there are statistically significant differences between group medians.
    
    Args:
        df (pd.DataFrame): The dataset containing the groups and metrics.
        group_col (str): The column name defining the categorical groups.
        metric_col (str): The column name containing the numerical metric to test.
        
    Returns:
        tuple: (is_significant (bool), p_value (float), test_statistic (float))
    """
    # Group the target metric by the specified categories
    groups = [group[metric_col].values for name, group in df.groupby(group_col)]
    
    # Perform the Kruskal-Wallis test
    kw_stat, kw_p = stats.kruskal(*groups)
    
    print("=========================================")
    print("     KRUSKAL-WALLIS H-TEST RESULTS       ")
    print("=========================================")
    print(f"Statistic : {kw_stat:.4f}")
    print(f"P-value   : {kw_p:.4e}")
    
    # Determine significance using standard alpha = 0.05
    is_significant = kw_p < 0.05
    
    if is_significant:
        print("\n✅ Result: Statistically significant difference exists between groups.")
    else:
        print("\n❌ Result: No significant difference found.")
        
    return is_significant, kw_p, kw_stat


def run_posthoc_mannwhitney(df, group_col, metric_col, alpha=0.05):
    """
    Executes pairwise Mann-Whitney U tests with a Bonferroni correction to 
    identify which specific groups differ significantly from each other.
    
    Args:
        df (pd.DataFrame): The dataset containing the groups and metrics.
        group_col (str): The column name defining the categorical groups.
        metric_col (str): The column name containing the numerical metric.
        alpha (float): The significance level threshold (default is 0.05).
        
    Returns:
        pd.DataFrame: A summary table of pairwise comparisons, adjusted p-values, 
                      significance flags, and the winning group based on medians.
    """
    unique_groups = sorted(df[group_col].unique())
    pairs = list(itertools.combinations(unique_groups, 2))
    p_values = []
    
    # Calculate raw p-values for every possible pair
    for p1, p2 in pairs:
        g1 = df[df[group_col] == p1][metric_col]
        g2 = df[df[group_col] == p2][metric_col]
        _, p_val = stats.mannwhitneyu(g1, g2, alternative='two-sided')
        p_values.append(p_val)
        
    # Apply Bonferroni correction to control the family-wise error rate
    reject, p_adjusted, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')
    
    results = []
    
    # Compile the results and determine the better performing group by median
    for pair, p_adj, rej in zip(pairs, p_adjusted, reject):
        median1 = df[df[group_col] == pair[0]][metric_col].median()
        median2 = df[df[group_col] == pair[1]][metric_col].median()
        
        winner = "Tie"
        if rej:
            winner = f"Promotion {pair[0]}" if median1 > median2 else f"Promotion {pair[1]}"
            
        results.append({
            'Comparison': f"{pair[0]} vs {pair[1]}",
            'Adjusted P-Value': round(p_adj, 6),
            'Significant': rej,
            'Winner (by Median)': winner
        })
        
    return pd.DataFrame(results)