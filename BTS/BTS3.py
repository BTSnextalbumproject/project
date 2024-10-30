import pandas as pd
import ast
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import seaborn as sns

df = pd.read_csv('final_data_senti.csv').drop('Unnamed: 0', axis = 1)
df[['R', 'G', 'B']] = df['rgb1'].dropna().apply(lambda x: pd.Series([int(i) for i in x.strip('()').split(',')]))
# 2. 결측값 처리 - 각 칼럼의 평균으로 대체
df['R'] = df['R'].fillna(df['R'].mean())
df['G'] = df['G'].fillna(df['G'].mean())
df['B'] = df['B'].fillna(df['B'].mean())
# 3. R, G, B 칼럼의 데이터 타입을 int로 변환
df[['R', 'G', 'B']] = df[['R', 'G', 'B']].astype(int)
df['First_Genre'] = df['Genre'].astype(str).str.split(',').str[0]
print(df[['Genre', 'First_Genre']].head())
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import shap

# PCA를 위한 데이터 준비
numeric_features = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
numeric_features.remove('Rank')  # 타겟 변수는 제외
df['Top20'] = np.where(df['Rank'] <= 20, '1','0')
df = df.loc[(df['Artist'].str.contains('BTS'))]
print(df)

genre_color = df.groupby('First_Genre')[['R','G','B']].mean().reset_index()
print(genre_color)

color = [(79/255, 58/255, 75/255),
         (238/255, 199/255, 192/255),
         (100/255, 95/255, 108/255),
         (249/255, 218/255, 7/255),
         (85/255, 74/255, 157/255)]

fig, axs = plt.subplots(1, 5, figsize=(12, 4))

# 색상 표시
for ax, color in zip(axs, color):
    ax.imshow([[color]])  # 색상을 단일 블록으로 표시
    ax.axis('off')        # 축 숨기기

# 제목 추가
axs[0].set_title('POP (RGB: 79, 58, 75)', fontsize=12)
axs[1].set_title('댄스 (RGB: 238, 199, 192)', fontsize=12)
axs[2].set_title('랩/힙합 (RGB: 100, 95, 108)', fontsize=12)
axs[3].set_title('록/메탈 (RGB: 249, 218, 7)', fontsize=12)
axs[4].set_title('R&B/Soul (RGB: 85, 74, 157)', fontsize=12)
plt.tight_layout()  # 레이아웃 조정
plt.show()

color = [(120/255, 154/255, 160/255),
         (120/255, 214/255, 198/255),
         (120/255, 138/255, 153/255),
         (120/255, 95/255, 108/255),
         (120/255, 218/255, 7/255),
         (120/255, 100/255, 168/255)]

fig, axs = plt.subplots(1, 6, figsize=(12, 4))

# 색상 표시
for ax, color in zip(axs, color):
    ax.imshow([[color]])  # 색상을 단일 블록으로 표시
    ax.axis('off')        # 축 숨기기

# 제목 추가
axs[0].set_title('POP (RGB: 120, 154, 160)', fontsize=12)
axs[1].set_title('댄스 (RGB: 120, 214, 198)', fontsize=12)
axs[2].set_title('랩/힙합 (RGB: 120, 138, 153)', fontsize=12)
axs[3].set_title('록/메탈 (RGB: 120, 218, 7)', fontsize=12)
axs[4].set_title('R&B/Soul (RGB: 120, 74, 157)', fontsize=12)
axs[5].set_title('Insight (RGB: 120, 100, 168)', fontsize=12)
plt.tight_layout()  # 레이아웃 조정
plt.show()

pd.DataFrame(df, columns = df.columns)
