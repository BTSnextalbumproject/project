import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver 경로 설정
driver_path = 'C:/chromedriver-win64/chromedriver.exe'

# Selenium을 사용하여 멜론에서 첫 번째 곡의 장르를 크롤링하는 함수
def get_genre_from_melon_with_selenium(artist, title):
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-images")  # 이미지 로드를 비활성화하여 속도 향상

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        search_url = f'https://www.melon.com/search/song/index.htm?q={artist}-{title}&section=&searchGnbYn=Y&kkoSpl=N&kkoDpType='
        driver.get(search_url)

        # 첫 번째 곡 정보 링크 클릭
        try:
            first_song_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#frm_defaultList > div > table > tbody > tr > td:nth-child(3) > div > div > a.btn.btn_icon_detail'))
            )
            first_song_element.click()
        except Exception:
            print(f"검색 결과를 찾을 수 없습니다 (아티스트: {artist}, 제목: {title})")
            return None

        # 장르 정보 추출
        try:
            genre_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)'))
            )
            genre = genre_element.text.strip()
        except Exception:
            print(f"장르 정보를 찾을 수 없습니다 (아티스트: {artist}, 제목: {title})")
            return None

        return genre

    except Exception:
        print(f"Error (아티스트: {artist}, 제목: {title})")
        return None

    finally:
        if driver is not None:
            driver.quit()

# 병렬 처리를 위한 함수
def fetch_genre(row):
    artist = row['Artist']
    title = row['Cleaned_Title']  # 괄호 이후 내용이 제거된 제목 사용
    time.sleep(2)  # 요청 사이의 지연 추가 (IP 차단 방지용)
    genre = get_genre_from_melon_with_selenium(artist, title)
    return genre

# 엑셀 파일 읽기
file_path = './data/null_Top100_genres.csv'
df = pd.read_csv(file_path, encoding='cp949')

# 타이틀에서 괄호 이후 내용을 임시로 제거한 새로운 열 생성
df['Cleaned_Title'] = df['Title'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', x).strip())

# 병렬 처리를 통한 크롤링 실행 함수
def resume_crawling(df, batch_size=50, output_file_path='./data/re_re_billboardTop100_with_genres.csv'):
    try:
        processed_df = pd.read_csv(output_file_path, encoding='cp949')
        last_processed_index = len(processed_df)
        print(f"{last_processed_index}개의 데이터를 이미 처리했습니다. 이어서 작업을 시작합니다.")
    except FileNotFoundError:
        last_processed_index = 0
        print("CSV 파일이 존재하지 않습니다. 처음부터 시작합니다.")

    total_rows = len(df)
    for start_row in range(last_processed_index, total_rows, batch_size):
        end_row = min(start_row + batch_size, total_rows)
        batch_df = df.iloc[start_row:end_row].copy()

        print(f"Processing rows {start_row} to {end_row}...")

        # 멀티스레딩을 사용하여 병렬로 크롤링
        with ThreadPoolExecutor(max_workers=3) as executor:  # 스레드 수를 줄여 서버 부하 감소
            batch_df['Genre'] = list(executor.map(fetch_genre, [row for _, row in batch_df.iterrows()]))

        # 50개씩 저장
        if start_row == 0 and last_processed_index == 0:
            batch_df.to_csv(output_file_path, index=False, encoding='cp949', mode='w')  # 처음 저장 (덮어쓰기)
        else:
            batch_df.to_csv(output_file_path, index=False, encoding='cp949', mode='a', header=False)  # 이후 추가 저장 (이어쓰기)

        print(f"Batch {start_row} to {end_row} saved to {output_file_path}")

        # 마지막 5개의 크롤링 결과를 출력
        print("마지막 5개의 크롤링 결과:")
        print(batch_df[['Artist', 'Title', 'Genre']].tail(5))

# 크롤링 후 원래 타이틀로 복구
df['Title'] = df['Title']  # 원래 Title로 복구 (이미 복사한 상태)

# 결과 확인을 위해 50개씩 처리하여 장르 추가 후 저장
output_file_path = './data/re_re_billboardTop100_with_genres.csv'
resume_crawling(df, batch_size=50, output_file_path=output_file_path)

print(f"모든 데이터가 {output_file_path}에 저장되었습니다.")
