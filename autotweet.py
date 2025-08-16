import tweepy
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Azure Key Vault の URL ※ 私はAzure KeyVaultを使用していますがAWSでもGoogleCloudでも何でもいいと思います。
# ここに自身のKey VaultのURLを記述してください。例: "https://your-key-vault-name.vault.azure.net/"
key_vault_url = "[Azure Key VaultのURLをここに記述]" [1, 3]

# Key Vault から取得するシークレット名と、Key Vault内での対応するシークレット名
# これらのシークレットはKey Vaultにあらかじめ設定しておく必要があります。
SECRET_NAMES = {
    "BEARER_TOKEN": "BearerToken",
    "CLIENT_ID": "ClientID", # ソース[1]に記載がありますが、このプログラムのtweepyクライアントでは直接使用されていません。
    "CLIENT_SECRET": "ClientSecret2", # ソース[1]に記載がありますが、このプログラムのtweepyクライアントでは直接使用されていません。
    "ACCESS_TOKEN": "AccessToken",
    "ACCESS_TOKEN_SECRET": "AccessTokenSecret",
    "API_KEY": "APIKey",
    "API_SECRET_KEY": "APIKeySecret"
} [1, 3]

credential = DefaultAzureCredential() [1, 3]
kv_client = SecretClient(vault_url=key_vault_url, credential=credential) [2, 3]

# Key Vault から各種APIキーの値を取得
secrets = {k: kv_client.get_secret(v).value for k, v in SECRET_NAMES.items()} [2, 4]

# Tweepy クライアントの初期化（Twitter API v2向け）
# 投稿には、Bearer Token, Consumer Key (API Key), Consumer Secret (API Secret Key), Access Token, Access Token Secretが必要です。
client = tweepy.Client(
    bearer_token=secrets["BEARER_TOKEN"],
    consumer_key=secrets["API_KEY"],
    consumer_secret=secrets["API_SECRET_KEY"],
    access_token=secrets["ACCESS_TOKEN"],
    access_token_secret=secrets["ACCESS_TOKEN_SECRET"]
) [2, 4]

# Twitter API v1.1向けの認証（一部機能や過去のサンプルコードとの互換性のため）
# EssentialアクセスレベルではTwitter API v2のみ使用可能です [5]。
# この部分が現在のFreeプランでの投稿に必須ではない場合がありますが、ソースに記載があるため含めます [2, 6]。
auth = tweepy.OAuthHandler(secrets["API_KEY"], secrets["API_SECRET_KEY"]) [2]
auth.set_access_token(secrets["ACCESS_TOKEN"], secrets["ACCESS_TOKEN_SECRET"]) [2]
api = tweepy.API(auth) [6]
print("認証ok") [6]

# 投稿するテキストの例
tweet_text = "自動ポストテスト！🚀 #Azure #Python" [4, 6]

# ツイートの実行
response = client.create_tweet(text=tweet_text) [4, 6]
print("✅ 投稿成功:", response) [4, 6]