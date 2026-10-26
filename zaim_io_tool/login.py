import requests
import os
import re
from urllib.parse import urlparse
from dotenv import load_dotenv

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright
from websession.websession import WebSession


TWO_FACTOR_CODE_SELECTOR = (
    'input:not([type="hidden"])[autocomplete="one-time-code"], '
    'input:not([type="hidden"])[name*="otp" i], '
    'input:not([type="hidden"])[name*="code" i], '
    'input:not([type="hidden"])[placeholder*="認証コード"], '
    'input:not([type="hidden"])[placeholder*="ワンタイム"]'
)


def prompt_two_factor_code() -> str:
  """Prompt for a TOTP code without saving it anywhere."""
  code = os.getenv("ZAIM_TOTP_CODE")
  if code is not None:
    if re.fullmatch(r"[0-9]{6}", code):
      return code
    raise ValueError("ZAIM_TOTP_CODEは6桁の数字で指定してください。")

  while True:
    code = input("Zaimの認証アプリに表示された6桁のコードを入力してください: ").strip()
    if re.fullmatch(r"[0-9]{6}", code):
      return code
    print("認証コードは6桁の数字で入力してください。")


def submit_two_factor_code_if_requested(page) -> None:
  """Complete the TOTP challenge only when Zaim displays one."""
  code_input = page.locator(TWO_FACTOR_CODE_SELECTOR).first
  try:
    code_input.wait_for(state="visible", timeout=5000)
  except PlaywrightTimeoutError:
    return

  code_input.fill(prompt_two_factor_code())
  code_input.press("Enter")
  page.wait_for_load_state("domcontentloaded")

def login(
    env_file: str = ".env",
) -> WebSession:

  session = requests.Session()
  response = session.get(
    "https://zaim.net/user_session/new", allow_redirects=True)
  response.raise_for_status()

  load_dotenv(env_file)
  zaim_username = os.getenv('ZAIM_USERNAME')
  zaim_password = os.getenv('ZAIM_PASSWORD')

  cookies_playwright = []

  with sync_playwright() as playwright:
    websession = WebSession(playwright, record_video=False)

    websession.page.goto(response.url)
    websession.page.get_by_placeholder("メールアドレス").click()
    websession.page.get_by_placeholder("メールアドレス").fill(zaim_username)
    websession.page.get_by_placeholder("パスワード").click()
    websession.page.get_by_placeholder("パスワード").fill(zaim_password)
    websession.page.get_by_role("button", name="利用規約に同意して ログイン").click()
    submit_two_factor_code_if_requested(websession.page)

    cookies_playwright = websession.context.cookies()

    websession.close()

  # Playwrightのクッキーをrequests形式に変換
  for cookie in cookies_playwright:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

  response = session.get("https://zaim.net/home")
  response.raise_for_status()
  if urlparse(response.url).hostname == "id.kufu.jp":
    raise RuntimeError("Zaimへのログインが完了していません。認証コードを確認してください。")

  return session


if __name__ == '__main__':

  login()
