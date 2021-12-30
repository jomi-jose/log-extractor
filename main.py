
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
        date_match = re.search('\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}', log)
        pump_match = re.search('Pump - \d', log)
        pump = pump_match.group(0).split(' ')[2] if pump_match else None 
        # print(pump_match)
        dt = date_match.group(0)
        log_parts = log.split(' ')
        log_detail = {
            'created_at': parser.parse(dt),
            'pump': pump
        }
        print(log_detail)


def main():
    logs = read_log_file()
    convert_log_to_dict(logs)
  
  
# __name__
if __name__=="__main__":
    main()