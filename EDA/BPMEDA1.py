import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# df_1 = pd.read_csv('BTS.csv')

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

df_bpm = pd.read_csv('final_data_senti.csv')
df_bpm = df_bpm.loc[(df_bpm['Artist'].str.contains('BTS'))]
print(df_bpm)
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

df_bpm['Year-Month'] = df_bpm['Year'].astype(str) + '-' + df_bpm['Month'].astype(str)
# print(df_bpm)
bpm_mean = df_bpm.groupby(['Year'])['BPM'].mean().reset_index(name='Average BPM')
# print(bpm_mean)
print(bpm_mean)
# bpm_mean['Year-Month'] = bpm_mean['Year'].astype(str) + '-' + bpm_mean['Month'].astype(str)
# # print(bpm_mean)

# quarter_bpm = bpm_mean.groupby(bpm_mean.index // 1).agg({'Year-Month': 'first','Average BPM': 'mean'}).reset_index(drop=True)
# print(quarter_bpm)



x = bpm_mean['Year']
y = bpm_mean['Average BPM']

plt.figure(figsize=(14, 6))
x = np.arange(len(bpm_mean['Year']))  # X축 위치 설정
# # Count1과 Count2를 같은 축에 그리기

plt.plot(x, bpm_mean['Average BPM'], color = 'skyblue', linestyle = '-', marker = 'o')

for i in range(len(x)):
    height = y[i]
    plt.text(x[i]-0.25, height+0.1, '%.1f'%height)

# for i in range(len(x)):
#     height = y[i]
#     plt.text(x[i]-0.2, height+300, '%.1f'%height)

# for i in range(len(x)):
#     height = y_2[i]
#     plt.text(x[i]-0.25, height+0.5, '%.0f'%height)

plt.legend(loc = 'upper right')
plt.title('BTS of BPM from 2014 to 2023')
plt.xticks(x, bpm_mean['Year'], rotation=45)
plt.xlabel('Year')
plt.ylabel('BTS of BPM')
plt.ylim(50,200)
plt.tight_layout()

plt.show()