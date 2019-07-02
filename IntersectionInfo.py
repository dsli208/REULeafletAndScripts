import csv
from math import *


fields = []
rows = []
IntersectionFields = []
intersections = []
R = 6371

def findIntersectionRow(intersectionID, intersectionTable):
    for j in range(0, len(intersectionTable)):
        if intersectionTable[j][0] == intersectionID:
            break
    return j

def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))
    a = pow(sin(deltaLat/2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon/2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def getIntersectionLocation(intersectionID, intersections):
    for b in range(0, len(intersections)):
        if intersectionID == intersections[b][0]:
            break
    return (float(intersections[b][1]), float(intersections[b][2]))

def getTimeDifferenceInSeconds(time1List, time2List):
    timefromMid1 = time1List[0] * 3600.0 + time1List[1] * 60.0 + time1List[2]
    timefromMid2 = time2List[0] * 3600.0 + time2List[1] * 60.0 + time2List[2]
    return (timefromMid2 - timefromMid1) % 86400


if __name__ == "__main__":
    with open("C:/my collection/REU 2019/R Programming directory/GPS Copy/FilteredData/finalwithIntersection.csv"
            , 'r') as csvfile:

        print("Reading csv file")
            # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    with open("C:/my collection/REU 2019/R Programming directory/Intersection_Info_comb.csv", 'r') as csvfile:
        print("Reading csv file")
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        IntersectionFields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            intersections.append(row)

    newFields = []
    newIntersectionInfo = [ [] for i in range(len(intersections)) ]
    columnLength = len(rows[0])

    newFields.extend(IntersectionFields[0:3])
    newFields.extend(['Number of Firetruck Locations', 'Average Speeds(mph)', 'Number of Times Intersection is Passed', 'Average Delays(sec)'])

    for i in range(0, len(intersections)):
        newIntersectionInfo[i][0:3] = intersections[i][0:3]
        newIntersectionInfo[i][3:7] = [0, 0, 0, 0]

    for row in rows:
        approaches = [g for g in range(columnLength - 16, columnLength - 10) if row[g] == 'Yes']
        if row[columnLength - 16: columnLength - 10].count('Yes') == 1:
            intersectionID = row[approaches[0] - 6]
        elif row[columnLength - 16: columnLength - 10].count('Yes') > 1:
            approaches = [g for g in range(columnLength - 16, columnLength - 10) if row[g] == 'Yes']
            intersectionID = row[approaches[0] - 6]
            intersectionLoc = getIntersectionLocation(int(intersectionID), intersections)
            leastDistance = getDistance((float(row[1]), float(row[2])), intersectionLoc)

            for q in range(1, len(approaches)):
                d = getDistance((float(row[1]), float(row[2])), getIntersectionLocation(row[approaches[q] - 6], intersections))
                if d < leastDistance:
                    leastDistance = d
                    intersectionID = rows[i][approaches[q] - 6]


        j = findIntersectionRow(intersectionID, newIntersectionInfo)
        newIntersectionInfo[j][3] += 1
        newIntersectionInfo[j][4] = newIntersectionInfo[j][4] * (newIntersectionInfo[j][3] - 1) + float(row[6])
        newIntersectionInfo[j][4] /= newIntersectionInfo[j][3]

    ignoreList = []
    for i in range(0, len(rows)):
        interID = rows[i][columnLength - 22: columnLength - 16]
        for j in range(0, len(interID)):
            if interID[j] == "":
                break

        for k in range(0, j - 1):
            ID = interID[k]
            if ID in ignoreList:
                continue
            for m in range(i, len(rows)):
                if ID not in rows[m]:
                    break
            if m - 1 == i:
                continue
            time1 = rows[i][0]
            time2 = rows[m - 1][0]
            time1List = [float(time1[11:13]), float(time1[14:16]), float(time1[17:23])]
            time2List = [float(time2[11:13]), float(time2[14:16]), float(time2[17:23])]
            timediff = getTimeDifferenceInSeconds(time1List, time2List)

            a = findIntersectionRow(ID, newIntersectionInfo)
            newIntersectionInfo[a][5] += 1
            newIntersectionInfo[a][6] = newIntersectionInfo[a][6] * (newIntersectionInfo[a][5] - 1) + timediff
            newIntersectionInfo[a][6] /= newIntersectionInfo[a][5]

            ignoreList.append(ID)

        for b in range(len(ignoreList) - 1, -1, -1):
            if ignoreList[b] not in rows[i]:
                ignoreList.remove(ignoreList[b])

    for j in range(len(newIntersectionInfo) - 1, -1, -1):
        if newIntersectionInfo[j][3] == 0:
            newIntersectionInfo.remove(newIntersectionInfo[j])

    with open('C:/my collection/REU 2019/R Programming directory/GPS Copy/FilteredData/IntersectionAverages.csv'
            , 'w', newline="") as myfile:
            print("Writing csv file")
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            wr.writerow(newFields)
            for row in newIntersectionInfo:
                wr.writerow(row)