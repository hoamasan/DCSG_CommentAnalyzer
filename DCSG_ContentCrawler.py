from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_content(post_url):
    # ✅ 1. 크롬 옵션 설정
    options = Options()
    options.headless = False  # True로 하면 브라우저가 안 뜨지만, False로 설정해서 테스트하는 게 좋음
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ 2. 크롬 드라이버 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print(driver.page_source)
    try:
        # ✅ 3. 게시글 페이지 접속
        driver.get(post_url)
        time.sleep(5)  # 페이지가 완전히 로드될 시간을 줌 (최소 5초 이상)

        # ✅ 4. JavaScript 실행 후 HTML 가져오기
        page_source = driver.execute_script("return document.body.innerHTML;")
        soup = BeautifulSoup(page_source, "html.parser")

        # ✅ 5. 게시글 내용 크롤링
        content_element = soup.select_one("#container > section > article:nth-child(3) > div.view_content_wrap > div > div.inner.clear > div > div.write_div > div")

        if content_element:
            content = content_element.get_text(strip=True)
        else:
            print("❌ 게시글 본문을 찾을 수 없음")
            content = None

    except Exception as e:
        print(f"❌ 게시글 내용 크롤링 중 오류 발생: {e}")
        content = None

    # ✅ 6. 브라우저 종료
    driver.quit()

    return content
