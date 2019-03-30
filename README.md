#crawler
webjob为微职位课程,仅支持下载已购买的课程。
但随着51cto接口的变化可能无法使用

!目前视频可下载，但是被加密了无法观看，我正在寻求解密方法，如果您对此有了解并愿意提供帮助，
请联系我
##环境
python2.7 、pip

##安装模块
pip install -r requirements.txt

##用法
```python WeiJob.py```

按提示输入您要下载的微职位id进行下载

注：程序不会上传用户账号，仅会将账号保存在本地cache文件夹中的auth中，
cookie信息保存在cache文件夹中的cookies中，避免每次下载都需要输入密码。
