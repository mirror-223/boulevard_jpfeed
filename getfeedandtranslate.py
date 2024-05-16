import os
import feedparser
from googletrans import Translator

# Security BoulevardのフィードのURL
RSS_FEED_URL = 'https://securityboulevard.com/feed/'

# Slackのwebhook URL
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# 翻訳器の初期化
translator = Translator()

def translate_article(article):
    """記事の内容を日本語に翻訳する"""
    title = translator.translate(article.title, dest='ja').text
    summary = translator.translate(article.summary, dest='ja').text
    return title, summary

def post_to_slack(title, summary):
    """Slackのチャンネルに投稿する"""
    payload = {
        "text": f"*{title}*\n{summary}"
    }
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def lambda_handler(event, context):
    """メインの処理"""
    feed = feedparser.parse(RSS_FEED_URL)
    for article in feed.entries:
        title, summary = translate_article(article)
        post_to_slack(title, summary)

    return {
        'statusCode': 200,
        'body': 'RSS feed processed and posted to Slack'
    }
