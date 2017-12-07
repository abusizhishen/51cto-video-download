#encoding=utf-8
import json,requests,re,os,threading,math,time,random,sys,cto
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

class Course(object):
    def course(self, headers, course_id, path = '../学习'):
        course_name = self.get_course_info(course_id)
        path = path+'/'+course_name
        lessons = self.get_lesson_list(headers, course_id)

        self.show_lessons(lessons)
        #如果分为很多章节
        if lessons['chapter']:
            for capter_id,lesson in lessons['chapter'].items():
                file_path = path +'/%s'%(lesson['title'])
                self.lesson_download(lesson['lesson'],file_path)
        else:
            self.lesson_download(lessons['lesson'],path)
        return

    def get_download_url(self,headers,lesson_id,video_id):
        url_m3u8 = 'http://edu.51cto.com/center/player/play/get-lesson-info?type=course&lesson_type=course&sign=999&lesson_id=%d' % (lesson_id)
        res = requests.get(url_m3u8,headers=headers).text

        if res != 'nobuy':
            url = json.loads(res)['dispatch_list'][1]['value'][0]['url']
            # url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=course&lesson_type=course'%(lesson_id,video_id)
            res = requests.get(url)
            return re.findall(r'https.*', res.text)
        else:
            return[]

    def lesson_download(self,lessons,path):
        for lesson in lessons:
            lesson_id = int(lesson['lesson_id'])
            video_id  = int(lesson['video_id'])
            filename  = path + "/%d.%s.ts" % (lesson['number'], lesson['title'].replace('/', '&'))
            cto.check_or_make_dir(path)

            if os.path.exists(filename): continue
            urls = self.get_download_url(headers, lesson_id, video_id)

            if urls : cto.download(filename, urls)
            else    :  print '未购买,无法下载-%d.%s' % (lesson['number'],lesson['title'])
            return

    def show_lessons(self,lessons):
        if lessons['chapter']:
            for lesson in lessons['chapter']:
                print lesson['number'],lesson['title']
        else:
            for lesson in lessons['lesson']:
                print lesson['number'],lesson['title']
        return

    def get_lesson_list(self, headers, course_id):
        infos = {
            'chapter':{},
            'lesson':[]
        }
        currentPage = 1
        while(currentPage):
            url = 'http://edu.51cto.com/center/course/index/lesson-list?page=%d&size=20&id=%d' % ( currentPage, course_id)
            res = requests.get(url, headers=headers).text
            data = json.loads(res)['data']
            currentPage = currentPage + 1 if data['currentPage'] < data['pageCount'] else 0

            for m in data['lessonList']:
                if m['chapter_id']:
                    if m['type'] == 'chapter':
                        infos['chapter'][m['chapter_id']] = {}
                        infos['chapter'][m['chapter_id']]['title'] = str(m['sorted'])+'.'+m['title']
                        infos['chapter'][m['chapter_id']]['lesson'] = []
                    else:
                        info = {
                            'title': m['title'],
                            'lesson_id': m['lesson_id'],
                            'video_id': m['url'][31:],
                            'number': m['sorted']
                        }
                        infos['chapter'][m['chapter_id']]['lesson'].append(info)
                else:
                    info = {
                        'title': m['title'],
                        'lesson_id': m['lesson_id'],
                        'video_id': m['url'][31:],
                        'number': m['sorted']
                    }
                    infos['lesson'].append(info)
        return infos

    def get_course_info(self,course_id):
        url = 'http://edu.51cto.com/course/%d.html'%(course_id)
        res = requests.get(url).text
        soup = BeautifulSoup(res,'html.parser')
        title = soup.title.string[0:-8]
        return title

