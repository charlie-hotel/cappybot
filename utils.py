import re

# Cleans HTML tags from a string
def remove_html(html):
    cleaner = re.compile('<.*?>')
    rst = re.sub(cleaner, '', html)
    return rst