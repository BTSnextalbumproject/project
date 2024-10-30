import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
file_path = './billboardTop100Total_with_BPM_Duration.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# 연도별 평균 BPM 계산
average_bpm_per_year = data.groupby("Year")["BPM"].mean()

# 2019년 이전과 이후 데이터 분리
pre_2019 = average_bpm_per_year[average_bpm_per_year.index <= 2019]
post_2019 = average_bpm_per_year[average_bpm_per_year.index >= 2019]

# 그래프 생성
plt.figure(figsize=(12, 6))
plt.plot(pre_2019.index, pre_2019, color="gray", marker="o", linestyle="-", label="Pre-2019", alpha=0.5)
plt.plot(post_2019.index, post_2019, color="blue", marker="o", linestyle="-", label="2019 Onwards")

# 제목 및 라벨 설정
plt.title("Average BPM Change (Emphasizing from 2019 Onwards)")
plt.xlabel("Year")
plt.ylabel("Average BPM")
plt.xticks(average_bpm_per_year.index)
plt.legend()
plt.grid(True)

# 그래프 표시
plt.show()
