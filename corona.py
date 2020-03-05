import requests
import os
from requests import get
from bs4 import BeautifulSoup


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

countries = []
country2code = []
total_cases = []
new_cases = []
total_deaths = []
new_deaths = []
active_cases = []
total_recovered = []
criticals = []


url = "https://www.worldometers.info/coronavirus/#countries"

result = requests.get(url, verify=False)

soup = BeautifulSoup(result.text, "html.parser")
for country_table in soup.find_all('table', id='main_table_countries'):
    #print(country_table)
    for a in country_table.find_all('tr'):
        
        b =  a.find('td')
        if b is not None:
            countries.append(b.text)
            total_case = b.find_next('td')
            new_case = total_case.find_next('td')
            total_death = new_case.find_next('td')
            new_death = total_death.find_next('td')
            active_case = new_death.find_next('td')
            total_recover = active_case.find_next('td')
            critical = total_recover.find_next('td')
        
            total_cases.append(total_case.text)
            new_cases.append(new_case.text)
            total_deaths.append(total_death.text)
            new_deaths.append(new_death.text)
            active_cases.append(active_case.text)
            total_recovered.append(total_recover.text)
            criticals.append(critical.text)
        
f= open("tempfile.txt","w+")        
a = 0        
for i in countries:
    if i.strip() != "Total:":
        url2 = "https://www.iban.com/country-codes"
        result = requests.get(url2, verify=False)
        soup = BeautifulSoup(result.text, "html.parser")
        for country_table in soup.find_all('table', id='myTable'):
            for z in country_table.find_all('tr'):
                b =  z.find('td')
                if b is not None:
                    if b.text == i.strip():
                        twocode = b.find_next('td').text
                    if i.strip() == "S. Korea":
                        twocode = "KR"
                    if i.strip() == "Iran":
                        twocode = "IR"   
                    if i.strip() == "USA":
                        twocode = "US"                                                
                    if i.strip() == "U.K.":
                        twocode = "GB"
                    if i.strip() == "Taiwan":
                        twocode = "TW"                                                 
                    if i.strip() == "Netherlands":
                        twocode = "NL"                           
                    if i.strip() == "U.A.E.":
                        twocode = "AE"                           
                    if i.strip() == "Vietnam":
                        twocode = "VN"                           
                    if i.strip() == "Philippines":
                        twocode = "PH"                           
                    if i.strip() == "Russia":
                        twocode = "RU"                           
                    if i.strip() == "Dominican Republic":
                        twocode = "DO"                           
                    if i.strip() == "North Macedonia":
                        twocode = "MK"    
                    if i.strip() == "Diamond Princess":
                        twocode = "DP" 
     
        if total_cases[a].strip():
            f.write("case_total{country=\"" + twocode +"\"} " + total_cases[a].replace(',', '').strip() )
        if new_cases[a].strip():
            f.write("\ncase_new{country=\"" + twocode +"\"} " + new_cases[a].replace(',', '').strip() )
        if total_deaths[a].strip():
            f.write("\ndeath_total{country=\"" + twocode +"\"} " + total_deaths[a].replace(',', '').strip() )
        if new_deaths[a].strip():
            f.write("\ndeath_new{country=\"" + twocode +"\"} " + new_deaths[a].replace(',', '').strip() )
        if active_cases[a].strip():
            f.write("\ncase_active{country=\"" + twocode +"\"} " + active_cases[a].replace(',', '').strip() )
        if total_recovered[a].strip():
            f.write("\nrecovered_total{country=\"" + twocode +"\"} " + total_recovered[a].replace(',', '').strip() )
        if criticals[a].strip():
            f.write("\ncritical_total{country=\"" + twocode +"\"} " + criticals[a].replace(',', '').strip())
        f.write("\n")
        a = a+1

f.close()
cmd = 'cat tempfile.txt |  curl --data-binary @- http://d.fajri.net:9091/metrics/job/corona' 
os.system(cmd)