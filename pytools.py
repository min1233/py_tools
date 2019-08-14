import requests
import time
import sys
import re

def print_result(result):
    print("-"*30)
    print(result)
    print("-"*30)

def menu():
    menu = '''1. admin page find tools
2. robots find tools
3. create email file tools
4. find specific email in email file
0. exit'''
    print_result(menu)
    
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

    result = ""
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
    print_result(result)
    return result

def robots():
    f = open("url_list","r")
    url = f.read().split()
    result =""
    for i in range(len(url)):
        temp = url[i]+"/robots.txt"
        result += temp+"\n"
        try:
            response = requests.get(temp)
            text = response.text
            result += text+"\n\n"
        except:
            result += "Not Found"+"\n"
    print_result(result)
    return result

def save(file_name,result):
    file_name = file_name.replace(":","")
    file_name = file_name.replace("/","_")
    print("Save result, File Path : "+file_name)
    f = open(file_name,"a")
    f.write(result.encode('utf-8')) # fix up breaking hangul
    f.close()

def create_email_file():
    pattern = re.compile("[a-z0-9]*@[^-]*")
    cred = open("cred","r")
    email = open("email","w")

    save_email(cred,email,pattern)

    print("Regular expression search complete")
    cred.close()    
    email.close()
    

def find_email():
    string = raw_input("Enter the domain you want to search for in email file >> ") # python 2.7
    pattern = re.compile(".*@"+string+".*")
    
    email = open("email","r")
    result = open(string,"w")
    
    save_email(email,result,pattern)

    print("Regular expression search complete")
    email.close()
    result.close()

def save_email(tmp1, tmp2,pattern):
    while(1):
        buf=tmp1.read(500000)
        if buf:
            result = pattern.findall(buf)
            for c in result:
                tmp2.write(c+"\n")
        else:
            break

while(1):
    try:
        num = menu()
        if num==1:
            path= raw_input("Please enter the path that append when the program find admin page.( Ex : homepage/ )\nIf you don`t want to use this function, Press the Enter : ")
            error_text= raw_input("\nPleas enter the text that appeares when the program can`t find admin page.\nIf you want to use the default value, Press the Enter (default=404) : ")
            url,port = argu_check()    
            page = file_type_check()
            result = admin_check(url,port,page,path,error_text)
            save(url+path,result)
        elif num==2:
            result = robots()
            save("robots.txt",result)
        elif num==3:
            create_email_file()
        elif num==4:
            find_email()
        elif num==0:
            break
    except:
        pass