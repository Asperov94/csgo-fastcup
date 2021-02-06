from flask import Flask
from flask import request
from flask import render_template
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from time import sleep
from flask import send_file
import re
import requests


def csgonamemap(csgo_map):
    driver = webdriver.Chrome()
    driver.get(csgo_map)
    main_page = driver.page_source

    soup = BeautifulSoup(main_page, "html.parser")
    sleep(2)
    driver.quit()
    return soup.findAll("div", {"class": "_2Fhou"})[2].text



def csgomapname(csgo_map):
    result = re.findall(r"match(.*?)/", csgo_map)
    result = 'https://csgo.fastcup.net/match' + ''.join(result)
    print (str(result))
    return result

def csgo_read(csgo_map, csgonamemap):
    #===VARIABLES===
    user=kill=dead=assist=''
    #===---===
    csgo_map = csgo_map + '/stats'
    driver = webdriver.Chrome()
    driver.get(csgo_map)
    main_page = driver.page_source
    try:
        os.remove('stat.txt')
    except OSError:
        pass
    try:
        os.remove('csv.csv')
    except OSError:
        pass
    
    with open("stat.txt", "w") as file:
    	file.write(main_page)

    stat = open('stat.txt', 'r')

    soup = BeautifulSoup(stat, "html.parser")

    user_all = soup.findAll("div", {"class": "_2Q_mv"})
    csv = open('csv.csv', 'w')
    for i in user_all:
        user=i.find("span", class_="_38-ZC")
        if user == None:
            user = 'USER'
        else:
        	user=i.find("span", class_="_38-ZC").text
        kill=i.find("div", class_="_3UiPH _2SMgu").text
        dead=i.find("div", class_="_3UiPH _1Fe8v").text
        assist=i.find("div", class_="_3UiPH _26k4_")
        if assist == None:
            assist = 'A'
        else:
        	assist=i.find("div", class_="_3UiPH _26k4_").text
        csv.write(f'{user};{kill};{dead};{assist};{csgonamemap} \n' )
    csv.close()
    stat.close()
    sleep(5)
    driver.quit()
    

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    csmap=''
    csgo_map = request.form.get('csgo_map')
    print (str(csgo_map))
    csgo_map = csgomapname(csgo_map)
    csgonamemap1 = csgonamemap(csgo_map)

    csgo_read(csgo_map, csgonamemap1)

    return send_file(os.path.join("." , "csv.csv"), as_attachment=True)


if __name__ == '__main__':
    app.run(port=5000)