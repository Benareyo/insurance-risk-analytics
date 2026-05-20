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

import matplotlib.pyplot as plt
import seaborn as sns

def plot_geographic_risk(df, output_path='notebooks/plots/geo_risk.png'):
    """Generates a professional comparative chart of loss ratios by province."""
    plt.figure(figsize=(12, 6))
    # Using CalculatedPremiumPerTerm if TotalPremium isn't explicitly named
    p_col = 'TotalPremium' if 'TotalPremium' in df.columns else 'CalculatedPremiumPerTerm'
    
    geo_df = df.groupby('Province').agg(
        Claims=('TotalClaims', 'sum'),
        Premiums=(p_col, 'sum')
    ).reset_index()
    geo_df['Loss_Ratio'] = (geo_df['Claims'] / geo_df['Premiums']) * 100
    geo_df = geo_df.sort_values(by='Loss_Ratio', ascending=False)
    
    sns.barplot(x='Loss_Ratio', y='Province', data=geo_df, palette='coolwarm')
    plt.axvline(x=100, color='red', linestyle='--', label='Breakeven Threshold (100%)')
    plt.title('AlphaCare Portfolio Loss Ratio Across South African Provinces', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Loss Ratio (%) - Lower Indicates Higher Profitability', fontsize=11)
    plt.ylabel('Province', fontsize=11)
    plt.legend(loc='lower right')
    plt.tight_layout()
    
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"📊 Geographic Risk Visualization saved cleanly to: {output_path}")

def plot_financial_distributions(df, output_path='notebooks/plots/financial_outliers.png'):
    """Generates boxplots to capture risk metrics and outlier polarization."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left subplot: Custom Value Estimates
    if 'CustomValueEstimate' in df.columns:
        sns.boxplot(y=df['CustomValueEstimate'], ax=axes[0], color='#3b82f6')
        axes[0].set_title('Vehicle Custom Value Estimate Spread', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Asset Value (ZAR)')
        
    # Right subplot: Total Claims
    if 'TotalClaims' in df.columns:
        sns.boxplot(y=df['TotalClaims'], ax=axes[1], color='#ef4444')
        axes[1].set_title('Total Claim Outlays Polarization Boxplot', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Claim Amount (ZAR)')
        
    plt.suptitle('Outlier Identification Matrix for Key Financial Variables', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"📊 Outlier Distribution Visualization saved to: {output_path}")

def plot_temporal_trends(df, output_path='notebooks/plots/temporal_trends.png'):
    """Plots monthly claim frequency and severity shifts across the 18-month window."""
    if 'TransactionMonth' not in df.columns:
        print("⚠️ Skipping temporal plot: 'TransactionMonth' column missing or unparsed.")
        return
        
    # Group by transaction timeline monthly intervals
    df['Month_Period'] = df['TransactionMonth'].dt.to_period('M')
    monthly_stats = df.groupby('Month_Period').agg(
        Avg_Severity=('TotalClaims', lambda x: x[x > 0].mean()),
        Claim_Count=('TotalClaims', lambda x: (x > 0).sum()),
        Total_Policies=('TotalClaims', 'count')
    ).reset_index()
    
    monthly_stats['Claim_Frequency'] = (monthly_stats['Claim_Count'] / monthly_stats['Total_Policies']) * 100
    monthly_stats['Month_Period'] = monthly_stats['Month_Period'].astype(str)
    
    fig, ax1 = plt.subplots(figsize=(13, 6))
    
    # Primary axis: Claim Frequency Line
    color = '#0f2c59'
    ax1.set_xlabel('Timeline Horizon (Feb 2014 - Aug 2015)', fontsize=11, labelpad=10)
    ax1.set_ylabel('Claim Frequency (%)', color=color, fontsize=11, fontweight='bold')
    sns.lineplot(x='Month_Period', y='Claim_Frequency', data=monthly_stats, marker='o', color=color, linewidth=2.5, ax=ax1, label='Frequency (%)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticklabels(monthly_stats['Month_Period'], rotation=45)
    
    # Secondary axis for Severity
    ax2 = ax1.twinx()
    color_sec = '#ea580c'
    ax2.set_ylabel('Average Claim Severity (ZAR)', color=color_sec, fontsize=11, fontweight='bold')
    sns.lineplot(x='Month_Period', y='Avg_Severity', data=monthly_stats, marker='s', color=color_sec, linewidth=2.5, ax=ax2, label='Severity (ZAR)')
    ax2.tick_params(axis='y', labelcolor=color_sec)
    
    plt.title('18-Month Operational Risk Run-Rate Trends (ACIS Portfolio)', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"📊 Temporal Trend Analysis saved cleanly to: {output_path}")
