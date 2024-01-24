from zaim_io_tool.login import login
from zaim_io_tool.upload_function import upload_csv

if __name__ == '__main__':

  import argparse
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser(description='ZaimのWebサイト経由で家計簿のcsvファイルをアップロード')
  parser.add_argument('input', help='入力ファイル名を指定')
  parser.add_argument('-e', '--env-file', help='.envファイル名指定(デフォルト .env)', default='.env')

  args = parser.parse_args()

  # ログイン
  print("Trying to login...")
  session = login(args.env_file)

  # csvファイルをアップロード
  print("Uploading csv file...")
  upload_csv(session, args.input)

  print("Upload of csv file completed.")
