import csv
from math import *
import numpy as np

fields = []
rows = []
R = 6371

Fire_Station_4 = (33.9698, -84.2237)

def getDistance(tuple1, tuple2):
    deltaLat = radians(abs(tuple1[0] - tuple2[0]))
    deltaLon = radians(abs(tuple1[1] - tuple2[1]))
    a = pow(sin(deltaLat/2.0), 2) + cos(tuple1[0]) * cos(tuple2[0]) * pow(sin(deltaLon/2.0), 2)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def kmToFeet(value):
    return value * 1000.0 * 100.0 / 2.54 / 12.0

def kmToMi(value):
    return kmToFeet(value) / 5280.0

def getTimeDiffFromStr(str1, str2):
    secString1 = str1[17:23]
    secString2 = str2[17:23]
    return float(secString2) - float(secString1)

if __name__ == "__main__":
    with open("C:/Users/dsli/Documents/Civic Data Science/unzip_2/unzip_6628/2a0306ef_20190325/2a0306ef_20190325.csv", 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    i = 0
    while i < len(rows[:]):
        fireTruckLocation = (float(rows[i][1]), float(rows[i][2]))
        d = getDistance(Fire_Station_4, fireTruckLocation)

        if (kmToFeet(d) < 400.0):
            rows.remove(rows[i])
        else:
            i += 1

    npRows = np.array(rows)
    times = npRows.T[0].tolist()
    lats = npRows.T[1].tolist()
    lons = npRows.T[2].tolist()
    speeds = npRows.T[6].tolist()

    for i in range(0, len(times)):
        if speeds[i] == "":
            distance = kmToMi(getDistance((float(lats[i - 1]), float(lons[i - 1])), (float(lats[i]), float(lons[i]))))
            timeString1 = times[i - 1]
            timeString2 = times[i]
            timeDiff = getTimeDiffFromStr(timeString1, timeString2)
            if(timeDiff < 0):
                timeDiff += 60
            newspeed = distance / (timeDiff / 3600.0)
            speeds[i] = newspeed

    npRows[:, 6] = np.array(speeds)

    speeds = npRows.T[6].tolist()

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
                if timediff < 0.0:
                    timediff += 60.0
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


    with open('C:/Users/dsli/Documents/Civic Data Science/script_filtered_2/filtered_2a0306ef_20190325.csv', 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(fields)
        for row in rows:
            wr.writerow(row)

    with open('low_speed.csv', 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(fields)
        for a in range(0, len(speeds)):
            speed = speeds[a]
            if 2.0 <= float(speed) and float(speed) <= 10.0:
                wr.writerow(rows[a])
            else:
                continue

    with open('almost_stop.csv', 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(fields)
        for a in range(0, len(speeds)):
            speed = speeds[a]
            if 0.0 <= float(speed) and float(speed) <= 5.0:
                wr.writerow(rows[a])
            else:
                continue




