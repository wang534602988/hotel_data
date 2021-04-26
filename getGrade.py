# -*- coding: utf-8 -*-
#将各个数据整合为分数数据，用于之后的算法
#对于评论数据产生的分数，之后删除一些无意义属性（无意义属性经常是数值差异性过低的属性，该步骤仍然有待提高）
import csv
import os
import re

fileList = os.listdir('data/review')
filename0 = 'data/hotelList.csv'
filename1 = 'data/spot.csv'
filename2 = 'data/station.csv'
filename3 = 'data/restaurant.csv'
filename4 = 'data/shop.csv'
filename5 = 'data/Gprice.csv'
filename6 = 'data/Gspot.csv'
filename7 = 'data/Gstation.csv'
filename8 = 'data/Grestaurant.csv'
filename9 = 'data/Gshop.csv'
filename10 = 'data/Greview.csv'
filename11 = 'data/avarageSales.csv'


#评论文本处理
def txtSplit(txt):
    review = []
    result = re.sub(r'[很非常可最也超级。，特别或者就还以推荐挺\'\[\],!"a-zA-Z]*', '', str(txt))
    result = re.sub(r'[差]', '不好', result)
    result = re.sub(r'[(不错)(给力)新(繁华)(热情)赞]', '不好', result)
    result = result.split(' ')
    for item in result:
        if 4 >= len(item) >= 2:
            review.append(item)
    return review

def getCount(data):
    id = []
    count = []
    for row in data:
        id.append(int(row[0]))
        year = 2022- int(row[1][0:4])
        count_sum = int(row[12])
        count.append(count_sum/year)
    return list(dict(zip(id, count)).items())

def cla_price(data):
    price = []
    id = []
    grade = []
    pSum = 0
    for row in data:
        price.append(int(row[7]))
        id.append(int(row[0]))
        pSum = pSum + int(row[7])
    pArg = pSum / len(data)
    for i in price:
        grade.append(1 - i / pArg / 2)
    return list(dict(zip(id, grade)).items())


def cla_ard(data):
    fix = {}
    dSum = 0
    for row in data:
        if row[9][-2] == 'k':
            d = float(row[9][2:-2]) * 1000
        else:
            d = float(row[9][2:-1])
        dSum += d
        i = row[0]
        if i not in fix:
            fix[i] = []
        fix[i].append(d)
    dArg = dSum / len(data)
    for row in fix.items():
        check = [d <= dArg for d in row[1]]
        fix[row[0]] = sum(check) + 1
    gArg = sum(fix.values()) / len(fix.values())
    for row in fix.items():
        fix[row[0]] = row[1] / gArg / 2
    return list(fix.items())


def cla_review(data):
    id = []
    review = []
    for row in data:
        review.append(txtSplit(row[-1]))
        # print(row[-1])
        id.append(row[0])
    mix = dict(zip(id, review))
    # 获取常见标签
    word = []
    for line in review:
        word = word + line
    count = {}
    for i in word:
        if count.__contains__(i):
            count[i] = count[i] + 1
        else:
            count[i] = 1
    count = sorted(count.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    count = count[0:20]
    print(count)
    word.clear()
    aveg = []
    for line in count:
        word.append(line[0])
        aveg.append(line[1] / len(data))
    print(word)
    print(aveg)
    # 计算分数
    rGrade = []
    for row in list(mix.items()):
        grade = []
        grade.append(row[0])
        for order in range(len(word)):
            c = 1
            for i in row[1]:
                if i == word[order]:
                    c = c + 1
            c = c / aveg[order]
            grade.append(c)
        rGrade.append(grade)
    return rGrade, word

#计算年平均订购量
with open(filename0, 'r') as f:
    reader = csv.reader(f)
    data0 = [row for row in reader]
with open(filename11, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'count'])
    writer.writerows(getCount(data0))
# print(cla_price(data0))

#计算价格因素
with open(filename0, 'r') as f:
    reader = csv.reader(f)
    data0 = [row for row in reader]
with open(filename5, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'price'])
    writer.writerows(cla_price(data0))
# print(cla_price(data0))

#计算景点分数
with open(filename1, 'r',encoding='gbk') as f:
    reader = csv.reader(f)
    data1 = [row for row in reader]
    # print(cla_ard(data1))
with open(filename6, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'spot'])
    writer.writerows(cla_ard(data1))
#计算车站分数
with open(filename2, 'r') as f:
    reader = csv.reader(f)
    data2 = [row for row in reader]
# print(cla_ard(data2))
with open(filename7, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'station'])
    writer.writerows(cla_ard(data2))
#计算餐饮分数
with open(filename3, 'r') as f:
    reader = csv.reader(f)
    data3 = [row for row in reader]
# print(cla_ard(data3))
with open(filename8, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'restaurant'])
    writer.writerows(cla_ard(data3))

#计算购物因素
with open(filename4, 'r') as f:
    reader = csv.reader(f)
    data4 = [row for row in reader]
# print(cla_ard(data4))
with open(filename9, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'shop'])
    writer.writerows(cla_ard(data4))


#计算评论分数
data5 = []
id, review = [], []
for line in fileList:
    with open('data/review/' + line, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        id.append(line[3:-4])
        review.append([row[2] for row in reader])
data5 = list(dict(zip(id, review)).items())
grade, word = cla_review(data5)
word = ['id'] + word
with open(filename10, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(word)
    writer.writerows(grade)
