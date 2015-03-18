点评数据获取及处理介绍
==================
    本例基于python语言编写而成
    在运行时如遇到包缺失等问题,请安装相应的library
# 1、数据获取流程
    数据获取dataretrieval代码可以在dataRetr文件夹的getNBRestaurants.py中获得
## 1.0 初始化
    代码：
    app = DianpingCity()
	app.dbinit()
执行该代码后，dataRetr中将出现一个nbrestaurants.db的sqlite数据库，其中有2个数据表:
    nb_restaurant : 负责记录每个POI的信息
    nb_restaurant_score : 负责记录每个POI对应的评论信息

## 1.1 宁波规划区全部餐饮POI获取
    app.getNBplandistRestaurants()
执行改代码后，宁波规划区范围的餐饮店名称及对应URL被保存到nb_restaurant表中

    其它区域替换时需要替换下列url中g101以后部分
    lgurl = 'http://www.dianping.com/search/category/11/10/g101r8' + str(m) + 'p' + str(i)
    上面的url中，r80为海曙,江东81,江北82,鄞州83
    p{d}为第d页
    
##1.2 获得单个POI的具体信息（不包含地理坐标）
    app.getSingleShopInfo()
执行改代码后，宁波规划区范围的餐饮店的点评数量、平均消费、口味评分、环境评分、服务评分和地址被保存到nb_restaurant表中
    
##1.3 设置每个POI的地理坐标
    使用高德地理编码工具
    app.setPOIGeo()
执行改代码后，宁波规划区范围的餐饮店的地理坐标被保存到nb_restaurant表中

##1.4 设置WGS84坐标
    setWGS84()
    为数据表中的LAT84和LNG84添加上对应的值。
    高德的坐标为GCJ02
    
##1.5 获得每个POI的点评数值
    getSingleShopComment()
    获得每个POI的记录时间、用户打分、口味评分、环境评分、服务评分

    在sqlite数据库中执行以下命令，生成一个视图
    create view nb_restaurant_score_by_year
    AS
    select pk, REC_DATE2, avg(SCORE) as avg_score , avg(TAS) as avg_tas ,avg(ENV) as avg_env ,avg(SER) as avg_ser from
     nb_restaurant_score group by pk, REC_DATE2;
    视图中将会按POI的年份展示用户打分、口味评分、环境评分、服务评分