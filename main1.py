#coding:utf-8
import re
import sys
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urlparse
import random

#读取给定网址内容（待读网址，用户抬头）
def get_urlContent(url,user_headers,content_replaces):
    '''读取给定网址的指定内容及下一待读取网址'''

    #清空内容，以便多次读取
    urlContent=[]

    #定义网址打开错误尝试次数为5次以内
    i_try=0
    while i_try<5:
        #超时重连机制
        try:
            #定义超时时间（连接，读取）
            url_res=requests.get(url=url, headers=user_headers,timeout=(5,10))
            url_res.encoding='gbk'

            #如果错误，抛出异常，停止程序；否则无动作
            url_res.raise_for_status()
            #创建对象
            novel_soup=BeautifulSoup(url_res.text,features='html.parser')
            #获取title标签内容-标题
            novel_section_name = novel_soup.title.string
            #print(novel_section_name)

            #判断是否检索到id='nrl'。如有，
            if novel_soup.select('#nr1'):
                #假设需要的内容是检索到的第1个对象
                novel_section_content=novel_soup.select('#nr1')[0].get_text()
            #如无，提示该网址未检索到内容
            else:
                novel_section_content =url+'未检索到内容'


            #判断是否检索到id='nrl',类='fy'。如有，
            if novel_soup.select('#nr1 .fy'):
                content_replace_3 = novel_soup.select('#nr1 .fy')[0].get_text()
                novel_section_content=novel_section_content.replace(content_replace_3,'')

            #指定内容文本替换
            #content_replace_1=' '
            #content_replace_2=' '

            #novel_section_content=novel_section_content.replace(content_replace_1,'').replace(content_replace_2,'').replace(u'\xa0','')

            # 指定内容文本替换为空
            if content_replaces:
                for content_replace in content_replaces:
                    novel_section_content = novel_section_content.replace(content_replace, '')


            #print(content_replace_3)
            #print(novel_section_content)
            #novel_section_content=novel_section_content.replace("<br />","\n")
            #novel_section_content=re.sub( '\s+', '\r\n\t', novel_section_content).strip('\r\n')

            url_type='www.biqugetv.com'
            #自动判断识别

            #读取下一章节页的网址，第1个id='pb_next'的对象的href的值
            url_next_chapter = novel_soup.select('#pb_next')[0]['href']
            #print(url_next_chapter)

            #将下一章网址赋值给下一网址
            url_next_link = url_next_chapter

            #读取下一网址所在对象，并用for循环根据其内容是否是'下一页'判断所需的网址，读取其href的值
            url_next_pages = novel_soup.select('#nr1 .fy a')
            for url_next_page in url_next_pages:
                #print('hello')
                if url_next_page.get_text() == '下一页':
                    url_next_link = url_next_page['href']
                    break

            #将读取到的内容写入列表，并反馈
            urlContent.append(novel_section_name)
            urlContent.append(novel_section_content)
            urlContent.append(url_next_link)
            return urlContent

        except requests.exceptions.RequestException:
            i_try+=1

def txt_name(txt_name_num):
    '''随机生成文件名称'''
    def_j = txt_name_num
    txt_name_pre = []
    # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    txt_name_pre = ''.join(str(def_i) for def_i in random.sample(range(0, 9), def_j))
    txt_name=txt_name_pre+'.txt'
    #print(type(txt_name))
    return txt_name

def write_txt(contents,txt_name):
    '''写入TXT文件'''
    #写入地址
    save_path='E:\\STUDYing\\PYTHON\\PycharmProjects\\novelmy\\test'
    #写入名称
    save_name=txt_name
    save_fullpath=os.path.join(save_path,save_name)
    with open(save_fullpath,'a',encoding='utf-8') as f:
        #f.write(contents+'\n'+'\n')
        f.write(contents)

#def get_nexturl(lasturl)

#当前为主函数时，
if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    user_headers = {'User-Agent': user_agent}
    #print(user_headers)

    #直输整个列表，删除重复地址，并保持原来排序
    url_novels_unset = list(input('请输入小说网址,可多个,以","为分隔符:').split(','))
    url_novels = list(set(url_novels_unset))
    url_novels.sort(key=url_novels_unset.index)
    print(url_novels,'\n')

    if not url_novels:
        print('无小说抓取')
        exit()

    #print('检查以下程序是否被执行')

    # 依次输入小说网址，以STOP或直接回车结束
    # url_novels = []
    # url_novel_input_stop = ['stop', '']
    # while True:
    #     url_novel_input = input('请输入小说网址\n')
    #     if url_novel_input.lower() in url_novel_input_stop:
    #         break
    #     elif url_novel_input not in url_novels:
    #         url_novels.append(url_novel_input)
    #     else:
    #         print('地址重复，请重新输入，或结束输入或直接回车')
    #     print(url_novels)

    #直输整个替换列表，删除重复内容，并保持原来排序
    content_replaces_unset = list(input('请输入替换内容,可多个,以","为分隔符:').split(','))
    content_replaces = list(set(content_replaces_unset))
    content_replaces.sort(key=content_replaces_unset.index)
    print(content_replaces,'\n')

    for url_novel in url_novels:
        if url_novel:
            #待读取的网址
            #url_novel = 'www.163.com'
            #print(url_novel)
            #获取次末级网址
            last_url=url_novel[0:url_novel.rfind('/', 1) + 1]
            print(last_url)
            #获取域名
            pre_url = urlparse(url_novel).scheme+'://'+urlparse(url_novel).netloc
            #产生一个5位的文件名
            txt_name=txt_name(5)
            #用i来记录读取次数
            i=1
            while True:
                print(url_novel)
                #调用读取函数
                novel_all=get_urlContent(url_novel,user_headers,content_replaces)
                #print(novel_all[0])
                #print(novel_all[1])
                #print(type(novel_all[1]))
                #print(novel_all[2])

                # 调用写入函数，写入章节号
                # novel_section_no='第'+str(i)+'节'
                novel_section_no = '第 %d 节\n' % (i)
                write_txt(novel_section_no, txt_name)
                #调用写入函数，写入内容
                write_txt(novel_all[1],txt_name)
                print(i)
                print(novel_all[2])
                #print('kuhong' in novel_all[2])
                #判断，当下一页网址跳回至根目录时，结束。否则继续。
                if (pre_url+novel_all[2] == last_url):
                    break
                if(pre_url not in novel_all[2]):
                    url_novel=pre_url+novel_all[2]
                else:
                    url_novel=novel_all[2]
                i+=1
                #if i==5:
                    #break
        else:
            pass