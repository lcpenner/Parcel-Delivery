'''
Author: Luke Penner
Student ID: 010102640
Date: 8 August 2022
'''

from Hash import *
from CSV import *
from Truck import *
from datetime import *
from Utility import *

# load packages to Hash Table that will contain package data
# package id is the key and package data is the value
packageHash = HashTable()
loadPackageData('WGUPS_Package_File_Scrubbed.csv', packageHash)

# load destinations to Hash Table that will contain indexes of associated address-zipCode combos
# address-zipCode is the key and index is the value
destinationHash = HashTable()
loadDestinationData('WGUPS_Address_Table.csv', destinationHash)

# load distance data into matrix that will contain distances between address locations based on indexes
distanceMatrix = loadDistanceData('WGUPS_Distance_Table_Scrubbed.csv', destinationHash)

# load first truck
truck1departureTime = datetime(2022, 12, 24, 8,0,0)
truck1 = Truck(truck1departureTime)

truck1.addPackage(packageHash.search(1))
truck1.addPackage(packageHash.search(6))
truck1.addPackage(packageHash.search(13))
truck1.addPackage(packageHash.search(14))
truck1.addPackage(packageHash.search(15))
truck1.addPackage(packageHash.search(16))
truck1.addPackage(packageHash.search(19))
truck1.addPackage(packageHash.search(20))
truck1.addPackage(packageHash.search(29))
truck1.addPackage(packageHash.search(30))
truck1.addPackage(packageHash.search(31))
truck1.addPackage(packageHash.search(34))
truck1.addPackage(packageHash.search(37))
truck1.addPackage(packageHash.search(40))


# load second truck
truck2departureTime = datetime(2022, 12, 24, 9, 10, 0)
truck2 = Truck(truck2departureTime)

truck2.addPackage(packageHash.search(3)) # can only be on truck 2
truck2.addPackage(packageHash.search(18)) # delayed on flight => must be on truck 2 to meet delivery deadline
truck2.addPackage(packageHash.search(25))
truck2.addPackage(packageHash.search(32))
truck2.addPackage(packageHash.search(33))
truck2.addPackage(packageHash.search(35))
truck2.addPackage(packageHash.search(36))
truck2.addPackage(packageHash.search(38))
truck2.addPackage(packageHash.search(39))


# receive update on package 9 delivery address at 10:20 and update hash table accordingly
packageUpdate = packageHash.search(9)
packageUpdate.address = '410 S State St'
packageUpdate.zipCode = 84111
packageHash.insert(9, packageUpdate)

# load third truck
truck3departureTime = datetime(2022, 12, 24, 11, 0, 0)
truck3 = Truck(truck3departureTime)

truck3.addPackage(packageHash.search(2))
truck3.addPackage(packageHash.search(4))
truck3.addPackage(packageHash.search(5))
truck3.addPackage(packageHash.search(7))
truck3.addPackage(packageHash.search(8))
truck3.addPackage(packageHash.search(9))
truck3.addPackage(packageHash.search(10))
truck3.addPackage(packageHash.search(11))
truck3.addPackage(packageHash.search(12))
truck3.addPackage(packageHash.search(17))
truck3.addPackage(packageHash.search(21))
truck3.addPackage(packageHash.search(22))
truck3.addPackage(packageHash.search(23))
truck3.addPackage(packageHash.search(24))
truck3.addPackage(packageHash.search(26))
truck3.addPackage(packageHash.search(27))
truck3.addPackage(packageHash.search(28))

# first truck route
# loop as long as there are packages in the truck's packageList

# time is 8:00 => update truck1 package departure times
for package in truck1.packageList:
    package.departureTime = datetime(2022, 12, 24, 8,0,0)
    packageHash.insert(package.id, package)

# start truck1 on route
while len(truck1.packageList)>0:
    # initialize the shortest distance to infinity
    closestStop = float('inf')

    # check for last stop
    if len(truck1.packageList) == 1:
        lastStop = True
    else:
        lastStop = False

    # iterate through each package in the package list and look for the closest address to the current location
    for package in truck1.packageList:

        # find index for package location and truck location
        packageLocationIndex = destinationHash.search((package.address,package.zipCode))
        truckLocationIndex = destinationHash.search(truck1.location)

        # find distance from truck's location to package location
        distance = float(distanceMatrix[packageLocationIndex][truckLocationIndex])

        # if the distance to the package location is closer than the closest stop, then update the closestStop distance
        # assign current package to be the next package drop
        if distance < closestStop:
            closestStop = distance
            nextPackageDropId = package.id

    # after iterating through for loop to find the next package to deliver:
    #   * add the distance to the next closest stop to the total distance
    #   * update current truck location to the next package drop
    #   * drop off the package
    #   * update the package delivery time

    truck1.milesDriven += closestStop
    truck1.location = (packageHash.search(nextPackageDropId).address,packageHash.search(nextPackageDropId).zipCode)
    truck1.packageList.remove(packageHash.search(nextPackageDropId))

    tempPackage = packageHash.search(nextPackageDropId)
    tempPackage.deliveryTime = truck1.add_seconds(truck1.milesDriven)

    packageHash.insert(tempPackage.id, tempPackage)

    # if it's the last stop, add the distance back to the hub
    if lastStop == True:
        truck1.milesDriven += float(distanceMatrix[0][destinationHash.search(truck1.location)])

# time is 11:00 => update truck2 packages to en route
for package in truck2.packageList:
    package.departureTime = datetime(2022, 12, 24, 11, 0, 0)
    packageHash.insert(package.id, package)

