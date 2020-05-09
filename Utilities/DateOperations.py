from datetime import datetime

def get_date_in_millis(date):
    if date == "":
        return 0

    dt_obj = datetime.strptime(str(date),
                               '%Y-%m-%d %H:%M:%S')
    return dt_obj.timestamp() * 1000