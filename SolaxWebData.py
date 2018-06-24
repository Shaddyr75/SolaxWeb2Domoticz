import requests
import urllib
from lxml import html
from bs4 import BeautifulSoup
import time

USERNAME = "Your Username"
PASSWORD = "Your Password"

URL = "https://www.solax-portal.com/dz/User/your status domain"
LOGIN_URL = "https://www.solax-portal.com/home/login?"

def main():
    session_requests = requests.session()
    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='ValidateCode']/@value")))[0]
    authenticity_url = list(set(tree.xpath("//input[@name='url']/@value")))[0]
    # Create payload
    payload = {
        'username': USERNAME, 
        'password': PASSWORD,
        'ValidateCode' : authenticity_token,
        'url': authenticity_url,       
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    
    # Scrape url
    result = session_requests.get(URL)
    
    tree = html.fromstring(result.content)
    WebData = result.content
    
    SolaxData =[]
    soup = BeautifulSoup(WebData,"html.parser")
    table = soup.find("table",{"class":"table table-hover table-striped"})
       
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        SolaxData.append([ele for ele in cols if ele])        
    
    iCurrent = SolaxData[0]
    iVoltage = SolaxData[1]
    OCurrentVoltage = SolaxData[2]
    Energy = SolaxData[3]
    iPower = SolaxData[4]
    Power = SolaxData[5]
    NotUsed = SolaxData [6]
    #debug purposes
    #print(iCurrent)
    #print(iVoltage)
    #print(OCurrentVoltage)
    #print(Energy)
    #print(iPower)
    #print(Power)
    
    #Additional information and update
    SolaxData2 =[]
    table = soup.find("div",{"class":"table col-md-12"})
       
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('th')
        cols = [ele.text.strip() for ele in cols]
        SolaxData2.append([ele for ele in cols if ele])     
    InverterSerial = SolaxData2[0]
    LastUpdate = SolaxData2[9]
       
    #upload to Domoticz 
    #IDX Virtual sensors
    IDXPowerNow = "XX"
    IDXPowerPV1 = "XX"
    IDXPowerPV2 = "XX"
    IDXEnergyAll = "XX"
    IDXEnergyToday = "XX"
    IDXOutputCurrent = "XX"
    IDXNetVolt = "XX"
    IDXVoltPV1 = "XX"
    IDXVoltPV2 = "XX"
    IDXCurrentPV1 = "XX"
    IDXCurrentPV2 = "XX"
    print(Energy[3].replace("kWh",""))
    EnergyConvert1 = 1000*float(Energy[3].replace("kWh",""))
    EnergyConvert2 = 1000*float(Energy[1].replace("kWh",""))
    
    #send to Domoticz
    
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXPowerNow) + "&nvalue=0&svalue=" + str(float(Power[1].replace("W",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXPowerPV1) + "&nvalue=0&svalue=" + str(float(iPower[1].replace("W",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXPowerPV2) + "&nvalue=0&svalue=" + str(float(iPower[3].replace("W",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXEnergyAll) + "&nvalue=0&svalue=" + str(EnergyConvert1))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXEnergyToday) + "&nvalue=0&svalue=" + str(EnergyConvert2))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXOutputCurrent) + "&nvalue=0&svalue=" + str(float(OCurrentVoltage[1].replace("A",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXNetVolt) + "&nvalue=0&svalue=" + str(float(OCurrentVoltage[3].replace("V",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXVoltPV1) + "&nvalue=0&svalue=" + str(float(iVoltage[1].replace("V",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXVoltPV2) + "&nvalue=0&svalue=" + str(float(iVoltage[3].replace("V",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXCurrentPV1) + "&nvalue=0&svalue=" + str(float(iCurrent[1].replace("A",""))))
    time.sleep(0.5)
    httpresponse= urllib.request.urlopen("http://YOUR DOMOTICZ:8080/json.htm?type=command&param=udevice&idx=" + str(IDXCurrentPV2) + "&nvalue=0&svalue=" + str(float(iCurrent[3].replace("A",""))))
if __name__ == '__main__':
    main()
