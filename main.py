from bs4 import BeautifulSoup as BS
import requests
import datetime
import calendar
import sys
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def search_string(x):
	''' Input:serial name output:last broadcast date
	
	Takes valid serial name and gives when it was last aired in T.V in
	%day %monthname format.
	'''
	#Name of serials registered with their broadcasting weekday.
	serials = {'meribassai':0, 'bhadragol':4}
	tweekday = datetime.date.today().weekday()#todays weekday in int
	serial_no = serials.get(x.lower())#getting the weekday of serial
	#calculating the day diff betn today and last airing of serial 
	interval = datetime.timedelta(days=abs(serial_no-tweekday))
	#calculating full date of serial aired last time 
	date = datetime.date.today() - interval
	month = date.month#getting this month in int
	monthname = calendar.month_name[month]#changing to word
	return '{0} {1}'.format(str(date.day),str(monthname))#giving string
serials = ["bhadragol", ' ']
for serial in serials:
	search_day = search_string(serial)	
	url = "https://youtube.com/results?search_query=" + '{0} {1}'.format(serial,search_day)
	response = requests.get(url)
	soup = BS(response.content,'lxml')
	#print(soup.prettify())
	vids = soup.find_all('h3',class_= 'yt-lockup-title')
	link = None
	for vid in vids:
	    prefix_link= 'https://m.youtube.com'#watch?v=gb63zWfSwLQ
	    suffix_link = vid.a['href']
	    link = prefix_link + suffix_link
	    title = vid.a['title']
	    break
	    
	hashes = []
	with open('hashes.py', 'r') as fr:
		with open('hashes.py', 'w') as fw:
			hashes = list(fr.read())
			if link not in hashes:
				hashes.append(link)
				fw.write(hashes)
				os.system('youtube-dl -f 134 ' + link)
			else:
				sys.exit()

	  	  