import requests
import time
from datetime import datetime

from bark import SendMsg

# 监控周期，单位：秒
monitor_interval = 60  # 每隔 60 秒查询一次

# API URL
api_url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48&pageNo=1&pageSize=20"

# 记录已经处理过的文章ID，避免重复提醒
processed_article_ids = set()


# 打印时加上时间戳
def log_with_time(message):
    """打印带时间戳的消息"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time}: {message}")


# 初始化时获取现有的文章ID
def initialize_processed_articles():
    """初始化时获取当前所有文章ID，避免启动时提醒已有文章"""
    try:
        response = requests.get(api_url)
        data = response.json()

        if data["code"] == "000000" and data["data"]:
            articles = data["data"]["catalogs"][0]["articles"]

            for article in articles:
                article_id = article["id"]
                # 记录当前已有的所有文章ID，启动时不做提醒
                processed_article_ids.add(article_id)

        log_with_time("Initialization complete. Monitoring new articles...")

    except Exception as e:
        log_with_time(f"Error during initialization: {e}")


# 检查是否有包含 "Launchpool" 关键字的文章
def check_for_launchpool_articles():
    """检查API中是否有包含“Launchpool”的新文章"""
    try:
        response = requests.get(api_url)
        data = response.json()

        if data["code"] == "000000" and data["data"]:
            articles = data["data"]["catalogs"][0]["articles"]

            for article in articles:
                article_id = article["id"]
                title = article["title"]
                # 如果文章ID之前没有处理过，并且标题中包含 "Launchpool"
                if article_id not in processed_article_ids and "Will" in title:
                    # 记录已处理过的文章ID
                    processed_article_ids.add(article_id)

                    # if article_id not in processed_article_ids in title:
                    log_with_time(f"New Launchpool article found: {title}")
                    # 在此处可以扩展，例如发送邮件或其他通知
                    data = {
                        "group": "CEX",
                        "title": "新上代币",
                        "level": "timeSensitive",
                        "isArchive": "1",
                        "body": title + datetime.now().strftime("%d %H:%M:%S")
                    }
                    SendMsg(data)

    except Exception as e:
        log_with_time(f"Error fetching or processing data: {e}")


# 持续监控
def main():
    """启动监控程序"""
    # 初始化，获取当前所有文章ID
    initialize_processed_articles()

    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        check_for_launchpool_articles()

        time.sleep(monitor_interval)


if __name__ == "__main__":
    main()
