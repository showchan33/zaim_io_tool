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
* **無料会員でダウンロードする場合**
    * 以下の項目が取得できず、代わりに全て"(プレミアム会員で表示)"という文字列が表示されてしまいます。
        * 通貨, 振替, 残高調整, 通貨変換前の金額, 集計の設定
    * 「支出」「収入」「振替」のうち、「振替」のデータはダウンロードできないようです。

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
* **無料会員でアップロードする場合**
    * 「カテゴリ」や「カテゴリの内訳」の列にZaimに登録されていないものが含まれるとアップロードに失敗します（[Zaimサイトの参考情報](https://content.zaim.net/manuals/show/51#:~:text=%E9%A3%9F%E8%B2%BB%E3%81%AA%E3%81%A9%E3%80%81%E3%81%99%E3%81%A7%E3%81%AB%E3%81%82%E3%82%8B%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA,%E5%86%85%E8%A8%B3%E3%81%8B%E3%82%89%E8%BF%BD%E5%8A%A0%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%E3%80%82&text=%E5%86%85%E8%A8%B3%E3%82%92%E7%B7%A8%E9%9B%86-,%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC%EF%BC%9E%E5%AE%B6%E8%A8%88%E7%B0%BF%E3%81%AE%E8%A8%AD%E5%AE%9A%EF%BC%9E%E6%94%AF%E5%87%BA%E3%81%AE%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA,%E5%86%85%E8%A8%B3%E8%A8%AD%E5%AE%9A%20%E3%81%8B%E3%82%89%E7%B7%A8%E9%9B%86%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82)）
        * ↑アップロードに失敗した場合でも、スクリプトは現状正常に処理が終了してしまいます。お手数ですがWebサイトやZaimのアプリで正常にアップロードできているかをご確認ください。

# Author
showchan33

# License
"zaim_io_tool" is under [GPL license](https://www.gnu.org/licenses/licenses.en.html).
