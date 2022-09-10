import csv
from datetime import *
from Hash import *

# create class for individual packages
class Package:
    def __init__(self, id, address, city, zipCode, deadline, weight):
        self.id = id
        self.address = address
        self.city = city
        self.zipCode = zipCode
        self.deadline = deadline
        self.weight = weight
        self.departureTime = datetime.now() # temporary departure time value will be updated in main at time of truck departure
        self.deliveryTime = datetime.now() # temporary delivery time value will be updated in main at time of truck departure

    def __str__(self):  # overwrite print(Package) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s" % (
        self.id, self.address, self.city,self.zipCode,self.deadline,self.weight)

# loadPackageData function is based on C950 recorded webinar "Getting Greedy, Who Moved My Data"
def loadPackageData(fileName, packageHash):

    with open(fileName, encoding='utf-8-sig') as packages:

        packageData = csv.reader(packages, delimiter=',')

        for package in packageData:
            pId = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pZipCode = int(package[3])
            pDeadline = package[4]
            pWeight = package[5]

            # package object
            p = Package(pId, pAddress, pCity, pZipCode, pDeadline, pWeight)

            # insert it into the hash table
            packageHash.insert(pId, p)

    return

# create class for individual destination

def loadDestinationData(fileName, destinationHash):

    with open(fileName, encoding='utf-8-sig') as destinations:

        destinationData = csv.reader(destinations, delimiter=',')

        index = 0

        for destination in destinationData:
            dAddress = destination[0]
            dZipCode = int(destination[1])

            # insert it into the hash table
            destinationHash.insert((dAddress,dZipCode),index)
            #test
            #print(destinationHash.search((dAddress,dZipCode)))
            index += 1

    return

def loadDistanceData(fileName, destinationHash):

    with open(fileName, encoding='utf-8-sig') as distances:
        distanceMatrix = list(csv.reader(distances, delimiter=','))

    return distanceMatrix