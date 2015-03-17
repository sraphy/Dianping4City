# _*_ coding: utf-8 _*_

from urllib2 import *
import json


class baiduMapService:
	## 百度地图Place服务详见http://developer.baidu.com/map/webservice-placeapi.htm
	## 如果要返回多条数据，调整url中的pagesize和pagenum
	def __init__(self, key):
		self.key = key

	def getPlaceByNameBounds(self, searchText, bounds, start, end):
		"""
		根据模糊地名和矩形范围获得地名详情
		:param searchText: 查询文本
		:param bounds: 查新范围
		:param start: 起始页
		:param end: 终止页
		"""
		for i in range(start, end):
			## 每页查询20个POI
			url = 'http://api.map.baidu.com/place/v2/search?&query=' + searchText + \
			      '&bounds=' + bounds + '&output=json&ak=' + self.key + '&page_size=20&page_num=' + str(i)
			req = urlopen(url).read()
			# print req
			res = json.loads(req)
			for poi in res["results"]:
				info = poi["name"] + "\t" + poi["address"] + "\t" + str(poi["location"]["lat"]) + "\t" + str(
					poi["location"]["lng"]) + "\t" + poi["uid"]
				print info


	def getPlaceByNameRegion(self, searchText, region, start, end):
		"""
		根据模糊地名和所在城市（市、县）获得地名详情
		:param searchText: 查询文本
		:param region: POI所在区域，只到市级
		:param start: 起始页
		:param end: 终止页
		"""
		for i in range(start, end):
			url = 'http://api.map.baidu.com/place/v2/search?&query=' + searchText + \
				    '&region=' + region + '&output=json&ak=' + self.key + '&page_size=20&page_num=' + str(i)
			req = urlopen(url).read()
			# print req
			res = json.loads(req)
			for poi in res["results"]:
				info = poi["name"] + "\t" + poi["address"] + "\t" + str(poi["location"]["lat"]) + "\t" + str(
					poi["location"]["lng"]) + "\t" + poi["uid"] + "\t"
				print info

	def getPlaceByNameLocation(self, searchText, location, radius , start, end):
		"""
		根据模糊地名，中心点坐标和半径获得地名详情
		:param searchText:
		:param location:
		:param radius:
		"""
		for i in range(start, end):
			url = 'http://api.map.baidu.com/place/v2/search?&query=' + searchText + \
			      '&location=' + location + '&radius=' + str(radius) + \
			      '&output=json&ak=' + self.key + '&page_size=20&page_num=' + str(i)
			req = urlopen(url).read()
			# print req
			res = json.loads(req)
			for poi in res["results"]:
				info = poi["name"] + "\t" + poi["address"] + "\t" + str(poi["location"]["lat"]) + "\t" + str(
					poi["location"]["lng"]) + "\t" + poi["uid"]
				print info

	def getPlaceDetail(self, uid):
		"""
		根据地名的uid检索其详细信息
		:param uid:
		"""
		url = 'http://api.map.baidu.com/place/v2/detail?&uid=' + uid + \
		      '&output=json&scope=2&ak=' + self.key
		req = urlopen(url).read()
		# print req
		res = json.loads(req)
		poi = res["result"]
		info = poi["name"] + "\t" + poi["address"] + "\t" + str(poi["location"]["lat"]) + "\t" + str(
			poi["location"]["lng"]) + "\t" + poi["uid"] + "\t" + poi["detail_info"]["tag"]
		print info

	def baiduGeocoder(self, placename):
		"""
		百度地理编码器
		:param placename:
		"""
		url = 'http://api.map.baidu.com/geocoder/v2/?address=' + placename + '&output=json&ak=' + self.key + '&callback=showLocation'
		req = urlopen(url).read()
		text = req[27:-1]
		res = json.loads(text)
		poi = res["result"]
		info = str(poi["precise"]) + '\t' + str(poi["confidence"]) + '\t' + poi["level"] + '\t' + str(
			poi["location"]["lat"]) + "\t" + str(poi["location"]["lng"])
		print info
		return str(poi["location"]["lat"]) + "\t" + str(poi["location"]["lng"])

	def baiduDecoder(self, location):
		"""
		百度反地理编码器
		:param location:
		"""
		url = 'http://api.map.baidu.com/geocoder/v2/?ak=' + self.key + '&callback=renderReverse&location=' + location + '&output=json&pois=1'
		req = urlopen(url).read()
		text = req[29:-1]
		res = json.loads(text)
		pois = res["result"]
		info = pois["formatted_address"]
		print info
		for poi in pois["pois"]:
			print   poi["addr"] + '\t' + poi["name"]

	def gaodeGeoCoder(self, placename):
		url = 'http://restapi.amap.com/v3/place/text?keywords=' + placename + '&key=c84af8341b1cc45c801d6765cda96087&offset=15&page=1&city=021&callback=jsonp'
		url = url.replace('%20', '').replace(' ', '')
		# print url
		req = urlopen(url).read()
		# print req
		res = json.loads(req[6:-1])
		loc = res['pois'][0]['location']
		# print loc,res['pois'][0]['name']
		return loc.split(',')[1] + '\t' + loc.split(',')[0]

	def gaodeGeoCoder2(self, address, districtcode):
		url = 'http://restapi.amap.com/v3/geocode/geo?address='+address+\
		      '&key=a2c256158f9d95cfdcff434dfc966e6f&s=rsv3&city='+ districtcode+'&callback=_61985_'
		url = url.replace('%20', '').replace(' ', '')
		# print url
		req = urlopen(url).read()
		res = json.loads(req[8:-1])
		# print res
		try:
			loc = res['geocodes'][0]['location']
			return loc.split(',')[1] + '\t' + loc.split(',')[0]
		except:
			return '0\t0'