import json,requests,re,os,threading,asyncio,math, time
from bs4 import BeautifulSoup

class cto(object):

    def course(self, headers, course_id, path):
        course_name = self.get_course_info(course_id)
        path = path+'/'+course_name
        os.path.exists(path) or os.mkdir(path)
        print('获取课程列表')
        lessons = obj.get_course_list(headers, course_id)

        for i in lessons:
            lesson_id = int(i['lesson_id'])
            video_id  = int(i['video_id'])
            filename = path+"/%d.%s.ts" % (i['number'], i['title'])

            if os.path.exists(filename):
                continue
            print('获取下载地址')
            urls = self.get_download_url(lesson_id, video_id)
            print(filename)

            continue
            self.download_video(filename, urls)
            return


    def get_download_url(self,lesson_id,video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=course&lesson_type=course'%(lesson_id,video_id)
        res = requests.get(url)
        return re.findall(r'https.*',res.text)

    def download_video(self,filename,urls):
        print('下载中-%s' % (filename))
        file = open(filename, 'ab')
        for i in urls:
            res = requests.get(i)
            file.write(res.content)
            file.flush()
        file.close()
        print(filename + '下载完毕')
        return

    def get_course_list(self, headers, course_id):
        infos = []
        currentPage = 1
        pageCount   = 1

        while(currentPage <= pageCount):
            url = 'http://edu.51cto.com/center/course/index/lesson-list?page=%d&size=20&id=%d' % ( currentPage, course_id)
            res = requests.get(url, headers=headers).text
            data = json.loads(res)
            page = data['data']['lessonList']
            pageCount = data['data']['pageCount']
            currentPage = currentPage+1

            for m in page:
                info = {
                    'title': m['title'],
                    'lesson_id': m['lesson_id'],
                    'video_id': m['url'][31:],   # '/center/course/lesson/index?id=166797'
                    'number': m['sorted']
                }

                infos.append(info)
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
'Cookie': 'www51cto=221B572B3256EF62D1130BBB0E5B46FBhRNw; _ourplusFirstTime=117-9-9-12-30-48; EDUACCOUNT=5f16b8d56b9a7faf506c0cf43fe13c53c16062dcca19a6b521e0d0a921b0efcaa%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22EDUACCOUNT%22%3Bi%3A1%3Bs%3A32%3A%22cb34aa578b53251559121b20c84a7299%22%3B%7D; callback_api_url=http%3A%2F%2Fhome.51cto.com%2Finfo%2Fbind-social; bdshare_firstime=1505662991476; pgv_pvi=376323072; 11552349flag=yes; Box09011=1; lookedPlayerH5Intro=1; playTime102316=2368.261904; _ga=GA1.2.1522624200.1505664621; _qddaz=QD.8u34ij.5an1ey.j7oxu9rd; playTime492_166130=389.700497; playTime102317=646.278676; playTime102321=646.436323; playTime492_166132=12.811746; playTime492_166133=642; eduSearchkey=alex; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1507791064; playTime492_167295=781.5; playTime492_167298=671.7; playTime492_167300=464.538411; playTime492_166661=749.307935; h5playersd=1; playTime492_167306=545; useNewPlayerStream=1; looyu_id=3e8ac569e96b7f69053157f51eca9284c4_20000923%3A15; pub_cookietime=864000; playTime492_201922=499.066484; playTime492_166131=525.469336; playTime492_201908=63.3; playTime492_201907=452.1; playTime492_201906=256.893475; playTime166806=117.271377; playTime166805=711.085436; playTime166785=395.185983; playTime166784=243.46904; h5playervoice=0.09; playTime166782=1075.2333; playTime166783=109.295701; pub_sauth1=AAZMFwwfXwtAXFdfaghXAQEBB1BfOwQEUloFVAVcVQI; pub_sauth2=c57b47c0cd0e990e119c698f7b2dae7e; playTime492_169541=95.656916; playTime492_169542=845.034806; playTime492_169543=526.875465; acw_tc=AQAAAGuW8WIGEAYA4Gzb3SwvTiiBvI4R; PHPSESSID=oc94e3h63a0ugfjrjs2dv5btsi; _identity=bfa70a0c76b4d639179329e98252535bc1c0703e07a646c078b24fed8572029ba%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B1353200%2Ctrue%2C43200%5D%22%3B%7D; BigUser=3ad36cc7bc0baadb681c7acfd75161a79b0387888bcdd2a8eff521dc3204dda8a%3A2%3A%7Bi%3A0%3Bs%3A7%3A%22BigUser%22%3Bi%3A1%3Bs%3A90%3A%22fe1fcAiTcWSM-mOtpcOBxWw1QWSt8A-Dxuyzks4oksM8IU0AC8AL8tj01T6AA9bvYOI_oJu1uKKADPHhJccUzhj40w%22%3B%7D; _csrf=bb4ee16e64c17f6f0d28d5cb9209c1f4f04bce9de16cc97155046a45eb51c07aa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22U%15%F0N%8F%E9%EDk%60.%2CfL%7E%0FQp%F8rP%F6%0A%01r%FF%2C%D3%B6%B4%B0%B2q%22%3B%7D; Hm_lvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509115873,1509199403,1509200882,1509287002; Cto_lvt_=1509199404,1509200881,1509200882,1509287002; playTime492_201927=3.792101; playTime492_201926=261.526348; playTime492_201925=440.432592; Box1111=1; playTime492_166656=644.912099; _ourplusReturnCount=195; _ourplusReturnTime=117-10-30-0-15-49; Hm_lpvt_8c8abdb71d78d33dfdb885e0bc71dae0=1509293749; Cto_lpvt_=1509293750'}

time1 = time.time()
obj = cto()
#77 164
course_id = 1691
path = 'd:/videos/course'

obj.course(headers,course_id,path)

time_total = time.time()-time1
print('总计花费时间%d秒'%(time_total))



