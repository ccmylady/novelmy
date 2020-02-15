#coding:utf-8
import re
import sys
from bs4 import BeautifulSoup
import requests
import os

def get_urlContent(url,user_headers):
    urlContent=[]
    url_res=requests.get(url=url, headers=user_headers)
    url_res.encoding='gbk'
    url_res.raise_for_status()

    novel_soup=BeautifulSoup(url_res.text,features='html.parser')
    novel_section_name = novel_soup.title.string
    #print(novel_section_name)

    #novel_section_content=novel_soup.select('p')[0].text 'for www.kanunu8.com
    novel_section_content=novel_soup.select('.readcontent')[0].get_text()
    #print(novel_section_content)
    #novel_section_content=novel_section_content.replace("<br />","\n")
    #novel_section_content=re.sub( '\s+', '\r\n\t', novel_section_content).strip('\r\n')

    url_next_link = novel_soup.select('a#linkNext')[0]['href']

    urlContent.append(novel_section_name)
    urlContent.append(novel_section_content)
    urlContent.append(url_next_link)
    return urlContent

def write_txt(contents):
    save_path='E:\\STUDYing\\PYTHON\\PycharmProjects\\novelmy\\test'
    save_name='test.txt'
    save_fullpath=os.path.join(save_path,save_name)
    with open(save_fullpath,'a',encoding='utf-8') as f:
        f.write(contents+'\n'+'\n')

#def get_nexturl(lasturl)

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    user_headers = {'User-Agent': user_agent}
    #print(user_headers)
    url_novel = 'https://www.163.com'

    pre_url=url_novel[0:url_novel.rfind('/', 1) + 1]
    print(pre_url)
    i=1
    while True:
        print(url_novel)
        novel_all=get_urlContent(url_novel,user_headers)
        #print(novel_all[0])
        #print(novel_all[1])
        #print(type(novel_all[1]))
        #print(novel_all[2])
        write_txt(novel_all[1])
        print(i)
        #print(novel_all[2])
        #print('kuhong' in novel_all[2])
        if (novel_all[2] == pre_url):
            break
        if(pre_url not in novel_all[2]):
            url_novel=pre_url+novel_all[2]
        else:
            url_novel=novel_all[2]
        i+=1
        #if i==5:
            #break