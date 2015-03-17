# _*_ coding: utf-8 _*_
import urllib2
import cookielib
import sys
from BeautifulSoup import *






## 本代码用于从点评网中抽取出宁波规划区范围[鄞州、海曙、江东、江北]的餐饮业数据
## http://www.dianping.com/search/category/11/10/g101r80p2
## 上面的url中，r80为海曙,江东81,江北82,鄞州83
from webutil import baiduMapService


def getNBplandistRestaurants():
	cookie = cookielib.CookieJar()
	cookie_handler = urllib2.HTTPCookieProcessor(cookie)
	###有些网站反爬虫，这里用headers把程序伪装成浏览器
	hds = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}

	f = open('dpshops/nb_restaurants0.dat', "a")
	for m in range(0, 4):
		for i in range(1, 51):
			lgurl = 'http://www.dianping.com/search/category/11/10/g101r8' + str(m) + 'p' + str(i)
			req = urllib2.Request(url=lgurl, headers=hds)  # 伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
			opener = urllib2.build_opener(cookie_handler)  # 绑定handler，创建一个自定义的opener
			try:
				response = opener.open(req)  # 请求网页，返回句柄
				page = response.read()  # 读取并返回网页内容

				soup = BeautifulSoup(page)
				shops = soup.findAll('a', {'data-hippo-type': 'shop'})
				for shop in shops:
					info = shop['title'] + '\t' + 'http://www.dianping.com' + shop['href']
					f.write(info + '\n')
				print '---------' + str(m) + '------' + str(i) + '-----------------'
			except:
				continue

	f.close()
	print 'OK'


def getSingleShopInfo(url, f):
	cookie = cookielib.CookieJar()
	cookie_handler = urllib2.HTTPCookieProcessor(cookie)
	###有些网站反爬虫，这里用headers把程序伪装成浏览器
	hds = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
	req = urllib2.Request(url=url, headers=hds)  # 伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
	opener = urllib2.build_opener(cookie_handler)
	response = opener.open(req)  # 请求网页，返回句柄
	page = response.read()  # 读取并返回网页内容

	shopinfo = ''
	soup = BeautifulSoup(page)
	name = soup.find('h1', {'class': 'shop-name'})
	shopinfo += name.contents[0].replace('\n', '').replace('\t','')
	shopinfo += '\t'
	try:
		scores = soup.findAll('span', {'class': 'item'}, limit=5)
		i = 0
		for score in scores:
			if i == 0:
				i = 1
				continue
			s = score.text.split('：')
			shopinfo = shopinfo + s[1] + '\t'
		address = soup.find('span', {'itemprop': 'street-address'})
		# print address.text
		shopinfo = shopinfo + '宁波' +address.text +'\t \t \t'+ url
		f.write(shopinfo)
		print shopinfo
	except:
		return

def setPOIGeo(service):
	f = open('dpshops/nb_restaurants1.dat')
	f2 = open('dpshops/nb_restaurants2.csv','a')
	for line in f.readlines():
		info = line.split('\t')
		print info[5]
		f2.write(info[0]+'\t'+info[1]+'\t'+info[2]+'\t'+info[3]+'\t'+info[4]+'\t'+info[5]+'\t'+service.gaodeGeoCoder2(info[5])+'\t'+info[8])
	f2.close()
	print 'OK'

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	sys.getfilesystemencoding()

	## 获得宁波规划区的所有餐饮POI名称
	# getNBplandistRestaurants()

	## 获取每个POI的具体信息
	# f = open('dpshops/nb_restaurants0.dat')
	# f2 = open('dpshops/nb_restaurants1.dat', "a")
	# f2.write('名称\t均价\t口味\t环境\t服务\t地址\tLat\tLng\tURL\n')
	# for line in f.readlines():
	# 	info = line.split('\t')
	# 	# print info[0]
	# 	getSingleShopInfo(info[1], f2)
	# f2.close()

	## 将每个POI的空间坐标添加上去
	service = baiduMapService('CBf77b6c299fe052b8d9e869438c6301')
	setPOIGeo(service)