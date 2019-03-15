'''
知乎文章和回答静态化为html文件
参考了用户lilydjwg的morerss项目
https://github.com/lilydjwg/morerssplz

其实我想要的不是静态化，而是备份+检索。静态化不是一个好的备份方式。
'''

from lxml.html import fromstring, tostring
import requests
import re
import json
from base import tidy_content
import sys
import os

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
headers = {
    'User-Agent': user_agent,
}

page_template = '''\
<!DOCTYPE html>
<meta charset="utf-8" />
<meta name="referrer" value="no-referrer" />

<title>{title} - {author}</title>
<style type="text/css">
body {{ max-width: 700px; margin: auto; }}
</style>
<h2>{title}</h2>
<h3>作者: <a href="https://www.zhihu.com/people/{people}">{author}</a></h3>
{body}
<hr/>
<footer><a href="{url}">原文链接</a></footer>
'''

article_title_image = '''\
<figure><img src="{}" referrerpolicy="no-referrer"></figure>
'''

def static(url, post_type, id):
    response = requests.get(url, headers = headers)
    page = response.text
    doc = fromstring(page)
    static = doc.xpath('//script[@id="js-initialData"]')[0]
    content = json.loads(static.text)['initialState']

    article = content['entities'][post_type][id]

    # 清洗内容
    body = article['content']
    doc = fromstring(body)
    tidy_content(doc)
    body = tostring(doc, encoding=str)

    author = article['author']['name']
    # 用户的urlToken
    people = article['author']['urlToken']
    # 文章和回答的标题获取方式不一样
    title = ''
    if post_type == 'articles':
        title = article['title']
        # 文章题图
        title_image = article['titleImage']
        body = article_title_image.format(title_image) + body
    else:
        title = article['question']['title']
        # 文件名：暂时设置为：问题id-回答id
        id = str(article['question']['id']) + '-' +id

    path = os.path.abspath('.')
    path = os.path.join(path,'static_files_backup')
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path,(str(id)+'.html')),'w') as f:
        f.write(page_template.format_map(vars()))


def main(argv):
    # 两种可能，文章或回答
    pattern_ans = r'https://www.zhihu.com/question/\d+/answer/(\d+)'
    pattern_article = r'https://zhuanlan.zhihu.com/p/(\d+)'
    res = re.match(pattern_ans,argv[0])
    post_type = ''
    if res:
        post_type = "answers"
    else:
        res = re.match(pattern_article, argv[0])
        post_type = "articles"
    static(argv[0],post_type,res.group(1))


if __name__ == '__main__':
    main(sys.argv[1:])
