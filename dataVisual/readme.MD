数据可视化
-----------------
1、生产数据
-----------------
我们现在可以生产两类数据：一是将nb_restaurant中的数据导出为csv格式，以形成当前状态下的宁波6区的餐厅分布位置图（包含各种有用的信息）
二是可以在sqlite中执行以下SQL语句（从2008至2015）：

    create view nb_rest_score_2015
    as
    select * from nb_restaurant_score_by_year_name where REC_DATE2='2015';
    
![hello world](pic/a.png)

将这些数据导出。见data文件夹。

2、可视化
--------------------
加载csv数据

![hello world](pic/QQ20150319-1.png)
注意横纵坐标的字段
![hello world](pic/QQ20150319-2.png)
选择4326为坐标系
![hello world](pic/QQ20150319-3.png)
加载OSM数据为底层地图，如果QGIS上没有这一菜单，请安装OpenLayers plugin插件
![hello world](pic/QQ20150319-4.png)
调整图层次序
![hello world](pic/QQ20150319-5.png)