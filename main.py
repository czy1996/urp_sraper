import requests
from bs4 import BeautifulSoup


main_url = 'http://202.204.193.215/'
login_url = main_url + 'loginAction.do'
login_form = {'zjh': '2014011606', 'mm': 'czy5183031'}
calender_url = main_url + 'xkAction.do?actionType=6'

"""
>>> payload = {'key1': 'value1', 'key2': 'value2'}

>>> r = requests.post("http://httpbin.org/post", data=payload)
>>> print(r.text)
{
  ...
  "form": {
    "key2": "value2",
    "key1": "value1"
  },
  ...
}
"""

# r = requests.post(login_url, data=login_form)
# print(r.headers)


class Course(object):
    """
     培养方案
     课程号
     课程名
     课序号
     学分
     课程属性
     考试类型
     教师
     大纲日历
     修读方式
     选课状态

     周次
     星期
     节次
     节数
     校区
     教学楼
     教室

    """
    def __init__(self, form):
        self.plan = form.get('plan', None)
        self.serial = form.get('serial', None)
        self.name = form.get('name', None)
        self.index = form.get('index', None)
        self.credit = form.get('credit', None)
        self.attr = form.get('attr', None)
        self.test = form.get('test', None)
        self.teacher = form.get('teacher', None)
        self.studyStat = form.get('studyStat', None)
        self.status = form.get('status', None)


class Lesson():
    """
     周次
     星期
     节次
     节数
     校区
     教学楼
     教室
    """
    def __init__(self, lesson):
        self.weeks = lesson.get('weeks', None)
        self.day = lesson.get('day', None)
        self.lesson_index = lesson.get('lesson_index', None)
        self.lesson_num = lesson.get('lesson_num', None)
        self.campus = lesson.get('campus', None)
        self.building = lesson.get('building', None)
        self.room = lesson.get('room', None)
        self.course = None

    def set_course(self, form):
        self.course = Course(form)

    def __repr__(self):
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        classname = self.__class__.__name__
        s = '\n'.join(properties)
        return '< {}\n{}>'.format(classname, s)


"""
计划试用会话管理cookies
会话对象具有主要的 Requests API 的所有方法。

s = requests.Session()

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")

print(r.text)
# '{"cookies": {"sessioncookie": "123456789"}}'
"""


def calender_page():
    """

    :return: html page
    """
    with requests.session() as s:
        s.post(login_url, login_form)  # log in
        r = s.get(calender_url)  # get the calender
        return r.text


def get_tr():
    """

    :return: all tr containing lessons
    """
    calender_soup = BeautifulSoup(calender_page())
    calender_table = calender_soup.find_all('table')[-2]
    all_tr = calender_table.find_all('tr', 'odd')
    return all_tr


def get_td(tr):
    return tr.find_all('td')


def get_td_main(tr):
    return tr.find_all(rowspan=True)


def get_lessons(trs):
    lesson_list = []
    for tr in trs:
        tds = get_td(tr)
        rowspan = tds[0].get('rowspan', None)
        if rowspan is None:
            offset = 0
        else:
            offset = 11
        form = {
            'weeks': tds[offset + 0].string,
            'day': tds[offset + 1].string,
            'lesson_index': tds[offset + 2].string,
            'lesson_num': tds[offset + 3].string,
            'campus': tds[offset + 4].string,
            'building': tds[offset + 5].string,
            'room': tds[offset + 6].string
        }
        lesson_list.append(Lesson(form))
    return lesson_list


def fill_course(trs, lessons):
    for i, tr in enumerate(trs):
        rowspaan = tr[0].get('rowspan', None)
        if rowspaan is None:
            pass
        else:
            rowspaan = int(rowspaan)
            dict
            for t in range(0, rowspaan):



def test():
    trs = get_tr()
    lessons = get_lessons(trs)


if __name__ == '__main__':
    test()