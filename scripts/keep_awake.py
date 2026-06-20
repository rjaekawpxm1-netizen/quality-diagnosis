"""
keep_awake.py
Streamlit Community Cloud 앱이 비활성으로 잠드는 것을 방지한다.

동작:
  1. 헤드리스 크롬으로 배포 앱 URL을 실제로 연다.
  2. 페이지가 완전히 로드될 때까지 대기한다.
  3. "잠자는 앱"이면 나타나는 깨우기 버튼
     ("Yes, get this app back up!" 등)을 찾아 클릭한다.
  4. 깨어날 시간을 준 뒤 종료한다.

GitHub Actions에서 cron으로 주기 실행된다.
"""

import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


APP_URL = "https://quality-diagnosis-ukjavywxy5hsxhuwvm5exn.streamlit.app/"

# 깨우기 버튼 텍스트 (Streamlit이 표시하는 문구 변형 대응)
WAKE_BUTTON_TEXTS = [
    "get this app back up",
    "Yes, get this app back up!",
    "app back up",
]


def build_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,1024")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=opts)


def click_wake_button(driver) -> bool:
    """깨우기 버튼이 있으면 클릭. 클릭했으면 True."""
    # 1) 버튼 텍스트로 탐색
    for text in WAKE_BUTTON_TEXTS:
        try:
            xpath = (
                f"//button[contains(translate(., "
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{text.lower()}')]"
            )
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            print(f"[OK] 깨우기 버튼 클릭: '{text}'")
            return True
        except TimeoutException:
            continue

    # 2) 일반 텍스트 노드로도 한 번 더 탐색 (버튼이 div/span일 때)
    for text in WAKE_BUTTON_TEXTS:
        try:
            xpath = (
                f"//*[contains(translate(., "
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{text.lower()}')]"
            )
            el = driver.find_element(By.XPATH, xpath)
            el.click()
            print(f"[OK] 깨우기 요소 클릭: '{text}'")
            return True
        except Exception:
            continue

    return False


def main():
    print(f"[INFO] 대상 URL: {APP_URL}")
    driver = None
    try:
        driver = build_driver()
        driver.set_page_load_timeout(60)
        driver.get(APP_URL)
        print("[INFO] 페이지 로드 요청 완료")

        # 초기 렌더 대기
        time.sleep(8)

        clicked = click_wake_button(driver)
        if clicked:
            # 앱이 다시 빌드/기동될 시간을 충분히 준다
            print("[INFO] 앱 기동 대기 중 (40초)...")
            time.sleep(40)
            print("[OK] 잠든 앱을 깨웠습니다.")
        else:
            print("[OK] 앱이 이미 깨어 있습니다 (깨우기 버튼 없음).")

        # 실제 트래픽 발생을 위해 잠시 더 머무름
        time.sleep(5)
        title = driver.title
        print(f"[INFO] 페이지 타이틀: {title}")
        print("[DONE] keep-awake 완료")

    except WebDriverException as e:
        print(f"[ERROR] WebDriver 오류: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 예기치 못한 오류: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()