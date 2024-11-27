import requests
import os
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
from websession.websession import WebSession

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

    cookies_playwright = websession.context.cookies()

    websession.close()

  # Playwrightのクッキーをrequests形式に変換
  for cookie in cookies_playwright:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

  response = session.get("https://zaim.net/home")
  response.raise_for_status()

  return session


if __name__ == '__main__':

  login()
