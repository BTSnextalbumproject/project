import pandas as pd

# 파일 경로 설정
file_genre = './billboardTop100Totalduplicate_with_genres.csv'  # Genre 값이 있는 첫 번째 파일 경로
file_target = './billboardTop100Total_with_BPM_Duration.csv'  # Genre 값을 추가할 두 번째 파일 경로

# 데이터셋 불러오기 (인코딩 방식 명시적으로 설정, 한국어를 처리하기 위한 인코딩 사용)
df_genre = pd.read_csv(file_genre, encoding='EUC-KR')  # 첫 번째 파일을 데이터프레임으로 불러옴 (Genre 값이 있는 파일)
df_target = pd.read_csv(file_target, encoding='EUC-KR')  # 두 번째 파일을 데이터프레임으로 불러옴 (Genre 값을 추가할 파일)

# 'Title'과 'Artist'가 일치하는 항목들에 대해 Genre 값을 추가하는 병합
df_merged = pd.merge(df_target, df_genre[['Title', 'Artist', 'Genre']], on=['Title', 'Artist'], how='left')

# 결과를 새로운 CSV 파일로 저장 (저장 시에도 같은 인코딩 방식 사용)
output_file_path = './billboardTop100Total_with_BPM_Duration_Genres.csv'
df_merged.to_csv(output_file_path, index=False, encoding='EUC-KR')  # 결과를 CSV 파일로 저장할 때도 같은 인코딩

print("Merged file saved at:", output_file_path)
