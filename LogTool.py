import matplotlib.pyplot as plt

class Math(object):
	"""Basic statistical math functions"""
	def sum(self, array):
		total = 0
		for i in array:
			total += i
		return total

	def avg(self, array):
		return sum(array) / len(array)

	def std(self, array):
		avg = self.avg(array)
		sum = 0

		for i in array:
			sum += (i - avg) ** 2
		return (sum / (len(array) - 1)) ** (1.0/2.0)


	def numOf(self, num, array):
		count = 0
		for x in array:
			if(x == num):
				count += 1
		return count

class FileLoader(object):
	"""Load log file data into program"""
	def __init__(self, fileName):
		self.fileName = fileName
		self.loadFile();

	def loadFile(self):
		self.logs = {}
		file = open(self.fileName, 'r')

		for line in file:
			if not line.strip():
				continue
			else:
				key = line[line.index(':') + 2 : line.index('=') - 1]
				self.logs.setdefault(key, []).append(float(line[line.index("=") + 2:].rstrip()))
				print key + "\t" + line[line.index("=") + 1 :]

	def getValues(self, val):
		return self.logs[val]

				


# math = Math()
# array = [1, 2, 3, 4, 5]
# print "Sum", math.sum(array)
# print "Avg", math.avg(array)

# print "Std", math.std(array)
# print "Num Of", math.numOf(3, array)


loader = FileLoader("log.txt")
math = Math()

print math.sum(loader.getValues("Right Encoder"))
print loader.getValues("Right Velocity")

plt.plot([10, 20, 30, 20, 15, 13, 14, 12])
plt.ylabel('Battery Voltage')
plt.show()