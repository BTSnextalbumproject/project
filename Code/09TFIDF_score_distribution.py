#./tf_idf.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 엑셀 파일 로드
file_path = './tf_idf.csv'
df = pd.read_csv(file_path)

# 불용어 리스트 설정 (불필요한 단어들 제거)
stopwords = ['boo', 'na', 'da', 'la', 'doo', 'oh', 'yeah', 'ooh', 'que', 'nigga', 'like', 'want', 
             'know', 'baby', 'uh', 'woo', 'hey', 'yo', 'eh', 'ha', 'bam', 'wiggle', 'uhh', 'blah', 'mm', 
             'boaw', 'shh', 'hol', 'dah']

# 불용어 제거
filtered_df = df[~df['keyword'].isin(stopwords)]

# TF-IDF Score 분포 시각화
plt.figure(figsize=(8, 6))
sns.histplot(filtered_df['TF-IDF'], bins=30, kde=True)
plt.title('TF-IDF Score Distribution')
plt.xlabel('TF-IDF Score')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
