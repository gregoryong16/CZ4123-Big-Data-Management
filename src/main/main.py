# python version 3.8.15
import csv
from disklist import DiskList
matri_num = "U2021043D"


# id,Timestamp,Station,Temperature,Humidity
idColumn = DiskList()
dateColumn = DiskList()
stationColumn = DiskList()
tempColumn = DiskList()
humidColumn = DiskList()

# improvement 1: check for number of items, if > ram size, store in disk
# store min max for region since its sorted with date


# Create Column store
with open("resources/SingaporeWeather.csv", 'r') as f:
    reader = csv.DictReader(f)
    # current_month = ''
    # count = 0
    for row in reader:
        idColumn.append(row['id'])
        stationColumn.append(row['Station'])
        tempColumn.append(row['Temperature'])
        humidColumn.append(row['Humidity'])

        # convert "yyyy-mm-dd hh:mm" -> "yyyy-mm"
        timeStamp = row['Timestamp'].split()[0][:7]
        # if current_month != timeStamp:
        #     # print(current_month == timeStamp, current_month)
        #     print(current_month, "count:", count+1)
        #     current_month = str(timeStamp)
        #     count = 0
        # count += 1
        dateColumn.append(timeStamp)


def main():

    # Query Input processing
    year1 = '200' + matri_num[7]
    year2 = '201' + matri_num[7]
    location = ''
    if int(matri_num[6]) % 2 == 0:
        location = 'Changi'
    else:
        location = 'Paya Lebar'


if __name__ == "__main__":
    # main()
    pass
