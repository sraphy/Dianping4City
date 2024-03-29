# _*_ coding: utf-8 _*_
import urllib2
import cookielib
import sys
import json
from BeautifulSoup import *
from sqlalchemy import *
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## 本代码用于从点评网中抽取出宁波规划区范围[鄞州、海曙、江东、江北]的餐饮业数据
## http://www.dianping.com/search/category/11/10/g101r80p2
## 上面的url中，r80为海曙,江东81,江北82,鄞州83
from webutil import baiduMapService

Base = declarative_base()
engine = create_engine('sqlite:///dpshops/nbrestaurants.db', echo=True)


class POI(Base):
	# 表的名字:
	__tablename__ = 'nb_restaurant'

	# 表的结构:
	id = Column(Integer, primary_key=True)
	NAME = Column(String(40))
	COM_COUNT = Column(Integer)
	AVE_PRICE = Column(Float(precision=2))
	TAS_SCORE = Column(Float(precision=2))
	ENV_SCORE = Column(Float(precision=2))
	SER_SCORE = Column(Float(precision=2))
	LAT = Column(Float(precision=8))
	LNG = Column(Float(precision=8))
	LAT84 = Column(Float(precision=8))
	LNG84 = Column(Float(precision=8))
	ADDR = Column(String(100))
	URL = Column(String(100))

class POI_SCORE(Base):
	__tablename__ = 'nb_restaurant_score'

	id = Column(Integer, primary_key=True)
	pk = Column(Integer)
	SCORE = Column(Integer)
	TAS = Column(Integer)
	ENV = Column(Integer)
	SER = Column(Integer)
	REC_DATE = Column(Date)
	REC_DATE2 = Column(String(12))

