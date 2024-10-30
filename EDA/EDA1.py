import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('billboardTop100Total.csv')
df_error = df.loc[df['Artist'].isna()]
df_error[['Title', 'Artist']] = df_error['Title'].str.split('Meek', n=1, expand=True)
print(df_error)

df_concat = pd.concat([df, df_error])
print(df_concat.info())

df = df_concat.dropna(subset = 'Artist', axis = 0)
print(df.info())

df_1 = pd.read_csv('billboardTop100Totalduplicate.csv')
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

featuring = df[df['Artist'].str.contains('Featuring')]
print(featuring)
non_featuring = df[~df['Artist'].str.contains('Featuring')]
monthly_count = featuring.groupby(['Year', 'Month']).size().reset_index(name='Count')
monthly_count_1= non_featuring.groupby(['Year', 'Month']).size().reset_index(name='Count')
monthly_count['Year-Month'] = monthly_count['Year'].astype(str) + '-' + monthly_count['Month'].astype(str)
monthly_count_1['Year-Month'] = monthly_count_1['Year'].astype(str) + '-' + monthly_count['Month'].astype(str)


quarter_count = monthly_count.groupby(monthly_count.index // 6).agg({'Year-Month': 'first','Count': 'sum'}).reset_index(drop=True)
quarter_count_1 = monthly_count_1.groupby(monthly_count_1.index // 6).agg({'Year-Month': 'first','Count': 'sum'}).reset_index(drop=True)
quarter_count_total = pd.concat([quarter_count, quarter_count_1], axis = 1)
# print(quarter_count)
# print(quarter_count_1)
print(quarter_count_total)
x_1 = quarter_count['Year-Month']
y_1 = quarter_count['Count']
x = quarter_count_1['Year-Month']
y = quarter_count_1['Count']
plt.figure(figsize=(12, 6))
plt.plot(quarter_count['Year-Month'], quarter_count['Count'], color='orange',linestyle ='-')
plt.plot(quarter_count_1['Year-Month'], quarter_count_1['Count'], color='skyblue',linestyle ='-')

for i in range(len(x)):
    height = y[i]
    plt.text(x[i], height+0.25, '%.0f'%height, ha = 'center')
plt.text('2017-7', 2027, 'Important Point', fontsize = 12, color = 'red', ha = 'center', va = 'top' )

for j in range(len(x_1)):
    height = y_1[j]
    plt.text(x_1[j], height+0.25, '%.0f'%height, ha = 'center')


plt.legend(loc = 'upper right')
plt.title('Quarter Featuring Count from 2014 to 2023')
plt.xlabel('Year-Month')
plt.ylabel('Featuring Count')
plt.tight_layout()
plt.show()