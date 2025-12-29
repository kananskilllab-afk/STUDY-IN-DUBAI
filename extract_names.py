import pandas as pd
import sys

# Force utf-8 output for console if possible, but file is safer
try:
    df = pd.read_excel('Dubai University List.xlsx')
    with open('university_names.txt', 'w', encoding='utf-8') as f:
        f.write("Columns: " + ", ".join(df.columns.astype(str)) + "\n")
        f.write("-" * 20 + "\n")
        # Assuming the first column or a column named 'University'/'Name' holds the names
        # Let's just dump the first few rows of all columns
        f.write(df.head(20).to_string())
    print("Success")
except Exception as e:
    with open('university_names.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}")
    print("Error")
