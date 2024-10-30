import pandas as pd

df = pd.read_csv('billboardTop100Total.csv')

df_BTS = df.loc[df['Artist'].str.contains('BTS')]
# df_BTS.to_csv('BTS.csv', index = False)
print(df_BTS)