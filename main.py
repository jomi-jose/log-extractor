
import re
from dateutil import parser

def read_log_file():
    with open('logfile/ITLControl.Log','r') as file:
        logs = file.readlines()
    return logs

def convert_log_to_dict(logs):
    for log in logs:
        extract_log(log)

def extract_log(log):
    date_match = re.search('\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}', log)
    if date_match:
        #pump_total attributes
        nozzle= None
        grade = None
        volumeH = None
        volumeL = None
        valueH = None
        valueL = None
        # transaction total attributes
        volume = None
        value = None
        grade_price = None

        date_match = re.search('\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}', log)
        pump_match = re.search('Pump - \d', log)
        pump = pump_match.group(0).split(' ')[2] if pump_match else None
        status_match = re.search('new status = \d', log)
        status = status_match.group(0).split(' ')[2] if status_match else None
        running_total_match = re.search('RunningTotals', log)
        pump_total_match = re.search('PumpTotals(.*)', log)
        # print(pump_total_match)
        clear_delivery_match = re.search('Clear delivery', log)
        transaction_total_match = re.search('transaction totals.*', log)
        
        
        
        # running_total = running_total_match.group(0).split(' ')[2] if running_total_match else None
        log_type = None
        if status:
            log_type = "status_log"
        elif running_total_match:
            log_type = "running_total_log"
        elif pump_total_match:
            log_type = "pump_total_log"
            p_t_match_group = pump_total_match.group(0)
            pump_total_log_detail = p_t_match_group[p_t_match_group.find("(")+1:p_t_match_group.find(")")]
            pump_match = re.search('Pump \d', pump_total_log_detail)
            pump = pump_match.group(0).split(' ')[1] if pump_match else None
            nozzle_match = re.search('Nozzle \d', pump_total_log_detail)
            nozzle = nozzle_match.group(0).split(' ')[1] if nozzle_match else None
            grade_match = re.search('Nozzle \d', pump_total_log_detail)
            grade = grade_match.group(0).split(' ')[1] if grade_match else None
            VolumeH_match = re.search('VolumeH \d*', pump_total_log_detail)
            volumeH = VolumeH_match.group(0).split(' ')[1] if VolumeH_match else None
            VolumeL_match = re.search('VolumeL \d*', pump_total_log_detail)
            volumeL = VolumeL_match.group(0).split(' ')[1] if VolumeL_match else None
            ValueH_match = re.search('ValueH \d*', pump_total_log_detail)
            valueH = ValueH_match.group(0).split(' ')[1] if ValueH_match else None
            ValueL_match = re.search('ValueL \d*', pump_total_log_detail)
            valueL = ValueL_match.group(0).split(' ')[1] if ValueL_match else None
            # print(pump_total_log_detail)
            # print(volumeH)
            # print(volumeL)
        elif clear_delivery_match:
            log_type = "clear_delivery_log"
        elif transaction_total_match:
            log_type = "transaction_total_log"
            # print(transaction_total_match.group(0))
            ttm_group = transaction_total_match.group(0)
            volume_match = re.search('Volume \d*', ttm_group)
            volume = volume_match.group(0).split(' ')[1] if volume_match else None
            value_match = re.search('Value \d*', ttm_group)
            value = value_match.group(0).split(' ')[1] if value_match else None
            grade_price_match = re.search('Grade price \d*', ttm_group)
            grade_price = grade_price_match.group(0).split(' ')[2] if grade_price_match else None

        
        # print(pump_match)
        dt = date_match.group(0)
        log_parts = log.split(' ')
        log_detail = {
            'created_at': parser.parse(dt),
            'pump': pump,
            'log_type': log_type,
            'nozzle': nozzle,
            'grade': grade,
            'volumeH': volumeH,
            'volumeL': volumeL,
            'valueH': valueH,
            'valueL': valueL,
            'volume': volume,
            'value': value,
            'grade_price': grade_price

        }
        print(log_detail)


def main():
    logs = read_log_file()
    convert_log_to_dict(logs)
  
  
# __name__
if __name__=="__main__":
    main()