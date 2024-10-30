import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

df_1 = pd.read_csv('billboardTop100Totalduplicate_with_BPM.csv')

# print(df)

# df_1['TitleArtist'] = df_1['Title'] + df_1['Artist']
# # print(df)

# df = pd.read_csv('billboardTop100Total.csv')
# df_error = df.loc[df['Artist'].isna()]
# df_error[['Title', 'Artist']] = df_error['Title'].str.split('Meek', n=1, expand=True)

# df_concat = pd.concat([df, df_error])

# df = df_concat.dropna(subset = 'Artist', axis = 0)
# df = df.sort_values(by=['Year', 'Month'])

# df['TitleArtist'] = df['Title'] + df['Artist']
# # print(df_total)

# def match(row):
#     # row에서 TitleArtist 값을 가져와 df에서 확인
#     matched_row = df_1[df_1['TitleArtist'] == row['TitleArtist']]
    
#     if not matched_row.empty:
#         return matched_row['BPM'].values[0]  # 일치하는 BPM 반환
#     else:
#         return 0  # 일치하는 값이 없으면 0 반환

# # BPM 열 업데이트
# df['BPM'] = df.apply(match, axis=1)
# print(df)

# 결과 출력
# print(df_total)
# df.to_csv('billboardTop100BPM.csv', index = False)

df_bpm = pd.read_csv('billboardTop100BPM.csv')
df_bpm = df_bpm.loc[(df_bpm['Artist'].str.contains('BTS'))]
df_gerne = pd.read_csv('selected_columns_genre.csv')

font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)
print()
df_bpm['Year-Month'] = pd.to_datetime(df_bpm[['Year', 'Month']].assign(DAY=1))

# Year-Month별 평균 BPM 계산

bpm_mean = df_bpm.groupby(['Year','Month'])['BPM'].mean().reset_index(name='Average BPM')
print(bpm_mean)
bpm_mean['Year-Month'] = bpm_mean['Year'].astype(str) + '-' + bpm_mean['Month'].astype(str)

# monthly_data_start = monthly_data_start.dropna()
# 연도별로 그룹화하여 plot에 사용할 준비
# bpm_mean['Year'] = bpm_mean['Year-Month'].dt.year
# bpm_mean['Month'] = bpm_mean['Year-Month'].dt.month

# 라인 플롯 그리기
# plt.figure(figsize=(14, 7))

# for year in range(2014, 2024):
#     monthly_data = bpm_mean[bpm_mean['Year'] == year]
#     plt.plot(monthly_data['Month'], monthly_data['Average BPM'], marker='o', label=str(year))

# plt.xticks(monthly_data['Month'])
# plt.title('Average BPM by Month from 2014 to 2023')
# plt.xlabel('Month')
# plt.ylabel('Average BPM')
# plt.legend(title='Year', loc = 'upper right')
# plt.grid()
# plt.tight_layout()
# plt.show()
plt.figure(figsize = (10,7))

x = np.arange(len(bpm_mean['Year-Month']))
y = bpm_mean['Average BPM']

for i in range(len(x)):
    height = y[i]
    plt.text(x[i]-0.2, height+2, '%.1f'%height)


plt.plot(bpm_mean['Year-Month'], bpm_mean['Average BPM'], linestyle = '-', marker = 'o')
plt.xticks(bpm_mean['Year-Month'], rotation=30)
plt.title('BTS BPM by Month from 2014 to 2023')
plt.xlabel('Month')
plt.ylabel('Average BPM')
plt.legend(title='Year', loc = 'upper right')
plt.grid()
plt.tight_layout()
plt.show()