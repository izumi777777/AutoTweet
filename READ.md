はい、承知いたしました。提供された情報と会話履歴に基づいて、両方のソースコードに関する`README.md`ファイルを作成します。

---

# X (旧 Twitter) 自動ポストプログラム集

このリポジトリには、X (旧 Twitter) API v2 を使用して自動投稿を行うためのPythonスクリプトが含まれています。APIキーの管理方法や投稿の自動化方法が異なる2つの主要なプログラムを提供します。

## 目次

1.  [はじめに](#はじめに)
2.  [X (旧 Twitter) API キーの取得について](#x-旧-twitter-api-キーの取得について)
    *   [X Developer Portalでの登録](#x-developer-portalでの登録)
    *   [APIキーの種類と取得](#apiキーの種類と取得)
    *   [認証設定](#認証設定)
    *   [無料プランの制限](#無料プランの制限)
3.  [プログラム一覧](#プログラム一覧)
    *   [1. `X自動ポストプログラム.py` (Azure Key Vaultを利用)](#1-x自動ポストプログラムpy-azure-key-vaultを利用)
    *   [2. `autotweet.py` (画像・テキストファイルからの投稿とスケジュール機能)](#2-autotweetpy-画像テキストファイルからの投稿とスケジュール機能)
4.  [必要なライブラリのインストール](#必要なライブラリのインストール)

---

## はじめに

X (旧 Twitter) は、投稿を自動化するためのAPIを提供しています。X API は基本的に有料ですが、**投稿機能だけであれば無料プランで利用可能です**。ただし、APIキーの取得プロセスは「**非常に面倒**」であると述べられています。

本リポジトリでは、以下の2つの異なるアプローチでXへの自動投稿を実現するPythonスクリプトを提供します。

*   `X自動ポストプログラム.py`: APIキーをAzure Key Vaultで安全に管理し、シンプルなテキスト投稿を行うプログラム。
*   `autotweet.py`: ローカルの画像ファイルとテキストファイルを読み込んで投稿し、スケジュール機能を持つプログラム。APIキーはスクリプト内に直接記述します。

## X (旧 Twitter) API キーの取得について

自動投稿プログラムを動作させるには、X Developer Portal でAPIキーを取得する必要があります。

### X Developer Portalでの登録

1.  **X（Twitter）Developer Portal** にアクセスします。
2.  画面右上の **「開発者ポータル」** をクリックします。ログインしていない場合は、X(Twitter)アカウントでログインします。
3.  **「Sign up for Free Account」** を選択し、無料アカウントを登録します。
4.  いくつかの項目（英語）の入力が求められます。特に「**Describe all of your use cases of Twitter’s data and API**」（X(Twitter)のAPIとデータの全ての使用事例を説明してください）の項目は、英語での記載が推奨されています。
    *   英語が苦手な場合は、DeepL や OpenAI の ChatGPT を利用して日本語の申請文を翻訳すると良いでしょう。
    *   **申請例**: 「I am a developer specializing in programming and design, and also a blogger focusing on app development. I am currently crafting a tool that automatically posts relevant tips and blog content to X. These posts, comprising text, images, and related blog URLs, are designed to adhere to X’s policies and provide value to my followers.」
    *   長文にしすぎず、翻訳しやすい日本語を使うとスムーズです。
5.  規約に関する3つのチェックボックスをチェックし、**「Submit」** ボタンを押します。

### APIキーの種類と取得

X API には**合計7つのAPIキー**が存在します。以前はプロジェクトとアプリの作成が必要でしたが、現在は自動生成されるため手続きが簡略化されています。

必要なキーは以下の通りです:
*   Consumer API Key
*   Consumer API Secret
*   Client ID
*   Client Secret
*   Bearer Token
*   Access Token
*   Access Token Secret

**Client IDとClient Secret**の2つは、**認証設定を行うと入手できます**。これらのキーはプログラムの認証で直接使用されない場合もありますが、設定を行っておかないとプログラムが認証エラーになるため、取得が必須です。
残りの5つは認証設定完了後に簡単に生成できます。

### 認証設定

X Developer Portalで認証設定を行う必要があります。

1.  X(Twitter) Developer Portal を開きます。
2.  画面左側にある**自身のアプリ名**をクリックします。
3.  **「User authentication settings」の「Set up」** をクリックします。
4.  以下の項目を設定します:
    *   **Read and write**: ポスト（投稿）する場合、書き込みが必要なため、これを選択します。**APIキーを生成する前にこの設定を行うか、設定後にAPIキーを再生成してください**。
    *   **Web App, Automated App or Bot**: 対象のアプリケーションタイプを選択します。
    *   **Callback URI / Redirect URL**: コールバックURLを入力します。これはユーザーごとにユニークなIDとなります。Google Apps Script (GAS) を利用して取得する例が示されています（`https://script.google.com/macros/d/[ID]/usercallback` の形式）。
    *   **Website URL**: 自身のウェブサイトのURLを入力します。X(Twitter)のURLでも構いません。
    *   その他の項目は空欄でも問題ありません。
5.  設定後、**「Save」>「Yes」** と進みます。
6.  表示される**OAuth 2.0 クライアント ID とクライアント シークレット**は一度しか表示されないため、**必ずメモしておきましょう**。
7.  **「Done」>「Yes, I saved it」** を選択します。
8.  **「Keys and tokens」** タブで、残りのAPIキーを確認・生成します。

### 無料プランの制限

X API Freeプランの主な制限は以下の通りです:
*   **無料**
*   **できること**: ツイートの投稿、自己アカウントの情報取得、Twitterログイン
*   **月間ツイート投稿上限**: 500件 (以前は1,500件)
*   **1日のAPI経由投稿上限**: 17件 (以前は50件)
*   **アプリのID数**: 1件まで

**注意点**:
*   Essentialアクセスレベル（無料プラン）では、**Twitter API v2のエンドポイントのみ**使用可能です。`tweepy.API()`を使用したAPI v1.1向けのコードは「`403 Forbidden`」エラーを発生させます。`tweepy.Client()`を使用してください。
*   Twitter API v1.1のメディアアップロード機能は、**2025年4月30日に廃止予定**です。

## プログラム一覧

### 1. `X自動ポストプログラム.py` (Azure Key Vaultを利用)

このプログラムは、APIキーをコード内に直接記述せず、**Azure Key Vault**から安全に取得して使用します。これにより、APIキーの漏洩リスクを大幅に低減します。

*   **ファイル名**: `X自動ポストプログラム.py`
*   **特徴**:
    *   **高いセキュリティ**: APIキーをAzure Key Vaultから取得するため、コード内へのハードコーディングよりもはるかに安全です。
    *   **Twitter API v2対応**: `tweepy.Client`を使用してツイートを投稿します。
    *   シンプルなテキスト投稿。
*   **セットアップ**:
    1.  **Azure Key Vaultの設定**:
        *   AzureにKey Vaultをセットアップします。
        *   取得した7つのX APIキーをKey Vaultのシークレットとして保存します。スクリプト内の`SECRET_NAMES`辞書に対応するシークレット名で保存してください (例: `BearerToken`, `APIKey`, `APIKeySecret`, `AccessToken`, `AccessTokenSecret`, `ClientID`, `ClientSecret2`)。
    2.  **スクリプトの編集**:
        *   `key_vault_url`変数に、自身のKey VaultのURLを記述します (例: `"https://your-key-vault-name.vault.azure.net/"`)。
    3.  **Azure認証の設定**:
        *   プログラムを実行する環境で、Azure Key Vaultへのアクセス権を持つ認証情報を設定します (例: Azure CLIでログインする、マネージドIDを利用するなど)。`DefaultAzureCredential`がこれらの認証情報を自動的に利用します.
*   **使用方法**:
    スクリプトを実行すると、`tweet_text`に指定された内容がXに投稿されます。

### 2. `autotweet.py` (画像・テキストファイルからの投稿とスケジュール機能)

このプログラムは、ローカルのフォルダから画像とテキストを読み込んで投稿し、スケジュール機能も持っています。APIキーはコード内に直接記述されます。

*   **ファイル名**: `autotweet.py`
*   **特徴**:
    *   **画像とテキストの動的読み込み**: 指定されたフォルダ内のPNG画像ファイルとTXTテキストファイルを読み込んで、投稿内容とします。
    *   **スケジュール機能**: `schedule`モジュールを使用し、フォルダ名で指定された時間（例: 「0900」フォルダは午前9時に投稿）に自動投稿を実行します。
    *   投稿済みのファイルは自動的に「sumi」というサブフォルダに移動します。
    *   このプログラムを動作させるには、**24時間稼働し続けるPCが必要**です。
*   **セットアップ**:
    1.  **APIキーの入力**: スクリプト内の各APIキー変数に、X Developer Portalで取得した7つのキーを直接入力します。
        ```python
        consumer_api_key = "（キーを入力）"
        consumer_api_secret = "（キーを入力）"
        bearer_token = "（キーを入力）"
        access_token = "（キーを入力）"
        access_token_secret = "（キーを入力）"
        # client_id, client_secretは認証設定に必要ですが、このtweepyクライアントでは直接使用されません。
        ```
    2.  **ベースフォルダの設定**: `base_folder`変数に、投稿する画像とテキストファイルが格納されているルートフォルダのパスを記述します (例: `r"C:\path\to\your\tweet_data"`)。
    3.  **フォルダ構造の準備**:
        *   `base_folder`内に、投稿したい時間を示す4桁の数字（例: `0900`, `1830`）を名前に持つサブフォルダを作成します。
        *   各サブフォルダ内に、投稿したいPNG画像ファイルと、ツイート内容が記述されたTXTテキストファイルをそれぞれ1つずつ配置します。
        *   各サブフォルダ内に、投稿済みのファイルを移動するための「`sumi`」という名前の空のフォルダを作成します。
        ```
        (指定したBaseとなるフォルダー)
        ├── 0900/
        │   ├── your_image.png
        │   ├── your_tweet.txt
        │   └── sumi/
        ├── 1830/
        │   ├── another_image.png
        │   ├── another_tweet.txt
        │   └── sumi/
        └── ...
        ```
*   **使用方法**:
    1.  コマンドプロンプトやターミナルを開きます。
    2.  `cd`コマンドで、`autotweet.py`を保存したフォルダに移動します。
    3.  以下のコマンドでプログラムを起動し、そのまま放置しておきます。スケジュールされた時間に自動的に投稿が実行されます。
        ```bash
        python autotweet.py
        ```

## 必要なライブラリのインストール

両方のプログラムはPythonで動作し、`tweepy`ライブラリが必要です。Azure Key Vaultを利用する場合は`azure-identity`と`azure-keyvault-secrets`が、スケジュール機能を利用する場合は`schedule`も必要になります。

コマンドプロンプトまたはターミナルで、以下のコマンドを実行して必要なライブラリをインストールしてください。

```bash
pip install tweepy
pip install azure-identity azure-keyvault-secrets # X自動ポストプログラム.py を使う場合
pip install schedule # autotweet.py を使う場合
```