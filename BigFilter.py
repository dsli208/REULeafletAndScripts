import csv
from math import *


fields = []
rows = []
IntersectionFields = []
intersections = []
R = 6371


def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))
    a = pow(sin(deltaLat/2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon/2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def getBearing(tuple1, tuple2):
    X = cos(radians(tuple2[0])) * sin(radians(abs(tuple1[1] - tuple2[1])))
    Y = cos(radians(tuple1[0])) * sin(radians(tuple2[0])) - sin(radians(tuple1[0])) * cos(radians(tuple2[0])) * \
        cos(radians(abs(tuple1[1] - tuple2[1])))
    beta = degrees(atan2(X, Y))
    if beta < 0:
        beta += 360
    return beta

def kmToFeet(value):
    return value * 1000.0 * 100.0 / 2.54 / 12.0

def getIntersectionLocation(intersectionID, intersections):
    for b in range(0, len(intersections)):
        print("IntersectionID is " + str(intersectionID))
        print("intersections[b][0] is " + intersections[b][0])
        if intersectionID == intersections[b][0]:
            break
    return (float(intersections[b][1]), float(intersections[b][2]))



if __name__ == "__main__":

    with open("C:/Users/dsli/Documents/Civic Data Science/script_filtered_2/newfile.csv", 'r') as csvfile:
        print("Reading csv file")
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    for j in range(len(rows) - 1, -1, -1):
        if rows[j][0] == 'time':
            rows.pop(j)

    with open("C:/Users/dsli/Documents/Civic Data Science/Intersection_Info_comb.csv", 'r') as csvfile:
        print("Reading csv file")
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        IntersectionFields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            intersections.append(row)

    columnLength = len(rows[0])

    for row in rows:
        for i in range(columnLength, columnLength + 22):
            row.append("")

    print("Finding Intersections for Locations")
    i = 0
    for row in rows:
        print("i is " + str(i))
        print("Length of Rows is " + str(len(rows)))
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



    print("Figuring out Approaching or Receding")
    for i in range(0, len(rows)):
        print("i is " + str(i))
        print("Length of Rows is " + str(len(rows)))
        fireTruckLocation1 = (float(rows[i][1]), float(rows[i][2]))
        for j in range(columnLength + 1, columnLength + 7):
            print("rows[i][j] is " + rows[i][j])
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
                    if d2 > d1:
                        if j == columnLength + 1:
                            rows[i][columnLength + 7] = 'No'
                        elif j == columnLength + 2:
                            rows[i][columnLength + 8] = 'No'
                        elif j == columnLength + 3:
                            rows[i][columnLength +9] = 'No'
                        elif j == columnLength + 4:
                            rows[i][columnLength + 10] = 'No'
                        elif j == columnLength + 5:
                            rows[i][columnLength + 11] = 'No'
                        elif j == columnLength + 6:
                            rows[i][columnLength + 12] = 'No'

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

    print("Fixing Bearing Values")
    for i in range(0, len(rows)):
        if rows[i][5] == "":

            if i != 0:
                c1 = (float(rows[i-1][1]), float(rows[i - 1][2]))
                c2 = (float(rows[i][1]), float(rows[i][2]))
                rows[i][5] = getBearing(c1, c2)


            else:
                c1 = (float(rows[i + 1][1]), float(rows[i - 1][2]))
                c2 = (float(rows[i][1]), float(rows[i][2]))
                rows[i][5] = getBearing(c2, c1)

    print("Figuring out Turns")
    for i in range(0, len(rows)):
        if rows[i][columnLength + 7] == 'Yes':
            fireTruckLocation = (float(rows[i][1]), float(rows[i][2]))
            if rows[i][columnLength + 7:columnLength + 13].count('Yes') == 1:
                intersectionID = rows[i][columnLength + 1]
                intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)

                print("intersectionID is " + str(intersectionID))
                print(type(int(intersectionID)))

                print("fireTruckLocation is " + str(fireTruckLocation))
                print("intersectionLoc is " + str(intersectionLoc))

                leastDistance = getDistance(fireTruckLocation, intersectionLoc)

            elif rows[i][columnLength + 7:columnLength + 13].count('Yes') > 1:
                approaches = [g for g in range(columnLength + 7, columnLength + 13) if rows[i][g] == 'Yes']
                intersectionID = rows[i][approaches[0] - 6]
                intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)
                print("fireTruckLocation is " + str(fireTruckLocation))
                print("intersectionLoc is " + str(intersectionLoc))
                leastDistance = getDistance(fireTruckLocation, intersectionLoc)
                for q in range(1, len(approaches)):
                    print("Approaches length is " + len(approaches))
                    d = getDistance(fireTruckLocation, getIntersectionLocation(rows[i][approaches[q] - 6], intersections))
                    if d < leastDistance:
                        leastDistance = d
                        intersectionID = rows[i][approaches[q] - 6]
                        intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)

            j = i
            print("J is " + str(j))
            while j < len(rows):
                if intersectionID in rows[j][columnLength + 1:columnLength + 7]:
                    j += 1
                else:
                    break

            if j >= i:
                break

            if j == len(rows):
                j = len(rows) - 1

            for k in range(i, j):
                ind = rows[k].index(str(intersectionID))
                if rows[k][ind + 6] == 'No':
                    break

            for g in range(k - 1, i - 1, -1):
                distance = kmToFeet(getDistance((float(rows[g][1]), float(rows[g][2])), intersectionLoc))
                if distance > 200.0:
                    break

            if g == i - 1:
                g = i

            for h in range(k, j):
                print("h is " + str(h))
                distance = kmToFeet(getDistance((float(rows[h][1]), float(rows[h][2])), intersectionLoc))
                if distance > 200.0:
                    break

            if h == j:
                h = j - 1

            FireTruckLocation1 = (float(rows[g][1]), float(rows[g][2]))
            FireTruckLocation2 = (float(rows[h][1]), float(rows[h][2]))
            bearing2 = getBearing(intersectionLoc, FireTruckLocation2)
            bearing1 = getBearing(intersectionLoc, FireTruckLocation1)
            diffBearing = bearing2 - bearing1

            if 75 <= diffBearing and diffBearing <= 105:
                for u in range(i, k + 1):
                    rows[u][columnLength + 19] = 0
                    rows[u][columnLength + 20] = 0
                    rows[u][columnLength + 21] = 1

            elif (-105 <= diffBearing and diffBearing <= -180) or (105 < diffBearing and diffBearing <= 180):
                for u in range(i, k + 1):
                    rows[u][columnLength + 19] = 1
                    rows[u][columnLength + 20] = 0
                    rows[u][columnLength + 21] = 0

            elif -75 < diffBearing < 75:
                for u in range(i, k + 1):
                    rows[u][columnLength + 19] = 0
                    rows[u][columnLength + 20] = 1
                    rows[u][columnLength + 21] = 0

        i = k
        while i < len(rows):
            if 'Yes' not in rows[i]:
                i += 1

        i = i - 1


    fields.extend(['Number of Intersections', 'Intersection 1 ID', 'Intersection 2 ID', 'Intersection 3 ID',
                   'Intersection 4 ID', 'Intersection 5 ID', 'Intersection 6 ID', 'Approaching Intersection 1',
                   'Approaching Intersection 2', 'Approaching Intersection 3', 'Approaching Intersection 4',
                   'Approaching Intersection 5', 'Approaching Intersection 6', 'Distance to Intersection 1 (feet)',
                   'Distance to Intersection 2 (feet)', 'Distance to Intersection 3 (feet)',
                   'Distance to Intersection 4 (feet)', 'Distance to Intersection 5 (feet)',
                   'Distance to Intersection 6 (feet)', 'Left Turn', 'Straight', 'Right Turn'])
    with open('C:/Users/dsli/Documents/Civic Data Science/script_filtered_2/final_filtered_bigfilter.csv', 'w',
              newline="") as myfile:
        print("Writing csv file")
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(fields)
        for row in rows:
            wr.writerow(row)