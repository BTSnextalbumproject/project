#./tf_idf.csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

font_path = "C:/Windows/Fonts/malgun.ttf"  

fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())

file_path = './tf_idf.csv'
df = pd.read_csv(file_path)

stopwords = ['boo', 'na', 'da', 'la', 'doo', 'oh', 'yeah', 'ooh', 'que', 'nigga', 'like', 'want', 
             'know', 'baby', 'uh', 'woo', 'hey', 'yo', 'eh', 'ha', 'bam', 'wiggle', 'uhh', 'blah', 'mm', 
             'boaw', 'shh', 'hol', 'dah']
filtered_df = df[~df['keyword'].isin(stopwords)]

top_keywords_per_year = filtered_df.loc[filtered_df.groupby(['year'])['TF-IDF'].idxmax()]

plt.figure(figsize=(15, 10))
for i, year in enumerate(sorted(top_keywords_per_year['year'].unique()), 1):
    plt.subplot(2, 5, i)  
    year_data = top_keywords_per_year[top_keywords_per_year['year'] == year]
    wordcloud = WordCloud(
        font_path=font_path, width=400, height=300, background_color="white", colormap="viridis"
    ).generate_from_frequencies(year_data.set_index('keyword')['TF-IDF'])
    
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(f"{year}년 주요 키워드", fontproperties=fontprop)
    plt.axis("off")

plt.suptitle("연도별 키워드 트렌드 변화 (2014 - 2023)", fontproperties=fontprop)
plt.tight_layout()
plt.show()
