import pandas as pd
import numpy as np
import os

def download_and_clean_data():
    """Download the IBM Telco churn sample, clean it and add Tableau-friendly fields."""
    print("1. Downloading the actual dataset from the original repository...")
    # Raw GitHub mirror of IBM's original sample file
    url = "https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        df = pd.read_csv(url)
        print(f"Dataset downloaded successfully. Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        # Untouched copy of the source, kept for lineage
        original_file_path = os.path.join(script_dir, "Original_Telco_Churn.csv")
        df.to_csv(original_file_path, index=False)
        print(f"Original dataset saved in: {original_file_path}")
        
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    print("\n2. Starting data cleaning...")
    # TotalCharges arrives as text: missing values are stored as a blank " "
    df['TotalCharges'] = df['TotalCharges'].replace(" ", np.nan)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

    # The 11 blanks are customers with tenure 0, not billed yet: their total really is 0
    df['TotalCharges'] = df['TotalCharges'].fillna(0)

    print("3. Feature Engineering...")
    # 0/1 flag, so the churn rate is AVG([Churn_Flag]) in Tableau, LODs included
    df['Churn_Flag'] = np.where(df['Churn'] == 'Yes', 1, 0)

    # Tenure bands (tenure goes from 0 to 72 months)
    df['Tenure_Group'] = pd.cut(df['tenure'], 
                                bins=[-1, 12, 24, 48, 60, np.inf], 
                                labels=['0-12 months', '13-24 months', '25-48 months', '49-60 months', '61-72 months'])

    # SeniorCitizen is the only 0/1 column; Yes/No matches every other flag in the dataset
    df['SeniorCitizen'] = df['SeniorCitizen'].map({1: 'Yes', 0: 'No'})


    print("4. Saving the final dataset...")
    # utf-8-sig writes a BOM, so Excel also opens the CSV with the right encoding
    cleaned_file_path = os.path.join(script_dir, "Cleaned_Telco_Churn.csv")
    df.to_csv(cleaned_file_path, encoding='utf-8-sig', index=False)
    print(f"-> Process complete! The file ready for Tableau is:{cleaned_file_path}\n")

if __name__ == "__main__":
    download_and_clean_data()