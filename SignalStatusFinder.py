import csv # Reading in CSV file
from math import * # Math functions (sin, cos, etc.)
import sys # Potentially could be used for running in command line
from enum import Enum # Enums for traffic turns
import datetime as dt # Used for timestamps
import SignalFinder # From SignalDataAPI, from Zixiu Fu (zixiufu@gatech.edu)

args = sys.argv[1:]
print(args)

fields = []
rows = []
intersections = []

R = 6371

ignoreInter = []

# Invoke a new SignalFinder instance
s = SignalFinder.SignalFinder('./testData')

# Constant values regarding direction
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

# Takes in a direction value and adjusts accordingly
def leftTurn(direction):
    if direction == 0:
        return Direction.WEST
    elif direction == 1:
        return Direction.NORTH
    elif direction == 2:
        return Direction.EAST
    else:
        return Direction.SOUTH

# Takes in a direction value and adjusts accordingly
def rightTurn(direction):
    if direction == 3:
        return Direction.NORTH
    elif direction == 0:
        return Direction.WEST
    elif direction == 1:
        return Direction.SOUTH
    else:
        return Direction.EAST


def getBearing(tuple1, tuple2):
    X = cos(radians(tuple2[0])) * sin(radians(abs(tuple1[1] - tuple2[1])))
    Y = cos(radians(tuple1[0])) * sin(radians(tuple2[0])) - sin(radians(tuple1[0])) * cos(radians(tuple2[0])) * \
        cos(radians(abs(tuple1[1] - tuple2[1])))
    beta = (degrees(atan2(X, Y)) + 360.0) % 360

    return beta


def kmToFeet(value):
    return value * 1000.0 * 100.0 / 2.54 / 12.0


