import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

df = pd.read_csv('billboardTop100TotalDuration.csv')
df_1 = pd.read_csv('selected_columns_genre.csv')
df_2 = pd.read_csv('billboardTop100BPM.csv')
df_3 = pd.read_csv('billboardTop100Featuring.csv')
# print(df)

font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

genre_dbf = pd.concat([df_1, df['Duration_sec'], df_2['BPM'], df_3['Featuring']], axis = 1)

genre_dbf['Year-Month-Week'] = genre_dbf['Year'].astype(str) +  '-' + genre_dbf['Month'].astype(str) +  '-' + genre_dbf['Week'].astype(str)
# `top_10_per_100 = genre_dbf.groupby(genre_dbf.index // 100).head(100)`

genre_dbf['Score'] = 101 - genre_dbf['Rank']
genre_dbf.to_csv('GenreScore.csv', index = False)
genre_dbf['Quarter'] = ((genre_dbf['Month'] - 1) // 3) + 1
genre_dbf['Year-Quarter'] = genre_dbf['Year'].astype(str) +  '-' + genre_dbf['Quarter'].astype(str)
genre_dbf = genre_dbf.loc[genre_dbf['Artist'] == 'BTS']
print(genre_dbf)







# GenreScore = genre_dbf.groupby(['Year-Quarter', 'Genre'])['Score'].sum().reset_index(name = 'ScoreSum')
# # print(GenreScore)
# # GenreScore.to_csv('GenreQuarter.csv', index = False)
# def min_max_scale(group):
#     min = group['ScoreSum'].min()
#     max = group['ScoreSum'].max()
#     group['Score_Scale'] = (group['ScoreSum']-min) / (max-min)
#     return group

# # # GenreScore['GenreScore'] = GenreScore.groupby(['Year']).apply(min_max_scale)


# MinMaxgs = GenreScore.groupby(['Year-Quarter']).apply(min_max_scale)
# print(MinMaxgs)
# # MinMaxgs.to_csv('MinMaxQuarter.csv', index = False)

# # # 연도와 분기로 그룹화하여 평균 계산

# MinMaxgs['Year-Quarter'] = pd.Categorical(MinMaxgs['Year-Quarter'], ordered=True)
# top_genres_2014 = MinMaxgs[MinMaxgs['Year-Quarter'] == '2014-1'].nlargest(3, 'Score_Scale')
# top_genres_2023 = MinMaxgs[MinMaxgs['Year-Quarter'] == '2023-4'].nlargest(3, 'Score_Scale')

# # Create the line plot
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=MinMaxgs, x='Year-Quarter', y='Score_Scale', hue='Genre', marker='o')
# for i in range(len(top_genres_2014)):
#     if (top_genres_2014['Year-Quarter'][i] == '2014-1'):
#         plt.text(top_genres_2014['Year-Quarter'][i], top_genres_2014['Score_Scale'][i], top_genres_2014['Genre'][i], 
#                  horizontalalignment='left', size='medium', color='black', weight='semibold')
        
#     if (top_genres_2023['Year-Quarter'][i] == '2023-4'):
#         plt.text(top_genres_2023['Year-Quarter'][i], top_genres_2023['Score_Scale'][i], top_genres_2023['Genre'][i], 
#                  horizontalalignment='left', size='medium', color='black', weight='semibold')



# plt.title('Score Scale by Year-Quarter and Genre')
# plt.xlabel('Year-Quarter')
# plt.ylabel('Score Scale')
# plt.xticks(rotation=45)
# plt.legend().remove()
# plt.tight_layout()
# plt.show()