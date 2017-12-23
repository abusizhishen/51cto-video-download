# coding=utf-8
from bs4 import BeautifulSoup
import json,requests,re,os,time,random,datetime,sys,cto

reload(sys)
sys.setdefaultencoding('utf-8')

class Wejob(object,):
    action = ('info','download')
    def __init__(self,headers, train_id, path = '学习'):
        self.headers = headers
        self.train_id = train_id
        current_path = os.path.abspath(__file__)
        self.path = os.path.abspath(os.path.join(current_path,'../../',path))

    def train(self):
        train_start = time.time()
        train = self.get_train_info()
        train_name = train['name']
        self.path+='/'+train_name

        print '微职位名称:'+train_name+'\n获取课程列表'
        courses = train['courses']

        total_course = len(courses)
        print '总计%d门course' % (total_course)
        #打印course名称
        for course in courses:
            print(str(courses.index(course)+1)+'.'+course['course_name'])

        action = raw_input('是否下载y/n? 默认y:')
        if action == 'n':
            print '终止下载,程序退出'
            exit()
        for course in courses:
            course_id = int(course['train_course_id'])
            course_index = courses.index(course)+1

            file_path = os.path.join(self.path, course['number']+'.'+course['course_name'])
            cto.check_or_make_dir(file_path)

            print('%d/%d获取%s详情' % (course_index, total_course,course['course_name']))
            lessons = self.get_course_info(course_id)
            total_lesson = len(lessons)

            for lesson in lessons:
                lesson_id = '_'.join([str(course_id), str(lesson['lesson_id'])])
                lesson_index = lessons.index(lesson)+1
                filename = os.path.join(file_path, "%d.%s.ts" % (lesson_index, lesson['lesson_name']))
                if os.path.exists(filename):
                    continue

                print datetime.datetime.now().strftime("%H:%M:%S")+' 正在下载(%d/%d)-%s' % (lesson_index,total_lesson,lesson['lesson_name'])
                urls = self.get_download_url(lesson_id, lesson['video_id'])
                try:
                    cto.download(filename, urls)
                except Exception :
                    time.sleep(random.uniform(5,10))
                    cto.download(filename, urls)

        print 'train下载用时总计'+cto.total_time(time.time()-train_start)

    def get_download_url(self,lesson_id,video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=wejoboutcourse&lesson_type=course'\
              %(lesson_id,video_id)
        res = requests.get(url).text
        return re.findall(r'https.*',res)

    def get_course_info(self,course_id):
        infos = []
        current_page = 1
        while(current_page):
            url  = 'http://edu.51cto.com/center/wejob/usr/course-infoajax?train_id=%d&train_course_id=%d&page=%d&size=20'\
                  %(self.train_id, course_id,current_page)
            res  = requests.get(url, headers=self.headers).text
            data = json.loads(res)['data']
            current_page = data['current_page'] + 1 if data['current_page'] < data['count_page'] else 0
            pages = data['data']

            for m in pages:
                info = {
                    'lesson_name': m['lesson_name'],
                    'lesson_id'  : m['lesson_id'],
                    'video_id'   : m['video_id']
                }
                infos.append(info)
        return infos

    def get_train_info(self):
        train = {'name':self.get_train_name(),'courses':[]}
        current_page = 1

        while (current_page):
            url = 'http://edu.51cto.com/center/wejob/usr/courseajax?train_id=%d&page=%d&size=1000'%\
                  (self.train_id,current_page)
            res = requests.get(url,headers=self.headers)
            res = json.loads(res.text)['data']
            current_page = res['current_page']+1 if  res['current_page'] < res['count_page'] else 0

            for i in res['data']:
                course = {
                    'course_name':i['course_name'].encode('utf-8'),
                    'train_id':i['train_id'],
                    'train_course_id':i['train_course_id'],
                    'lesson_num':i['lesson_num'],
                    'number':i['number']
                }
                train['courses'].append(course)
        return train

    def get_train_name(self):
        url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'html.parser')
        title = soup.find('h2', id='CourseTitle')
        return title.string

    def show_train_course_list(self):
        train = self.get_train_info()
        for i in train['course']:
            print '微职位_id: %d; 课程名称: %s ; 总课程数: %d' % (i['train_id'],i['course_name'], i['lesson_num'])
        return

