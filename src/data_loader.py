import pandas as pd
import os

def load_insurance_data(file_path="data/insurance_data.csv"):
    """
    Safely ingest the ACIS insurance dataset and perform initial type adjustments.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Target data file not found at: {file_path}. Please place your downloaded CSV there.")
        
    print(f"🔄 Ingesting dataset from {file_path}...")
    df = pd.read_csv(file_path)
    
    # Strip whitespace from column names and cast to clean types
    df.columns = [col.strip() for col in df.columns]
    
    # Attempt to automatically parse transactional timeline dates
    if 'TransactionMonth' in df.columns:
        df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'], errors='coerce')
        
    print(f"✅ Loaded matrix successfully. Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df
