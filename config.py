import pymysql.cursors

class database:
    def __init__(self, u, p, h, d):
        # Connect to the database
        try:
            self._connection = pymysql.connect(host = h, user = u, password = p, db = d, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        except:
            print("ERROR")
            exit()

    def __del__(self):
        try:
            self._conection.close()
            print("connection closed.")
        except:
            print("connection closed.")
