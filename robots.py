import requests
import time

url='''

'''

url = url.split()
port = "80"

result =""
for i in range(len(url)):
    temp = "http://"+url[i]+":"+port+"/robots.txt"
    result += temp+"\n"
    response = requests.get(temp)
    text = response.text
    try:
        if(text.index("Disallow")):
            result += text+"\n"
    except:
        result += "Not Found"+"\n"

print("\n\n\n")
print("robots.txt Result")
print(result)