headers = {
'Host': 'edu.51cto.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
'Referer': 'http://edu.51cto.com/center/wejob/usr/course-info?train_id=165&train_course_id=492',
'Cookie': 'www51cto=221B572B3256EF62D1130BBB0E5B46FBhRNw; _ourplusFirstTime=117-9-9-12-30-48; EDUACCOUNT=5f16b8d56b9a7faf506c0cf43fe13c53c16062dcca19a6b521e0d0a921b0efcaa%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22EDUACCOUNT%22%3Bi%3A1%3Bs%3A32%3A%22cb34aa578b53251559121b20c84a7299%22%3B%7D; callback_api_url=http%3A%2F%2Fhome.51cto.com%2Finfo%2Fbind-social; bdshare_firstime=1505662991476; pgv_pvi=376323072; 11552349flag=yes; Box09011=1; lookedPlayerH5Intro=1; playTime102316=2368.261904; _ga=GA1.2.1522624200.1505664621; _qddaz=QD.8u34ij.5an1ey.j7oxu9rd; playTime492_166130=389.700497; playTime102321=646.436323; playTime492_166132=12.811746; playTime492_166133=642; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1507791064; playTime492_167295=781.5; playTime492_167298=671.7; playTime492_167300=464.538411; playTime492_166661=749.307935; h5playersd=1; playTime492_167306=545; useNewPlayerStream=1; pub_cookietime=864000; playTime492_201922=499.066484; playTime492_201907=452.1; playTime492_201906=256.893475; playTime166806=117.271377; playTime166805=711.085436; playTime166785=395.185983; playTime166784=243.46904; h5playervoice=0.09; playTime166782=1075.2333; playTime166783=109.295701; pub_sauth1=AAZMFwwfXwtAXFdfaghXAQEBB1BfOwQEUloFVAVcVQI; pub_sauth2=c57b47c0cd0e990e119c698f7b2dae7e; playTime492_169541=95.656916; playTime492_201927=3.792101; playTime492_201926=261.526348; playTime492_201925=440.432592; playTime492_166656=644.912099; playTime492_201908=1.616333; playTime492_166131=41.216299; playTime492_169543=527.406423; playTime492_169542=16.322924; __utmz=1.1509529471.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _identity=bfa70a0c76b4d639179329e98252535bc1c0703e07a646c078b24fed8572029ba%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B1353200%2Ctrue%2C43200%5D%22%3B%7D; BigUser=b5ba750b1ae8280f1cbc7a009076c7f4c567f04322fb05563ed82914c0471c18a%3A2%3A%7Bi%3A0%3Bs%3A7%3A%22BigUser%22%3Bi%3A1%3Bs%3A90%3A%22cbf2cAiTcWSM-mOtpcOBxWw1QWSt8A-Dxuyzks4oksM8IU2Zxe840FEVVq10NtPn_bekBe4UpLYYaJwDxlnNBkhzFQ%22%3B%7D; Box1111=1; looyu_id=3e8ac569e96b7f69053157f51eca9284c4_20000923%3A22; __utma=1.1522624200.1505664621.1509529471.1509605654.2; acw_tc=AQAAAIhPhQ66XQkA4Gzb3WYku+2c5XFo; PHPSESSID=lc61r8ci5ja6846k94iaga6v2q; _csrf=095b85ca9da3fb5728af023655de0115cd624dc83e72c892f2ea6bad40bca379a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22%06qs%DF%DB%FC-%17%92%D1%7C%9C%D7%DE%BD%AC%FB_%EA%16%04%95Q%8D8%A2%0Dq%AA%14t%F5%22%3B%7D; Hm_lvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509526089,1509537975,1509599579,1509627609; Cto_lvt_=1509526089,1509537975,1509599579,1509627609; eduSearchkey=Python3.6ç¬è«å·¥ç¨å¸å¿çè§é¢æç¨_å±36è¯¾æ¶,pythonç¬è«,python,å´åºæ,ç¬è«; playTime166778=21.216843; playTime166779=8.049182; playTime102317=657.700962; playTime39285=2.768569; playTime192840=66.705784; _ourplusReturnCount=498; _ourplusReturnTime=117-11-3-0-44-17; playTime192836=2.37858; Cto_lpvt_=1509641072; Hm_lpvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509641072',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive',
}

time1 = time.time()
obj = Course()

course_id = 8360
obj.course(headers,course_id)
