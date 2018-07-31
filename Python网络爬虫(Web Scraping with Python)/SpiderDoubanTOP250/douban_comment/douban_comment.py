import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
from os import path
import json
import codecs
import jieba
from bs4 import BeautifulSoup
from PIL import Image
from wordcloud import WordCloud
from scipy.misc import imread


headers = {"Host": "www.douban.com",
           "Referer": "https://www.douban.com/",
           'User-Agent': 'Mozilla/5.0 (Windows NT 20.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.226 Safari/537.36 Edge/25.25063'
           }

# 使用cookie登录信息
session = requests.session()  # session
session.cookies = cookielib.LWPCookieJar(filename='cookies')

try:
    session.cookies.load(ignore_discard=True)
    print('成功加载cookie!')
except:
    print("cookie 未能加载!")


""" 获取验证码 """


def get_captcha(url):
    # 获取验证码
    # pillow 的 Image 显示验证码
    print('成功获取验证码', url)
    captcha_url = url
    response = session.get(captcha_url, headers=headers)
    # 保存验证码
    with open('captcha.jpg', 'wb') as f:
        f.write(response.content)
        f.close()
    try:
        image = Image.open('captcha.jpg')
        image.show()  # 主动打开验证码图片
        image.close()
    except:
        print('请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("请输入验证码\n>")
    return captcha


""" 判断是否登录 """


def isLogin():
    # 登录个人主页，查看是否登录成功
    url = 'https://www.douban.com/people/154293529/'
    login_code = session.get(url, headers=headers,
                             allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


""" 登录 """


def login(acount, secret):
    homeurl = "https://www.douban.com/"
    htmlcha = session.get(homeurl, headers=headers).text
    # 带验证码请求
    patterncha = r'id="captcha_image" src="(.*?)" alt="captcha"'
    httpcha = re.findall(patterncha, htmlcha)
    pattern2 = r'type="hidden" name="captcha-id" value="(.*?)"'
    hidden_value = re.findall(pattern2, htmlcha)
    print(hidden_value)

    data = {
        "source": "index_nav",
        'form_email': acount,
        'form_password': secret
    }
    # 模拟登录请求
    if len(httpcha) > 0:
        print('验证码连接', httpcha)
        capcha = get_captcha(httpcha[0])
        data['captcha-solution'] = capcha
        data['captcha-id'] = hidden_value[0]

    print(data)
    post_url = 'https://www.douban.com/accounts/login'
    login_page = session.post(post_url, data=data, headers=headers)
    # 保存cookies
    session.cookies.save()

    if isLogin():
        print('登录成功，开始爬取数据。')
    else:
        print('登录失败！')


""" 爬取评论 """


def get_comment(filename):  # filename为爬取得内容保存的文件
    begin = 1
    next_url = '?start=20&limit=20&sort=new_score&status=P'
    f = open(filename, 'w+', encoding='utf-8')
    # while(True):
    time.sleep(5)
    comment_url = 'https://movie.douban.com/subject/26752088/comments'
    # data = {
    #     'start': '27',
    #     'limit': '-20',
    #     'sort': 'new_score',
    #     'status': 'P'
    # }
    headers2 = {
        "Host": "movie.douban.com",
        "Referer": "https://www.douban.com/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 20.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.226 Safari/537.36 Edge/25.25063',
        'Connection': 'keep-alive',
    }

    html = session.get(
        url='https://movie.douban.com/subject/26752088/comments' + next_url, headers=headers2)
    soup = BeautifulSoup(html.text, 'html.parser')

    # 爬取当前页面的所有评论
    result = soup.find_all('div', {'class': 'comment'})  # 爬取得所有的短评
    pattern4 = r'<p class=""> (.*?)' \
               r'</p>'
    for item in result:
        s = str(item)
        count2 = s.find('<p class="">')
        count3 = s.find('</p>')
        s2 = s[count2 + 12:count3]  # 抽取字符串中的评论
        if 'class' not in s2:
            f.write(s2)

    # # 获取下一页的链接
    # next_url = soup.find_all('div', {'id': 'paginator'})
    # pattern3 = r'href="(.*?)">后页'
    # if(len(next_url) == 0):
    #     break
    # next_url = re.findall(pattern3, str(next_url[0]))  # 得到后页的链接
    # if(len(next_url) == 0):  # 如果没有后页的链接跳出循环
    #     break
    # next_url = next_url[0]
    # print('%d爬取下一页评论...' % begin)
    # begin = begin + 1
    # # 如果爬取了6次则多休息2秒
    # if(begin % 6 == 0):
    #     time.sleep(30)
    #     print('休息...')
    # print(next_url)
    f.close()


"""保存结巴分词结果"""


def save_jieba_result(file_name):
    # 设置多线程切割
    # jieba.enable_parallel(4)
    dirs = path.join(path.dirname(__file__), file_name)
    print(dirs)
    # 文件读取
    with codecs.open(dirs, encoding='utf-8') as f:
        comment_text = f.read()
    # jieba 分词
    cut_text = " ".join(jieba.cut(comment_text))
    # 保存txt文件
    with codecs.open('pjl_jieba.txt', 'w', encoding='utf-8') as f:
        f.write(cut_text)


"""WordCloud词云"""


def draw_wordcloud(file_name):
    # 读取分词文件内容
    with codecs.open(file_name, encoding='utf-8') as f:
        comment_text = f.read()
    color_mask = imread('template.png')  # 读取背景图片
    # 排除词
    stopwords = [u'就是', u'电影', u'你们', u'这么', u'不过', u'但是', u'什么', u'没有', u'这个', u'那个', u'大家', u'比较', u'看到', u'真是',
                 u'除了', u'时候', u'已经', u'可以', u'一个', u'题材']
    font = r'C:\Windows\Fonts\simfang.ttf'  # 设置字体
    # WordCloud词云
    cloud = WordCloud(font_path=font, background_color='white', max_words=20000,
                      max_font_size=200, min_font_size=4, mask=color_mask, stopwords=stopwords)
    word_cloud = cloud.generate(comment_text)  # 产生词云
    word_cloud.to_file('pjl_cloud.jpg')


if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
    	login('账号', '密码')# 输入账号', '密码
    get_comment('key.txt')
    save_jieba_result('key.txt')
    draw_wordcloud('pjl_jieba.txt')
