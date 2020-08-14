import csv  # Important Library for Reading and Writing csv files
from math import *  # Important Library for some math operations
R = 6371  # Stores Radius of Earth in km

# Function that gets the index of the intersection given the intersection ID as well as where the intersection
# information is stored in
def findIntersectionRow(intersectionID, intersectionTable):
    for y in range(0, len(intersectionTable)):
        if intersectionTable[y][0] == intersectionID:
            break
    return y

# Function that returns a (latitude, longitude) tuple given a intersection ID and where the intersection information is
# stored
def getIntersectionLocation(intersectionID, intersections):
    for b in range(0, len(intersections)):
        if intersectionID == intersections[b][0]:
            break
    return (float(intersections[b][1]), float(intersections[b][2]))

# Function that returns the distance between a pair of (latitude, longitude) tuples in km.  Make sure the values in each
# tuples are not strings.  Ran into this error often when debugging
def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))  # Calculate difference in latitude values
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))  # Calculate difference in longitude values
    a = pow(sin(deltaLat/2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon/2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# This script reads in a big csv file containing the fire truck locations with the signals status at the current
# location and generates three csv files, each

if __name__ == "__main__":    # Main class, where the program starts
    newFields = []  # Stores the header of the csv file
    newGreen = []  # Stores the rows that have green lights
    newYellow = []  # Stores the rows that have yellow lights
    newRed = []  # Stores the rows that have red lights
    fields = []  # Stores the header of the big csv file
    IntersectionFields = []  # Stores the header from the intersection file
    intersections = []  # Stores information about the intersections

    # Reads data about intersections and stores in list variable intersections
    with open("C:/Users/dsli/Documents/Civic Data Science/Intersection_Info_comb.csv", 'r') as csvfile:
        print("Reading csv file")
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        IntersectionFields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            intersections.append(row)

    # Puts headers that will be read in the output file
    newFields.extend(IntersectionFields[0:3])
    newFields.extend(['Number of Firetruck Locations', 'Average Speeds(mph)', 'Signal Stat'])

    # Inititalize the rows for the output file
    for i in range(0, len(intersections)):
        newRed.append(intersections[i][0:3])
        newRed[i] += [0, 0, '']
        newYellow.append(intersections[i][0:3])
        newYellow[i] += [0, 0, '']
        newGreen.append(intersections[i][0:3])
        newGreen[i] += [0, 0, '']

    # Opens the file that had the fire truck location
    with open('C:/Users/dsli/Documents/Civic Data Science/signal_status.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            columnLength = len(row)
            #Check if the traffic signal is the last item in the row
            if (row[columnLength - 1] == 'Green') or (row[columnLength - 1] == 'Yellow') or (row[columnLength - 1] == 'Red'):
                for i in range(columnLength - 23, columnLength - 17):
                    if row[i] == '':
                        break
                    else:
                        # Find all indexes for approaching intersections
                        approaches = [g for g in range(columnLength - 17, columnLength - 11) if row[g] == 'Yes']
                        # Case where only one approach intersection exists
                        if row[columnLength - 17: columnLength - 11].count('Yes') == 1:
                            intersectionID = row[approaches[0] - 6]
                        # Case where only more than one approach intersection exists
                        elif row[columnLength - 17: columnLength - 11].count('Yes') > 1:
                            approaches = [g for g in range(columnLength - 17, columnLength - 11) if row[g] == 'Yes']
                            intersectionID = row[approaches[0] - 6]
                            intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)
                            leastDistance = getDistance((float(row[1]), float(row[2])), intersectionLoc)

                            for q in range(1, len(approaches)):
                                d = getDistance((float(row[1]), float(row[2])),
                                                getIntersectionLocation(row[approaches[q] - 6], intersections))
                                if d < leastDistance:
                                    leastDistance = d
                                    intersectionID = row[approaches[q] - 6]

                            # find the index of the intersection in the intersections information list of lists
                            j = findIntersectionRow(intersectionID, intersections)

                            # if last column says Green
                            if row[columnLength - 1] == 'Green':
                                newGreen[j][3] += 1  # Add the number of firetruck location counter

                                # Get Average Speed
                                newGreen[j][4] = newGreen[j][4] * (newGreen[j][3] - 1) + float(row[6])
                                newGreen[j][4] /= newGreen[j][3]
                                newGreen[j][5] = 'Green'

                            # Same as Previous case
                            elif row[columnLength - 1] == 'Yellow':
                                newYellow[j][3] += 1
                                newYellow[j][4] = newYellow[j][4] * (newYellow[j][3] - 1) + float(row[6])
                                newYellow[j][4] /= newYellow[j][3]
                                newYellow[j][5] = 'Yellow'

                            # Same as previous case
                            elif row[columnLength - 1] == 'Red':
                                newRed[j][3] += 1
                                newRed[j][4] = newRed[j][4] * (newRed[j][3] - 1) + float(row[6])
                                newRed[j][4] /= newRed[j][3]
                                newRed[j][5] = 'Red'

    # Remove all intersection rows where the number of firetruck intersections is 0
    for j in range(len(intersections) - 1, -1, -1):
        if newRed[j][3] == 0:
            del newRed[j]

        if newYellow[j][3] == 0:
            del newYellow[j]

        if newGreen[j][3] == 0:
            del newGreen[j]

    # Write all data into red file
    with open('C:/Users/dsli/Documents/Civic Data Science/Presentation Data/RedAverages.csv', 'w', newline="") as myfile:
        print("Writing csv file")
        # Creates csv writer object.  Second argument prevents quotation marks from being written in
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(newFields)  # Writes Header of csv file
        # Write all rows into red csv file
        for row in newRed:
            wr.writerow(row)

    # Same as red file above except involving yellow light data
    with open('C:/Users/dsli/Documents/Civic Data Science/Presentation Data/YellowAverages.csv', 'w', newline="") as myfile:
        print("Writing csv file")
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(newFields)
        for row in newYellow:
            wr.writerow(row)

    # Same as red file except involving green light data
    with open('C:/Users/dsli/Documents/Civic Data Science/Presentation Data/GreenAverages.csv', 'w', newline="") as myfile:
        print("Writing csv file")
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(newFields)
        for row in newGreen:
            wr.writerow(row)








