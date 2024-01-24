from zaim_io_tool.login import login
from zaim_io_tool.download_function import create_download_param
from zaim_io_tool.download_function import download_csv

if __name__ == '__main__':

  import argparse
  parser = argparse.ArgumentParser(description='ZaimのWebサイトから指定した月の家計簿をダウンロード')
  parser.add_argument('year', help='取得年')
  parser.add_argument('month', help='取得月')
  parser.add_argument('-o', '--output', help='出力ファイル名を指定(デフォルト output.csv)', default="output.csv")
  parser.add_argument('-e', '--env-file', help='.envファイル名指定(デフォルト .env)', default=".env")
  parser.add_argument('-c', '--charset', help='文字コード指定(utf8(default)またはsjis)', default="utf8")

  args = parser.parse_args()

  # ログイン
  print("Trying to login...")
  session = login(args.env_file)

  # ダウンロードに必要なパラメータを作成
  download_param = create_download_param(args.year, args.month, args.charset)

  # ファイルをダウンロード
  print("Downloading csv file...")
  download_csv(session, download_param, args.output)

  print(f"Saved as {args.output}.")
