#!/usr/bin/env python
# encoding=utf-8

import json
import requests
import xlwt
import time
from lxml import etree
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.request
import sys


def get_information(url,lid,ka):
    ua = UserAgent()
    my_headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        #'Referer': 'https://www.zhipin.com/job_detail/?query=&scity=101010100&industry=&position='  # ,
        # ':authority':'www.zhipin.com',
        # ':method':'GET',
        # ':path':urlparams,
        # ':scheme':'https'
    }
    cookies = {
        'Cookie': 'sid=sem_pz_bdpc_dasou_title; lastCity=101010100; JSESSIONID=""; __c=1528099446; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%26oq%3Djson%2525E6%2525A0%2525BC%2525E5%2525BC%25258F%2525E5%25258C%252596%26rsv_pq%3Dcf1bef1e00038c57%26rsv_t%3D258crJXHMaljaz7Hj%252F5fWVxOquzrvxEk4z7Fq0X%252FZqF4Arqb1WT0vR1ji8s%26rqlang%3Dcn%26rsv_enter%3D1%26inputT%3D5160%26rsv_sug3%3D25%26rsv_sug1%3D27%26rsv_sug7%3D100%26bs%3Djson%25E6%25A0%25BC%25E5%25BC%258F%25E5%258C%2596&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1526545770,1528099446; t=hG8BDFFw2hVoU7as; wt=hG8BDFFw2hVoU7as; __a=47029706.1526545768.1526545768.1528099446.45.2.44.44; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1528104487'
    }

    time.sleep(2)

    datas = {
        'ka': ka,
        'lid': lid
    }
    urllast='https://www.zhipin.com/%(url)s?ka=%(ka)s&lid=%(lid)s' % {'url': url,'ka':ka,'lid':lid}
    content = requests.post(url=urllast, cookies=cookies,headers=my_headers, data=datas)
    # print(content.text)
    soup = BeautifulSoup(content.text, 'lxml')
    information = []
    for temp in soup.find_all('div', class_='job-sec'):
        if temp.h3.string=='工商信息':
            #print(temp)
            information.append(temp.find('div',class_='name').string)  # 公司名称-企查查
            information.append(temp.find('li',class_='res-time').get_text().replace('成立时间：',''))  # 成立时间
            information.append(temp.find('li', class_='company-type').get_text().replace('企业类型：',''))  # 企业类型
            information.append(temp.find('li', class_='manage-state').get_text().replace('经营状态：',''))  # 经营状态
            information.append(temp.find_all('li')[0].get_text().replace('法人代表：',''))  # 法人代表
            information.append(temp.find_all('li')[1].get_text().replace('注册资金：',''))  # 注册资金
            #print(information)
    return information


    # 获取存储职位信息的json对象，遍历获得公司名、福利待遇、工作地点、学历要求、工作类型、发布时间、职位名称、薪资、工作年限
def get_json(urlparams, datas):
    ua = UserAgent()
    my_headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.zhipin.com/job_detail/?query=&scity=101010100&industry=&position='#,
        #':authority':'www.zhipin.com',
        #':method':'GET',
        #':path':urlparams,
        #':scheme':'https'
    }
    cookies = {
        'Cookie': 'sid=sem_pz_bdpc_dasou_title; lastCity=101010100; JSESSIONID=""; __c=1528099446; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%26oq%3Djson%2525E6%2525A0%2525BC%2525E5%2525BC%25258F%2525E5%25258C%252596%26rsv_pq%3Dcf1bef1e00038c57%26rsv_t%3D258crJXHMaljaz7Hj%252F5fWVxOquzrvxEk4z7Fq0X%252FZqF4Arqb1WT0vR1ji8s%26rqlang%3Dcn%26rsv_enter%3D1%26inputT%3D5160%26rsv_sug3%3D25%26rsv_sug1%3D27%26rsv_sug7%3D100%26bs%3Djson%25E6%25A0%25BC%25E5%25BC%258F%25E5%258C%2596&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1526545770,1528099446; t=hG8BDFFw2hVoU7as; wt=hG8BDFFw2hVoU7as; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1528101606; __a=47029706.1526545768.1526545768.1528099446.37.2.36.36'
    }
    time.sleep(10)
    #time.sleep(20 + random.randint(0, 20))
    content = requests.post(url='https://www.zhipin.com%(urlparams)s'%{'urlparams':urlparams}, cookies=cookies, headers=my_headers, data=datas)
    # content.encoding = 'utf-8'
    result = content.text
    #print(result)
    soup = BeautifulSoup(result, 'lxml')
    info_list = []
    for temp in soup.find_all('div',class_='info-primary'):
        url=temp.a.get('href')
        lid=temp.a.get('data-lid')
        ka=temp.a.get('ka')
        information=get_information(url,lid,ka)
        info_list.append(information)
    # print info
    return info_list


def main():
    #page = int(input('输入抓取页数:'))
    page = 2
    # kd = raw_input('请输入你要抓取的职位关键字：')
    # city = raw_input('请输入你要抓取的城市：')
    info_result = []
    title = ['公司全名-企查查', '成立时间', '企业类型', '经营状态', '法人代表', '注册资金']
    info_result.append(title)
    for x in range(1, page + 1):
        try:
            print('page:%(vv)d 开始:'%{'vv':x})
            url = '/c101010100/h_101010100/?page=%(index)d&sort=2&ka=page-%(index)d'%{'index':x}
            datas = {
                'page':x,
                'sort':2,
                'ka':'page-%(index)d'%{'index':x}
            }
            info = get_json(url, datas)
            if len(info)==0:
                break
            info_result = info_result + info
            print('info_result lengths:%(len)d ,info lengths:%(leninfo)d , page:%(vv)d 结束.' % {'len':len(info_result), 'leninfo':len(info), 'vv': x})
        except:
            break;

    # 创建workbook,即excel
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建表,第二参数用于确认同一个cell单元是否可以重设值
    worksheet = workbook.add_sheet('lagouzp', cell_overwrite_ok=True)
    for i, row in enumerate(info_result):
        # print row
        for j, col in enumerate(row):
            # print col
            worksheet.write(i, j, col)
    workbook.save('d:\\boss.xls')


if __name__ == '__main__':
    main()
