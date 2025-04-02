import requests
from bs4 import BeautifulSoup
import csv
import re
import time


def get_activities(url):
    """위비티 대외활동 페이지에서 정보를 추출하는 함수"""
    print(f"{url} 페이지에서 대외활동 정보를 추출합니다...")
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        activities = []
        items = soup.select('.tit a')

        for item in items:
            title = item.text.strip()
            wevity_url = 'https://www.wevity.com' + item['href']

            # 상세 페이지에서 이미지 URL 가져오기
            image_url = get_image_url(wevity_url)

            # 상세 페이지에서 상세 내용 요약 가져오기
            description = get_description(wevity_url)

            activities.append({
                '제목': title,
                '위비티 URL': wevity_url,
                '이미지 URL': image_url,
                '상세 내용': description
            })
            time.sleep(1)
        print(f"{url} 페이지에서 대외활동 정보 추출 완료.")
        return activities
    except requests.exceptions.RequestException as e:
        print(f"{url} 페이지 오류: {e}")
        return []


def get_image_url(url):
    """대외활동 상세 페이지에서 이미지 URL을 추출하는 함수"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 여러 위치에서 이미지 찾기
        img_element = soup.select_one('.thumb img') or soup.select_one('.content-txt img')
        if img_element and 'src' in img_element.attrs:
            image_url = img_element['src'].strip()
            if image_url.startswith('/'):
                image_url = 'https://www.wevity.com' + image_url
            return image_url
        return "이미지 없음"
    except requests.exceptions.RequestException:
        return "이미지 없음"


def get_description(url):
    """대외활동 상세 페이지에서 상세 내용을 요약하여 추출하는 함수"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 상세 내용이 존재할 가능성이 있는 모든 태그 선택
        content_sections = [
            soup.select_one('.content-txt'),
            soup.select_one('.view-cont'),
            soup.select_one('.cont-box'),
            soup.select_one('.view-box'),
            soup.select_one('.info'),
            soup.select_one('.desc'),
            soup.select_one('.detail'),
            soup.select_one('.text-box'),
            soup.select_one('.article'),
            soup.select_one('.entry-content'),
            soup.select_one('.contest-detail'),
            soup.select_one('.description'),
            soup.select_one('.contest-info'),
            soup.select_one('.paragraph'),
            soup.select_one('.context')
        ]


        description_texts = []
        for section in content_sections:
            if section:
                description_texts.append(re.sub(r'\s+', ' ', section.get_text(separator='\n', strip=True)))

        if description_texts:
            description = ' '.join(description_texts)
            return description[:250] + ('...' if len(description) > 300 else '')

        return "상세 내용 없음"
    except requests.exceptions.RequestException:
        return "상세 내용 없음"


def save_to_csv(data, filename='wevity_activitiesFINAL.csv'):
    """추출한 데이터를 CSV 파일로 저장하는 함수"""
    if not data:
        print("저장할 데이터가 없습니다.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"{filename} 파일에 저장되었습니다.")
    except Exception as e:
        print(f"CSV 파일 저장 오류: {e}")


if __name__ == "__main__":
    base_url = 'https://www.wevity.com/?c=find&s=1&gub=1'
    all_activities = []
    page = 1
    max_pages = 90

    while page <= max_pages:
        url = f'{base_url}&spage={page}'
        activities = get_activities(url)
        if not activities:
            break
        all_activities.extend(activities)
        page += 1

    save_to_csv(all_activities)
    print("전체 페이지 크롤링 및 CSV 파일 저장 완료.")
