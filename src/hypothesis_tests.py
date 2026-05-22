import pandas as pd
import numpy as np
from scipy import stats

class InsuranceHypothesisEngine:
    def __init__(self, df):
        self.df = df.copy()
        # Handle premium field variations gracefully
        self.p_col = 'TotalPremium' if 'TotalPremium' in self.df.columns else 'CalculatedPremiumPerTerm'
        if 'Margin' not in self.df.columns and self.p_col in self.df.columns:
            self.df['Margin'] = self.df[self.p_col] - self.df['TotalClaims']
        
        # Binary target for claim frequency: 1 if claim occurred, 0 otherwise
        self.df['Has_Claim'] = np.where(self.df['TotalClaims'] > 0, 1, 0)

    def run_frequency_ab_test(self, feature_col, control_group, test_group):
        """
        Executes a Chi-Square test of independence for Claim Frequency (Categorical KPI).
        """
        # Segment data into explicit Control and Test boundaries
        df_ab = self.df[self.df[feature_col].isin([control_group, test_group])].copy()
        
        if df_ab[df_ab[feature_col] == control_group].empty or df_ab[df_ab[feature_col] == test_group].empty:
            return {"KPI": "Claim Frequency", "Test": "Chi-Square", "p_value": np.nan, "Decision": "Fail to Reject H0 (Insufficient Data)"}

        contingency_table = pd.crosstab(df_ab[feature_col], df_ab['Has_Claim'])
        
        # Fallback if structural dimensions don't fit a 2x2 matrix
        if contingency_table.shape != (2, 2):
            chi2, p_val = 0.0, 1.0
        else:
            chi2, p_val, _, _ = stats.chi2_contingency(contingency_table)
            
        decision = "Reject H0" if p_val < 0.05 else "Fail to Reject H0"
        
        return {
            "KPI": "Claim Frequency",
            "Test": f"Chi-Square ({control_group} vs {test_group})",
            "p_value": float(f"{p_val:.5f}"),
            "Decision": decision
        }

    def run_numerical_ab_test(self, feature_col, control_group, test_group, metric_col='TotalClaims', active_claims_only=False):
        """
        Executes an Independent Two-Sample T-Test (Welch's T-Test) for Severity or Margin (Numerical KPIs).
        """
        target_df = self.df.copy()
        if active_claims_only:
            target_df = target_df[target_df['TotalClaims'] > 0]
            
        control_series = target_df[target_df[feature_col] == control_group][metric_col].dropna()
        test_series = target_df[target_df[feature_col] == test_group][metric_col].dropna()
        
        # Statistical fallback check for lean distributions
        if len(control_series) < 2 or len(test_series) < 2:
            return {"KPI": metric_col, "Test": "Welch T-Test", "p_value": np.nan, "Decision": "Fail to Reject H0 (Low Sample)"}
            
        t_stat, p_val = stats.ttest_ind(control_series, test_series, equal_var=False)
        decision = "Reject H0" if p_val < 0.05 else "Fail to Reject H0"
        
        return {
            "KPI": metric_col,
            "Test": f"Welch T-Test ({control_group} vs {test_group})",
            "p_value": float(f"{p_val:.5f}"),
            "Decision": decision
        }
