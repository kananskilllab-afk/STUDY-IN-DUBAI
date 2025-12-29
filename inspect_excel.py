import pandas as pd
import os

file_path = 'Dubai University List.xlsx'
try:
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        print("Excel content loaded successfully.")
        print("Columns:", df.columns.tolist())
        print("First 5 rows:")
        print(df.head())
        # Check for columns that might look like image filenames
        for col in df.columns:
            if df[col].astype(str).str.contains(r'\.(png|jpg|jpeg|svg)', case=False).any():
                print(f"Column '{col}' seems to contain image filenames.")
    else:
        print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error reading Excel file: {e}")
