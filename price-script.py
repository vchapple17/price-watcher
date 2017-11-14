from selenium import webdriver
from datetime import date, datetime, time
from selenium.webdriver.common.keys import Keys

print("Loading...")
filename = "flight_log.csv"

page_url = "https://www.southwest.com/"
DEPARTURE = "MCI"
ARRIVAL = "LAS"
DEPART_DATE = "02/02/2018"
SCREENSHOT = "/Users/valchapple/Documents/price-watcher/screen.png"
FLIGHT_TYPE = "C"   # A: Business Select, B: Anytime, C: Wanna Get Away

class FlightInfo:
    def __init__(self, departureCity, arrivalCity, departDate, departTime, arriveTime, duration, cost, isNonstop, flightNo):
        self.departureCity = departureCity
        self.arrivalCity = arrivalCity
        self.departDate = departDate
        self.departTime = departTime
        self.arriveTime = arriveTime
        self.duration = duration
        self.cost = cost
        self.nonstop = isNonstop
        self.flightNo = flightNo
    def getDepartureCity(self):
        return self.departureCity
    def getArrivalCity(self):
        return self.arrivalCity
    def getDepartDate(self):
        return self.departDate
    def getDepartTime(self):
        return self.departTime
    def getArriveTime(self):
        return self.arriveTime
    def getDuration(self):
        return self.duration
    def getCost(self):
        return self.cost
    def isNonstop(self):
        return self.nonstop
    def getFlightNo(self):
        return self.flightNo

def saveFlightInfo(info, file):
    row = str(datetime.now())
    row += ", "
    row += info.getDepartureCity()
    row += ", "
    row += info.getArrivalCity()
    row += ", "
    row += info.getDepartDate()
    row += ", "
    row += info.getFlightNo()
    row += ", "
    row += info.getDepartTime()
    row += ", "
    row += info.getArriveTime()
    row += ", "
    row += info.getDuration()
    row += ", "
    row += str(info.getCost())
    if (info.isNonstop()):
        row += ", nonstop"
    row += "\n"
    file.write(row)



# Open Headless Chrome or Regular Chrome
try:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
except:
    browser = webdriver.Chrome()

# Open Itenerary Page
browser.get(page_url)
print("Filling out Request For Flights.")
radio = browser.find_element_by_xpath('//*[@id=\"trip-type-one-way\"]')
radio.send_keys(" ")
browser.find_element_by_id('air-city-departure').clear()
browser.find_element_by_id('air-city-departure').send_keys(DEPARTURE)
browser.find_element_by_id('air-city-arrival').clear()
browser.find_element_by_id('air-city-arrival').send_keys(ARRIVAL)
browser.find_element_by_id('air-date-departure').clear()
browser.find_element_by_id('air-date-departure').send_keys(DEPART_DATE)
submitBtn = browser.find_element_by_id('jb-booking-form-submit-button')
browser.get_screenshot_as_file(SCREENSHOT)
print("Submitting Request For Flights.")
submitBtn.click()

numDepartFlights = len(browser.find_elements_by_xpath('//*[@id=\"faresOutbound\"]/tbody/tr'))
for i in range(1, numDepartFlights+1):

    # Price
    priceCellId = "Out" + str(i) + FLIGHT_TYPE + "Container"
    price = browser.find_element_by_xpath("//*[@id=\"" + priceCellId + "\"]/div/div[2]/div/label[1]").text
    price = price.replace("$","")
    price = int(price)

    # Flight Number
    flightNumCell = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_" + str(i) + "\"]/td[3]/div/span/span/span[2]/a").text
    flightNum = flightNumCell.split()[0]
    
    #//*[@id="outbound_flightRow_1"]/td[3]/div/span/span[3]/span[2]/a

    print(flightNum)
    # Depart time
    departTime = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i) + "\"]/td[1]/div[2]/span").text

    # Arrival time
    arrivalTime = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i) + "\"]/td[2]/div/span").text

    # Duration
    duration = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_" + str(i) + "\"]/td[5]/div/span").text

    # Routing ... Nonstop or not? True/False
    routingCell = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i)+ "\"]/td[4]/div/span[2]/a").text

    isNonstop = False
    if (routingCell.split()[0] == "Nonstop"):
        isNonstop = True

    # Save Results
    flight = FlightInfo( DEPARTURE, ARRIVAL, DEPART_DATE, departTime, arrivalTime, duration, price, isNonstop, flightNum)
    csvFile = open(filename, "a")
    saveFlightInfo( flight, csvFile )
    csvFile.close()

browser.close()
