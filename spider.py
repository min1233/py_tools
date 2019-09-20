import urllib2
import re
import threading
import time
import sys
from collections import OrderedDict # remove duplication in Order

reload(sys) # fix bug - ascii range(128)
sys.setdefaultencoding('utf-8') # fix bug - ascii range(128)

lock = threading.Lock()
t_max = 20
sem = threading.Semaphore(t_max)

url = raw_input("Enter the url : ")
find_text = raw_input("Enter the find text : ")
url_list = [url]

file_name = url.replace(":","")
file_name = file_name.replace("/","_")
file_name = file_name.replace(".","_")
f = open("./spider/"+file_name,"w")

def debug(url_list):
	print("-"*50)
	for c in url_list:
		print(c)
	print("-"*50)

def debug2(url,url_path1,url_path2):
	print(url)
	print(url_path1.encode("utf-8"))
	print(url_path2.encode("utf-8"))

def file_type_check(url,check_list):
        for file_type in check_list:
                if(url.lower().find(file_type)!=-1):
                        return 1
        return 0

def url_process1(url):
	index1 = url.find("//")+2 # shcema://
	index2 = url.find("/",index1)+1 # find path1 (path) # tmp -> 
	index3 = url.rfind("/")+1 #find path2 (path2/./)

	url_path1 = url[:index2]
	url_path2 = url[:index3]

	return index1,url_path1,url_path2

def url_process2(url):
        url = url.replace("/./","/")
        index1 = url.find("://")+3
        path = index1+url[index1:].find("/")

        while(1):
                index2 = url.find("../")
                if(index2==-1):break

                index3 = url[:index2].rfind("/")
                index4 = url[:index3].rfind("/")

                if(index1-1==index4):
                        url = url.replace("../","")
                        break
                tmp = url[index4:index3+3]
                url = url.replace(tmp,"")
	url = url[:index1]+url[index1:].replace("//","/")
        return url

def pattern_check(data,check_list): # src="path/filename.filetype
        result = []
        regular = '''[\"\'][\w\#\?\.\-&=_%/()]*'''
        for file_type in check_list:
                pattern4 = re.compile(regular+file_type.replace(".","\.")+"\W") # chagne Regular
                tmp = pattern4.findall(data)
                if(tmp):
                        result = result + tmp
        return result


def slush_remove(path):
	path = path.replace("\\","")[1:]
	if(path[0]=="/"): path = path[1:]
	return path

def url_request(url):
	try:
		rep = urllib2.urlopen(url,timeout=5)
		text = rep.read()
		rep.close()
		return text
	except Exception as e:
		return "error"

def reg(data,tmp):
	tmp1 = [] # url_list
	index1,url_path1,url_path2 = url_process1(tmp) # http:// start index, http://example.com/, http://example.com/path/

	pattern = re.compile("http[^\"\'\n<>,`;|]*") # chagne Regular
	pattern2 = re.compile("[\"\']/+[\w\#\?\.\-&=_%/()]*") # change Regular
	pattern3 = re.compile("[\"\'][\.]+/[\w\#\?\.\-&=_%/()]*") # chagne Regular

	tmp2 = list(OrderedDict.fromkeys(pattern.findall(data))) # http://example.com
	tmp3 = list(OrderedDict.fromkeys(pattern2.findall(data))) # /Absolute Path
	tmp4 = list(OrderedDict.fromkeys(pattern3.findall(data))) # ./Relative Path

	check_list = [".js",".html",".jsp",".php",".asp"]
	tmp5 = list(OrderedDict.fromkeys(pattern_check(data,check_list))) # Relative Path

	for c in tmp2:
		url = c.replace("\\","")
		url = url_process2(url)
		tmp1.append(url)
	for c in tmp3:
		if(c[1:3]=="//"):continue
		c = slush_remove(c)
		url = url_process2(url_path1+c)
		tmp1.append(url)
	for c in tmp4:
		url = url_process2(url_path2+c.replace("\\","")[1:])
		tmp1.append(url)
	for c in tmp5:
		url = url_process2(url_path2+c.replace("\'","").replace("\"",""))
		tmp1.append(url)
	return list(OrderedDict.fromkeys(tmp1))

def check(url_list,find_list):
	lock.acquire()
	return_value = []
	check_list = [".jpg",".png",".gif",".pdf",".mp4",".exe",".tgz",".ids",".xls",".eot",".woff",".otf",".ttf",".svg"]
	for url in find_list:
		path1 = re.compile(":[0-9]+") # find port regex
		port1 = path1.findall(url)
		if(port1==[]): port1 = ""
		else: port1 = port1[0]

		index1 = url.find("//")+2 # scheam://
		if(url.find(find_text)==-1): continue
		elif(file_type_check(url,check_list)): continue
		true_false1 = 1
		for url2 in url_list:
			path2 = re.compile(":[0-9]+") # find port regex
			port2 = path2.findall(url2)
			if(port2==[]): port2 = ""
			else: port2 = port2[0]

			index2 = url2.find("//")+2 # schema://
			if(url[index1:].replace(port1,"")!=url2[index2:].replace(port2,"")): # check after except schema
				continue
			else:
				true_false1 = 0
				break
		if(true_false1):
			return_value.append(url)
	if(return_value!=[]):
		for tmp2 in return_value:	
			f.write(tmp2+"\n")
			url_list.append(tmp2)

	#debug(url_list)
	lock.release()
	return 1

def th_main(tmp):
	sem.acquire()
	data = url_request(tmp)
	if(data=="error"):
		sem.release()
		return 0;
	find_list = reg(data,tmp)
	check(url_list,find_list)
	sem.release()

start = time.time()
threads = []
true_false2 = 0 # thread start
count = 0

for i,tmp in enumerate(url_list):
	if(len(url_list)-i>3):true_false2 = 1
	else: true_false2 = 0

	if(true_false2):
		count = count+1
		th = threading.Thread(target=th_main,args=(tmp,))
		th.start()
		threads.append(th)
	else:
		print("\nCount : "+str(i+1)+" / len(url_list) : "+str(len(url_list)))
		th_main(tmp)

	if(count==t_max or not(true_false2)):
		count = 0
		for th in threads:
			th.join()
			threads.pop(0)

for th in threads:
	th.join()

f.close()
debug(url_list)

print("Search Count : "+str(i+1))
print("end")
print(time.time()-start)	
