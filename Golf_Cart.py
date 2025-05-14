
class Golf_Cart:
    def __init__(self,plate_number,location):
        self.__plate_number=plate_number
        self.__location=location#College that the cart belong to


    def get_plate_number(self):
        return self.__plate_number

    # Getter for location
    def get_location(self):
        return self.__location

    # Setter for plate_number
    def set_plate_number(self, plate_number):
        self.__plate_number = plate_number

    # Setter for location
    def set_location(self, location):
        self.__location = location




