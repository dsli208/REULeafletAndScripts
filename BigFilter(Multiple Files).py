import csv  # Used to read csv files in
import os  # Used for file management
from math import *  # Math library, used for functions to determine intersection rotation (sin, cos, atan, etc.)

fields = []  # Stores header of csv location file
rows = []  # Stores the contents of a csv location file in lists
IntersectionFields = []  # Stores the header of the csv intersection file
intersections = []  # Stores the contents of the csv intersection file in lists
R = 6371  # Radius of Earth in km

# Takes in two tuples representing data points (lat, long), returns the distance between these two points
def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))
    a = pow(sin(deltaLat / 2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon / 2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Takes in two tuples representing data points (lat, long), returns a bearing value in degrees (between 0-360)
def getBearing(tuple1, tuple2):
    X = cos(radians(tuple2[0])) * sin(radians(abs(tuple1[1] - tuple2[1])))
    Y = cos(radians(tuple1[0])) * sin(radians(tuple2[0])) - sin(radians(tuple1[0])) * cos(radians(tuple2[0])) * \
        cos(radians(abs(tuple1[1] - tuple2[1])))
    beta = (degrees(atan2(X, Y))) % 360.0

    return beta

# takes in a KM value, converts to FEET (float/double format)
def kmToFeet(value):
    return value * 1000.0 * 100.0 / 2.54 / 12.0

# Takes in a intersectionID and intersections array, returning a tuple
def getIntersectionLocation(intersectionID, intersections):
    for b in range(0, len(intersections)):
        if intersectionID == intersections[b][0]:
            break
    return (float(intersections[b][1]), float(intersections[b][2]))

# Main method - this script is a revised version of the BigFilter, revised to take in multiple files instead of one.
# This script takes in a combined file consisting of data from smaller traffic data csv's that were previously filtered
# using filter.py.  Like filter.py, this script filters out points that are not deemed to be associated with a
# particular intersection
# Notice: This file is not completely working, as of recently, this file stopped working after processing 294/368 csv
# files
if __name__ == "__main__":  # Main class, where the script starts running

    # Reading and storing  the intersection Information
    # Need 'Intersection_Info_comb.csv' file, may need to modify the below path depending on where that file is located
    # in your computer
    with open("C:/Users/dsli/Documents/Civic Data Science/Intersection_Info_comb.csv", 'r') as csvfile:
        print("Reading csv file")
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        IntersectionFields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            intersections.append(row)

    # change directory variable for different directories
    directory = 'C:/Users/dsli/Documents/Civic Data Science/Filtered_Location_Data'
    folder = sorted(os.listdir(directory))
    c = 0
    for file in folder:
        # Keeps track of how many files  have been processed
        # Can increase the number after the modular arithmetic for greater speed or comment out entire if block if you
        # don't need to know
        if c % 50 == 0:
            print("c is " + str(c) + " and there are " + str(len(folder)) + " in the folder")

        c += 1

        # If it is not a csv file, skip it
        if '.csv' not in file:
            print("File skipped")
            continue

        with open(directory + "/"+ file, 'r') as csvfile:
            print("Reading csv file")
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields = next(csvreader)

            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)

        # If the row in the file is empty, skip it
        if rows[0] is None or len(rows[0]) == 0:
            continue

        # Get length of existing columns
        columnLength = len(rows[0])

        # Add additional blank columns to each row
        for row in rows:
            for i in range(columnLength, columnLength + 23):
                row.append("")

        # Find intersections for locations
        print("Finding Intersections for Locations")
        i = 0
        for row in rows:
            if i % 1000 == 0:
                print(" i is " + str(i) + " and length of rows is " + str(len(rows)))
            LocationIndex = columnLength + 1
            NumIntersection = 0
            fireTruckLocation = (float(row[1]), float(row[2]))
            for j in range(0, len(intersections)):
                interLocation = (float(intersections[j][1]), float(intersections[j][2]))
                latDistance = kmToFeet(getDistance((fireTruckLocation[0], 0), (interLocation[0], 0)))
                lonDistance = kmToFeet(getDistance((0, fireTruckLocation[1]), (0, interLocation[1])))
                if latDistance < 1000.0 and lonDistance < 1000.0:
                    row[LocationIndex] = intersections[j][0]
                    LocationIndex += 1
                    NumIntersection += 1
            if NumIntersection != 0:
                row[columnLength] = NumIntersection
            i += 1

        # Figuring out if fire truck is approaching or receding
        print("Figuring out Approaching or Receding")
        for i in range(0, len(rows)):
            fireTruckLocation1 = (float(rows[i][1]), float(rows[i][2]))
            for j in range(columnLength + 1, columnLength + 7):
                if rows[i][j] != "":
                    for k in range(0, len(intersections)):
                        if intersections[k][0] == rows[i][j]:
                            break
                    intersec = intersections[k]
                    intersectionLoc = (float(intersec[1]), float(intersec[2]))
                    d1 = getDistance(fireTruckLocation1, intersectionLoc)
                    if i == 0:
                        fireTruckLocation2 = (float(rows[i + 1][1]), float(rows[i + 1][2]))
                        d2 = getDistance(fireTruckLocation2, intersectionLoc)
                        # Only occurs it it is at beginning of csv file
                        # Case receding intersection
                        if d2 > d1:
                            if j == columnLength + 1:
                                rows[i][columnLength + 7] = 'No'
                            elif j == columnLength + 2:
                                rows[i][columnLength + 8] = 'No'
                            elif j == columnLength + 3:
                                rows[i][columnLength + 9] = 'No'
                            elif j == columnLength + 4:
                                rows[i][columnLength + 10] = 'No'
                            elif j == columnLength + 5:
                                rows[i][columnLength + 11] = 'No'
                            elif j == columnLength + 6:
                                rows[i][columnLength + 12] = 'No'
                        # Case approaching intersection
                        elif d2 < d1:
                            if j == columnLength + 1:
                                rows[i][columnLength + 7] = 'Yes'
                                rows[i][columnLength + 13] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            elif j == columnLength + 2:
                                rows[i][columnLength + 8] = 'Yes'
                                rows[i][columnLength + 14] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            elif j == columnLength + 3:
                                rows[i][columnLength + 9] = 'Yes'
                                rows[i][columnLength + 15] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            elif j == columnLength + 4:
                                rows[i][columnLength + 10] = 'Yes'
                                rows[i][columnLength + 16] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            elif j == columnLength + 5:
                                rows[i][columnLength + 11] = 'Yes'
                                rows[i][columnLength + 17] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            elif j == columnLength + 6:
                                rows[i][columnLength + 12] = 'Yes'
                                rows[i][columnLength + 18] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))

                    else:
                        fireTruckLocation2 = (float(rows[i - 1][1]), float(rows[i - 1][2]))
                        d2 = getDistance(fireTruckLocation2, intersectionLoc)
                        # Will go to this case for rest of the file
                        # Case approaching intersection
                        if d2 > d1:
                            if j == columnLength + 1:
                                rows[i][columnLength + 7] = 'Yes'
                                rows[i][columnLength + 13] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            if j == columnLength + 2:
                                rows[i][columnLength + 8] = 'Yes'
                                rows[i][columnLength + 14] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            if j == columnLength + 3:
                                rows[i][columnLength + 9] = 'Yes'
                                rows[i][columnLength + 15] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            if j == columnLength + 4:
                                rows[i][columnLength + 10] = 'Yes'
                                rows[i][columnLength + 16] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            if j == columnLength + 5:
                                rows[i][columnLength + 11] = 'Yes'
                                rows[i][columnLength + 17] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                            if j == columnLength + 6:
                                rows[i][columnLength + 12] = 'Yes'
                                rows[i][columnLength + 18] = kmToFeet(getDistance(fireTruckLocation1, intersectionLoc))
                        # Case receding intersection
                        elif d2 < d1:
                            if j == columnLength + 1:
                                rows[i][columnLength + 7] = 'No'
                            if j == columnLength + 2:
                                rows[i][columnLength + 8] = 'No'
                            if j == columnLength + 3:
                                rows[i][columnLength + 9] = 'No'
                            if j == columnLength + 4:
                                rows[i][columnLength + 10] = 'No'
                            if j == columnLength + 5:
                                rows[i][columnLength + 11] = 'No'
                            if j == columnLength + 6:
                                rows[i][columnLength + 12] = 'No'

        # Append headers to newly created columns
        fields.extend(['Number of Intersections', 'Intersection 1 ID', 'Intersection 2 ID', 'Intersection 3 ID',
                       'Intersection 4 ID', 'Intersection 5 ID', 'Intersection 6 ID', 'Approaching Intersection 1',
                       'Approaching Intersection 2', 'Approaching Intersection 3', 'Approaching Intersection 4',
                       'Approaching Intersection 5', 'Approaching Intersection 6',
                       'Distance to Intersection 1 (feet)', 'Distance to Intersection 2 (feet)',
                       'Distance to Intersection 3 (feet)', 'Distance to Intersection 4 (feet)',
                       'Distance to Intersection 5 (feet)', 'Distance to Intersection 6 (feet)', ])

        ignoreInter = []
        # Figuring out turns using the differnce in bearing values
        print("Figuring out Turns")
        for i in range(0, len(rows)):
            if i % 1000 == 0:
                print("i is " + str(i) + " and length of rows is " + str(len(rows)))
            if rows[i][columnLength + 7] != "":
                fireTruckLocation = (float(rows[i][1]), float(rows[i][2]))
                if rows[i][columnLength + 7:columnLength + 13].count('Yes') == 1:
                    approaches = [g for g in range(columnLength + 7, columnLength + 13) if rows[i][g] == 'Yes']
                    intersectionID = rows[i][approaches[0] - 6]
                    intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)
                    leastDistance = getDistance(fireTruckLocation, intersectionLoc)

                elif rows[i][columnLength + 7:columnLength + 13].count('Yes') > 1:
                    rows[i][columnLength + 22] = 'Low'
                    approaches = [g for g in range(columnLength + 7, columnLength + 13) if rows[i][g] == 'Yes']
                    intersectionID = rows[i][approaches[0] - 6]
                    intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)
                    leastDistance = getDistance(fireTruckLocation, intersectionLoc)
                    for q in range(1, len(approaches)):
                        d = getDistance(fireTruckLocation,
                                    getIntersectionLocation(rows[i][approaches[q] - 6], intersections))
                        if d < leastDistance:
                            leastDistance = d
                            intersectionID = rows[i][approaches[q] - 6]
                            intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)

                # No associated IntersectionID case
                if intersectionID in ignoreInter or rows[i][columnLength + 19] != "":
                    continue
                j = i
                while j < len(rows):
                    if intersectionID in rows[j][columnLength + 1:columnLength + 7]:
                        j += 1
                    else:
                        break

                if j == i:
                    continue

                if j == len(rows):
                    j = len(rows) - 1

                for k in range(i, j):
                    ind = rows[k].index(str(intersectionID))
                    if rows[k][ind + 6] == 'No':
                        break

                if k == i:
                    continue

                for g in range(k - 1, i - 1, -1):
                    distance = kmToFeet(getDistance((float(rows[g][1]), float(rows[g][2])), intersectionLoc))
                    if distance > 200.0:
                        break

                if g == i - 1:
                    g = i

                for h in range(k, j):
                    distance = kmToFeet(getDistance((float(rows[h][1]), float(rows[h][2])), intersectionLoc))
                    if distance > 200.0:
                        break

                if h == j:
                    h = j - 1

                FireTruckLocation1 = (float(rows[g][1]), float(rows[g][2]))
                FireTruckLocation2 = (float(rows[h][1]), float(rows[h][2]))
                bearing2 = getBearing(intersectionLoc, FireTruckLocation2)
                bearing1 = getBearing(FireTruckLocation1, intersectionLoc)
                diffBearing = (bearing2 - bearing1) % 360

                # Case right turn
                if 75 <= diffBearing and diffBearing <= 105:
                    for u in range(i, k):
                        rows[u][columnLength + 19] = 0
                        rows[u][columnLength + 20] = 0
                        rows[u][columnLength + 21] = 1
                # Case left turn
                elif 105 < diffBearing and diffBearing <= 285:
                    for u in range(i, k):
                        rows[u][columnLength + 19] = 1
                        rows[u][columnLength + 20] = 0
                        rows[u][columnLength + 21] = 0
                # Case going straight
                elif (285 < diffBearing and diffBearing < 360) or (0 <= diffBearing and diffBearing < 75):
                    for u in range(i, k):
                        rows[u][columnLength + 19] = 0
                        rows[u][columnLength + 20] = 1
                        rows[u][columnLength + 21] = 0

                ignoreInter.append(intersectionID)

            for b in range(len(ignoreInter) - 1, -1, -1):
                if ignoreInter[b] not in rows[i]:
                    del ignoreInter[b]

        fields.extend(['Left Turn', 'Straight', 'Right Turn', 'Low Confidence'])

        filename = os.path.splitext(file)[0]
        print(filename)
        # Write to a new directory, make sure directory is made
        with open('C:/Users/dsli/Documents/Civic Data Science/LocationWithMoreInfo/' + filename + 'withIntersection.csv',
                  'w', newline="") as myfile:
            print("Writing csv file" + filename)
            # Creates csv writer object.  Second argument prevents quotation marks from being written in
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            wr.writerow(fields)  # Writes Header of csv file
            # Write all rows into the csv file
            for row in rows:
                wr.writerow(row)

        rows.clear()  # clears list for new file to be read in
