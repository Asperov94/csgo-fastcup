import os
import re
from time import sleep
from flask import Flask
from flask import request
from flask import render_template
from flask import send_file

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup



def csgomapname(csgo_map):
    """Это докстринг модуля, он однострочный."""
    result = re.findall(r"match(.?.?.?.?.?.?.?)", csgo_map)
    print('REGULAR: ' + str(result) )
    result = 'https://csgo.fastcup.net/match' + ''.join(result)
    print (result)
    return result

def csgonamemap(csgo_map):
    """Это докстринг модуля, он однострочный."""
    driver = webdriver.Remote("http://selenium-chrome:4444/wd/hub", DesiredCapabilities.CHROME)
    #driver = webdriver.Chrome()
    driver.get(csgo_map)
    main_page = driver.page_source

    soup = BeautifulSoup(main_page, "html.parser")
    sleep(3)
    driver.quit()

    for i in soup.find_all("div", {"class": "_2Fhou"}):
        print (i)
    csgo_map_name = soup.findAll("div", {"class": "_2Fhou"})[2].text

    csgo_win = str(soup.find("span", {"class": "_3kfeE _2xoXg _2QNqw"}).text) + ':' + str(soup.find("span", {"class": "_3kfeE _1Wlu4"}).text)
    if int(soup.find("span", {"class": "_3kfeE _2xoXg _2QNqw"}).text) > int(soup.find("span", {"class": "_3kfeE _1Wlu4"}).text):
        z=1
    else:
        z=2 
    print (str(csgo_map_name))
    print (csgo_win)
    return csgo_map_name, csgo_win, z

def csgo_read(csgo_map, csgonamemap1, csgo_win, z):
    """Это докстринг модуля, он однострочный."""
    #===VARIABLES===
    user=kill=dead=assist=''

    g=0
    #===---===
    csgo_map = csgo_map + '/stats'
    print('-=-=-=-=-=-=-csgo_read (csgo_map)=' + csgo_map)
    driver = webdriver.Remote("http://selenium-chrome:4444/wd/hub", DesiredCapabilities.CHROME)
    #driver = webdriver.Chrome()
    driver.get(csgo_map)
    main_page = driver.page_source
    os.remove('csv.csv')
    soup = BeautifulSoup(main_page, "html.parser")
    sleep(4)
    csv = open('csv.csv', 'w')
    print('stage4')

    print (soup.find_all("div", class_="_2Q_mv"))
    if soup.find_all("div", class_="_2Q_mv") == []:
        csgo_read(csgo_map, csgonamemap1, csgo_win, z)
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
    
    csv.close()
    driver.quit()
app = Flask(__name__)
@app.route('/csgo', methods=['GET'])
def index():
    """Это докстринг модуля, он однострочный."""
    return render_template('index.html')
@app.route('/csgo', methods=['POST'])
def index_post():
    """Это докстринг модуля, он однострочный."""
    csgo_map = request.form.get('csgo_map')
    print('STAGE1' + csgo_map)
    csgo_map = csgomapname(csgo_map)
    print('STAGE2' + csgo_map)
    csgonamemap1, csgo_win, z = csgonamemap(csgo_map)
    csgo_read(csgo_map, csgonamemap1, csgo_win, z)
    return send_file(os.path.join("." , "csv.csv"), as_attachment=True)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
