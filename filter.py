import csv  # Important Library for Reading and Writing csv files
from math import *  # Important Library for some math operations
import numpy as np
import os  # Important Library for File Management
import datetime as dt  # Library that helps represent date and time objects

fields = []  # Stores header of csv location file
rows = []  # Stores the contents of a csv location file in lists
R = 6371

# All fire stations in Gwinnett County
Fire_Station_1 = (33.943832, -84.210733)
Fire_Station_2 = (33.8798, -84.1639)
Fire_Station_3 = (33.8575, -84.0985)
Fire_Station_4 = (33.9698, -84.2237)
Fire_Station_5 = (33.957201, -84.107871)
Fire_Station_6 = (33.7901, -84.0448)
Fire_Station_7 = (34.005214, -84.124628)
Fire_Station_8 = (33.8926, -83.9500)
Fire_Station_9 = (33.9112, -84.0307)
Fire_Station_10 = (34.0465, -83.9971)
Fire_Station_11 = (33.9115, -84.2011)
Fire_Station_12 = (33.8424, -84.0129)
Fire_Station_14 = (34.098467, -84.011699)
Fire_Station_15 = (33.946674, -83.987459)
Fire_Station_16 = (33.9926, -83.8976)
Fire_Station_17 = (33.9475, -83.8597)
Fire_Station_18 = (34.0600, -83.8784)
Fire_Station_19 = (33.9825, -84.1696)
Fire_Station_20 = (33.9546, -84.0582)
Fire_Station_21 = (34.0135, -84.0559)
Fire_Station_22 = (33.8244, -84.0954)
Fire_Station_23 = (33.9241, -84.1479)
Fire_Station_24 = (34.0656, -83.9723)
Fire_Station_25 = (33.911597, -84.101369)
Fire_Station_26 = (34.126397, -84.074938)
Fire_Station_27 = (34.034462, -83.915368)
Fire_Station_28 = (33.835553, -83.961375)
Fire_Station_29 = (34.0983, -83.8896)
Fire_Station_30 = (33.8901, -83.8955)
Fire_Station_31 = (33.985183, -84.002307)

Fire_Stations = [Fire_Station_1, Fire_Station_2, Fire_Station_3, Fire_Station_4, Fire_Station_5, Fire_Station_6,
                 Fire_Station_7, Fire_Station_8, Fire_Station_9, Fire_Station_10, Fire_Station_11, Fire_Station_12,
                 Fire_Station_14, Fire_Station_15, Fire_Station_16, Fire_Station_17, Fire_Station_18, Fire_Station_19,
                 Fire_Station_20, Fire_Station_21, Fire_Station_22, Fire_Station_23, Fire_Station_24, Fire_Station_25,
                 Fire_Station_26, Fire_Station_27, Fire_Station_28, Fire_Station_29, Fire_Station_30, Fire_Station_31]

