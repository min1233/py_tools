import requests
import time

end = "\033[0m"
bold = "\033[1m"
red = "\033[31m"
green = "\033[32m"

url='http://url'

f = open('admin_page_list', mode='r')
page = f.read().split()
port = "80"
result = '\n\n\n----------------result----------------\n\n\n'

for i in range(len(page)):
    try:
        temp = url+":"+port+"/"+page[i]
        response = requests.get(temp)
        text = response.text
        if(text.find("404")!=-1):
            print("\n"+bold+red+"[-]"+end+" "+temp)
            print("Not Found\n")
        else:
            result += bold+green+"[+]"+end+" "+temp
            result += text
            print("\n"+bold+green+"[+]"+end+" "+temp)
            print(text)
            break
    except:
        print("\n"+bold+red+"[-]"+end+" "+temp)
        print("Error\n")
    #time.sleep(5)
print(result)

