import csv
import os.path as path
import datetime as dt


class DataMayMissingError(Exception):
	def __init__(self):
		self.message = 'Data may missing for the timestamp.'

	def __str__(self):
		return self.message


class PhaseNotExistError(Exception):
	def __init__(self):
		self.message = 'Phase may not exist.'

	def __str__(self):
		return self.message


class CSVNotFoundError(Exception):
	def __init__(self, errID, errorDate):
		self.message = "Signal %i @ %s is not in the database." % (errID, errorDate)
		self.errSignalID = errID
		self.errorDate = errorDate

	def __str__(self):
		return self.message


class DataEntry(object):
	def __init__(self, timeObject, para, event):
		self.dtObject = timeObject
		self.Parameter = para
		self.EventID = event


class SignalFinder(object):

	def __init__(self, dataPath):
		self.currList = None
		self.currID = None
		self.currDate = None
		self.currPath = None

		self.prevList = None
		self.prevDate = None
		self.prevPath = None

		self.dataPath = dataPath
		self.translateMap = {1: "Green", 8: "Yellow", 10: "Red"}

	def findSignalStatus(self, phaseInterested, signalNumber, checkDtString=None, checkDtObject=None):
		if checkDtString == None and checkDtObject == None:
			raise ValueError("Must enter a timeStamp to check!")
		if checkDtString != None:
			checkDtObject = dt.datetime.strptime(checkDtString, '%Y-%m-%d %H:%M:%S')
		thisDate = checkDtObject.strftime('%Y-%m-%d')

		if self.currID != signalNumber or self.currDate != thisDate:
			thisPath = path.join(self.dataPath, 'ID' + str(signalNumber), thisDate + '.csv')
			try:
				self.currList = self.loadCSV(thisPath)
			except FileNotFoundError:
				raise CSVNotFoundError(signalNumber, thisDate)

			self.currDate = thisDate
			self.currID = signalNumber
			self.currPath = thisPath

		# binary search
		left = 0
		right = self.currList.__len__() - 1
		while left < right - 1:
			mid = (left + right) // 2
			if self.currList[mid].dtObject > checkDtObject:
				right = mid - 1
			else:
				left = mid
		currIndex = left
		# print(self.currList[currIndex].dtObject)

		# search back for phase
		# while self.currList[currIndex].Parameter != phaseInterested or self.currList[
		# 	currIndex].EventID not in self.translateMap:
		# 	if self.currList[currIndex].dtObject < checkDtObject - dt.timedelta(minutes=30):
		# 		raise DataMayMissingError
		# 	if currIndex == -1:
		# 		self.checkForPrevDay(phaseInterested, checkDtObject)
		# 	currIndex -= 1

		seenPhase = False
		while True:
			if self.currList[currIndex].Parameter == phaseInterested and seenPhase == False:
				seenPhase = True

			if self.currList[currIndex].dtObject < checkDtObject - dt.timedelta(minutes=30):
				if seenPhase:
					raise DataMayMissingError
				else:
					for count in range(0, 1000):
						currIndex -= 1
						if self.currList[currIndex].Parameter == phaseInterested:
							raise DataMayMissingError
					raise PhaseNotExistError

			if currIndex == -1:
				self.checkForPrevDay(phaseInterested, checkDtObject)

			if self.currList[currIndex].Parameter == phaseInterested and self.currList[
				currIndex].EventID in self.translateMap:
				break
			currIndex -= 1

		return self.translateMap[self.currList[currIndex].EventID]

	def checkForPrevDay(self, phaseInterested, checkDtObject):
		# load prev date:
		thisDate = (dt.datetime.strptime(self.currDate, "%Y-%m-%d") - dt.timedelta(days=1)).strftime('%Y-%m-%d')
		if self.prevDate != thisDate:
			thisPath = path.join(self.dataPath, 'ID' + str(self.currID), thisDate + '.csv')
			try:
				self.prevList = self.loadCSV(thisPath)
			except FileNotFoundError:
				raise CSVNotFoundError(self.currID, thisDate)

			self.prevDate = thisDate
			self.prevPath = thisPath

		currIndex = -1
		seenPhase = False
		while True:
			if self.prevList[currIndex].Parameter == phaseInterested and seenPhase == False:
				seenPhase = True

			if self.prevList[currIndex].dtObject < checkDtObject - dt.timedelta(minutes=30):
				if seenPhase:
					raise DataMayMissingError
				else:
					for count in range(0, 1000):
						currIndex -= 1
						if self.prevList[currIndex].Parameter == phaseInterested:
							raise DataMayMissingError
					raise PhaseNotExistError
			if self.currList[currIndex].Parameter == phaseInterested and self.currList[
				currIndex].EventID in self.translateMap:
				break
			currIndex -= 1

	def loadCSV(self, csvPath):
		currList = []
		with open(csvPath) as csvfile:
			reader: object = csv.reader(csvfile, delimiter=',')
			reader.__next__()
			for row in reader:
				thisTime = row[0]
				if thisTime[-3:-1] == '00':
					thisTime = thisTime[:-3]
					dtObj = dt.datetime.strptime(thisTime, '%Y-%m-%d %H:%M:%S.%f')
				# 2019-05-06 00:00:08.700000000
				else:
					dtObj = dt.datetime.strptime(thisTime, '%Y-%m-%d %H:%M:%S')
				currList.append(DataEntry(dtObj, float(row[3]), int(row[2])))

		return currList
