#implement logging to track reservations
import logging
logging.basicConfig(filename='ReservationLog.log',
                  filemode='a',
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  level=logging.DEBUG)

class Reservation:
    def __init__(self,start_time,end_time,date):#we take the user ID from the user that is currently logged in
        self.__start_time=start_time
        self.__end_time=end_time
        self.__date=date

    def get_ID(self):
        return self.__ID

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_date(self):
        return self.__date

    # Setter methods
    def set_ID(self, ID):
        self.__ID = ID

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time

    def set_date(self, start_date):
        self.__date = start_date


