import pandas as pd

try:
    df = pd.read_excel('Dubai University List.xlsx')
    # Get all rows
    universities = df['University Name'].dropna().tolist()
    
    with open('all_universities.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total Universities Found: {len(universities)}\n")
        f.write("-" * 30 + "\n")
        for i, uni in enumerate(universities, 1):
            f.write(f"{i}. {uni}\n")
            
    print(f"Successfully extracted {len(universities)} names.")
except Exception as e:
    print(f"Error: {e}")