# Function that returns the distance between a pair of (latitude, longitude) tuples in km.  Make sure the values in each
# tuples are not strings.  Ran into this error often when debugging
def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))
    a = pow(sin(deltaLat / 2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon / 2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Converts a kilometer value to a feet value
def kmToFeet(value):
    return value * 1000.0 * 100.0 / 2.54 / 12.0

# Converts a kilometer value to a mile value
def kmToMi(value):
    return kmToFeet(value) / 5280.0

# Calculates the time difference in seconds given
def getTimeDiffFromStr(str1, str2):
    time1 = dt.datetime(int(str1[0:4]), int(str1[5:7]), int(str1[8:10]), int(str1[11:13]), int(str1[14:16]),
                        int(float(str1[17:23])), round((float(str1[17:23]) % 1 * 1E6)))
    time2 = dt.datetime(int(str2[0:4]), int(str2[5:7]), int(str2[8:10]), int(str2[11:13]), int(str2[14:16]),
                        int(float(str2[17:23])), round((float(str2[17:23]) % 1 * 1E6)))
    return abs((time2 - time1).total_seconds())

# This script reads in all files in a directory and then runs various filters to get remove points not important to the
# analysis of the

if __name__ == "__main__":  # Main Function, where the script starts
    # change directory variable for different directories
    directory = 'S:/Gwinnett/raw_data/GPS_data/unzipped'
    folder = sorted(os.listdir(directory))
    c = 0  # Keeps track of how many files have been processed
    for file in folder:
        # Can increase the number after the modular arithmetic for greater speed or comment out entire if block if you
        # don't need to know
        if c % 50 == 0:
            print("c is " + str(c) + " and there are " + str(len(folder)) + " files in the folder")
        c += 1

        if '.csv' not in file:  # If the file is not a csv file, skip it
            print("File skipped")
            continue
        # Open the file for reading
        with open(directory + '/' + file, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields = next(csvreader)

            #extracting each data row one by one
            for row in csvreader:
                rows.append(row)

        # Removes all points that are within a 400 feet radius from the fire station
        i = 0
        for i in range(len(rows) - 1, -1, -1):
            fireTruckLocation = (float(rows[i][1]), float(rows[i][2]))
            for j in range(0, len(Fire_Stations)):
                d = getDistance(Fire_Stations[j], fireTruckLocation)
                if (kmToFeet(d) < 400.0):
                    rows.pop(i)
                    break

        # If the file was emptyed out, move on to next file
        if len(rows) == 0:
            print("File was emptyed")
            continue

        # Creates a numpy array from a list of lists
        npRows = np.array(rows)
        times = npRows.T[0].tolist()
        lats = npRows.T[1].tolist()
        lons = npRows.T[2].tolist()
        speeds = npRows.T[6].tolist()

        # Calculate speeds for locations with missing speed values
        for i in range(0, len(times)):
            if speeds[i] == "":
                distance = kmToMi(getDistance((float(lats[i - 1]), float(lons[i - 1])), (float(lats[i]), float(lons[i]))))
                timeString1 = times[i - 1]
                timeString2 = times[i]

                timeDiff = getTimeDiffFromStr(timeString1, timeString2)

                newspeed = distance / (timeDiff / 3600.0)
                speeds[i] = newspeed

        npRows[:, 6] = np.array(speeds)

        # Removes all locations where the speeds is over 85 mph
        for i in range(len(npRows) - 1, -1, -1):
            if float(npRows[i, 6]) > 85.0:
                np.delete(npRows, i, 0)

        speeds = npRows.T[6].tolist()

        # Removes all points that occur when the fire truck is traveling less than 7 mph in a continuous 4 minute window
        i = 0
        time = 0
        while i < len(speeds):
            j = i
            while j < len(speeds) and float(speeds[j]) < 7.0:
                j += 1
            if j == i:
                i += 1
            else:
                time = 0
                for k in range(i, j - 1):
                    timediff = getTimeDiffFromStr(times[k], times[k + 1])
                time += timediff
                if time > 240.0:
                    for d in range(j - 1, i - 1, -1):
                        npRows = np.delete(npRows, (d), axis=0)

                    times = npRows.T[0].tolist()
                    lats = npRows.T[1].tolist()
                    lons = npRows.T[2].tolist()
                    speeds = npRows.T[6].tolist()

                else:
                    i = j

        rows = npRows.tolist()

        # Append the Device ID to the end of each row
        elem = file.split('_')
        deviceID = elem[0]
        for i in range(0, len(rows)):
            rows[i] += [deviceID]

        # Make directory beforehand, Come up with own format of file name

        fields += ['Device ID']
        with open('S:/Gwinnett/Jason Chen/Filtered_Location_Data/filtered_' + deviceID + '_' + elem[1], 'w', newline="")\
                as myfile:
            # Creates csv writer object.  Second argument prevents quotation marks from being written in
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            wr.writerow(fields)   # Writes Header of csv file
            # Write all rows into the csv file
            for row in rows:
                wr.writerow(row)

        rows.clear()  # Clears rows for next file to be read in directory/folder
