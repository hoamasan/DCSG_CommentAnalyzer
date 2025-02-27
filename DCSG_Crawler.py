import requests
from bs4 import BeautifulSoup

# 검색할 주식명 (예: '엔비')
stock_name = "엔비"

# 게시글 목록 페이지 URL
base_url = "https://gall.dcinside.com/mgallery/board/lists/"
params = {
    "id": "tenbagger",
    "s_type": "search_subject_memo",  # 제목 + 본문 검색
    "s_keyword": stock_name,  # 검색 키워드
}

# 페이지 요청
response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

# 게시글 목록 가져오기
posts = []
for row in soup.select(".ub-content"):  # 게시글 리스트
    title_tag = row.select_one(".gall_tit a")  # 제목 링크
    date_tag = row.select_one(".gall_date")  # 작성 날짜

    if title_tag and date_tag:
        title = title_tag.text.strip()  # 게시글 제목
        post_url = "https://gall.dcinside.com" + title_tag["href"]  # 게시글 URL
        date = date_tag.text.strip()  # 작성 시간

        posts.append({"title": title, "url": post_url, "date": date})

# 결과 출력
for post in posts:
    print(post)