class DianpingCity():

	def dbinit(self):
		Base.metadata.create_all(engine)
		print '数据库初始化成功'

	def getNBplandistRestaurants(self):
		cookie = cookielib.CookieJar()
		cookie_handler = urllib2.HTTPCookieProcessor(cookie)
		###有些网站反爬虫，这里用headers把程序伪装成浏览器
		hds = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}

		DBSession = sessionmaker()
		DBSession.configure(bind=engine)
		session = DBSession()
		#
		discode = ['80''81','82','83','417','3949']
		for m in discode:
			for i in range(1, 51):
				lgurl = 'http://www.dianping.com/search/category/11/10/g101r' + str(m) + 'p' + str(i)
				req = urllib2.Request(url=lgurl, headers=hds)  # 伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
				opener = urllib2.build_opener(cookie_handler)  # 绑定handler，创建一个自定义的opener
				try:
					response = opener.open(req)  # 请求网页，返回句柄
					page = response.read()  # 读取并返回网页内容

					soup = BeautifulSoup(page)
					shops = soup.findAll('a', {'data-hippo-type': 'shop'})
					for shop in shops:
						poi = POI()
						poi.NAME = shop['title']
						poi.URL = 'http://www.dianping.com' + shop['href']
						session.add(poi)

					print '---------' + str(m) + '------' + str(i) + '-----------------'
				except Exception, e:
					print e
					break
			session.flush()
			session.commit()
		print 'OK'

	def getSingleShopInfo(self):
		cookie = cookielib.CookieJar()
		cookie_handler = urllib2.HTTPCookieProcessor(cookie)
		###有些网站反爬虫，这里用headers把程序伪装成浏览器
		hds = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
		opener = urllib2.build_opener(cookie_handler)

		DBSession = sessionmaker()
		DBSession.configure(bind=engine)
		session = DBSession()
		query = session.query(POI).filter(POI.ADDR == None )

		try:
			for obj in query:
				print obj.NAME

				req = urllib2.Request(url=obj.URL, headers=hds)  # 伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
				response = opener.open(req)  # 请求网页，返回句柄
				page = response.read()  # 读取并返回网页内容
				soup = BeautifulSoup(page)
				try:
					COM_COUNT = 0
					AVE_PRICE = 0.0
					TAS_SCORE = 0.0
					ENV_SCORE = 0.0
					SER_SCORE = 0.0

					scores = soup.findAll('span', {'class': 'item'}, limit=5)
					if str(scores[0].text).find('评论')>0:
						tag = scores[0].text.find('条')
						COM_COUNT = int(scores[0].text[0:tag ])
						AVE_PRICE_str = scores[1].text
						if AVE_PRICE_str.split('：')[1]<> '-':
							AVE_PRICE = float(AVE_PRICE_str.split('：')[1][:-1])
						TAS_SCORE_str = scores[2].text
						if TAS_SCORE_str.split('：')[1]<> '-':
							TAS_SCORE = float(TAS_SCORE_str.split('：')[1])
						ENV_SCORE_str = scores[3].text
						if ENV_SCORE_str.split('：')[1]<> '-':
							ENV_SCORE = float(ENV_SCORE_str.split('：')[1])
						SER_SCORE_str = scores[4].text
						if SER_SCORE_str.split('：')[1]<> '-':
							SER_SCORE = float(SER_SCORE_str.split('：')[1])
					else:
						AVE_PRICE_str = scores[0].text
						if AVE_PRICE_str.split('：')[1]<> '-':
							AVE_PRICE = float(AVE_PRICE_str.split('：')[1][:-1])
						TAS_SCORE_str = scores[1].text
						if TAS_SCORE_str.split('：')[1]<> '-':
							TAS_SCORE = float(TAS_SCORE_str.split('：')[1])
						ENV_SCORE_str = scores[2].text
						if ENV_SCORE_str.split('：')[1]<> '-':
							ENV_SCORE = float(ENV_SCORE_str.split('：')[1])
						SER_SCORE_str = scores[3].text
						if SER_SCORE_str.split('：')[1]<> '-':
							SER_SCORE = float(SER_SCORE_str.split('：')[1])

					address = soup.find('span', {'itemprop': 'street-address'})
					print obj.id
					query.filter(POI.id == obj.id).update({'ADDR':'宁波市'+address.text,'COM_COUNT':COM_COUNT, 'AVE_PRICE':AVE_PRICE,
					                                       'TAS_SCORE':TAS_SCORE, 'ENV_SCORE':ENV_SCORE,
					                                       'SER_SCORE':SER_SCORE})

				except Exception , e:
					# session.commit()
					print e
			session.flush()
			session.commit()
		except Exception,e:
			print e
			session.flush()
			session.commit()

	def setPOIGeo(self, service):
		DBSession = sessionmaker()
		DBSession.configure(bind=engine)
		session = DBSession()
		query = session.query(POI).filter(POI.LAT == None )

		for obj in query:
			print obj.ADDR
			latlng = service.gaodeGeoCoder2(obj.ADDR, '0574')
			query.filter(POI.id == obj.id).update({'LAT':latlng.split('\t')[0], 'LNG':latlng.split('\t')[1]})

		session.flush()
		session.commit()
		print 'OK'

	def setWGS84(self):
		DBSession = sessionmaker()
		DBSession.configure(bind=engine)
		session = DBSession()
		query = session.query(POI).filter(POI.LAT84 == None )

		for obj in query:
			print obj.NAME
			try:
				req = urllib2.urlopen('http://api.zdoz.net/gcj2wgs.aspx?lat='+ str(obj.LAT)+'&lng='+str(obj.LNG)).read()
				print 'http://api.zdoz.net/gcj2wgs.aspx?lat='+ str(obj.LAT)+'&lng='+str(obj.LNG)
				latlng = json.loads(req)
				query.filter(POI.id == obj.id).update({'LAT84':latlng['Lat'], 'LNG84':latlng['Lng']})
			except:
				session.flush()
				session.commit()
				continue

		session.flush()
		session.commit()

	def getSingleShopComment(self):
		DBSession = sessionmaker()
		DBSession.configure(bind=engine)
		session = DBSession()
		query1 = session.query(POI).filter(POI.COM_COUNT>0 )
		query = query1.filter(POI.id>2165)

		cookie = cookielib.CookieJar()
		cookie_handler = urllib2.HTTPCookieProcessor(cookie)
		###有些网站反爬虫，这里用headers把程序伪装成浏览器
		hds = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
		opener = urllib2.build_opener(cookie_handler)

		for obj in query:
			print obj.NAME
			# m = int(obj.COM_COUNT/20)+2
			for i in range(1, 101):
				try:
					url = obj.URL+'/review_all?pageno='+str(i)
					print url
					req = urllib2.Request(url=url, headers=hds)  # 伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
					response = opener.open(req)  # 请求网页，返回句柄
					page = response.read()  # 读取并返回网页内容
					soup = BeautifulSoup(page)
					scores = soup.findAll('div', {'class': 'content'})
					if len(scores)==0:
						break
					for score in scores:
						poiscore = POI_SCORE()
						poiscore.pk = obj.id
						dt = score.find('span', {'class':'time'}).text[0:11].replace('&nbsp;','').replace('&nb','')
						if len(dt)==5:
							poiscore.REC_DATE2 = '2015'
						else:
							poiscore.REC_DATE2 = '20'+dt[:2]
						rsts = score.findAll('span', {'class':'rst'})
						if len(rsts)==3:
							poiscore.TAS = rsts[0].text[2:3]
							poiscore.ENV = rsts[1].text[2:3]
							poiscore.SER = rsts[2].text[2:3]
						elif len(rsts)==0:
							continue
						else:
							poiscore.TAS = rsts[1].text[2:3]
							poiscore.ENV = rsts[2].text[2:3]
							poiscore.SER = rsts[3].text[2:3]
						# for rst in rsts:
						# 	print rst.text[2:3]
						star = str(score.find('span',{'title':''})).split('irr-star')[1][:2]
						poiscore.SCORE = int(star)/10
						session.add(poiscore)
				except Exception,e :
					# session.flush()
					# session.commit()
					print e
					continue
			session.flush()
			session.commit()

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	sys.getfilesystemencoding()

	## 数据库初始化, 在程序中只需要执行一次
	app = DianpingCity()
	# app.dbinit()
	## 获得宁波规划区的所有餐饮POI名称
	# app.getNBplandistRestaurants()
	# app.getSingleShopInfo()

	## 将每个POI的空间坐标添加上去
	# service = baiduMapService('CBf77b6c299fe052b8d9e869438c6301')
	# app.setPOIGeo(service)

	## 将GJC02坐标转化为WGS84坐标
	# app.setWGS84()
	app.getSingleShopComment()

