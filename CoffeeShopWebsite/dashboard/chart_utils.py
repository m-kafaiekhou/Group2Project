
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

range_m = list(range(1,31+1))
month = list(map(str,range_m))

def year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0
    
    return year_dict


def month_dict():
    month_dict = dict()

    for day in month:
        month_dict[day] = 0
    
    return month_dict