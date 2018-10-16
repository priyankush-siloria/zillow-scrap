from selenium import webdriver
import time
import re


driver = webdriver.Chrome("/home/rajinder/projects/morgan/chromedriver")
output_list = []

def check_for_captcha(driver):
	if _is_element_displayed(driver, "captcha-container", "class"):
		print("\nCAPTCHA!\n"\
			  "Manually complete the captcha requirements.\n"\
			  "Once that's done, if the program was in the middle of scraping "\
			  "(and is still running), it should resume scraping after ~30 seconds.")
		_pause_for_captcha(driver)

def _pause_for_captcha(driver):
	while True:
		time.sleep(30)
		if not _is_element_displayed(driver, "captcha-container", "class"):
			break

def _is_element_displayed(driver, elem_text, elem_type):
	if elem_type == "class":
		try:
			out = driver.find_element_by_class_name(elem_text).is_displayed()
		except:
			out = False
	elif elem_type == "css":
		try:
			out = driver.find_element_by_css_selector(elem_text).is_displayed()
		except:
			out = False
	else:
		raise ValueError("arg 'elem_type' must be either 'class' or 'css'")
	return(out)

def scrapingFunction(driver):
	all_house_div = driver.find_elements_by_xpath(".//div[@class='zsg-photo-card-content zsg-aspect-ratio-content']")
	for item in all_house_div:
		data = {}
		try:
			item.click()
			time.sleep(10)
			heading = driver.find_element_by_xpath(".//h1[@class='notranslate']").text
			bedrooms = driver.find_element_by_xpath(".//span[@class='addr_bbs']").text
			ownerdata = driver.find_elements_by_xpath(".//div[@class='info flat-star-ratings sig-col']")[-1]
			owner_number = ownerdata.find_element_by_xpath(".//span[@class='snl phone']").text
			data["heading"] = heading
			data["bedrooms"] = bedrooms
			data["number"] = owner_number
			output_list.append(data)
			driver.find_element_by_xpath(".//button[@class='zsg-toolbar-button zsg-button hc-back-to-list']").click()
			time.sleep(10)
		except Exception as e:
			continue

def writingFile():
	for items in output_list:
		bed = re.findall(r"[-+]?\d*\.\d+|\d+", items["bedrooms"])[0]
		with open('output.csv', 'a+') as file:
			file.write((items["heading"]).replace('\n', ''))
			file.write("#")
			if bed == "3" or bed == "4":
				file.write(items["bedrooms"])
			else:
				file.write("not available")
			file.write("#")
			file.write(items["number"])
			file.write("\n")

try:
	driver.get("https://www.zillow.com/homes/fsbo/Gwinnett-County-GA/house_type/2314_rid/3-_beds/1-_baths/200000-400000_price/796-1592_mp/1000-_size/globalrelevanceex_sort/34.294665,-83.145905,33.61805,-84.933929_rect/8_zm/0_mmm/")
	check_for_captcha(driver)
	time.sleep(3)
	li_list = driver.find_elements_by_xpath(".//ul[@id='property-sort-control']/li")
	li_list[1].click()
	while True:
		time.sleep(15)
		scrapingFunction(driver)
		try:
			driver.find_element_by_xpath(".//li[@class='zsg-pagination-next']").click()
			continue
		except Exception as e:
			break
	writingFile()
	driver.quit()
except Exception as e:
	driver.quit()
	raise e
