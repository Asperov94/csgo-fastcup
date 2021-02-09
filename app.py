import os
import re
from time import sleep
from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup



def show_url(csgo_map):
    """парсит название матча """
    result = re.findall(r"match(.?.?.?.?.?.?.?)", csgo_map)
    print('REGULAR: ' + str(result) )
    html_url_map = 'https://csgo.fastcup.net/match' + ''.join(result)
    html_url_stat = html_url_map +'/stats'
    print ('===='+html_url_map+'=====')
    print ('===='+html_url_stat+'=====')
    return html_url_map, html_url_stat

def driver_web(setmap, setstat):
    driver = webdriver.Remote("http://standalone-chrome:4444/wd/hub", DesiredCapabilities.OPERA)
    driver.get(setmap)
    sleep(2)
    setmap_html = driver.page_source
    driver.get(setstat)
    setstat_html= driver.page_source
    sleep(3)
    driver.quit()

    #=======
    soup_map_html = BeautifulSoup(setmap_html, "html.parser")
    soup_stat_html = BeautifulSoup(setstat_html, "html.parser")
    print('driver ok=========')
    return soup_map_html, soup_stat_html



def csgonamemap(soup):
    print('===============================================csgo_map')


    for i in soup.find_all("div", {"class": "_2Fhou"}):
        print (i)
     
    csgo_map_name = soup.findAll("div", {"class": "_2Fhou"})[2].text
    if csgo_map_name == []:
        print('FAIL')

    csgo_win = str(soup.find("span", {"class": "_3kfeE _2xoXg _2QNqw"}).text) + ':' + str(soup.find("span", {"class": "_3kfeE _1Wlu4"}).text)
    if int(soup.find("span", {"class": "_3kfeE _2xoXg _2QNqw"}).text) > int(soup.find("span", {"class": "_3kfeE _1Wlu4"}).text):
        z=1
    else:
        z=2 
    print (str(csgo_map_name))
    print (csgo_win)

    return csgo_map_name, csgo_win, z

def csgo_read(soup, csgonamemap1, csgo_win, z):
    """Парсит КДА """
    print('KDA')

    #===VARIABLES===
    user=kill=dead=assist=''

    g=0
    #===---===
    try:
        os.remove('csv.csv')
    except OSError:
        print('not file')

    csv = open('csv.csv', 'w')

    print('stage4')

    print (soup.find_all("div", class_="_2Q_mv"))

    for i in soup.find_all("div", class_="_2Q_mv"):
        print (g)
        if z == 1 and g <6:
            csgo_false='win'
        elif z == 2 and g > 6:
            csgo_false='win'

        print(str(i))
        user=i.find("span", class_="_38-ZC")
        if user is None:
            user = 'USER'
        else:
            user=i.find("span", class_="_38-ZC").text

        kill=i.find("div", class_="_3UiPH _2SMgu").text
        dead=i.find("div", class_="_3UiPH _1Fe8v").text

        assist=i.find("div", class_="_3UiPH _26k4_")
        if assist is None:
            assist = 'A'
        else:
            assist=i.find("div", class_="_3UiPH _26k4_").text
        csv.write(f'{user};{kill};{dead};{assist};{csgonamemap1};{csgo_win};{csgo_false} \n' )
        print(f'{user};{kill};{dead};{assist};{csgonamemap1};{csgo_win};{csgo_false} \n')
        csgo_false='lost'
        g+=1
  
app = Flask(__name__)
@app.route('/csgo', methods=['GET'])
def index():
    """отдает html страницу"""
    return render_template('index.html')
@app.route('/csgo', methods=['POST'])
def index_post():
    """отдает файл"""
    data_url = request.form.get('csgo_map')
    print('STAGE1' + data_url)
    name_set_1, name_set_2 = show_url(data_url)
    print ("=================")
    soup_map_html, soup_stat_html = driver_web(name_set_1, name_set_2)
    out1, out2, out3 =  csgonamemap(soup_map_html)
    csgo_read( soup_stat_html ,out1, out2, out3)
    

    return send_file(os.path.join("." , "csv.csv"), as_attachment=True)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


