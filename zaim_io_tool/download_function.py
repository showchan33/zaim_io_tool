import requests
from bs4 import BeautifulSoup
import calendar
from collections import namedtuple

DownloadParam = \
  namedtuple(
    'DownloadParam',
    [
      'start_year',
      'start_month',
      'start_day',
      'end_year',
      'end_month',
      'end_day',
      'charset',
    ]
  )

# ダウンロードに必要なパラメータを作成
def create_download_param(
  year: str,
  month: str,
  charset: str,
) -> DownloadParam:
  
  month_zfilled = month.zfill(2)
  endday = str(calendar.monthrange(int(year), int(month))[1])

  return DownloadParam(
    start_year = year,
    start_month = month_zfilled,
    start_day = "01",
    end_year = year,
    end_month = month_zfilled,
    end_day = endday,
    charset = charset,
  )

# csvファイルのダウンロードをリクエストするために必要なpayloadを作成
def create_payload_for_download(
  response: requests.models.Response,
  download_param: DownloadParam,
) -> dict:

  soup = BeautifulSoup(response.content, features="lxml")

  form = soup.find("form", attrs={'action': "/home/money/download"})
  payload = {}

  inputs = form.find_all("input", recursive=True)
  ext_attrs = ["value"]
  for i in inputs:
    for attr in ext_attrs:
      if(i.get(attr) != None and i.get("name") != None):
        payload[i.get("name")] = i.get(attr)

  payload["start_year"] = download_param.start_year
  payload["start_month"] = download_param.start_month
  payload["start_day"] = download_param.start_day
  payload["end_year"] = download_param.end_year
  payload["end_month"] = download_param.end_month
  payload["end_day"] = download_param.end_day
  payload["charset"] = download_param.charset

  return payload

# csvファイルをダウンロードしてファイル保存
def download_csv(
  session: requests.sessions.Session,
  download_param: DownloadParam,
  filename: str = "output.csv"
):

  url_root = "https://content.zaim.net"

  # ファイル入出力のサイトに移動
  response = session.get(f"{url_root}/home/money")
  response.raise_for_status()

  payload = create_payload_for_download(response, download_param)

  response = session.post(f"{url_root}/home/money/download", data=payload)
  response.raise_for_status()

  with open(filename, 'w', encoding=download_param.charset) as f:
    f.write(str(response.content, encoding=download_param.charset))
