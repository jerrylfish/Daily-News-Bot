import feedparser
import requests
import json

# 1. 设置新闻源
NEWS_SOURCES = {
    "科技要闻": "https://36kr.com/feed",
    "华尔街见闻": "https://wallstreetcn.com/rss/news"
}

# 2. ⭐ 填写你刚才复制的钉钉 Webhook 地址
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=c7c6812afab21b0ef3236802aa8c1f7fedf356592d07d8f84d086b5c8b89d22e"

def get_news():
    news_list = []
    for cat, url in NEWS_SOURCES.items():
        feed = feedparser.parse(url)
        # 每个分类取最新的 3 条
        for entry in feed.entries[:3]:
            news_list.append(f"【{cat}】{entry.title}\n🔗 {entry.link}")
    
    return "\n\n".join(news_list)

def send_to_dingtalk(content):
    # 钉钉推送的格式要求
    headers = {'Content-Type': 'application/json'}
    payload = {
        "msgtype": "text",
        "text": {
            # ⭐ 注意：内容里必须包含你设置的关键词“情报”
            "content": f"📢 指挥官，今日情报已送达：\n\n{content}"
        }
    }
    
    try:
        response = requests.post(DINGTALK_WEBHOOK, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("🚀 钉钉推送成功！")
        else:
            print(f"❌ 推送失败，返回码：{response.status_code}")
    except Exception as e:
        print(f"❌ 发生错误：{e}")

if __name__ == "__main__":
    # 执行抓取
    news_data = get_news()
    if news_data:
        send_to_dingtalk(news_data)
    else:
        print("📭 未抓取到新内容")
