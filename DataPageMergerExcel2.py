import pandas as pd

# Wczytanie danych
df = pd.read_excel(r'OCR_VERSION2.xlsx')

# Sortowanie danych wg 'SCIEZKA' i 'NUMER STRONY' dla upewnienia się, że kolejność jest zachowana
df = df.sort_values(by=['SCIEZKA', 'NUMER STRONY'])

# Pusty DataFrame dla wyników
result = pd.DataFrame()

# Iteracja po unikalnych ścieżkach
for path, group in df.groupby('SCIEZKA'):
    temp_df = pd.DataFrame()
    # Dodanie kolumn dla każdej strony
    for idx, row in enumerate(group.itertuples(), start=1):
        # Tworzenie nazw kolumn z sufiksami
        new_columns = {col: f'{col}_{idx}' for col in df.columns}
        # Tworzenie DataFrame dla pojedynczej strony
        page_df = pd.DataFrame([row[1:]], columns=df.columns).rename(columns=new_columns)
        # Łączenie DataFrame'ów wzdłuż osi kolumn
        temp_df = pd.concat([temp_df, page_df], axis=1)
    
    # Dodanie przetworzonego wiersza do wynikowego DataFrame
    if result.empty:
        result = temp_df
    else:
        result = pd.concat([result, temp_df], ignore_index=True)

# Usunięcie kolumny 'Index' jeśli istnieje
result.drop(columns=[col for col in result.columns if 'Index' in col], errors='ignore', inplace=True)



# Opcjonalnie zapisujemy wyniki do Excela
result.to_excel(r'EXCEL_TRANSFORM2_VERSION2.xlsx', index=False)
