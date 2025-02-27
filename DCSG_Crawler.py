import requests
from bs4 import BeautifulSoup
from DCSG_CommentCrawler import get_comments

# 검색할 주식명 (예: '엔비')
stock_name = "엔비"

# 게시글 목록 페이지 URL
base_url = "https://gall.dcinside.com/mgallery/board/lists/"
params = {
    "id": "stockus",
    "s_type": "search_subject_memo",  # 제목 + 본문 검색
    "s_keyword": stock_name,  # 검색 키워드
}

# 페이지 요청
response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

# 게시글 목록 가져오기
posts = []
# 지정된 tr 태그 내의 게시글만 가져오기
for row in soup.select("div.gall_listwrap.list table.gall_list tbody.listwrap2 tr.ub-content.us-post"):
    title_tag = row.select_one(".gall_tit a")  # 제목 링크
    date_tag = row.select_one(".gall_date")  # 작성 날짜
    author_tag = row.select_one(".gall_writer")  # 작성자
    
    # 말머리가 '설문' 또는 'AD'인 게시글 제외
    if title_tag and date_tag and author_tag:
        title = title_tag.text.strip()  # 게시글 제목
        post_url = "https://gall.dcinside.com" + title_tag["href"]  # 게시글 URL
        date = date_tag.text.strip()  # 작성 시간
        author = author_tag.text.strip()  # 글쓴이
        
        # 게시글 제목 앞에 '설문'이나 'AD'가 포함되어 있으면 제외
        if "설문" in title or "AD" in title:
            continue

        posts.append({"title": title, "url": post_url, "date": date, "author": author})

# 결과 출력
for post in posts:
    print(f"제목: {post['title']}")
    print(f"URL: {post['url']}")
    print(f"작성일: {post['date']}")
    print(f"글쓴이: {post['author']}")
    
    """
    # 댓글 가져오기
    comments = get_comments(post_url)

    # 댓글 출력
    for comment in comments:
        print(f"작성자: {comment['author']}")
        print(f"내용: {comment['content']}")
        print("*" * 40)
    print("-" * 40)
    """

"""
# 댓글 크롤링

from DCSG_CommentCrawler import get_comments

# 예시 게시글 URL
#post_url = "https://gall.dcinside.com/mgallery/board/view/?id=tenbagger&no=6560122"

# 댓글 가져오기
comments = get_comments(post_url)

# 댓글 출력
for comment in comments:
    print(f"작성자: {comment['author']}")
    print(f"내용: {comment['content']}")
    print("-" * 40)
"""