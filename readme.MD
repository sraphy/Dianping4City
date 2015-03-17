点评数据获取及处理介绍
==================
# 1、数据获取流程
## 1.1 宁波规划区全部餐饮POI获取
    getNBplandistRestaurants()
    其它区域替换时需要替换下列url中g101以后部分
    lgurl = 'http://www.dianping.com/search/category/11/10/g101r8' + str(m) + 'p' + str(i)
    上面的url中，r80为海曙,江东81,江北82,鄞州83
    p{d}为第d页
    本方法将获得规划区全部的餐馆及其具体的url。数据结构为:
    NAME    URL
    
##1.2 获得单个POI的具体信息（不包含地理坐标）
    getSingleShopInfo
    输入参数: shop的url, file对象
    输出:
    NAME    人均消费    口味评分    环境评分    服务评分    地址  LAT LNG URL
    
##1.3 设置每个POI的地理坐标
    使用高德地理编码工具
    setPOIGeo
    输出:
    NAME    人均消费    口味评分    环境评分    服务评分    地址  LAT LNG URL