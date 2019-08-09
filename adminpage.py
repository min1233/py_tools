import requests
import time
import sys

def menu():
    print("-"*30)
    print("1. admin page find tools")
    print("2. robots find tools")
    print("-"*30)
    return input(">> ")

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
    #file_type = ["htm","cfm","brf","cgi","js"]
    file_type = ["htm","js"]
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

def admin_check(url,port,page,path,error_text): # check admin page (url:port/page)
    end = "\033[0m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    
    true_false = error_text!=""

    result = "----------------result----------------\n"
    for i in range(len(page)):
        try:
            temp = url+":"+port+"/"+path+page[i]
            response = requests.get(temp)
            response.encoding = None # fix up breaking hangul
            text = response.text
            if(text.find("404")!=-1):
                print("\n"+bold+red+"[-]"+end+" "+temp)
                print("Not Found\n")
            elif(true_false and text.find(error_text)!=-1):
                print("\n"+bold+red+"[-]"+end+" "+temp)
                print("Not Found\n")
            else:
                result += "\n"+bold+green+"[+]"+end+" "+temp+"\n"
                result += text+"\n"
                print("\n"+bold+green+"[+]"+end+" "+temp)
                print(text+"\n")
        except Exception as ex:
            print("\n"+bold+red+"[-]"+end+" "+temp)
            print("Error\n")
            print(ex)

    result += "--------------------------------------\n"
    print(result)
    return result

def robots(port):
    f = open("url_list","r")
    url = f.read().split()
    result = "----------------result----------------\n\n"
    for i in range(len(url)):
        temp = url[i]+":"+port+"/robots.txt"
        result += temp+"\n"
        try:
            response = requests.get(temp)
            text = response.text
            result += text+"\n\n"
        except:
            result += "Not Found"+"\n"
    result += "--------------------------------------\n"
    print("\nrobots.txt Result")
    print(result)
    return result

def save(file_name,result):
    file_name = file_name.replace(":","")
    file_name = file_name.replace("/","_")
    print("Save result, File Path : "+file_name)
    f = open(file_name,"w")
    f.write(result.encode('utf-8')) # fix up breaking hangul
    f.close()

num = menu()
if num==1:
    path= raw_input("Please enter the path that append when the program find admin page.( Ex : homepage/ )\nIf you don`t want to use this function, Press the Enter : ")
    error_text= raw_input("\nPleas enter the text that appeares when the program can`t find admin page.\nIf you want to use the default value, Press the Enter (default=404) : ")
    url,port = argu_check()    
    page = file_type_check()
    result = admin_check(url,port,page,path,error_text)
    save(url[s_index:]+path,result)
elif num==2:
    port = raw_input("Please enter the scan port : ")
    result = robots(port)
    save("robots.txt",result)
