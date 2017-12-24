import pymysql.cursors
from selenium import webdriver
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import sys

import plotly.offline as offline
import plotly.graph_objs as go

#import numpy as np


class database:
    def __init__(self, u, p, h, d):
        self._page_url = "https://www.southwest.com/"
        # Connect to the database
        try:
            self._connection = pymysql.connect(host = h, user = u, password = p, db = d, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        except:
            print("ERROR")
            exit()

    def __del__(self):
        try:
            self._conection.close()
            print("")
        except:
            print("")

    def _getActiveFutureJobs(self):
        try:
            with self._connection.cursor() as cursor:
                # Read All future and active jobs within 6 months
                sql = "SELECT j.job_id, j.day, j.dep, j.arr, j.class_type, j.status, c.code as dep, c2.code as arr FROM `job` j "
                sql += "INNER JOIN `city` c ON c.city_id = j.dep "
                sql += "INNER JOIN `city` c2 ON c2.city_id = j.arr "
                sql += "WHERE j.status=%s AND j.day >= CURDATE() AND j.day < DATE_ADD(now(), INTERVAL 6 MONTH);"
                cursor.execute(sql, "ACTIVE")
                result = cursor.fetchall()
                return result
        except:
            print("error getActiveFutureJobs")
            return None

    def _getJobs(self):
        try:
            with self._connection.cursor() as cursor:
                # Read All future and active jobs within 6 months
                sql = "SELECT j.job_id, j.day, j.dep, j.arr, j.class_type, j.status, c.code as dep, c2.code as arr FROM `job` j "
                sql += "INNER JOIN `city` c ON c.city_id = j.dep "
                sql += "INNER JOIN `city` c2 ON c2.city_id = j.arr;"
                cursor.execute(sql,)
                result = cursor.fetchall()
                return result
        except:
            print("error _getJobs")
            return None

    def _saveFlightPrices(self, job):
        DEPARTURE = job["c.dep"]
        ARRIVAL = job["c2.arr"]
        try:
            DEPART_DATE = job["day"].strftime("%m/%d/%Y")
        except:
            print("Date conversion error")
            exit()
        FLIGHT_TYPE = job["class_type"]

        # Open Headless Chrome or Regular Chrome
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=options)
        except:
            exit()

        try:
            print("Job: " + DEPARTURE + " to " + ARRIVAL + " on " + DEPART_DATE + " class: " + FLIGHT_TYPE)
            # Open Itenerary Page
            browser.get(self._page_url)
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

        except NoSuchElementException:
            print("Can't find element in submission form")
            browser.close()
            return

        try:
            print("--Submitting Request For Flights...")
            submitBtn.click()
        except:
            print("Error Submitting Request for Flights")
            browser.close()
            return


        try:
            numDepartFlights = len(browser.find_elements_by_xpath('//*[@id=\"faresOutbound\"]/tbody/tr'))
        except NoSuchElementException:
            print("Can't find number of flights element")
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
                continue

            try:
                # Flight Number
                flightNumCell = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_" + str(i) + "\"]/td[3]/div/span/span/span[2]/a").text
                flightNum = flightNumCell.split()[0]
            except NoSuchElementException:
                print("Can't find flight cell.")
                continue

            try:
                # Depart time
                departTime = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i) + "\"]/td[1]/div[2]/span").text.replace("\n", " ")
                departTime = departTime.split()
                departTime = departTime[0] + " " + departTime[1].lower()
            except NoSuchElementException:
                print("Can't find depart time cell.")
                continue

            try:
                # Arrival time
                arrivalTime = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i) + "\"]/td[2]/div/span").text.replace("\n", " ")
                arrivalTime = arrivalTime.split()
                arrivalTime = arrivalTime[0] + " " + arrivalTime[1].lower()

            except NoSuchElementException:
                print("Can't find arrival time cell.")
                continue

            try:
                # Duration
                duration = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_" + str(i) + "\"]/td[5]/div/span").text
            except NoSuchElementException:
                print("Can't find duration cell.")
                continue
            try:
                # Routing ... Nonstop or not? True/False
                routingCell = browser.find_element_by_xpath("//*[@id=\"outbound_flightRow_"+ str(i)+ "\"]/td[4]/div/span[2]/a").text
            except NoSuchElementException:
                print("Can't find nonstop cell.")
                continue

            isNonstop = 0
            if (routingCell.split()[0] == "Nonstop"):
                isNonstop = 1

            # Save Results
            try:
                self._saveFlightPrice(DEPARTURE, ARRIVAL, DEPART_DATE, FLIGHT_TYPE, flightNum, departTime, arrivalTime, duration, price, isNonstop, job["job_id"])
            except:
                print("ERROR SAVING")
                print(sys.exc_info()[0])
        browser.close()

    def _getCityIdFromCode(self, city_code):
        try:
            with self._connection.cursor() as cursor:
                # Read city id from code
                sql = "SELECT c.city_id, c.code FROM `city` c "
                sql += "WHERE c.code=%s;"
                cursor.execute(sql, city_code)
                result = cursor.fetchone()
                return result["city_id"]
        except:
            print("error _getCityIdFromCode:")
            print("sql: " + sql)
            print("city_code: " + city_code)
            return None

    def _getFlightIdFromData(self, num, dep, arr, dur, nonstop, job_id):
        # dep_id = self._getCityIdFromCode(dep)
        # arr_id = self._getCityIdFromCode(arr)
        try:
            with self._connection.cursor() as cursor:
                # Read city id from code
                sql = "SELECT flight_id FROM `flight` "
                sql += "WHERE num=%s AND dep=%s AND arr=%s AND dur=%s AND nonstop=%s AND job=%s;"
                # print(num, dep, arr, dur, nonstop, job_id)
                cursor.execute(sql, (num, dep, arr, dur, nonstop, job_id))
                result = cursor.fetchone()
                return result['flight_id']
        except:
            return  None
            #SELECT flight_id FROM `flight` WHERE num=1095 AND dep="05:25:00" AND arr="06:40:00" AND dur="3h 15m" AND nonstop=1 AND job=1;

    def _findOrCreate(self, num, dep, arr, dur, nonstop, job_id):
        depTime = time.strftime("%R", time.strptime(dep, "%I:%M %p"))
        arrTime = time.strftime("%R", time.strptime(arr, "%I:%M %p"))
        flight_id = self._getFlightIdFromData( num, depTime, arrTime, dur, nonstop, job_id)
        if flight_id != None:
            return flight_id
        else:
            # Add flight
            try:
                num = int(num)
            except:
                print("TypeError for integers: _saveFlight()")
                exit()

            try:
                with self._connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO flight (num, dep, arr, dur, nonstop, job) VALUES "
                    sql += "(%s, %s, %s, %s, %s, %s);"
                    cursor.execute(sql, (num, depTime, arrTime, dur, nonstop, job_id))
                self._connection.commit()
            except:
                print("ERROR: _saveFlight")
                return None
            return self._getFlightIdFromData( num, depTime, arrTime, dur, nonstop, job_id)


    def _saveFlightPrice(self, dep, arr, day, type, num, depTime, arrTime, dur, price, nonstop, job_id):
        # Check if flight is in database and get id
        flight_id = self._findOrCreate( num, depTime, arrTime, dur, nonstop, job_id)

        # Save price
        try:
            price = int(price)
        except:
            print("TypeError for integers: _saveFlightPrice()")
            exit()

        try:
            with self._connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO price (price, flight) VALUES "
                sql += "(%s, %s);"
                cursor.execute(sql, (price, flight_id))
            self._connection.commit()
            print("SUCCESS: _saveFlightPrice")
        except:
            print("ERROR: _saveFlightPrice")

    def _getPricesByFlightId(self, flight_id):
        try:
            with self._connection.cursor() as cursor:
                # Read
                sql = "SELECT created_on, price FROM `price` "
                sql += "WHERE flight=%s;"
                cursor.execute(sql, (flight_id))
                result = cursor.fetchall()
                return result
        except:
            return  None

    def _getFlightsByJobId(self, job_id):
        try:
            with self._connection.cursor() as cursor:
                # Read city id from code
                sql = "SELECT flight_id, num, dep, arr, dur, nonstop FROM `flight` "
                sql += "WHERE job=%s;"
                cursor.execute(sql, (job_id))
                result = cursor.fetchall()
                return result
        except:
            return  None

    def _graphJob(self, job):
        # print("GRAPHING JOB")
        offline.init_notebook_mode()

        # Job Info
        departCity = job["c.dep"]
        arriveCity = job["c2.arr"]
        day = job["day"]
        class_type = job["class_type"]

        # Graph File Name
        graph_name = "graph_"
        graph_name += departCity + "_"
        graph_name += arriveCity + "_"
        graph_name += str(day) + "_"
        graph_name += class_type

        flights = self._getFlightsByJobId( job["job_id"] )

        # Get flight prices
        data = []
        for f in flights:
            data_x = []
            data_y = []

            departTime = f["dep"] + datetime.strptime("2000-01-01", "%Y-%M-%d")
            data_name = (str(f["num"]) + " @ " + departTime.strftime("%I:%M %p")).lower()

            if f["nonstop"] == 1:
                data_name += (" ***")

            # Get Date and Prices Array for this flight
            date_price = self._getPricesByFlightId(f["flight_id"])
            for i in date_price:
                data_x.append(i["created_on"])
                data_y.append(int(i["price"]))

            if f["nonstop"] == 1:
                vis = True
            else:
                vis = "legendonly"

            data.append(
                go.Scatter(
                    x = data_x,
                    y = data_y,
                    mode = 'lines+markers',
                    name = data_name,
                    visible = vis
                )
            )
        # Graph Data
        layout = go.Layout(
            title=departCity + " to " + arriveCity + " on " + str(day),
            font=dict(size=16),
            width=800,
            height=640
        )

        offline.plot(
            { 'data': data, 'layout': layout},
            image='png'
        )
        return


    def graphJobs(self):
        print("Select job to graph: ")
        # Get jobs
        result = self._getJobs()

        # Graph Selection MENU
        s = 0
        while s < 1 or s > n+1:
            n = len(result)
            for i in range(0, n):
                print(str(i+1) + " - " + result[i]["c.dep"] + " to " + result[i]["c2.arr"] + " on " + str(result[i]["day"]))
            print(str(n+1) + " - Back")

            prompt = ">> "
            s = raw_input(prompt)
            try:
                s = int(s)
            except:
                s = -1
        s -= 1  # Adjust selection s to match zero-indexing

        # Graph selected job
        self._graphJob(result[s])


    def runPriceChecks(self):
        result = self._getActiveFutureJobs()
        for i in result:
            self._saveFlightPrices(i)




# try:
#     with connection.cursor() as cursor:
#     # Create a new record
#     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
#
# # connection is not autocommit by default. So you must commit to save
# # your changes.
# connection.commit()