# start truck2 on route
while len(truck2.packageList)>0:
    # initialize the shortest distance to infinity
    closestStop = float('inf')

    # check for last stop
    if len(truck2.packageList) == 1:
        lastStop = True
    else:
        lastStop = False

    # iterate through each package in the package list and look for the closest address to the current location
    for package in truck2.packageList:

        # find index for package location and truck location
        packageLocationIndex = destinationHash.search((package.address,package.zipCode))
        truckLocationIndex = destinationHash.search(truck2.location)

        # find distance from truck's location to package location
        distance = float(distanceMatrix[packageLocationIndex][truckLocationIndex])

        # if the distance to the package location is closer than the closest stop, then update the closestStop distance
        # assign current package to be the next package drop
        if distance < closestStop:
            closestStop = distance
            nextPackageDropId = package.id

    # after iterating through for loop to find the next package to deliver:
    #   * add the distance to the next closest stop to the total distance
    #   * update current truck location to the next package drop
    #   * drop off the package
    #   * update the package delivery time

    truck2.milesDriven += closestStop
    truck2.location = (packageHash.search(nextPackageDropId).address,packageHash.search(nextPackageDropId).zipCode)
    truck2.packageList.remove(packageHash.search(nextPackageDropId))

    tempPackage = packageHash.search(nextPackageDropId)
    tempPackage.deliveryTime = truck2.add_seconds(truck2.milesDriven)
    packageHash.insert(tempPackage.id,tempPackage)

    # if it's the last stop, add the distance back to the hub
    if lastStop == True:
        truck2.milesDriven += float(distanceMatrix[0][destinationHash.search(truck2.location)])


# time is 14:00 => update truck3 packages to en route
for package in truck3.packageList:
    package.departureTime = datetime(2022, 12, 24, 14, 0, 0)
    packageHash.insert(package.id, package)

# start truck3 on route
while len(truck3.packageList)>0:
    # initialize the shortest distance to infinity
    closestStop = float('inf')

    # check for last stop
    if len(truck3.packageList) == 1:
        lastStop = True
    else:
        lastStop = False

    # iterate through each package in the package list and look for the closest address to the current location
    for package in truck3.packageList:

        # find index for package location and truck location
        packageLocationIndex = destinationHash.search((package.address,package.zipCode))
        truckLocationIndex = destinationHash.search(truck3.location)

        # find distance from truck's location to package location
        distance = float(distanceMatrix[packageLocationIndex][truckLocationIndex])

        # if the distance to the package location is closer than the closest stop, then update the closestStop distance
        # assign current package to be the next package drop
        if distance < closestStop:
            closestStop = distance
            nextPackageDropId = package.id

    # after iterating through for loop to find the next package to deliver:
    #   * add the distance to the next closest stop to the total distance
    #   * update current truck location to the next package drop
    #   * drop off the package
    #   * update the package delivery time

    truck3.milesDriven += closestStop
    truck3.location = (packageHash.search(nextPackageDropId).address,packageHash.search(nextPackageDropId).zipCode)
    truck3.packageList.remove(packageHash.search(nextPackageDropId))

    tempPackage = packageHash.search(nextPackageDropId)
    tempPackage.deliveryTime = truck3.add_seconds(truck3.milesDriven)
    packageHash.insert(tempPackage.id, tempPackage)

    # if it's the last stop, add the distance back to the hub
    if lastStop == True:
        truck3.milesDriven += float(distanceMatrix[0][destinationHash.search(truck3.location)])

#print summary information
print(Format.underline + "\nTruck 1 Summary" + Format.end)
print("Departure Time: ", truck1.departureTime)
print("Return Time: ", truck1.add_seconds(truck1.milesDriven))
print("Total Miles Driven: ", round(truck1.milesDriven,1))

print(Format.underline + "\nTruck 2 Summary" + Format.end)
print("Departure Time: ", truck2.departureTime)
print("Return Time: ", truck2.add_seconds(truck2.milesDriven))
print("Total Miles Driven: ", round(truck2.milesDriven,1))

print(Format.underline + "\nTruck 3 Summary" + Format.end)
print("Departure Time: ", truck3.departureTime)
print("Return Time: ", truck3.add_seconds(truck3.milesDriven))
print("Total Miles Driven: ", round(truck3.milesDriven,1))

print(Format.underline + "\nTotal miles driven by trucks:"+ Format.end, end=" ")
print(round(truck1.milesDriven + truck2.milesDriven + truck3.milesDriven, 1) )

# start interface
runProgram = True
while runProgram:

    input_string = str(input("\nEnter a time after 08:00 (hh:mm) to check packages status or 'X' to exit: "))

    if input_string == 'X':
        exit()
    else:
        input_string = "2022-12-24 " + input_string

    checkTime = datetime.strptime(input_string, "%Y-%m-%d %H:%M")

    print(Format.underline + f"\nPackage Delivery Summary For {checkTime}" + Format.end)

    for i in range(1, len(packageHash.table) + 1):

        # address for package id 9 is not known until after 10:20
        if (i == 9 and checkTime < datetime(2022, 12, 24, 10, 20, 0)):
            wrongAddressPackage = packageHash.search(i)
            wrongAddressPackage.address = '300 State St'
            wrongAddressPackage.zipCode = 84103
            print(wrongAddressPackage, end = " ")
            print("At the Hub")
            wrongAddressPackage.address = '410 S State St'
            wrongAddressPackage.zipCode = 84111

        else:

            package = packageHash.search(i)
            print(package, end = " ")

            if checkTime < package.departureTime:
                print("At the Hub")
            elif package.departureTime < checkTime < package.deliveryTime:
                print("Enroute")
            else:
                print("Delivered", package.deliveryTime)



