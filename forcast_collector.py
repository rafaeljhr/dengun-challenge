import json
import requests
from bs4 import BeautifulSoup

url = 'https://weather.com/weather/hourbyhour/l/ISXX0026:1:IS'

cookies = {'unitOfMeasurement': 'm'}   # found this by inspecting the page and checking how to change the units. Found a cookie with this

response = requests.get(url, headers={'Cache-Control': 'no-cache'}, cookies=cookies) #Cache-Control is used for syncing html source and script

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
        PRECIP = div_PRECIP.find('span').text
        
        WIND_spans   = div_WIND.find('span').find_all('span')
        WIND_direction = WIND_spans[0].text
        WIND_value = WIND_spans[1].text
        
        WIND = WIND_direction + " " + WIND_value + " km/h"
        
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
        HUMIDITY = ul_childs[2].find('div').find_all('span')[1].text
        
        # print("FEEL: ", FEEL_celsius)
        # print("HUMIDITY: ", HUMIDITY)
        
        
        forcast_json = { TIME: {'DESC': DESC,
                        'TEMP': TEMP,
                        'FEEL': FEEL,
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
    
    


# aa