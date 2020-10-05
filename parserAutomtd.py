import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from result import result

outfile=open("standfordOut.txt","w")
driver = webdriver.Firefox()
driver.get("http://nlp.stanford.edu:8080/parser/index.jsp")

var = 1
while (var == 1) :
    inFile = str(input("Enter a sentence or a .txt file :"))
    if (str(inFile)=="quit"):
        print ("Good bye!")
        driver.quit()
        outfile.close()
        break
    elif (inFile.endswith(".txt")):
        input_file1=open(inFile,"r")
        input_data=input_file1.readlines()
        for data in input_data:
            data=str(data.strip())
            try:
                txtArea=driver.find_element_by_id("query")
                txtArea.clear()
                time.sleep(1)
                txtArea.send_keys(data)
                time.sleep(1)
                driver.find_element_by_id("parseButton").click()
                time.sleep(1)
                out=driver.find_element_by_id('parse').text
                parse_broke=out.split("\n")
                fin=parse_broke[0].strip()
                for s in parse_broke[1::]:
                    fin=fin+" "+s.strip()
                outfile.write(fin)
                outfile.write("\n")
            except:
                pass
        input_file1.close()
        break
    else:
        data=str(inFile.strip())
        try:
            txtArea=driver.find_element_by_id("query")
            txtArea.clear()
            time.sleep(1)
            txtArea.send_keys(data)
            time.sleep(1)
            driver.find_element_by_id("parseButton").click()
            time.sleep(1)
            out=driver.find_element_by_id('parse').text
            parse_broke=out.split("\n")
            fin=parse_broke[0].strip()
            for s in parse_broke[1::]:
                fin=fin+" "+s.strip()
            outfile.write(fin)
            outfile.write("\n")
        except:
            pass
outfile.close()
driver.quit()
result("standfordOut.txt")