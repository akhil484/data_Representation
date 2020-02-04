import urllib.request
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def scrape_data():

	url1="https://www.tapology.com/search/mma-event-figures/ppv-pay-per-view-buys-buyrate"
	ufc_link="https://www.ufc.com/athletes/all"



	row1=[]
	source1=urllib.request.urlopen(url1)
	soup1=BeautifulSoup(source1,"lxml")
	table1=soup1.select('table')[0]

	table1_row=table1.find_all('tr')
	for tr in table1_row:
		td=tr.find_all('td')
		temp=[i.text for i in td]
		row1.append(temp)
	row1=row1[1:]
	dic=dict()
	for r in row1:
		temp=''

		#To remove commas from amount
		for s in r[6]:
			if s!=',':
				temp=temp+s

		if int(temp)>1000000:
			temp1=r[2].split()
			for word in temp1:
				if word=='The' or re.match(r'[0-9vs]',word):    #remove unnecessary numbers and words from list
					continue

				elif word.isspace()==False:
					if word in dic:
						dic[word]=dic[word]+1
					else:
						dic[word]=1

	#Store name of fighter with highest key
	key_name=''
	value_num=0
	for key in dic:
		if dic[key]>value_num:
			key_name=key
			value_num=dic[key]


	def find(driver):
	    element = driver.find_element_by_xpath("//*[@id='block-mainpagecontent']/div/div/div[1]/div/div/ul/li/a")
	    if element:
	        return element
	    else:
	        return False



	#To click on load more button on the page
	driver=webdriver.Chrome(executable_path="/home/akhil/crawler/chromedriver_linux64/chromedriver")
	driver.get('https://www.ufc.com/athletes/all')
	delay = 7 #seconds

	while True:
	    try:
	        myElem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="block-mainpagecontent"]/div/div/div[1]/div/div/ul/li/a')))
	        print("found the btn")
	    except TimeoutException:
	        break

	    driver.execute_script("arguments[0].click()", myElem)
	    print('click')
	    driver.implicitly_wait(delay)
	    time.sleep(delay)
	    print('sleep')

	print("out")


	source = driver.page_source				#To store or save html page after clicking load more button

	#name_tree=urllib.request.urlopen(ufc_link)
	name_tree_request=BeautifulSoup(source,"lxml")
	link=''
	im=''
	fighters_info={}					#To store information of all fighters

	for i in name_tree_request.find_all('div',class_='c-listing-athlete-flipcard'):
		full_name=i.find('span',class_='c-listing-athlete__name').text
		first=full_name.split()
		sec=first[1]
		im=i.find('span',class_='c-listing-athlete__name')
		im=i.img['src']
		link=i.find('div',class_='c-listing-athlete-flipcard__action').a['href']
		fighters_info[sec]={}
		fighters_info[sec]['full_name']=full_name
		fighters_info[sec]['img']=im
		fighters_info[sec]['link']=link



	link_to_fighters_page=fighters_info[key_name]['link']
	fighters_image=fighters_info[key_name]['img']
	record=[]
	next_url="https://www.ufc.com"+link_to_fighters_page

	#print(next_url)
	source2=urllib.request.urlopen(next_url)
	soup2=BeautifulSoup(source2,"lxml")
	record_tree=soup2.find_all('div',class_='c-hero__headline-suffix')

	record=list(record_tree[0].text.split())

	fighters_name=fighters_info[key_name]['full_name']

	fighters_name=' '.join(fighters_name.split())
	fighters_record=' '.join(record)

	return fighters_name,fighters_record,dic

	
if __name__=='__main__':

	fighters_name,fighters_record,dic=scrape_data()