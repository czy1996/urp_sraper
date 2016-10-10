from model import User
from config import username, password

# r = requests.post(login_url, data=login_form)
# print(r.headers)


"""
计划试用会话管理cookies
会话对象具有主要的 Requests API 的所有方法。

s = requests.Session()

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")

print(r.text)
# '{"cookies": {"sessioncookie": "123456789"}}'
"""


def test():
    u = User(username, password)
    u.test()


if __name__ == '__main__':
    test()