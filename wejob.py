# -*- coding: utf-8 -*-
import json,requests,re,os, time, random
from bs4 import BeautifulSoup

class cto(object):
    def train(self, headers, train_id, path):
        os.path.exists(path) or os.mkdir(path)
        print('获取课程列表')
        courses = obj.get_train_courses(headers, train_id)

        #打印course名称
        for course in courses:
            print(course['course_name'])

        for course in courses:

            train_course_id = int(course['train_course_id'])
            file_path = path + '/'+course['number']+'.'+course['course_name'].replace(':',' ')
            os.path.exists(file_path) or os.mkdir(file_path)
            print('获取课程详情')
            res = obj.get_train_course_info(headers, train_id, train_course_id)

            for i in res:
                lesson_id = '_'.join([str(train_course_id), str(i['lesson_id'])])
                filename = file_path+"/%d.%s.ts" % (res.index(i) + 1, i['lesson_name'])
                if os.path.exists(filename):
                    continue
                urls = self.get_download_url(lesson_id, i['video_id'])
                try:
                    self.download_video(filename, urls)
                except Exception :
                    time.sleep(random.uniform(5,10))
                    self.download_video(filename, urls)

    def get_download_url(self,lesson_id,video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=wejoboutcourse&lesson_type=course'%(lesson_id,video_id)
        res = requests.get(url).text
        return re.findall(r'https.*',res)

    def download_video(self,filename,urls):
        time.sleep(random.uniform(0, 1))
        print(u'正在下载-'+filename)
        file = open(filename, 'ab')
        for i in urls:
            res = requests.get(i)
            file.write(res.content)
            file.flush()
        file.close()
        return

    def get_train_course_info(self, headers, train_id, train_course_id):
        infos = []
        current_page = 1
        while(current_page):
            url = 'http://edu.51cto.com/center/wejob/usr/course-infoajax?train_id=%d&train_course_id=%d&page=%d&size=20'%(train_id, train_course_id,current_page)
            res = requests.get(url, headers=headers).text
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

    def get_train_courses(self,headers,train_id):
        data = []
        current_page = 1
        while (current_page):
            url = 'http://edu.51cto.com/center/wejob/usr/courseajax?train_id=%d&page=%d&size=1000'%(train_id,current_page)
            res = requests.get(url,headers=headers)
            res = json.loads(res.text)['data']
            current_page = res['current_page']+1 if  res['current_page'] < res['count_page'] else 0

            for i in res['data']:
                course = {
                    'course_name':i['course_name'],
                    'train_id':i['train_id'],
                    'train_course_id':i['train_course_id'],
                    'lesson_num':i['lesson_num'],
                    'number':i['number']
                }
                data.append(course)
        return data

    def get_train_info(self,train_id):
        url = ''
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'html.parser')
        return

    def show_train_course_list(self,headers,train_id):
        data = self.get_train_courses(headers, train_id)
        for i in data:
            print(i)
        return

    def show_train_course_lists(self, headers, train_id):
        data = self.get_train_courses(headers, train_id)
        for i in data:
            print(i)
        return

headers = {
'Host': 'edu.51cto.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
'Referer': 'http://edu.51cto.com/center/wejob/usr/course-info?train_id=165&train_course_id=492',
'Cookie': 'www51cto=221B572B3256EF62D1130BBB0E5B46FBhRNw; _ourplusFirstTime=117-9-9-12-30-48; EDUACCOUNT=5f16b8d56b9a7faf506c0cf43fe13c53c16062dcca19a6b521e0d0a921b0efcaa%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22EDUACCOUNT%22%3Bi%3A1%3Bs%3A32%3A%22cb34aa578b53251559121b20c84a7299%22%3B%7D; callback_api_url=http%3A%2F%2Fhome.51cto.com%2Finfo%2Fbind-social; bdshare_firstime=1505662991476; pgv_pvi=376323072; 11552349flag=yes; Box09011=1; lookedPlayerH5Intro=1; playTime102316=2368.261904; _ga=GA1.2.1522624200.1505664621; _qddaz=QD.8u34ij.5an1ey.j7oxu9rd; playTime492_166130=389.700497; playTime102317=646.278676; playTime102321=646.436323; playTime492_166132=12.811746; playTime492_166133=642; eduSearchkey=alex; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1507791064; playTime492_167295=781.5; playTime492_167298=671.7; playTime492_167300=464.538411; playTime492_166661=749.307935; h5playersd=1; playTime492_167306=545; useNewPlayerStream=1; looyu_id=3e8ac569e96b7f69053157f51eca9284c4_20000923%3A15; pub_cookietime=864000; playTime492_201922=499.066484; playTime492_166131=525.469336; playTime492_201908=63.3; playTime492_201907=452.1; playTime492_201906=256.893475; playTime166806=117.271377; playTime166805=711.085436; playTime166785=395.185983; playTime166784=243.46904; h5playervoice=0.09; playTime166782=1075.2333; playTime166783=109.295701; pub_sauth1=AAZMFwwfXwtAXFdfaghXAQEBB1BfOwQEUloFVAVcVQI; pub_sauth2=c57b47c0cd0e990e119c698f7b2dae7e; playTime492_169541=95.656916; playTime492_169542=845.034806; playTime492_169543=526.875465; acw_tc=AQAAAGuW8WIGEAYA4Gzb3SwvTiiBvI4R; PHPSESSID=oc94e3h63a0ugfjrjs2dv5btsi; _identity=bfa70a0c76b4d639179329e98252535bc1c0703e07a646c078b24fed8572029ba%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B1353200%2Ctrue%2C43200%5D%22%3B%7D; BigUser=3ad36cc7bc0baadb681c7acfd75161a79b0387888bcdd2a8eff521dc3204dda8a%3A2%3A%7Bi%3A0%3Bs%3A7%3A%22BigUser%22%3Bi%3A1%3Bs%3A90%3A%22fe1fcAiTcWSM-mOtpcOBxWw1QWSt8A-Dxuyzks4oksM8IU0AC8AL8tj01T6AA9bvYOI_oJu1uKKADPHhJccUzhj40w%22%3B%7D; _csrf=bb4ee16e64c17f6f0d28d5cb9209c1f4f04bce9de16cc97155046a45eb51c07aa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22U%15%F0N%8F%E9%EDk%60.%2CfL%7E%0FQp%F8rP%F6%0A%01r%FF%2C%D3%B6%B4%B0%B2q%22%3B%7D; Hm_lvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509115873,1509199403,1509200882,1509287002; Cto_lvt_=1509199404,1509200881,1509200882,1509287002; playTime492_201927=3.792101; playTime492_201926=261.526348; playTime492_201925=440.432592; Box1111=1; playTime492_166656=644.912099; _ourplusReturnCount=195; _ourplusReturnTime=117-10-30-0-15-49; Hm_lpvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509293749; Cto_lpvt_=1509293750',
'Accept-Encoding':'gzip, deflate',
'Connection':'keep-alive'
}

time1 = time.time()
obj = cto()
trains = [
    165, #人工智能
    77,
    164,
    94, #Python高级自动化开发工程师微职位
    139
]

train_id = 165
#path = '%d'%(train_id)
path = u'../学习'
# obj.show_train_course_list(headers,train_id)
# res = obj.get_train_courses(headers, train_id)
#res = obj.get_train_course_info(headers,train_id,190)
obj.train(headers, train_id, path)
# res = obj.get_train_courses(headers, train_id)
# #res = obj.get_train_course_info(headers, train_id,536,2)
# for i in res:
#     print(i)
time_total = time.time()-time1
print('总计花费时间%d秒'%(time_total))



