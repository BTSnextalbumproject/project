import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

# df = pd.read_csv('billboardTop100Total.csv')
# df_1 = pd.read_csv('billboardTop100Totalduplicate_with_Duration.csv')

# df_1['TitleArtist'] = df_1['Title'] + df_1['Artist']

# df['TitleArtist'] = df['Title'] + df['Artist']

# def match(row):
#     # row에서 TitleArtist 값을 가져와 df에서 확인
#     matched_row = df_1[df_1['TitleArtist'] == row['TitleArtist']]
    
#     if not matched_row.empty:
#         return matched_row['Duration_sec'].values[0]  # 일치하는 BPM 반환
#     else:
#         return 0  # 일치하는 값이 없으면 0 반환

# df['Duration_sec'] = df.apply(match, axis=1)

# df.to_csv('billboardTop100TotalDuration.csv', index = False)

df = pd.read_csv('billboardTop100TotalDuration.csv')
df_1 = pd.read_csv('selected_columns_genre.csv')
df_2 = pd.read_csv('billboardTop100BPM.csv')
df_3 = pd.read_csv('billboardTop100Featuring.csv')
# print(df)

font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)


genre_dbf = pd.concat([df_1, df['Duration_sec'], df_2['BPM'], df_3['Featuring']], axis = 1)

