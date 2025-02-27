# DCSG_ComeentCrawler.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

def get_comments(post_url):
    # Selenium 설정
    options = Options()
    options.headless = True  # 브라우저를 실제로 띄우지 않음
    options.add_argument("--disable-gpu")  # GPU 비활성화
    options.add_argument("--no-sandbox")  # 샌드박스 비활성화
    options.add_argument("--disable-dev-shm-usage")  # 디버그 메시지 비활성화

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 게시글 페이지 열기
    driver.get(post_url)
    time.sleep(2)  # 페이지 로딩 대기

    # 댓글 로딩 (스크롤 다운을 통해 댓글을 로딩)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 댓글 로딩 대기

    # 댓글 크롤링
    comments = []
    comment_elements = driver.find_elements(By.CSS_SELECTOR, ".gall_comment li")  # 댓글 리스트
    for comment in comment_elements:
        author = comment.find_element(By.CSS_SELECTOR, ".gall_writer").text.strip()  # 댓글 작성자
        content = comment.find_element(By.CSS_SELECTOR, ".gall_text").text.strip()  # 댓글 내용
        comments.append({"author": author, "content": content})

    # 브라우저 종료
    driver.quit()

    return comments