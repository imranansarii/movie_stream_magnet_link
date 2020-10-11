import requests
from bs4 import BeautifulSoup
import re
import json
import subprocess,sys

def parser(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup


search_term = input("Enter the name of the movie to watch!  ")
movie_datas = f"http://movie-scraper-api.herokuapp.com/{search_term}"
response = requests.get(movie_datas)
datas = response.text
parsed_datas = json.loads(datas)
for i in range(0,len(parsed_datas),1):
  print(str(i) +"  " + parsed_datas[str(i)]["name"] + " ------> " + parsed_datas[str(i)]["size"])

choice = int(input("Enter the serial number of the movie list to watch...  "))
choice_link = parsed_datas[str(choice)]["link"]
print(choice_link)

def fun(movie_link):
    soup = parser(movie_link)
    containers = soup.findAll("div", {"class": "box-info"})
    
    for container in containers:
        for link in container.findAll("li"):
        
            l = [a['href'] for a in link.findAll('a', href=True)]
            return l[0]
                
magnet_link = fun(choice_link)

stream = 0
ch = int(input("Press 0 for download and 1 for stream...  "))
if ch == 1:
    stream = 1
elif ch == 0:
    stream = 0



def webtorrent(ch,stream,magnet_link):
    # cmd = f'peerflix "{magnet_link}" --vlc'
    # if stream == 0:
    #     cmd = f'peerflix "{magnet_link}"'
    
    cmd = f'webtorrent "{magnet_link}" --vlc'
    if stream == 0:
        cmd = f'webtorrent "{magnet_link}"'
        
    if sys.platform.startswith('linux'):
        subprocess.call(cmd)
    elif sys.platform.startswith('win32'):
        subprocess.call(cmd,shell=True)


webtorrent(ch,stream,magnet_link)