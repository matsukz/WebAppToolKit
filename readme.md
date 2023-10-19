# Webサーバースタートアップキッド
FlaskとMySQLを用いたWebサーバーをコマンド1つで構成するスタートアップキッドです。

## 作った理由
* 自由にポート開放ができない環境でもサービスを運営できる
* Cloudflare tunelを利用することでセキュリティリスクを減らすことができる
  * グローバルIPアドレス隠匿
  * ポート開放不要

## デメリット
* 複数のコンテナを実行するためリソースを消費する

## 構成
* 全体図
![image1](https://github.com/matsukz/WebAppToolKit/blob/main/image/map.png)
  * phpmyadminを利用しているため、ローカルネットワーク内で構築することを推奨します
### フロントエンド
* HTML (Jinja2)
* BootStrap v5.0.2
  * [BootStrap - はじめに](https://getbootstrap.jp/docs/5.0/getting-started/introduction/)
### バックエンド
* Flask
    項目|初期値
    |:---:|:---:|
    |ディレクトリ|./app|
    |ホスト側ポート|5050|
    |コンテナ内ポート|5000|
* MySQL5.7
    項目|初期値
    |:---:|:---:|
    |ディレクトリ|./mysql|
    |ホスト側ポート|3306|
    |コンテナ内ポート|3306|
    |ユーザー名|root|
    |パスワード|password|
* phpmyadmin
    項目|初期値
    |:---:|:---:|
    |ホスト側ポート|8081|
    |コンテナ内ポート|80|
  * [phpmyadmin/phpmyadmin - docker hub ](https://hub.docker.com/_/phpmyadmin)
* Cloudflared
  * [Cloudflare Tunnel - CLOUDFLARE](https://www.cloudflare.com/ja-jp/products/tunnel/)
  * [cloudflare/cloudflared - docker hub](https://hub.docker.com/r/cloudflare/cloudflared)

## 環境
### docker
```bash
$ docker -v
Docker version 24.0.6
```
* [Docker Engine インストール（Ubuntu 向け）- docker docs](https://matsuand.github.io/docs.docker.jp.onthefly/engine/install/ubuntu/#install-using-the-convenience-script)
  * OSはUbuntuでなくても構いません。あくまで一例です
### docker-compose
```bash
$ docker-compose -v
docker-compose version 1.29.2, build 5becea4c
```
* [Docker Compose のインストール - Docker-docs-ja](https://docs.docker.jp/v1.12/compose/install.html)
  * 公式サイトのコマンドでは古いバージョンのdocker-composeがダウンロードされトラブルの原因となるので以下のコマンドで代用してください(2023-10-19追記)
  ```bash
  $ sudo curl -L https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
  ```
  
  * Docker Desktopでは初期状態でdocker-composeが使えると思います 
### Visual Studio Code (以下VScode)
コンテナやプログラムの操作に使います。適宜インストールしてください。以下は一例です
* Remote Development
* Dev Containers
* docker
* python
### Cloudflare
* Cloudflareに登録した独自ドメイン
    * 最低限ネームサーバーをCloudflareに向けておく

## セットアップ
事前に上記3セットをセットアップしていることが前提となります

1. 各種ファイルをダウンロードし展開する
   * フォルダーパスに日本語や空白が含まれていると不具合の原因となります

2. Cloudflare Tunnelの作成
   * トンネルを作成しTOKENとURLをドメインを設定します
    1. ダッシュボードにログイン
         * [Cloudflare - Login](https://dash.cloudflare.com/login)
         * ブラウザの自動翻訳を適用するとエラーが発生します
    2. サイドバーから`Zero Trust`を選択
    3. サイドバーから`Access` から `Tunnels`を選択
    4. `Create a tunnel`を選択
    5. 任意のトンネル名を入力し次へ
    6. `Run the following command:`に表示されているコマンドをクリックしてコピーし`Next`で次へ
       * メモ帳などにペーストし`cloudflared.exe service install `を消しておく
    7. Public hostnameの設定
       1. 任意のサブドメインとルートドメイン、パスを入力
       2. `Select...`から`HTTP`を選択しURLに以下のアドレスを入力する
          ```
          flask:5000
          ```
    8. `Save tunnel`を押して保存
  
3. 設定ファイルの書き換え
   1. VScodeなどのテキストエディタで同梱の`docker-compose.yml`を開く
   2. `cloudflared:`にTOKENを設定する
      ```yml
      cloudflared: 
        # 省略
        environment:
          - TUNNEL_TOKEN=ここ
        # 省略
      ```
      * `ここ`に2-6で取得したコードを貼り付けます
   3. 保存

## 使い方
### 起動
* ターミナルを起動し以下のコマンドを実行する
  ```bash
  $ docker-compose up -d
  ```
    * 以下のように出力されれば完了です(たぶん)
      ```bash
      Creating webapptoolkit_mysql_1 ... done
      Creating flask                      ... done
      Creating webapptoolkit_phpmyadmin_1 ... done
      Creating webapptoolkit_cloudflared_1 ... done
      ``` 
  * もしエラーが発生した場合は以下の手順で起動する
  1.  VScodeを起動し`docker-compose.yml`を右クリックで選択
  2.  右クリックメニューから`Compose Up`を選択する
### 全体のログをリアルタイムで確認する
* ターミナルを起動し以下のコマンドを実行する
```bash
$ docker-compose logs -f
```
### 停止
```bash
$ docker-compose stop
```
* もしくは
  1. VScodeのdockerメニューからサービスを右クリック
  2. メニューから`Compose stop`を選択
### 削除
```bash
$ docker-compose down
``` 
* もしくは
  1. VScodeのdockerメニューからサービスを右クリック
  2. メニューから`Compose down`を選択

## Webサイト制作
* `app`ディレクトリにある[app.py](app\app.py)や[templates](./templates)ディレクトリ内のHTMLにコードを記述する
  * 保存すれば即反映されます(CDNやブラウザのキャッシュ注意)
  * FlaskやJinja2の使い方はググってください


# 参考・引用
いつもありがとうございます
## 参考にしたサイト様
* [Markdown記法 チートシート - qiita](https://qiita.com/Qiita/items/c686397e4a0f4f11683d)
* [【速攻】DockerでMySQLとphpMyAdminのコンテナ作成 - Zenn](https://zenn.dev/peishim/articles/f7a76ae6c253e4)
* [MisskeyをDocker Compose+Cloudflare Tunnelでサクッと建てる - Zenn](https://zenn.dev/hrko/scraps/29df6c7ac02f03)
## 画像引用
* [Cloudflareロゴ - CLOUDFLARE](https://www.cloudflare.com/ja-jp/logo/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [MySQL Logo Downloads](https://www.mysql.com/jp/about/legal/logos.html)
* [File:PhpMyAdmin logo.svg - wikipedia](https://en.m.wikipedia.org/wiki/File:PhpMyAdmin_logo.svg)
