import requests

# 推送参数 https://bark.day.app/#/tutorial?id=%e8%af%b7%e6%b1%82%e5%8f%82%e6%95%b0
apiKey = "xxx"
def SendMsg(data):
    # Bark 服务器的 URL，替换 `your_key` 为你的实际密钥
    url = "https://api.day.app/"+apiKey

    # 请求的 JSON 数据
    # data = {
    #     "body": "Test Bark Server",
    #     "title": "Test Title",
    #     "badge": 1,
    #     "category": "myNotificationCategory",
    #     "sound": "minuet.caf",
    #     "icon": "https://day.app/assets/images/avatar.jpg",
    #     "group": "test",
    #     "url": "https://mritd.com"
    # }

    # 发送 POST 请求
    response = requests.post(url, json=data, headers={"Content-Type": "application/json; charset=utf-8"})
    print(response.json())

# 输出响应结果
# print(response.status_code)
# print(response.json())

if __name__ == '__main__':
    data = {
        "group": "CEX",
        "title": "新上代币",
        "level": "timeSensitive",
        "isArchive": "1",
        "body": "币安新上代币"
    }
    SendMsg(data)
