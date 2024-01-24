import requests
from bs4 import BeautifulSoup

# csvファイルのアップロードをリクエストするために必要なpayloadを作成
def create_payload_for_upload(
  response: requests.models.Response,
  upload_path: str,
) -> dict:

  soup = BeautifulSoup(response.content, features="lxml")
  form = soup.find("form", attrs={'action': upload_path})

  payload = dict()

  inputs = form.find_all("input", recursive=True)
  ext_attrs = ["value"]
  for i in inputs:
    for attr in ext_attrs:
      if(i.get(attr) != None and i.get("name") != None):
        payload[i.get("name")] = i.get(attr)

  return payload

# csvファイルをアップロード
def upload_csv(
  session: requests.sessions.Session,
  filename: str,
):

  url_root = "https://content.zaim.net"
  upload_path = "/home/money/zaim_upload"

  # ファイル入出力のサイトに移動
  response = session.get(f"{url_root}/home/money")
  response.raise_for_status()

  payload = create_payload_for_upload(response, upload_path)

  files = {'zaim_upload_file': open(filename, 'r')}

  response = session.post(f"{url_root}{upload_path}", data=payload, files=files)
  response.raise_for_status()
