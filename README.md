# zaim_io_toolの概要

zaim_io_toolは、Zaimに登録している家計簿をCSV形式でアップロードおよびダウンロードできるツールです。<br>
ZaimのWebサイト上での以下の操作を、Pythonを使ってコマンドラインから実行できます。

* ZaimのWebサイトにログイン
* 「ファイル入出力」のページに移動
* 家計簿のデータをCSV形式でアップロードまたはダウンロード

# 必要条件

* OS
    * Linux
        * 動作確認OSはUbuntu 20.04のみ
    * ※WindowsとMacでの動作は未確認
* ツール
    * Python3
        * 3.9.7でのみ動作確認
    * pip3
        * Pythonパッケージをインストールするのに必要

# 事前準備

## パッケージのインストール

以下のコマンドで、ツールを動かすのに必要なパッケージをインストールします。

```
pip3 install -r requirements.txt
```

## Zaimにログインするための認証方法の設定

``.env.sample``を``.env``という名前でコピーします。<br>
以下の2つの環境変数を、お使いのアカウントのユーザ名とパスワードに変更します。

```shell:.env
ZAIM_USERNAME="your-email@example.com"
ZAIM_PASSQWORD="password"
```
↓ 変更例
```shell:.env
ZAIM_USERNAME="your-true-email@example.com"
ZAIM_PASSQWORD="01234567"
```

# 使い方

## 家計簿のダウンロード

```
$ python3 download.py -h
usage: download.py [-h] [-o OUTPUT] [-e ENV_FILE] [-c CHARSET] year month

ZaimのWebサイトから指定した月の家計簿をダウンロード

positional arguments:
  year                  取得年
  month                 取得月

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        出力ファイル名を指定(デフォルト output.csv)
  -e ENV_FILE, --env-file ENV_FILE
                        .envファイル名指定(デフォルト .env)
  -c CHARSET, --charset CHARSET
                        文字コード指定(utf8(default)またはsjis)
```
### 利用例
2024年1月の家計簿をダウンロードする例です。
#### 実行コマンド
```
python3 download.py 2024 1 -o ./csvoutput/202401.csv
```
#### 出力結果
```
Trying to login...
Downloading csv file...
Saved as ./csvoutput/202401.csv.
```

### 注意事項
* 現時点では月単位でしかcsvファイルをダウンロードできません。
* **無料会員の場合は正常にダウンロードできない**事象を確認しています。

## 家計簿のアップロード

```
$ python3 upload.py -h
usage: upload.py [-h] [-e ENV_FILE] input

ZaimのWebサイト経由で家計簿のcsvファイルをアップロード

positional arguments:
  input                 入力ファイル名を指定

optional arguments:
  -h, --help            show this help message and exit
  -e ENV_FILE, --env-file ENV_FILE
                        .envファイル名指定(デフォルト .env)
```
### 利用例

#### 実行コマンド
```
python3 upload.py csvinput/input-20240118.csv
```
#### 出力結果
```
Trying to login...
Uploading csv file...
Upload of csv file completed.
```

### 注意事項
* アップロード用のcsvファイルが必要です。csvファイルのデータはZaimのフォーマットになっている必要があります。データーフォマットが具体的にどのようなものかは、[csvinput/sample.csv](csvinput/sample.csv)やZaimのWebサイトからダウンロードしたcsvファイルの内容をご確認ください。
* アップロード用のcsvファイルの文字コードはUTF-8の必要があります。Shift_JISコード等での動作は未確認です。
* [csvinput/sample.csv](csvinput/sample.csv)を指定することでアップロードの動作確認が可能ですが、架空の口座情報（楽天カード XXXX-XXXX-XXXX-XXXX等）が追加されてしまう点にご注意ください。尚、追加された口座情報の削除はできませんが、非表示にすることは可能です。
* **無料会員の場合、アップロードしたデータが反映されない**事象を確認しています。

# Author
showchan33

# License
"zaim_io_tool" is under [GPL license](https://www.gnu.org/licenses/licenses.en.html).
