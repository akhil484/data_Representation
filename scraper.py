import urllib.request
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
url="http://boxing.nv.gov/results/Top_MMA_Gates/"
url1="https://www.tapology.com/search/mma-event-figures/ppv-pay-per-view-buys-buyrate"
ufc_link="https://www.ufc.com/athletes/all"






source=urllib.request.urlopen(url)
soup=BeautifulSoup(source,"lxml")
table=soup.find('table')
table_rows=soup.find_all('tr')
row=[]
row1=[]
for tr in table_rows:
	td=tr.find_all('td')
	temp=[i.text for i in td]
	row.append(temp)
row=row[1:36]





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
			if word=='The' or re.match(r'[0-9vs]',word):
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

"""driver=webdriver.Chrome(executable_path="/home/akhil/crawler/chromedriver_linux64/chromedriver")

driver.get('https://www.ufc.com/athletes/all')
driver.implicitly_wait(30)
element = driver.find_element_by_xpath("//*[@id='onetrust-close-btn-container']/a").click()
driver.implicitly_wait(3000)
element = driver.find_element_by_xpath("/html/body/div[1]/div/a").click()
topics_xpath="//*[@id='block-mainpagecontent']/div/div/div[1]/div/div/ul/li/a"
WebDriverWait(driver, 10000).until(expected_conditions.visibility_of_element_located((By.XPATH,topics_xpath)))
#element = driver.find_element_by_xpath("//*[@id='onetrust-close-btn-container']/a").click()
#driver.implicitly_wait(3000)
#element = driver.find_element_by_xpath("/html/body/div[1]/div/a").click()
with open('temp.html', 'w') as f:
    f.write(driver.page_source)
#element = driver.find_element_by_xpath("//a[@title='Go to next page']").click()

element = driver.find_element_by_xpath("//*[@id='block-mainpagecontent']/div/div/div[1]/div/div/ul/li/a").click()
hover = ActionChains(driver).move_to_element(element)
hover.perform().click()
"""
with open('Athletes - All _ UFC.html', 'r') as f:
    source_code = f.read()
name_tree=urllib.request.urlopen(ufc_link)
name_tree_request=BeautifulSoup(source_code,"lxml")
link=''
im=''
fighters_info={}
#temp_list=name_tree_request.find_all('div',class_='c-listing-athlete-flipcard')
for i in name_tree_request.find_all('div',class_='c-listing-athlete-flipcard'):
	full_name=i.find('span',class_='c-listing-athlete__name').text
	first=full_name.split()
	sec=first[1]
	#print(sec)
	im=i.find('span',class_='c-listing-athlete__name')
	im=i.img['src']
	link=i.find('div',class_='c-listing-athlete-flipcard__action').a['href']
	fighters_info[sec]={}
	fighters_info[sec]['full_name']=full_name
	fighters_info[sec]['img']=im
	fighters_info[sec]['link']=link
"""athlete_name=[]
for name in temp_list:
	athlete_name.append(name.a['href'])"""
#link=fighters_info[key_name]['link']
link_to_fighters_page=fighters_info[key_name]['link']
record=[]
next_url=link_to_fighters_page
source2=urllib.request.urlopen(next_url)
soup2=BeautifulSoup(source2,"lxml")
record_tree=soup2.find_all('div',class_='c-hero__headline-suffix')
for r in record_tree:
	record.append(r.text)

