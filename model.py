import requests
from bs4 import BeautifulSoup


class Mixin():
    def __repr__(self):
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        classname = self.__class__.__name__
        s = '\n'.join(properties)
        return '< {}\n{}>'.format(classname, s)


class Course(Mixin):
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
        self.plan = form.get('plan', '').strip()
        self.serial = form.get('serial', '').strip()
        self.name = form.get('name', '').strip()
        self.index = form.get('index', '').strip()
        self.credit = form.get('credit', '').strip()
        self.attr = form.get('attr', '').strip()
        self.test = form.get('test', '').strip()
        self.teacher = form.get('teacher', '').strip()
        self.studyStat = form.get('studyStat', '').strip()
        self.status = form.get('status', '').strip()


class Lesson(Mixin):
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
        self.weeks = lesson.get('weeks', '').strip('周')
        self.weeks = self.weeks.strip()  # 想想就掏粪啊
        self.day = lesson.get('day', '').strip()
        self.lesson_index = lesson.get('lesson_index', '').strip()
        self.lesson_num = lesson.get('lesson_num', '').strip()
        self.campus = lesson.get('campus', '').strip()
        self.building = lesson.get('building', '').strip()
        self.room = lesson.get('room', '').strip()
        self.course = None
        # ?

    def set_course(self, form):
        self.course = Course(form)


class User(Mixin):
    main_url = 'http://202.204.193.215/'
    login_url = main_url + 'loginAction.do'
    calender_url = main_url + 'xkAction.do?actionType=6'

    def __init__(self, username, password):
        """

        :param username: string
        :param password: string
        """
        self.login_form = {
            'zjh': username,
            'mm': password
        }
        self.trs = None
        self.lesson_list = []
        self.get_tr()
        self.get_lessons()
        self.fill_course()

    def calender_page(self):
        """

        :return: html page
        """
        with requests.session() as s:
            s.post(self.login_url, self.login_form)  # log in
            r = s.get(self.calender_url)  # get the calender
            # print(r.text)
            return r.text

    def get_tr(self):
        """

        set trs
        """
        calender_soup = BeautifulSoup(self.calender_page())
        calender_table = calender_soup.find_all('table')[-2]
        self.trs = calender_table.find_all('tr', 'odd')

    @staticmethod
    def get_td(tr):
        return tr.find_all('td')

    @staticmethod
    def get_td_main(tr):
        return tr.find_all(rowspan=True)

    def get_lessons(self):
        for tr in self.trs:
            tds = self.get_td(tr)
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
            # print(form)
            self.lesson_list.append(Lesson(form))

    def fill_course(self):
        for i, tr in enumerate(self.trs):
            tds = tr.find_all('td')
            rowspan = tds[0].get('rowspan', None)
            if rowspan is None:
                pass
            else:
                rowspan = int(rowspan)
                form = {
                    'plan': tds[0].string,
                    'serial': tds[1].string,
                    'name': tds[2].string,
                    'index': tds[3].string,
                    'credit': tds[4].string,
                    'attr': tds[5].string,
                    'test': tds[6].string,
                    'teacher': tds[7].string,
                    'studyStat': tds[9].string,
                    'status': tds[10].string
                }
                for t in range(i, i + rowspan):
                    # print(form)
                    self.lesson_list[t].course = Course(form)

    def test(self):
        print(self.lesson_list)
