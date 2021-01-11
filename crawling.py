from flask import Flask
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import lxml
from flask import send_file
import zipfile
import os
import shutil
app = Flask(__name__)
@app.route('/')
def hello_world():
   return 'Welcome to REECAP Web Crawling by CoderToCode(SAGAR K)'
@app.route('/<lang>/<heading>')
def crawling(lang, heading):
    my_zipfile = zipfile.ZipFile("output.zip", mode='w', compression=zipfile.ZIP_DEFLATED)
    url =requests.get("https://www.google.com/search?q="+lang+"+code+for+"+heading.replace("_","+"))
    html = url.content
    soup = BeautifulSoup(html, 'lxml')
    links=soup.find_all('a')
    # print(links)
    link=[]
    for i in links:
      link.append(i.get("href"))
    link1=[]
    for i in link:
      if(str(i).startswith('/url?q=')):
        i=str(i).replace('/url?q=',"")
        link1.append(i)
    link2=[]
    for i in link1:
      if i.find('&'):
        cou=i.find('&')
        s=i[:cou]
        link2.append(s)
    link2.pop()
    temp = ""
    os.mkdir("/home/ubuntu/reecap/" + heading)
    for i in link2:
      domain = urlparse(i).netloc
      domain = domain.replace("www.","")
      domain = domain[ 0 : domain.index('.')]
      url=requests.get(i)
      html = url.content
      soup1= BeautifulSoup(html, 'lxml')
      soup1=soup1.find_all('code')
      str_cells = str(soup1)
      cleantext1= BeautifulSoup(str_cells, "lxml").get_text()
      temp = temp + cleantext1.replace(",","") + ("-"*60)
      with open(heading + "/" + domain + "." + str(lang),"w") as txt_file:
          txt_file.write(temp)
      my_zipfile.write(heading + "/" + domain + "." + str(lang))
    my_zipfile.close()
    shutil.rmtree(os.path.join("/home/ubuntu/reecap/",heading))
    return send_file('output.zip',attachment_filename=heading+".zip")
if __name__ == '__main__':
   app.run(host='0.0.0.0')