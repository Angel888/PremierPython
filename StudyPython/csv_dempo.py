# 导入csv
import csv

# 打开rent.csv文件
csv_file = open("rent.csv", "wb")

# 创建writer对象，指定文件与分隔符
csv_writer = csv.writer(csv_file, delimiter=',')

# 写一行数据
csv_writer.writerow([house_title, house_location, house_money, house_url])

# 关闭文件
csv_file.close()