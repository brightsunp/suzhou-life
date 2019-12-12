#!/usr/bin/python
# coding=utf-8
"""
__author__ = 'sunp'
__date__ = '11/7/2019'
"""
import datetime

today = datetime.date.today().strftime('%Y%m%d')
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
data_file = 'data\\data.csv'

headers = ['Date', 'Daxia', 'Denn', 'Bo', 'HTP', 'JX', 'Lian', 'Linq',
           'Man', 'Monkey', 'TP', 'Six', 'XJ', 'XZ', 'Yi', 'consume', 'pool']
non_players = headers[-2:]
display_names = {'Daxia': '夜雨', 'XJ': '爱屋及乌', 'XZ': '48', 'Six': '铁头鱼',
                 'Yi': '公仔', 'JX': '小董', 'Denn': '尼斯哥', 'Bo': '思念'}
study_abroad = []

green_colors = ['#24b292', '#0a6955', '#0b5846', '#073c32', '#71cab5',
                '#1e9473', '#2fefb3', '#2fa591', '#17856f', '#148588', '#34e4ba']
red_colors = ['#DB4D6D', '#F596AA', '#F4A7B9', '#F8C3CD', '#8E354A',
              '#E16B8C', '#D0104C', '#D05A6E', '#E87A90', '#EB7A77', '#CB1B45']
yellow_color = '#C7802D'
