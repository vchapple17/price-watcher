from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from CONSTANTS import CONSTANTS
#
# Flight class:
#
class FlightInfo:
    filename = CONSTANTS.FLIGHT_FILENAME()#"flight_log.csv"
    page_url = "https://www.southwest.com/"
    SCREENSHOT = "/Users/valchapple/Documents/price-watcher/screen.png"

    def __init__(self, departureCity, arrivalCity, departDate, flightType, flightNo, departTime, arriveTime, duration, cost, isNonstop ):
        self.departureCity = departureCity
        self.arrivalCity = arrivalCity
        self.departDate = departDate
        self.flightType = flightType
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
    def getFlightType(self):
        return self.flightType
    def getFlightNo(self):
        return self.flightNo
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


    #
    # Save Flight Info to Files
    #
    def save(self):
        row = str(datetime.now())
        row += ","
        row += self.getDepartureCity()
        row += ","
        row += self.getArrivalCity()
        row += ","
        row += self.getDepartDate()
        row += ","
        row += self.getFlightType()
        row += ","
        row += self.getFlightNo()
        row += ","
        row += self.getDepartTime()
        row += ","
        row += self.getArriveTime()
        row += ","
        row += self.getDuration()
        row += ","
        row += str(self.getCost())
        if (self.isNonstop()):
            row += ",nonstop"
        row += "\n"

        try:
            csvFile = open(FlightInfo.filename, "r")
        except:
            csvFile = open(FlightInfo.filename, "w")
            csvFile.write("Log Date,Departure,Arrival,Date,Type,Flight,DepartTime,ArriveTime, Duration,Cost,Nonstop\n")
            csvFile.close()
        csvFile = open(FlightInfo.filename, "a")
        csvFile.write(row)
        csvFile.close()
    #
    # Search for flight Info online
    #
    @staticmethod
    def saveFlightCosts(job):
        DEPARTURE = job.depart
        ARRIVAL = job.arrive
        DEPART_DATE = job.day
        FLIGHT_TYPE = job.flightType

        # Open Headless Chrome or Regular Chrome
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=options)
        except:
            browser = webdriver.Chrome()

        try:
            print("Job: " + DEPARTURE + " to " + ARRIVAL + " on " + DEPART_DATE + " class: " + FLIGHT_TYPE)
            # Open Itenerary Page
            browser.get(FlightInfo.page_url)
            print("--Filling out Request...")
            radio = browser.find_element_by_xpath('//*[@id=\"trip-type-one-way\"]')
            radio.send_keys(" ")
            browser.find_element_by_id('air-city-departure').clear()
            browser.find_element_by_id('air-city-departure').send_keys(DEPARTURE)
            browser.find_element_by_id('air-city-arrival').clear()
            browser.find_element_by_id('air-city-arrival').send_keys(ARRIVAL)
            browser.find_element_by_id('air-date-departure').clear()
            browser.find_element_by_id('air-date-departure').send_keys(DEPART_DATE)
            submitBtn = browser.find_element_by_id('jb-booking-form-submit-button')
            #browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
        except NoSuchElementException:
            print("Can't find element in submission form")
            browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
            browser.close()
            return

        print("--Submitting Request For Flights...")
        submitBtn.click()


        try:
            numDepartFlights = len(browser.find_elements_by_xpath('//*[@id=\"faresOutbound\"]/tbody/tr'))
        except NoSuchElementException:
            print("Can't find number of flights element")
            browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
            browser.close()
            return

        # Iterate through each flight
        for i in range(1, numDepartFlights+1):
            try:
                # Price
                priceCellId = "Out" + str(i) + FLIGHT_TYPE + "Container"
                price = browser.find_element_by_xpath("//*[@id=\"" + priceCellId + "\"]/div/div[2]/div/label[1]").text

                price = price.replace("$","")
                price = int(price)
            except NoSuchElementException:
                print("Can't find price cell: " + priceCellId )
                browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
                continue

            try:
                # Flight Number
                flightNumCell = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_" + str(i) + "\"]/td[3]/div/span/span/span[2]/a").text
                flightNum = flightNumCell.split()[0]
            except NoSuchElementException:
                print("Can't find flight cell.")
                browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
                continue

            try:
                # Depart time
                departTime = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i) + "\"]/td[1]/div[2]/span").text.replace("\n", " ")
            except NoSuchElementException:
                print("Can't find depart time cell.")
                browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
                continue

            try:
                # Arrival time
                arrivalTime = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i) + "\"]/td[2]/div/span").text.replace("\n", " ")
            except NoSuchElementException:
                print("Can't find arrival time cell.")
                browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
                continue

            try:
                # Duration
                duration = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_" + str(i) + "\"]/td[5]/div/span").text
            except NoSuchElementException:
                print("Can't find duration cell.")
                browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
                continue
            try:
                # Routing ... Nonstop or not? True/False
                routingCell = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i)+ "\"]/td[4]/div/span[2]/a").text
            except NoSuchElementException:
                print("Can't find nonstop cell.")
                browser.get_screenshot_as_file(FlightInfo.SCREENSHOT)
                continue

            isNonstop = False
            if (routingCell.split()[0] == "Nonstop"):
                isNonstop = True

            # Save Results
            flight = FlightInfo( DEPARTURE, ARRIVAL, DEPART_DATE, FLIGHT_TYPE, flightNum, departTime, arrivalTime, duration, price, isNonstop)
            flight.save()
        browser.close()

    # Return flight cost data
    @staticmethod
    def getJobData(job):
        # Validate Job Details

        # Try to open File to read
        try:
            csvFile = open(FlightInfo.filename, "r")
        except:
            print("error reading flight information.")
            exit()

        # Keep data that matches Job
        jobData = [[]]
        # Double array where each row is a flight
        # a flight is equivalent if:
            # job details match (city, city, date, type)
            # flightNum is same
            # departtime is same
            # arrivetime is same
            # duration is same
            # nonstop is same

        # Need to SORT!!!!!

        for line in csvFile.readline():
            cells = line.split(",")
            logDateStr = cells[0]   # Date of data point
            departCity = cells[1]
            arriveCity = cells[2]
            departDate = cells[3]
            flightType = cells[4]
            flightNum = cells[5]
            departTime = cells[6]
            arriveTime = cells[7]
            duration = cells[8]
            cost = cells[9]
            boolNonstop = cells[10]


            # Save Graph data

            #priceStr =

            # Type of FLight (A, B, C)



        pass
