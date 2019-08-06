import requests
import time
import sys

def argu_check():
    argu_size = len(sys.argv)
    if(argu_size==1):
        print("Programe needs arguments.")
        print("Example) python ./adminpage.py http://url port [file type]")
        exit(0)
    if(argu_size>2):
        if(sys.argv[1].find("http")==-1):
            print("Schema must be included")
            exit(0)
            
        url = sys.argv.pop(1)
        port = sys.argv.pop(1)
        return url,port

def file_type_check(): # File type check
    f = open('page_list', mode='r')
    tmp = f.read().split()
    argu_size = len(sys.argv) # include allow file type in arguments
    file_type = ["htm","cfm","brf","cgi","js"]
    page = []
    if argu_size!=1:
        for i in range(0,len(tmp)):
            try:
                result = 0
                if(tmp[i][-1:]=="/"):
                    raise NotImplementedError
                for k in file_type:
                    if(tmp[i].find(k)!=-1):
                        raise NotImplementedError
                for j in range(1,argu_size):
                    if(tmp[i].find(sys.argv[j])!=-1):
                        raise NotImplementedError
            except:
                page.append(tmp[i])
    if(len(page)==0):
        return tmp
    else:
        return page

def admin_check(url,port,page,error_text=""): # check admin page (url:port/page)
    end = "\033[0m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    
    true_false = error_text!=""

    result = '\n\n\n----------------result----------------\n\n\n'

    for i in range(len(page)):
        try:
            temp = url+":"+port+"/"+page[i]
            response = requests.get(temp)
            text = response.text
            if(text.find("404")!=-1):
                print("\n"+bold+red+"[-]"+end+" "+temp)
                print("Not Found\n")
            elif(true_false and text.find(error_text)!=-1):
                print("\n"+bold+red+"[-]"+end+" "+temp)
                print("Not Found\n")
            else:
                result += bold+green+"[+]"+end+" "+temp
                result += text
                print("\n"+bold+green+"[+]"+end+" "+temp)
                print(text+"\n")
        except:
            print("\n"+bold+red+"[-]"+end+" "+temp)
            print("Error\n")
    print(result)
    return result

def save(url,result):
    s_index = url.find("//")+2
    print("Save result, File Path : ",url[s_index:])
    f = open(url[s_index:],"w")
    f.write(result)
    f.close()

string_404= raw_input("Pleas enter the text that appeares when the program can`t find admin page.\nIf you want to use the default value, Press the Enter (default=404) : ")
url,port = argu_check()
page = file_type_check()
result = admin_check(url,port,page,string_404)
save(url,result)