def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))
    a = pow(sin(deltaLat / 2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon / 2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def intersectionLookup(intersection_id):
    # find intersection if an ID can be found in one of the rows in the Intersection_Info file
    # Success: returns the associated array/row, otherwise returns None
    for i in range(0, len(intersections) - 1):
        if (intersections[i][0] == intersection_id):
            return intersections[i]
    return None


def getIntersectionLocation(intersectionID, intersections):
    for b in range(0, len(intersections)):
        if intersectionID == intersections[b][0]:
            break
    return (float(intersections[b][1]), float(intersections[b][2]))

# This script uses the Intersection_Info_comb.csv file
if __name__ == "__main__":

    if len(args) >= 1:
        readFile = args[0]
    else:
        readFile = "C:/Users/dsli/Documents/Civic Data Science/combine_locationwithmoreinfo.csv"  # change filepath before running it for the first tiem - assigned to readFile variable

    # Reading in CSV file
    with open(readFile, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        print(rows)

    # Specify filepath for Intersection Info CSV
    with open("C:/Users/dsli/Documents/Civic Data Science/Intersection_Info_comb.csv", 'r') as csvfile:
        print("Reading csv file")
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        IntersectionFields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            intersections.append(row)

    # Iterate through each row
    for i in range(0, len(rows) - 1):
        print("i is " + str(i))
        if (rows[i][20] == ''):
            continue

        columnLength = len(rows[0])

        # Getting bearing values
        if rows[i][25] != "":
            fireTruckLocation = (float(rows[i][1]), float(rows[i][2])) # tuple for lat, long of fire truck location
            if rows[i][25:31].count('Yes') == 1:
                approaches = [y for y in range(25, 31) if rows[i][y] == 'Yes']
                intersectionID = rows[i][approaches[0] - 6]
                intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)
                leastDistance = getDistance(fireTruckLocation, intersectionLoc)

            elif rows[i][25:31].count('Yes') > 1:
                rows[i][40] = 'Low'
                approaches = [y for y in range(25, 31) if rows[i][y] == 'Yes']
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

            if intersectionID in ignoreInter or rows[i][37] != "":
                continue
            j = i
            while j < len(rows):
                if ('Yes' in rows[j]) and (intersectionID in rows[j][19:25]):
                    j += 1
                else:
                    break

            if j == i:
                continue

            if j == len(rows):
                j = len(rows) - 1

            for x in range(i, j):
                ind = rows[x].index(str(intersectionID))
                if rows[x][ind + 6] == 'No':
                    break

            for y in range(x - 1, i - 1, -1):
                distance = kmToFeet(getDistance((float(rows[y][1]), float(rows[y][2])), intersectionLoc))
                if distance > 200.0:
                    break

            if y == i - 1:
                y = i

            for h in range(x, j):
                distance = kmToFeet(getDistance((float(rows[h][1]), float(rows[h][2])), intersectionLoc))
                if distance > 200.0:
                    break

            if x == j:
                x = j - 1

            FireTruckLocation1 = (float(rows[y][1]), float(rows[y][2]))
            FireTruckLocation2 = (float(rows[h][1]), float(rows[h][2]))
            bearing2 = getBearing(intersectionLoc, FireTruckLocation2)
            bearing1 = getBearing(FireTruckLocation1, intersectionLoc)
            print("bearing2 is " + str(bearing2))
            print("bearing1 is " + str(bearing1))
            diffBearing = bearing2 - bearing1

            print("i is " + str(i) + " and x is " + str(x) + " and j is " + str(j))
            print("diffBearing is " + str(diffBearing))
            # Right turn
            if 75 <= diffBearing and diffBearing <= 105:
                for u in range(i, k):
                    rows[u][37] = 0
                    rows[u][38] = 0
                    rows[u][39] = 1
            # Left turn
            elif (-105 <= diffBearing and diffBearing <= -180) or (105 < diffBearing and diffBearing <= 180):
                for u in range(i, x):
                    rows[u][37] = 1
                    rows[u][38] = 0
                    rows[u][39] = 0
            # Going straight
            elif -75 < diffBearing < 75:
                for u in range(i, x):
                    rows[u][37] = 0
                    rows[u][38] = 1
                    rows[u][39] = 0

            ignoreInter.append(intersectionID)

            for b in range(len(ignoreInter) - 1, -1, -1):
                if ignoreInter[b] not in rows[i]:
                    ignoreInter.remove(ignoreInter[b])

        # Now, look up intersection and based on bearing values figure out what direction truck is turning from Intersection_Info_comb
        # And therefore, which phase number to use
        intersectionRow = intersectionLookup(rows[i][20])

        print(intersectionRow)

        int_rotation_clockwise = int(intersectionRow[17])

        rotation_index = int_rotation_clockwise / 45

        if rotation_index == 0 or abs(rotation_index) == 7 or abs(rotation_index) == 8:
            direction = Direction.NORTH
        elif rotation_index == 1 or rotation_index == -6 or rotation_index == 2 or rotation_index == -5:
            direction = Direction.EAST
        elif abs(rotation_index) == 3 or abs(rotation_index) == 4:
            direction = Direction.SOUTH
        else:
            direction = Direction.WEST

        # Factoring in bearing values/turning
        if rows[i][37] == 1:
            direction = leftTurn(direction)
        elif rows[i][39] == 1:
            direction = righTurn(direction)

        # Now we have our final direction (5, 8, 11, 14)
        if direction == Direction.NORTH:
            phase = intersectionRow[5]
        elif direction == Direction.EAST:
            phase = intersectionRow[11]
        elif direction == Direction.SOUTH:
            phase = intersectionRow[8]
        else:
            phase = intersectionRow[14]

        phase_num = int(phase)
        intersection_row_num = int(intersectionRow[0])
        dt_str = rows[i][0]

        time1 = dt.datetime(int(dt_str[0:4]), int(dt_str[5:7]), int(dt_str[8:10]), int(dt_str[11:13]), int(dt_str[14:16]),
                            int(float(dt_str[17:23])), round((float(dt_str[17:23]) % 1 * 1E6)))

        dt_str2 = time1.strftime('%Y-%m-%d %H:%M:%S')

        print(phase)
        print(intersectionRow)
        print(dt_str2)

        # except cases for finding the signal status
        try:
            signalStatus = s.findSignalStatus(int(phase), int(intersectionRow[0]), dt_str2)
        except SignalFinder.CSVNotFoundError:
            pass
        except SignalFinder.DataMayMissingError:
            pass
        except SignalFinder.PhaseNotExistError:
            pass

        # After finding signal status, append to rows[i]
        rows[i].append(signalStatus)
        rows[i].append(phase)

    # Add new Signal Status header
    fields.append('Signal Status')
    fields.append('Phase')

    # Write out the new file
    with open('signal_status_with_header3.csv', 'w',
                newline="") as myfile:
        print("Writing csv file")
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(fields)
        for row in rows:
            wr.writerow(row)