genre_dbf['Year-Month'] = genre_dbf['Year'].astype(str) +  '-' + genre_dbf['Month'].astype(str)
top_10_per_100 = genre_dbf.groupby(genre_dbf.index // 100).head(10)

top10_quarter = top_10_per_100.groupby(['Year','Month'])['Genre'].value_counts().reset_index(name = 'Count')
# print(top10_quarter)
# quarter_count = top10_quarter.groupby(top10_quarter.index // 6).agg({'Year-Month': 'first','Count': 'sum'}).reset_index(drop=True)
# print(quarter_count)


# 1. 전체 개수에 대한 비율
top10_quarter['Year-Month'] = top10_quarter['Year'].astype(str) +  '-' + top10_quarter['Month'].astype(str)
total_count = top10_quarter.groupby('Year-Month')['Count'].transform('sum')
top10_quarter['Count_Ratio'] = top10_quarter['Count']/total_count
top10_quarter = top10_quarter[['Year','Month','Year-Month', 'Genre', 'Count', 'Count_Ratio']]
top10_quarter['Score'] = top10_quarter['Count'] * top10_quarter['Count_Ratio']
print(top10_quarter)
# def remove_top_two(top10_quarter):
#     top_two_counts = top10_quarter['Count'].nlargest(3)
#     return top10_quarter[~top10_quarter['Count'].isin(top_two_counts)]
# top10_quarter = top10_quarter.groupby('Year-Month', group_keys=False).apply(remove_top_two)
# print(top10_quarter)
'''
    Year-Month     Genre  Count  Count_Ratio     Score
0       2014-1       POP     14     0.466667  6.533333
1       2014-1      랩/힙합      6     0.200000  1.200000
2       2014-1      록/메탈      3     0.100000  0.300000
3       2014-1       발라드      3     0.100000  0.300000
4       2014-1        포크      3     0.100000  0.300000
..         ...       ...    ...          ...       ...
645    2023-12  R&B/Soul      8     0.160000  1.280000
646    2023-12      랩/힙합      8     0.160000  1.280000
647    2023-12        재즈      8     0.160000  1.280000
648    2023-12        댄스      4     0.080000  0.320000
649    2023-12       컨트리      1     0.020000  0.020000
'''


plt.figure(figsize=(12, 6))
sns.lineplot(data=top10_quarter, x='Genre', y='Score', hue='Month', marker='o')

# 축 및 제목 설정
plt.xticks(rotation=45)
plt.title('Month Average Score by Genre')
plt.xlabel('Month Group')
plt.ylabel('Average Score')
plt.legend(title='Month', loc = 'upper right')
plt.grid()
plt.tight_layout()
plt.show()



# plt.figure(figsize = (10,7))
# for year in range(2014, 2024):
#     monthly_data = top10_quarter[top10_quarter['Year'] == year]
#     plt.plot(monthly_data['Genre'], monthly_data['Score'], marker='o', label=str(year))

# plt.xticks(monthly_data['Month'])
# plt.title('Score from 2014 to 2023')
# plt.xlabel('Month')
# plt.ylabel('Score')
# plt.legend(title='Year', loc = 'upper right')
# plt.grid()
# plt.tight_layout()
# plt.show()


# 2. MinMaxScale

print(top10_quarter)

# def min_max_scale(group):
#     min = group['Count'].min()
#     max = group['Count'].max()
#     group['Count_Scale'] = (group['Count']-min) / (max-min)
#     return group

# top_10_quarter_group = top10_quarter.groupby('Year-Month').apply(min_max_scale)
# print(top_10_quarter_group)
'''
2014-1     0    2014      1       POP     14     2014-1     1.000000
           1    2014      1      랩/힙합      6     2014-1     0.384615
           2    2014      1      록/메탈      3     2014-1     0.153846
           3    2014      1       발라드      3     2014-1     0.153846
           4    2014      1        포크      3     2014-1     0.153846
...              ...    ...       ...    ...        ...          ...
2023-9     621  2023      9        댄스      5     2023-9     0.090909
           622  2023      9      록/메탈      5     2023-9     0.090909
           623  2023      9    일렉트로니카      5     2023-9     0.090909
           624  2023      9  R&B/Soul      4     2023-9     0.000000
           625  2023      9       컨트리      4     2023-9     0.000000
'''


# plt.figure(figsize=(12, 6))
# sns.lineplot(data=top_10_quarter_group, x='Year-Month', y='Score', hue='Genre', marker='o')

# # 축 및 제목 설정
# plt.xticks(rotation=45)
# plt.title('6-Month Average Score by Genre')
# plt.xlabel('6-Month Group')
# plt.ylabel('Average Score')
# plt.legend(title='Genre', loc = 'upper right')
# plt.grid()
# plt.tight_layout()
# plt.show()

# genre_dbf['Logic'] = np.where(genre_dbf['Genre'] == '컨트리', 1,0)
# print(genre_dbf)
# font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
# matplotlib.rc('font', family=font_name)

duration_1 = genre_dbf.groupby(['Year','Month'])['Duration_sec'].mean().reset_index(name='Duration_sec')
duration_2 = genre_dbf.groupby(['Year','Month'])['BPM'].mean().reset_index(name='BPM')
duration_3 = genre_dbf.groupby(['Year','Month'])['Duration_sec'].size().reset_index(name='Count')
# genre_counts = df.groupby(['Year', 'Genre']).size().reset_index(name='Count')
duration = pd.concat([duration_1,duration_2['BPM'],duration_3['Count']], axis = 1)

duration['Duration_Average'] = duration['Duration_sec']/duration['Count'] 
duration['BPM_Average'] = duration['BPM']/duration['Count'] 

print(stats.pearsonr(duration['Duration_sec'], duration['BPM']))
print(duration)

# # BPM과 Duration 상관관계 (장르는 컨트리만)
plt.figure(figsize=(10, 6))
sns.regplot(x='BPM_Average', y='Duration_Average', data=duration, marker='o', line_kws={'color': 'red'})
sns.lineplot(data=duration, x='BPM_Average', y='Duration_Average', hue='Month', marker='o')
plt.title('Linear Regression: Duration (Seconds) vs BPM')
plt.xlabel('Duration (Seconds)')
plt.ylabel('BPM')
plt.grid()
plt.show()

# 1. 장르별 Duration_sec

# plt.figure(figsize=(12, 6))
# sns.lineplot(x='Genre', y='Duration_sec', data=genre_dbf)
# plt.title('Duration (Seconds) by Genre')
# plt.xlabel('Genre')
# plt.ylabel('Duration (Seconds)')
# plt.xticks(rotation=45)
# plt.grid(axis='y')
# plt.show()

