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
genre_dbf['date'] = genre_dbf['Year-Month-Week'].apply(lambda x: f"{x[2:]}" if x.startswith("20") else x)
print(genre_dbf)

genre_dbf['Score'] = 101 - genre_dbf['Rank']
genre_dbf.to_csv('GenreScore.csv', index = False)
genre_dbf['Quarter'] = ((genre_dbf['Month'] - 1) // 3) + 1
genre_dbf['Year-Quarter'] = genre_dbf['Year'].astype(str) +  '-' + genre_dbf['Quarter'].astype(str)
genre_dbf = genre_dbf.loc[genre_dbf['Artist'].str.contains('BTS')]
print(genre_dbf)

plt.figure(figsize=(10,7))
sns.lineplot(data = genre_dbf, x = 'date', y ='Duration_sec', hue = 'Genre')

top_genres_2017 = genre_dbf[genre_dbf['Year-Month-Week'] == '17-10-1'].nlargest(3, 'Duration_sec')
top_genres_2023 = genre_dbf[genre_dbf['Year-Month-Week'] == '23-6-4'].nlargest(3, 'Duration_sec')

for i in range(len(top_genres_2017)):
    if (top_genres_2017['Year-Month-Week'][i] == '17-10-1'):
        plt.text(top_genres_2017['date'][i], top_genres_2017['Duration_sec'][i], top_genres_2017['Genre'][i], 
                 horizontalalignment='left', size='medium', color='black', weight='semibold')
        
    if (top_genres_2023['Year-Month-Week'][i] == '23-6-4'):
        plt.text(top_genres_2023['date'][i], top_genres_2023['Duration_sec'][i], top_genres_2023['Genre'][i], 
                 horizontalalignment='left', size='medium', color='black', weight='semibold')


plt.xticks(genre_dbf['date'], rotation=45)
plt.title('Duration_sec by Year-Month-Week from 2017 to 2023 Of BTS')
plt.xlabel('Year-Month-Week')
plt.ylabel('Average Duration_sec')
plt.legend(title='Genre', loc = 'upper right')
plt.grid()
plt.tight_layout()
plt.show()
