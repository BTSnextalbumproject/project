import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API 인증 정보
cid = 'b3bfdfab2faa44109237539ddadd391b'
secret = 'f7812dfde0694f1da4a29155d11d11db'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Duration 정보를 가져오는 함수
def get_duration(song, artist):
    retry_count = 0
    while True:
        try:
            track_info = sp.search(q=f'{song} {artist}', type='track', limit=1)
            if track_info["tracks"]["items"]:
                track_id = track_info["tracks"]["items"][0]["id"]
                features = sp.audio_features(tracks=[track_id])
                if features and features[0]:
                    # duration_ms를 초 단위로 변환해서 반환
                    return features[0]["duration_ms"] / 1000
            break
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", 1))
                print(f"요청이 제한되었습니다. {retry_after}초 후에 다시 시도합니다...")
                time.sleep(retry_after)
                retry_count += 1
                if retry_count >= 5:
                    print("최대 재시도 횟수에 도달했습니다. 10분 동안 휴식합니다...")
                    time.sleep(600)  # 10분 (600초) 휴식
                    retry_count = 0
            else:
                print(f"{song} - {artist}의 Duration을 가져오는 중 오류 발생: {e}")
                break
    return None

# 노래를 100개씩 배치로 처리하는 함수
def process_songs_in_batches(input_file, output_file, batch_size=100, start_idx=0):
    try:
        # 이미 진행된 데이터가 있다면 이어서 작업
        df_songs = pd.read_csv(output_file, encoding='utf-8-sig')
        print(f"처음부터 처리합니다...")
    except FileNotFoundError:
        # 새로운 데이터 시작
        df_songs = pd.read_csv(input_file, encoding='ISO-8859-1')
        df_songs['Duration_sec'] = None
        print(f"{start_idx + 1}번째 인덱스부터 시작합니다...")

    processed_count = 0  # 처리한 항목 수를 추적

    # 시작 인덱스를 포함하여 100개씩 배치로 처리
    for i in range(start_idx, len(df_songs), batch_size):
        batch_songs = df_songs.iloc[i:i+batch_size]
        for idx, row in batch_songs.iterrows():
            if pd.notna(row['Duration_sec']):
                # Duration 값이 이미 있는 경우 API 요청을 건너뜀
                print(f"{row['Title']} - {row['Artist']}은(는) 이미 처리됨, Duration: {row['Duration_sec']} 초")
                continue

            song = row['Title'].strip()
            artist = row['Artist'].strip()
            duration = get_duration(song, artist)
            
            # Duration을 가져온 후에 None이 아닌 경우에만 저장
            if duration is not None:
                df_songs.at[idx, 'Duration_sec'] = duration
                print(f"{song} - {artist} 처리 완료, Duration: {duration} 초")
            else:
                print(f"{song} - {artist}의 Duration 정보를 찾을 수 없습니다.")
            
            time.sleep(0.5)  # 요청 제한 방지
            processed_count += 1  # 처리한 항목 수 증가

            # 500개마다 5분 휴식
            if processed_count % 500 == 0:
                print(f"{processed_count}개의 항목을 처리했습니다. 5분 동안 휴식합니다...")
                time.sleep(300)  # 5분 (300초) 휴식

        # 배치 처리 후 중간 저장
        df_songs.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"{i // batch_size + 1}번째 배치 처리 완료 및 저장됨.")

    print("처리 완료. 모든 배치가 저장되었습니다.")

# 함수 호출
process_songs_in_batches('./billboardTop100Totalduplicate.csv', './billboardTop100Totalduplicate_with_Duration.csv')