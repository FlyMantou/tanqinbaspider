
from urllib import request
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('huanghai.db')
cursor = conn.cursor()
#cursor.execute('create table tanqinba (id INTEGER primary key AUTOINCREMENT, piano_url varchar(20),'
 #              'piano_name varchar(20),piano_des varchar(800),piano_singer varchar(20),'
 #              'piano_seeNum varchar(20),piano_collectNum varchar(20),piano_hard varchar(20),'
 #              'piano_uploadUser varchar(20),piano_uploadTime varchar(20))')
#定义爬虫方法
def runSpider(url):
    print('------正在爬取：%s地址的网页------' % url)
    page = request.urlopen(url)
    htmlcode = page.read()#读取页面源码

    soup = BeautifulSoup(htmlcode,"html.parser",from_encoding="utf-8")
    con404 = soup.find('div',id='con404')
    if con404!=None:
        print('------此地址不存在------')
        return
    try:
        name = soup.find('h1',class_='title_color').get_text()
    except:
        print('------此地址不存在------')
        return
    des = soup.find('p',class_='content_color').get_text()
    singer = soup.find('span',class_='brief_color').get_text()
    singer = singer[singer.find('/')+1:]
    seeNum = soup.find('span',class_='eyes').get_text()
    collectNum = soup.find('span',class_='c-num').get_text()
    hard = soup.find_all('span',class_='brief_color')[3].get_text()
    try:
        uploadUser = soup.find_all('h3',class_='title_color')[2].get_text()
        uploadTime = soup.find('div',class_='col_243').find_all('p','brief_color')[1].get_text()
    except:
        uploadUser = '无'
        uploadTime = soup.find('div',class_='col_243').find_all('p','brief_color')[1].get_text()



    print('正在保存信息至数据库')
    sql = '''
    insert into tanqinba 
    (piano_url, piano_name,piano_des,piano_singer,piano_seeNum,piano_collectNum,piano_hard,piano_uploadUser,piano_uploadTime) 
    values 
    (:pi_url, :pi_name,:pi_des,:pi_singer,:pi_seeNum,:pi_collectNum,:pi_hard,:pi_uploadUser,:pi_uploadTime)
    '''
    cursor.execute(sql,{'pi_url':url,'pi_name':name,'pi_des':des,'pi_singer':singer,'pi_seeNum':seeNum,'pi_collectNum':collectNum,'pi_hard':hard,'pi_uploadUser':uploadUser,'pi_uploadTime':uploadTime})

    conn.commit()
    print('输出信息：')
    print(name)
    print(des)
    print(singer)
    print(seeNum)
    print(collectNum)
    print(hard)
    print(uploadUser)
    print(uploadTime)
    print('------爬取结束------')
    #print(htmlcode)#在控制台输出
   # print(str(htmlcode))

#调用爬虫
for i in range(15201,100000):
    runSpider('http://www.tan8.com/yuepu-%s.html' % i)
#runSpider('http://www.tan8.com/yuepu-61037.html')


cursor.close()