headers = {
    'Host': 'edu.51cto.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Referer': 'http://edu.51cto.com/center/wejob/usr/course-info?train_id=165&train_course_id=492',
    'Cookie': 'www51cto=221B572B3256EF62D1130BBB0E5B46FBhRNw; _ourplusFirstTime=117-9-9-12-30-48; EDUACCOUNT=5f16b8d56b9a7faf506c0cf43fe13c53c16062dcca19a6b521e0d0a921b0efcaa%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22EDUACCOUNT%22%3Bi%3A1%3Bs%3A32%3A%22cb34aa578b53251559121b20c84a7299%22%3B%7D; callback_api_url=http%3A%2F%2Fhome.51cto.com%2Finfo%2Fbind-social; bdshare_firstime=1505662991476; pgv_pvi=376323072; 11552349flag=yes; Box09011=1; lookedPlayerH5Intro=1; playTime102316=2368.261904; _ga=GA1.2.1522624200.1505664621; _qddaz=QD.8u34ij.5an1ey.j7oxu9rd; playTime492_166130=389.700497; playTime102317=646.278676; playTime102321=646.436323; playTime492_166132=12.811746; playTime492_166133=642; eduSearchkey=alex; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1507791064; playTime492_167295=781.5; playTime492_167298=671.7; playTime492_167300=464.538411; playTime492_166661=749.307935; h5playersd=1; playTime492_167306=545; useNewPlayerStream=1; looyu_id=3e8ac569e96b7f69053157f51eca9284c4_20000923%3A15; pub_cookietime=864000; playTime492_201922=499.066484; playTime492_166131=525.469336; playTime492_201908=63.3; playTime492_201907=452.1; playTime492_201906=256.893475; playTime166806=117.271377; playTime166805=711.085436; playTime166785=395.185983; playTime166784=243.46904; h5playervoice=0.09; playTime166782=1075.2333; playTime166783=109.295701; pub_sauth1=AAZMFwwfXwtAXFdfaghXAQEBB1BfOwQEUloFVAVcVQI; pub_sauth2=c57b47c0cd0e990e119c698f7b2dae7e; playTime492_169541=95.656916; playTime492_169542=845.034806; playTime492_169543=526.875465; acw_tc=AQAAAGuW8WIGEAYA4Gzb3SwvTiiBvI4R; PHPSESSID=oc94e3h63a0ugfjrjs2dv5btsi; _identity=bfa70a0c76b4d639179329e98252535bc1c0703e07a646c078b24fed8572029ba%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B1353200%2Ctrue%2C43200%5D%22%3B%7D; BigUser=3ad36cc7bc0baadb681c7acfd75161a79b0387888bcdd2a8eff521dc3204dda8a%3A2%3A%7Bi%3A0%3Bs%3A7%3A%22BigUser%22%3Bi%3A1%3Bs%3A90%3A%22fe1fcAiTcWSM-mOtpcOBxWw1QWSt8A-Dxuyzks4oksM8IU0AC8AL8tj01T6AA9bvYOI_oJu1uKKADPHhJccUzhj40w%22%3B%7D; _csrf=bb4ee16e64c17f6f0d28d5cb9209c1f4f04bce9de16cc97155046a45eb51c07aa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22U%15%F0N%8F%E9%EDk%60.%2CfL%7E%0FQp%F8rP%F6%0A%01r%FF%2C%D3%B6%B4%B0%B2q%22%3B%7D; Hm_lvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509115873,1509199403,1509200882,1509287002; Cto_lvt_=1509199404,1509200881,1509200882,1509287002; playTime492_201927=3.792101; playTime492_201926=261.526348; playTime492_201925=440.432592; Box1111=1; playTime492_166656=644.912099; _ourplusReturnCount=195; _ourplusReturnTime=117-10-30-0-15-49; Hm_lpvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509293749; Cto_lpvt_=1509293750',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'keep-alive'
}


def go():
    args = sys.argv

    if len(args) < 2:
        train_id = raw_input('请输入train_id:')
    else:
        train_id = args[1]

    try:
        obj = Wejob(headers, int(train_id))
        obj.train()
    except KeyboardInterrupt:
        print('程序退出')
        exit()

go()