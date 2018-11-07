from bs4 import BeautifulSoup as BS
import requests
import os
import sys

# to mimic the browser useful for website that doesnot allow scripts.
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

serials = ['bhadragol', 'meribassai']
for i in serials:
    try:
        url = f"https://youtube.com/results?search_query={i}"
        response = requests.get(url, headers=headers)
    except:
        print("no internet")
        sys.exit()

    soup = BS(response.content, 'lxml')
    # print(soup.prettify())
    vids = soup.find_all('h3', class_='yt-lockup-title')

    def get_link():
        '''returns watch id and full link'''
        for vid in vids:
            prefix_link = 'https://m.youtube.com'  # watch?v=gb63zWfSwLQ
            suffix_link = vid.a['href']
            link = prefix_link + suffix_link
            # print(link, suffix_link)
            break  # stop at first search
        return suffix_link, link

    hash, link = get_link()
    download = False

    # check if file exists otherwise make it
    try:
        with open(".hashes", 'r+') as fr:
            pass
    except FileNotFoundError:
        with open(".hashes", 'w+') as fw:
            fw.write(" ")

    # check for duplicates
    with open(".hashes", 'r')as fr:
        for line in fr.readlines():
            if line.strip() == hash:
                print("file already downloaded")
                download = False
                break
            else:
                download = True

    if download:
        try:
            os.remove(f'/sdcard/videos/{i}.mp4')
            os.remove(f'/sdcard/videos/{i}.mp4.part')
        except:
            print("downloading....")

        with open('.hashes', 'a') as fw:
            download = True
            fw.write(hash)
            fw.write("\n")

        #os.system(f"start /wait cmd /c youtube-dl -f 36 -o serials/{i}.mp4 {link}")
        os.system(f"youtube-dl -f 36 -o /sdcard/videos/{i}.mp4 {link}")
        #os.system(f"youtube-dl -f 36 -o serials/{i}.mp4 {link}")
