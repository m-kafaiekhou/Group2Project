
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

def year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0
    
    return year_dict