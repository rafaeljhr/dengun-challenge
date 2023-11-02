import json
import math
import requests
from bs4 import BeautifulSoup

# Replace 'url' with the URL of the webpage you want to scrape
url = 'https://weather.com/weather/hourbyhour/l/ISXX0026:1:IS'

# Send an HTTP GET request to the URL
response = requests.get(url, headers={'Cache-Control': 'no-cache'}) #sync html source and script

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    index = 0 # the element in the html page I will be scraping

    details = soup.find('details', id='detailIndex'+str(index)) # if I want to get any other row, just need change the index, ex: detailIndex1, detailIndex2, ...

    if details:
        
        #### first element inside details
        
        summary = details.find('summary')
        div_DaypartDetails = summary.find('div')
        div_DetailsSummary = div_DaypartDetails.find('div')
        
        # fixing the time to be present in the pretended format, ex: 12:00 AM
        TIME_original = summary.find('h3').text #daypartName
        time_hour = TIME_original[:-3]
        
        if int(time_hour) <= 9:
            time_str = "0"+time_hour+":00"
        else :
            time_str = time_hour+":00"
        
        pm_am = (TIME_original[-2:]).upper()
        
        # fixed time format
        TIME = time_str + " " + pm_am
        
        all_childs = div_DetailsSummary.find_all('div')
         
        div_DESC   = all_childs[0]
        div_TEMP   = all_childs[1]
        div_PRECIP = all_childs[2]
        div_WIND   = all_childs[3]
        
        DESC   = div_DESC.find('span').text
        TEMP   = div_TEMP.find('span').contents[0].text
        TEMP_celsius = math.ceil((int(TEMP) - 32) * 5/9) if (int(TEMP) - 32) * 5/9 - int((int(TEMP) - 32) * 5/9) >= 0.5 else math.floor((int(TEMP) - 32) * 5/9)
        PRECIP = div_PRECIP.find('span').text
        
        WIND_spans   = div_WIND.find('span').find_all('span')
        WIND_1 = WIND_spans[0].text
        WIND_2 = WIND_spans[1].text
        WIND_2_KMH = math.ceil((float(WIND_2) * 1.60934)) if (float(WIND_2) * 1.60934) - int((float(WIND_2) * 1.60934)) >= 0.5 else math.floor((float(WIND_2) * 1.60934))
        
        WIND = WIND_1 + " " + str(WIND_2_KMH) + " km/h"
        
        # print("TIME: ", TIME)
        # print("DESC: ", DESC)
        # print("TEMP: ", TEMP_celsius)
        # print("PRECIP: ", PRECIP)
        # print("WIND: ", WIND)
        
        
        #### second element inside details
        
        # recursive=False avoids that the div inside the "summary" tag gets picked as the first div
        # I want python to see "summary" and "div" as the only childs of "details"
        div = details.find('div', recursive=False).find_all('div')[1].find('ul') 
        
        ul_childs = div.find_all('li')
        
        FEEL     = ul_childs[0].find('div').find_all('span')[1].contents[0].text
        FEEL_celsius = math.ceil((int(FEEL) - 32) * 5/9) if (int(FEEL) - 32) * 5/9 - int((int(FEEL) - 32) * 5/9) >= 0.5 else math.floor((int(FEEL) - 32) * 5/9)
        HUMIDITY = ul_childs[2].find('div').find_all('span')[1].text
        
        # print("FEEL: ", FEEL_celsius)
        # print("HUMIDITY: ", HUMIDITY)
        
        
        forcast_json = { TIME: {'DESC': DESC,
                        'TEMP': TEMP_celsius,
                        'FEEL': FEEL_celsius,
                        'PRECIP': PRECIP,
                        'HUMIDITY': HUMIDITY,
                        'WIND': WIND}}
        
        try:
            
            # Serializing json
            json_object = json.dumps(forcast_json, indent=2)
            
            # Writing to forcast_data.json
            with open("forcast_data.json", "w") as outfile:
                outfile.write(json_object)
                
            print("Writing to forcast_data.json SUCCEDED!")
            
        except:
            print("Writing to forcast_data.json FAILED!")
        
        
        
                    
    else:
        print("No details tag found.")
else:
    print("Failed to retrieve the web page.")