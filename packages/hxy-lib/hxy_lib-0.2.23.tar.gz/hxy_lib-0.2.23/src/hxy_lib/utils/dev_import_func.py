from datetime import datetime, date, timedelta
import time
import csv

def KK_data_read_single(path: str, name: str, begin: int=0, end: int=-1, channel: float='CH2'):
    t = []
    t_data = []
    f_1 = []
    with open(path + name, 'r') as file:
        userlines = file.readlines()
        file.close()
    for line in userlines[begin:end]:
        datetime_obj = datetime.strptime('20' + line.split()[0] + line.split()[1], "%Y%m%d%H%M%S.%f")
        t.append(time.mktime(datetime_obj.timetuple()) + datetime_obj.microsecond / 1E6)
        t_data.append(datetime_obj)
        if channel == 'CH1':
            f_1.append(float(line.split()[3]))
        elif channel == 'CH2':
            f_1.append(float(line.split()[4]))
        elif channel == 'CH3':
            f_1.append(float(line.split()[5]))
        elif channel == 'CH4':
            f_1.append(float(line.split()[6]))

    return t, t_data, f_1

def daq780_import(path, name, column, target_type='float'):
    data_list = []
    with open (path+name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if target_type == 'float':
                data_list.append(float(row[column]))
            else:
                data_list.append(row[column])
    return data_list

