import json,requests,re,os,threading,asyncio,math, time, random
from bs4 import BeautifulSoup

class cto(object):
    def topic(self, headers, topic_id, path):
        topic = self.get_train_courses(headers,topic_id)
        file_path = path+'/%s'%(topic['name'])
        os.path.exists(file_path) or os.mkdir(file_path)

        for course_id in topic['courses']:
            course_name = self.get_course_info(course_id)
            path = file_path+'/'+str(topic['courses'].index(course_id)+1)+'.'+course_name
            os.path.exists(path) or os.mkdir(path)
            lessons = obj.get_course_list(headers, course_id)

            for i in lessons:
                lesson_id = int(i['lesson_id'])
                video_id  = int(i['video_id'])
                filename = path+"/%d.%s.ts" % (i['number'], i['title'])

                if os.path.exists(filename):continue
                urls = self.get_download_url(lesson_id, video_id)
                try:self.download_video(filename, urls)
                except requests.HTTPError:
                    print('http异常，稍后重试')
                    time.sleep(random.uniform(5,10))
                    self.download_video(filename, urls)

    def get_download_url(self,lesson_id,video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=course&lesson_type=course'%(lesson_id,video_id)
        res = requests.get(url)
        return re.findall(r'https.*',res.text)

    def download_video(self,filename,urls):
        time.sleep(random.uniform(0,1))
        print('正在下载--'+filename)
        file = open(filename, 'ab')
        for i in urls:
            res = requests.get(i)
            file.write(res.content)
            file.flush()
        file.close()
        print('下载完毕--'+filename )
        return

    def get_train_courses(self, headers, train_id):
        url = 'http://edu.51cto.com/topic/%d.html' % (train_id)
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, 'html.parser')
        divs = soup.find_all('div', class_='middle')
        data = {
            'name': soup.h2.string,
            'courses': []
        }

        for i in divs:
            data['courses'].append(int((i.a['href']).split('=')[1]))
        return data

    def get_course_list(self, headers, course_id):
        infos = []
        currentPage = 1
        while(currentPage):
            url = 'http://edu.51cto.com/center/course/index/lesson-list?page=%d&size=20&id=%d' % ( currentPage, course_id)
            res = requests.get(url, headers=headers).text
            data = json.loads(res)['data']
            currentPage = currentPage + 1 if data['currentPage'] < data['pageCount'] else 0

            for m in data['lessonList']:
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
'Referer': 'http://edu.51cto.com',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'
}

time1 = time.time()
obj = cto()
topics = {

}
topic_id = 172
path = 'f:/videos/topic'

res = obj.topic(headers,topic_id,path)
print(res)
time_total = time.time()-time1
print('总计花费时间%d秒'%(time_total))