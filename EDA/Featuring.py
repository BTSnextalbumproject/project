import pandas as pd

df = pd.read_csv('billboardTop100Total.csv')
df_error = df.loc[df['Artist'].isna()]
df_error[['Title', 'Artist']] = df_error['Title'].str.split('Meek', n=1, expand=True)
print(df_error)

df_concat = pd.concat([df, df_error])

df = df_concat.dropna(subset = 'Artist', axis = 0)
print(df)
def Featuring(row):
    if 'Featuring' in row['Artist']:
        return 1  
    else:
        return 0  

# Featuring 열 업데이트
df['Featuring'] = df.apply(Featuring, axis=1)
sorted_grouped = df.sort_values(by=['Year', 'Month'])
print(sorted_grouped)

sorted_grouped.to_csv('billboardTop100Featuring.csv', index = False)