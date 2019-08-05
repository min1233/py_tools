import requests
import time

url=''

f = open('admin_page_list', mode='r')
page = f.read().split()
port = "80"
result = ''

for i in range(len(page)):
    temp = url+":"+port+"/"+page[i]
    result += temp+"\n"
    response = requests.get(temp)
    text = response.text
    if(text.find("404")!=-1):
        result += "Not Found\n"
    else:
        result += text
        break
    #time.sleep(5)
print(result)
