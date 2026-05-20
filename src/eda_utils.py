import pandas as pd
import numpy as np

class InsuranceDataProfiler:
    def __init__(self, df):
        self.df = df.copy()
        self._calculate_derived_metrics()

    def _calculate_derived_metrics(self):
        """Anchors derived KPIs requested by AlphaCare management."""
        # Ensure correct column nomenclature matches raw layouts
        p_col = 'TotalPremium' if 'TotalPremium' in self.df.columns else 'CalculatedPremiumPerTerm'
        c_col = 'TotalClaims'
        
        if p_col in self.df.columns and c_col in self.df.columns:
            # Derived KPI 1: Portfolio Margin
            self.df['Margin'] = self.df[p_col] - self.df[c_col]
            # Derived KPI 2: Loss Ratio per policy boundary
            self.df['Loss_Ratio'] = np.where(self.df[p_col] > 0, self.df[c_col] / self.df[p_col], 0)
        else:
            print("⚠️ Warning: Premium or Claim tracking vectors missing from active dataset columns.")

    def get_summary_statistics(self):
        """Returns descriptive statistics for structural data profiling."""
        cols_of_interest = [c for c in ['TotalPremium', 'TotalClaims', 'Margin', 'Loss_Ratio', 'CustomValueEstimate'] if c in self.df.columns]
        return self.df[cols_of_interest].describe().T

    def analyze_loss_ratio_by_dimension(self, dimension):
        """
        Computes aggregated loss ratios across a given column slice 
        (e.g., 'Province', 'Gender', 'VehicleType').
        """
        p_col = 'TotalPremium' if 'TotalPremium' in self.df.columns else 'CalculatedPremiumPerTerm'
        c_col = 'TotalClaims'
        
        if dimension not in self.df.columns:
            return f"❌ Dimension '{dimension}' not present in dataset matrix."
            
        summary = self.df.groupby(dimension).agg(
            Total_Premiums=(p_col, 'sum'),
            Total_Claims=(c_col, 'sum'),
            Policy_Count=(p_col, 'count')
        ).reset_index()
        
        summary['Segment_Loss_Ratio'] = summary['Total_Claims'] / summary['Total_Premiums']
        summary['Segment_Margin'] = summary['Total_Premiums'] - summary['Total_Claims']
        return summary.sort_values(by='Segment_Loss_Ratio', ascending=False)
