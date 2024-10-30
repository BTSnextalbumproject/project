import pandas as pd

# 파일 경로 설정
file_duration = './billboardTop100Totalduplicate_with_Duration.csv'  # Duration 값이 있는 파일 경로
file_target = './billboardTop100Total_with_BPM.csv'  # Duration 값을 추가해야 하는 파일 경로

# 데이터셋 불러오기 (인코딩 방식 명시적으로 설정)
df_duration = pd.read_csv(file_duration, encoding='ISO-8859-1')  # 첫 번째 파일을 데이터프레임으로 불러옴 (Duration 값이 있는 파일)
df_target = pd.read_csv(file_target, encoding='ISO-8859-1')  # 두 번째 파일을 데이터프레임으로 불러옴 (Duration 값을 추가할 파일)

# 'Title'과 'Artist'가 일치하는 항목들에 대해 Duration 값을 추가하는 병합
# 'Title'과 'Artist' 컬럼을 기준으로 두 데이터프레임을 병합하고, left join 방식으로 'Duration_sec' 값을 추가
df_merged = pd.merge(df_target, df_duration[['Title', 'Artist', 'Duration_sec']], on=['Title', 'Artist'], how='left')

# 결과를 새로운 CSV 파일로 저장
output_file_path = './billboardTop100Total_with_BPM_Duration.csv'  # 출력 파일 경로 설정
df_merged.to_csv(output_file_path, index=False)

print("Merged file saved at:", output_file_path)  # 출력 파일 경로 출력
