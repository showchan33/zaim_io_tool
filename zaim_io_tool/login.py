import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# ログインのために必要なpayloadを作成
def create_payload_for_login(
  response: requests.models.Response,
  env_file: str,
) -> dict:
  
  soup = BeautifulSoup(response.content, features="lxml")
  form = soup.find("form", attrs={'id': 'login-form'})

  payload = dict()
  inputs = form.find_all("input", recursive=True)
  ext_attrs = ["value", "placeholder"]
  for i in inputs:
    for attr in ext_attrs:
      if(i.get(attr) != None):
        payload[i.get("name")] = i.get(attr)

  load_dotenv(env_file)

  ZAIM_USERNAME = os.getenv('ZAIM_USERNAME')
  ZAIM_PASSWORD = os.getenv('ZAIM_PASSWORD')
  payload['email'] = ZAIM_USERNAME
  payload['password'] = ZAIM_PASSWORD

  return payload

# Zaimのサイトにログイン
def login(env_file: str = ".env") -> requests.sessions.Session:

  session = requests.Session()
  url_root = "https://id.zaim.net"
  response = session.get(url_root)
  response.raise_for_status()

  payload = create_payload_for_login(response, env_file)

  # ログイン
  response = session.post(f"{url_root}/login", data=payload)
  response.raise_for_status()

  return session

if __name__ == '__main__':
  login()
