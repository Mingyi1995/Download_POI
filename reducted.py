#!/usr/bin/env python
# coding: utf-8
import json
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import shutil
import os

ak = input('输入百度api key: ')
category = input('输入POI类型: ')
coord_type = input('输入坐标类型: ')
location = input('输入中心点坐标，先纬度后经度用英文逗号分隔不要加空格: ')
location_name = input('输入中心点名字，例如复华小区: ')
radius = input('输入搜索半径(只写数字，单位为米): ')
try:
    os.stat('%s'%location_name)
except:
    os.mkdir('%s'%location_name)

j = 0
info = pd.DataFrame()
lat = []
lng = []
url = 'http://api.map.baidu.com/place/v2/search?query='+category+'&page_size=20&page_num='+str(j)+'&coord_type=coord_type'+coord_type+'&location='+location+'&radius='+radius+'&output=json&ak=' + ak
data = requests.get(url)
text = json.loads(data.text)
for k in range(len(text['results'])):
    lat.append(text['results'][k]['location']['lat'])
    lng.append(text['results'][k]['location']['lng'])
while len(text['results']) > 19:
    j += 1
    url = 'http://api.map.baidu.com/place/v2/search?query='+category+'&page_size=20&page_num='+str(j)+'&coord_type=coord_type'+coord_type+'&location='+location+'&radius='+radius+'&output=json&ak=' + ak
    data = requests.get(url)
    text = json.loads(data.text)
    for k in range(len(text['results'])):
        lat.append(text['results'][k]['location']['lat'])
        lng.append(text['results'][k]['location']['lng'])
else:pass
info['lat'] = lat
info['lng'] = lng
if len(info) > 0:
    info.to_csv('%s_%s.csv'%(location_name,category), sep=',',encoding='utf-8', index=False)
    geometry = [Point(xy) for xy in zip(info.lng, info.lat)]
    crs = {'init': 'epsg:4326'}
    info_geo = gpd.GeoDataFrame(info, crs=crs, geometry=geometry)
    del info_geo['lat']
    del info_geo['lng']
    info_geo.to_file('%s/%s_%s.shp'%(location_name,location_name,category), driver='ESRI Shapefile')
    print('下载完成')
else:
    print('搜索无记录')

