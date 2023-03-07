# python version 3.8.15
import csv
import time
from disklist import DiskList

matri_num = "U2021043D"
year1 = '2003'
year2 = '2013'
location = 'Paya Lebar'


def main():

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
    start_time = start_time = time.time()
    position_dict = {}
    for i in range(len(dateColumn)):

        date = dateColumn[i]

        if date[:4] in (year1, year2):  # Filter by year(2003,2013) in column store
            # Filter by location(paya lebar) in column store
            if stationColumn[i] == location:
                key = date[0:7]

                if key not in position_dict:
                    position_dict[key] = []

                position_dict[key].append(i)

    # to store max and min temp of each month, eg key= (yyyy-mm,'Max Temp"), value=(pos,temp_value)
    temperature_dict = {}
    # to store max and min humidity of each month, eg key= (yyyy-mm,'Max Humidity") , value=(pos,humidity_value)
    humidity_dict = {}

    for year_month, positions in position_dict.items():
        max_temperature = -1
        max_temperature_pos = -1
        min_temperature = 101
        min_temperature_pos = -1
        for pos in positions:
            curr_temperature_str = tempColumn[pos]
            if curr_temperature_str == 'M':
                continue
            curr_temperature = float(curr_temperature_str)
            if curr_temperature > max_temperature:
                max_temperature = curr_temperature
                max_temperature_pos = pos
            if curr_temperature < min_temperature:
                min_temperature = curr_temperature
                min_temperature_pos = pos
        temperature_dict[year_month, 'Max Temperature'] = (
            max_temperature_pos, max_temperature)
        temperature_dict[year_month, 'Min Temperature'] = (
            min_temperature_pos, min_temperature)

        max_humidity = -1
        max_humidity_pos = -1
        min_humidity = 101
        min_humidity_pos = -1
        for pos in positions:
            curr_humidity_str = humidColumn[pos]
            if curr_humidity_str == 'M':
                continue
            curr_humidity = float(curr_humidity_str)
            if curr_humidity > max_humidity:
                max_humidity = curr_humidity
                max_humidity_pos = pos
            if curr_humidity < min_humidity:
                min_humidity = curr_humidity
                min_humidity_pos = pos
        humidity_dict[year_month, 'Max Humidity'] = (
            max_humidity_pos, max_humidity)
        humidity_dict[year_month, 'Min Humidity'] = (
            min_humidity_pos, min_humidity)

        end_time = time.time()

    print(f'Time taken for query processing: {round(end_time-start_time,4)}s')

    start_time = time.time()

    with open('result.csv', 'w') as f:
        header = ['Date', 'Station', 'Metric', 'Value']
        writer = csv.writer(f)
        writer.writerow(header)
        for key, value in temperature_dict.items():
            writer.writerow([dateColumn[value[0]], location, key[1], value[1]])
        for key, value in humidity_dict.items():
            writer.writerow([dateColumn[value[0]], location, key[1], value[1]])

    end_time = time.time()

    print(f'Time taken for result saving: {round(end_time-start_time,4)}s')


if __name__ == "__main__":
    main()
