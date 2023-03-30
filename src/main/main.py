# python version 3.8.15
import csv
import time
from disklist import DiskList

matri_num = "U2021043D"
year1 = '2003'
year2 = '2013'
location = 'Paya Lebar'


def main():

    matri_num = input("Please input your matriculation number: \n")
    last_num = matri_num[-2]

    # Choose the correct years to look at
    if last_num == '0' or last_num == '1':
        year1= '201' + last_num
        year2= '202'+last_num
        print("Year 1:",year1)
        print("Year 2:",year2)
    else:
        year1='200' + last_num
        year2= '201'+last_num
        print("Year 1:",year1)
        print("Year 2:",year2)

    # Choose correct location    
    second_last_num=matri_num[-3]
    # if num is even
    if int(second_last_num)%2 == 0:
        location="Changi"
    else:
        location="Paya Lebar"
    print("Location: ",location)

    # id,Timestamp,Station,Temperature,Humidity
    # idColumn = DiskList()
    dateColumn = DiskList()
    stationColumn = DiskList()
    tempColumn = DiskList()
    humidColumn = DiskList()

    # Create Column store
    print("initializing column store...")
    start_time = time.time()

    with open("resources/SingaporeWeather.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # idColumn.append(row['id'])
            stationColumn.append(row['Station'])
            tempColumn.append(row['Temperature'])
            humidColumn.append(row['Humidity'])

            # convert "yyyy-mm-dd hh:mm" -> "yyyy-mm" to conserve space on disk
            timeStamp = row['Timestamp'].split()[0]
            dateColumn.append(timeStamp)

    end_time = time.time()
    print(f'column store creation complete in {round(end_time-start_time,4)}s')

    # QUERY PROCESSING
    # Assume memory is able to hold positions
    start_time = time.time()

    position_dict = {}
    for i in range(len(dateColumn)):

        date = dateColumn[i]
        
        if date[:4] in (year1, year2):  # Filter by year(2003,2013) in column store
            # Filter by location in column store
            if stationColumn[i] == location:
                key = date[0:7]

                if key not in position_dict:
                    position_dict[key] = []

                position_dict[key].append(i)

    # to store max and min temp of each month, eg key= (yyyy-mm-dd,'Max Temp"), value= temp_value
    temperature_dict = {}
    # to store max and min humidity of each month, eg key= (yyyy-mm-dd,'Max Humidity") , value= humidity_value
    humidity_dict = {}

    for year_month, positions in position_dict.items():
        
        max_temp_list=[]
        min_temp_list=[]
        max_temperature = -1
        min_temperature = 101
        for pos in positions:
            curr_temperature_str = tempColumn[pos]
            if curr_temperature_str == 'M':
                continue
            curr_temperature = float(curr_temperature_str)
            if curr_temperature >= max_temperature:
                if curr_temperature == max_temperature:
                    max_temp_list.append(pos)
                else:
                    max_temperature = curr_temperature
                    # Clear list before appending new positions
                    max_temp_list=[]
                    max_temp_list.append(pos)
                    
            if curr_temperature <= min_temperature:
                if curr_temperature == min_temperature:
                    min_temp_list.append(pos)
                else:
                    min_temperature = curr_temperature
                    # Clear list before appending new positions
                    min_temp_list=[]
                    min_temp_list.append(pos)
        
        for i in range(len(max_temp_list)):
            temperature_dict[dateColumn[max_temp_list[i]], 'Max Temperature'] = max_temperature

        for i in range(len(min_temp_list)-1):    
            temperature_dict[dateColumn[min_temp_list[i]], 'Min Temperature'] = min_temperature
        
        max_humidity_list=[]
        min_humidity_list=[]
        max_humidity = -1
        min_humidity = 101
        for pos in positions:
            curr_humidity_str = humidColumn[pos]
            if curr_humidity_str == 'M':
                continue
            curr_humidity = float(curr_humidity_str)
            if curr_humidity >= max_humidity:
                if curr_humidity == max_humidity:
                    max_humidity_list.append(pos)
                else:
                    max_humidity = curr_humidity
                    # Clear list before appending new positions
                    max_humidity_list=[]
                    max_humidity_list.append(pos)
                    
            if curr_humidity <= min_humidity:
                if curr_humidity == min_humidity:
                    min_humidity_list.append(pos)
                else:
                    min_humidity = curr_humidity
                    # Clear list before appending new positions
                    min_humidity_list=[]
                    min_humidity_list.append(pos)

        for i in range(len(max_humidity_list)):
            humidity_dict[dateColumn[max_humidity_list[i]], 'Max Humidity'] = max_humidity
        
        for i in range(len(min_humidity_list)):
            humidity_dict[dateColumn[min_humidity_list[i]], 'Min Humidity'] = min_humidity

    end_time = time.time()

    print(f'Time taken for query processing: {round(end_time-start_time,4)}s')

    start_time = time.time()

    with open('result.csv', 'w') as f:
        header = ['Date', 'Station', 'Category', 'Value']
        writer = csv.writer(f)
        writer.writerow(header)
        for key, value in temperature_dict.items():
            writer.writerow([key[0], location, key[1], value])
        for key, value in humidity_dict.items():
            writer.writerow([key[0], location, key[1], value])

    end_time = time.time()

    print(f'Time taken for result saving: {round(end_time-start_time,4)}s')


if __name__ == "__main__":
    main()
