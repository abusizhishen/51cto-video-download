#crawler
webjob为微职位课程,仅支持下载购买的课程。

##环境
python2.7 、pip

##安装模块
pip install -r requirements.txt

##用法
python run.py train_id  #替换train_id为需要的微职位id
如 python run.py 139
微职位可在video.json中查看

程序不会上传用户账号，仅会将账号保存在本地cache文件夹中的auth中，
cookie信息保存在cache文件夹中的cookies中，避免每次下载都需要输入密码。
