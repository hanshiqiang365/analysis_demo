#author:hanshiqiang365

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random
from time import sleep
from openpyxl import Workbook
import datetime


h1 = {
	'Cookie': 'push_doumail_num=0; push_noty_num=0; __utma=30149280.1151507141.1691746479.1691838193.1691884263.3; __utmb=30149280.2.10.1691884263; __utmc=30149280; __utmv=30149280.26293; __utmz=30149280.1691746479.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1188941628.1691838193.1691838193.1691884263.2; __utmb=223695111.0.10.1691884263; __utmc=223695111; __utmz=223695111.1691838193.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=610164de88bfd1f6.1691838192.; _pk_ses.100001.4cf6=1; frodotk_db="476b96b00b85eedcd642c4102291cc94"; _vwo_uuid_v2=D9E118F4F6B78D49AA45E890651B60D83|f7399d09229b7a7906e386d7de9b51e3; __gads=ID=44e41150db843457-229c4d3ad1e200f5:T=1691884287:RT=1691884287:S=ALNI_Mb0FbtUn4Dl5XTVzWTi_bgHI2jyXw; __gpi=UID=00000c2be27ac58c:T=1691884287:RT=1691884287:S=ALNI_Mb-thWIP8vXox9B-gc1my-oFwNKdQ; __yadk_uid=X3aHdYAhG4sEH2yWtFmZSGWsvKkUwVcE; ll="118088"; __utmt=1; ap_v=0,6.0; ck=TvDm; dbcl2="262932835:S3nkDWyGCm4"; bid=bMogmzojhhM',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Host': 'movie.douban.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
	'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
	'Referer': 'https://movie.douban.com/subject/35267224/?from=showing',
	'Connection': 'keep-alive'
}

def trans_star(v_str):
	"""转换评论星级"""
	v_str = v_str[0]
	if v_str == 'allstar10':
		return '1'
	elif v_str == 'allstar20':
		return '2'
	elif v_str == 'allstar30':
		return '3'
	elif v_str == 'allstar40':
		return '4'
	elif v_str == 'allstar50':
		return '5'
	else:
		return '未知'

def get_short(v_movie_id):
	for page in range(1, max_page + 1):  # 爬取前n页
		requests.packages.urllib3.disable_warnings()
		url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=P&sort=new_score'.format(
			v_movie_id, (page - 1) * 20)
		response = requests.get(url, headers=h1, verify=False)
		#print(response.status_code)
		
		soup = BeautifulSoup(response.text, 'html.parser')
		reviews = soup.find_all('div', {'class': 'comment'})

		print('开始爬取第{}页，共{}条评论'.format(page, len(reviews)))
		sleep(random.uniform(1, 2))

		# 定义空列表用于存放数据
		user_name_list = []  # 评论者昵称
		star_list = []  # 评论星级
		time_list = []  # 评论时间
		ip_list = []  # 评论者ip属地
		vote_list = []  # 有用数
		content_list = []  # 评论内容
		for review in reviews:
			# 评论者昵称
			user_name = review.find('span', {'class': 'comment-info'}).find('a').text
			user_name_list.append(user_name)
			# 评论星级
			star = review.find('span', {'class': 'comment-info'}).find_all('span')[1].get('class')
			star = trans_star(star)
			star_list.append(star)
			# 评论时间
			time2 = review.find('span', {'class': 'comment-time'}).text.strip()
			print('评论时间：', time2)
			time_list.append(time2)
			# 评论者IP属地
			ip = review.find('span', {'class': 'comment-location'}).text
			ip_list.append(ip)
			# 有用数
			vote = review.find('span', {'class': 'votes vote-count'}).text
			vote_list.append(vote)
			# 评论内容
			content = review.find('span', {'class': 'short'}).text
			content = content.replace(',', '，').replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
			content_list.append(content)
		df = pd.DataFrame(
			{
				'页码': page,
				'用户名': user_name_list,
				'城市': ip_list,
				'评分': star_list,
				'评论': content_list,
				'评论时间': time_list,
				'有用数': vote_list,
			}
		)
		# 设置csv文件表头
		if os.path.exists(result_file):
			header = False
		else:
			header = True
		# 保存到csv文件
		df.to_csv(result_file, mode='a+', header=header, index=False, encoding='utf_8_sig')
		print('文件保存成功：', result_file)

#csv文件转存excel文件
def csv_to_xlsx_pd(sourcePath:str,savePath:str,encode='utf-8'):
    curr_time = datetime.datetime.now()
 
    f = open(sourcePath, 'r', encoding=encode)
    workbook = Workbook()
    worksheet = workbook.active
    workbook.title = 'sheet'
 
    for line in f:
        row = line.split(',')
        worksheet.append(row)
 
    workbook.save(savePath)
    curr_time2 = datetime.datetime.now()
    print(curr_time2-curr_time)

if __name__ == '__main__':
	# 电影id
	movie_id = '35556001'
	# 最大爬取页
	max_page = 10  # 最大为10页
	# 保存文件名
	result_file = '豆瓣短评_{}_前{}页.csv'.format(movie_id, max_page)
	# 如果csv文件存在，先删除之
	if os.path.exists(result_file):
		os.remove(result_file)
		print('结果文件存在，已删除: {}'.format(result_file))
	# 循环爬取短评
	get_short(movie_id) 

        #csv文件转存excel文件
	excel_file = '孤注一掷.xlsx'

	if os.path.exists(excel_file):
		os.remove(excel_file)

	csv_to_xlsx_pd(result_file, excel_file, 'utf-8')
