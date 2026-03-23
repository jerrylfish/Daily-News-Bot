import feedparser
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 1. 设置新闻源 (RSS 订阅源)
NEWS_SOURCES = {
    "科技要闻": "https://36kr.com/feed",
    "华尔街见闻": "https://wallstreetcn.com/rss/news"
}

def get_news():
    html_content = "<h2>今日情报摘要</h2>"
    for cat, url in NEWS_SOURCES.items():
        feed = feedparser.parse(url)
        html_content += f"<h3>【{cat}】</h3><ul>"
        for entry in feed.entries[:5]:
            html_content += f"<li><a href='{entry.link}'>{entry.title}</a></li>"
        html_content += "</ul>"
    return html_content

def send_mail(content):
    # --- 配置区 ---
    mail_host = "smtp.qq.com"
    mail_user = "28220987@qq.com"
    mail_pass = "sxectdcguqtgbgfi"
    receiver = "28220987@qq.com"

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header("AI情报助手", 'utf-8')
    message['To'] = Header("指挥官", 'utf-8')
    message['Subject'] = Header("早安！今日行业情报已送达", 'utf-8')

    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
        smtp_obj.login(mail_user, mail_pass)
        smtp_obj.sendmail(mail_user, [receiver], message.as_string())
        print("🚀 邮件发送成功")
    except Exception as e:
        print(f"❌ 发送失败: {e}")

if __name__ == "__main__":
    send_mail(get_news())
