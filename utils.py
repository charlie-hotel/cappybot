import re

# Cleans HTML tags from a string
def remove_html(html):
    cleaner = re.compile('<.*?>')
    rst = re.sub(cleaner, '', html)
    return rst

# Converts the Admiral Shark's Keebs document date format
# to something more pleasant
def date_2_str(date):
    if date == None:
        return "undated"
    
    rst = ""
    bits = date.split("-")

    if len(bits) == 3:
        
        if bits[1] != "00":
            if bits[1] == "01":
                rst += "January "
            if bits[1] == "02":
                rst += "February "
            if bits[1] == "03":
                rst += "March "
            if bits[1] == "04":
                rst += "April "
            if bits[1] == "05":
                rst += "May "
            if bits[1] == "06":
                rst += "June "
            if bits[1] == "07":
                rst += "July "
            if bits[1] == "08":
                rst += "August "
            if bits[1] == "09":
                rst += "September "
            if bits[1] == "10":
                rst += "October "
            if bits[1] == "11":
                rst += "November "
            if bits[1] == "12":
                rst += "December "

        if bits[0] != "0000":
            rst += bits[0]
        else:
            return "undated"
        
        return rst
    else:
        return "undated"