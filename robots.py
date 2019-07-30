import requests
import time

url='''
'''

url = url.split()
port = "80"

for i in range(len(url)):
    temp = "http://"+url[i]+":"+port+"/robots.txt"
    print(temp)
    try:
        response = requests.get(temp)
        text = response.text
        if(text.index("Disallow")):
            print(text)
    except:
        print("Not Found")
    time.sleep(5)

