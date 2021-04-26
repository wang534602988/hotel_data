#混合数据，将id相同的列合并，输出最终文件tg0.csv
#该程序需运行多次，将文件不断两两合并
import csv
filename1 = 'data/hotelList.csv'
filename2 = 'data/review.csv'
filename3 = 'data/tg0.csv'
with open(filename1, "r") as f:
    reader = csv.reader(f)
    data1 = [row for row in reader]
with open(filename2, "r") as f:
    reader = csv.reader(f)
    data2 = [row for row in reader]
for line1 in data1:
    for line2 in data2:
        if line1[0] == line2[0]:
            for i in range(len(line2)):
                line1.append(line2[i])
print(data1)
out = open(filename3, "w", newline="")
csv_writer = csv.writer(out)
for line in data1:
    csv_writer.writerow(line)
