import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('billboardTop100Total.csv')
df_error = df.loc[df['Artist'].isna()]
df_error[['Title', 'Artist']] = df_error['Title'].str.split('Meek', n=1, expand=True)
print(df_error)

df_concat = pd.concat([df, df_error])
print(df_concat.info())

df = df_concat.dropna(subset = 'Artist', axis = 0)
print(df.info())


font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

featuring = df[df['Artist'].str.contains('Featuring')]
non_featuring = df[~df['Artist'].str.contains('Featuring')]
monthly_count = featuring.groupby(['Year', 'Month']).size().reset_index(name='Count1')
monthly_count_1= non_featuring.groupby(['Year', 'Month']).size().reset_index(name='Count2')
monthly_count['Year-Month'] = monthly_count['Year'].astype(str) + '-' + monthly_count['Month'].astype(str)
monthly_count_1['Year-Month1'] = monthly_count_1['Year'].astype(str) + '-' + monthly_count['Month'].astype(str)


quarter_count = monthly_count.groupby(monthly_count.index // 6).agg({'Year-Month': 'first','Count1': 'sum'}).reset_index(drop=True)
quarter_count_1 = monthly_count_1.groupby(monthly_count_1.index // 6).agg({'Year-Month1': 'first','Count2': 'sum'}).reset_index(drop=True)
quarter_count_total = pd.concat([quarter_count, quarter_count_1['Count2']], axis = 1)
# print(quarter_count)
# print(quarter_count_1)
# print(quarter_count_total)

# x = quarter_count['Year-Month1']
# y = quarter_count['Count']

# x_1 = quarter_count_1['Year-Month']
# y_1 = quarter_count_1['Count']
print(quarter_count_total)

plt.figure(figsize=(14, 6))
x = np.arange(len(quarter_count_total['Year-Month']))  # X축 위치 설정

y = quarter_count_total['Count1']
y_1 = quarter_count_total['Count2']
# Count1과 Count2를 같은 축에 그리기
plt.bar(x - 0.2, quarter_count_total['Count1'], width=0.4, label='Featuring', color='skyblue', align='center')
plt.bar(x + 0.2, quarter_count_total['Count2'], width=0.4, label='Non-Featuring', color='orange', align='center')
plt.plot(quarter_count['Year-Month'], quarter_count['Count1'], color='blue',linestyle ='-')
plt.plot(quarter_count_1['Year-Month1'], quarter_count_1['Count2'], color='red',linestyle ='-')

for i in range(len(x)):
    height = y_1[i]
    plt.text(x[i], height+0.5, '%.0f'%height)

for i in range(len(x)):
    height = y[i]
    plt.text(x[i]-0.4, height+0.5, '%.0f'%height)


plt.text('2017-7', 2027, 'Important Point', fontsize = 12, color = 'red', ha = 'center', va = 'top' )

# 그래프 설정
plt.title('Featuring and Non-Featuring by Year-Month')
plt.xlabel('Year-Month')
plt.ylabel('Counts')
plt.xticks(x, quarter_count_total['Year-Month'], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()