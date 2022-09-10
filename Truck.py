# Truck class that will hold packages and track truck's location

from CSV import *
from datetime import *

class Truck:
    def __init__(self, departureTime):
        self.location = ('4001 South 700 East',84107)
        self.packageList = set()
        self.departureTime = departureTime
        self.milesDriven = 0
        self.truckSpeed = .005 # 18 miles per hour converted to miles per second

    def addPackage(self, package):
        self.packageList.add(package)

    def dropPackage(self, package):
        self.packageList.remove(package)

    def getPackage(self, package):
        if package in self.packageList:
            return package
        else:
            return None

    def add_seconds(self, distance):
        additionalSeconds = distance / self.truckSpeed
        return self.departureTime + timedelta(0,additionalSeconds)