# additional functions for main program

DIGITS = {
    1: '=',
    1000: 'K',
    1000000: 'M',
    1000000000: 'B'
    }


def format_number (number, max_len, ending=''):
    # 1548984     >> 1 548 K
    # 48975646    >> 48 975 K
    # 5489754642  >> 5 489 M
    c_len = len(str(number))
    i = 0
    for d in DIGITS:
        num = number // d
        if not len(str(num)) > max_len:
            res = num
            size = DIGITS[d]
            break
    return str(res) + ' ' + size + ending


def date_dict (date, year_first=True, delimiter=None):
    # 25042009 >> {'year': 2009, 'month': 4, 'day': 25}
    # 08012003 >> {'year': 2003, 'month': 1, 'day': 8}
    # 09112001 >> {'year': 2001, 'month': 11, 'day': 9}
    if delimiter is not None:
        l = date.split(delimiter)
        if year_first:
            year = l[0]
            month = l[1]
            day = l[2]
        else:
            day = l[0]
            month = l[1]
            year = l[2]
    else:
        if year_first:
            year = date[:4]
            month = date[4:6]
            day = date[6:]
        else:
            day = date[:2]
            month = date[2:4]
            year = date[4:]
    return {'year': year, 'month': month, 'day': day}


def format_date (date_d, year_first=False, delim='.'):
    # {'year': 2009, 'month': 4, 'day': 25} >> 25.04.2009
    # {'year': 2003, 'month': 1, 'day': 8}  >> 08.01.2003
    # {'year': 2001, 'month': 11, 'day': 9} >> 09.11.2001
    if year_first:
        fdate = f"{date_d['year']}{delim}{date_d['month']}{delim}{date_d['day']}"
    else:
        fdate = f"{date_d['day']}{delim}{date_d['month']}{delim}{date_d['year']}"
    return fdate
    


def format_time (seconds):
    # 1, 5   >> 01:05
    # 10, 10 >> 10:10
    # 4, 20  >> 04:20
    m = seconds // 60
    s = seconds % 60
    duration = f'{m:0>2}:{s:0>2}'
    # align d_m and d_s to right with zeros to 2 symbols
    return duration



def dict_without_keys(dict_, keys):
    # {'a': 5, 'b': 6, 'c': 7} ('c') >> {'a': 5, 'b': 6}
    return {k:dict_[k] for k in dict_ if not k in keys}

