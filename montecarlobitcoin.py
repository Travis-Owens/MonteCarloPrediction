import sys
import time
import random
import csv
import numpy as np
import matplotlib.pyplot as plt
import requests

n = 365*1 #number of days/years we want to simulate.
x = 25 #number of diffirent simulations
f = 24 #factor, increases or decreases density

csvFile = 'CSV/28_10_2018/market-price.csv'

savePlot = True #Save plot as image in working dir, True by default
imgName = "" #leave blank for time
imgFormat = ".png" #.png .jpeg .jpg .pdf .raw


#Verbose false is default, true for iterative messages (will slow down)
try:
	if(sys.argv[1] == '-v'):
		v = True
				#run the following for verbose:
				#python montecarlobitcoin.py -v
	else:
		v = False
except:
	v = False

def getBitcoinPrice():
	try:
		data = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
		price = data['bpi']['USD']['rate_float']
	except:
		if(v == True): 
			print("Coindesk API price look up failed")
			print("Please enter current bitcoin price: ", end='', flush=True)
			price = float(input())
		else:
			price = 6000

	return price

currentPrice = getBitcoinPrice()

def getTrueBitcoinPriceChange():
	truePrice = []
	truePercentualChangeArr = []
	print("Loading CSV file: ", csvFile)
	with open(csvFile) as pricelist:
			csvdoc = csv.reader(pricelist)
			for row in csvdoc:
				currPrice = float(row[1])
				if(v):
					date=row[0]
					print("r:{} $:{}".format(date[:10],currPrice))
				if(int(currPrice) <= 25000):
					truePrice.append(int(currPrice))
					truePercentualChangeArr.append(abs((truePrice[-1]-currPrice)/100))
			avrgPercentualChange = abs(sum(truePercentualChangeArr)/len(truePercentualChangeArr))
	return (avrgPercentualChange/f)

def simulation(currentPrice,s,x):
	currentSim = []
	for i in range(n*f):
		if(v):
			print("Simulation {} of {}. Day {} of {}".format(s+1,x,i+1,n*f))
		currentPrice = currentPrice + currentPrice * (random.choice([(change * -1), change]))
		currentSim.append(currentPrice)
	plt.plot(currentSim)

def plot():
	plt.title("Possible Asset price with avrg {}% daily change".format(round((change*f)*100,3)))
	plt.xlabel("Time in days/{}".format(f))
	plt.ylabel("Price in $")
	plt.grid(color='black', linestyle='--', linewidth=.5, alpha=.3)

	if(savePlot):
		if(imgName == ""):
			plt.savefig("IMG/" + str(time.strftime("%b_%d_%Y__[%H-%M-%S]")) + imgFormat)
		else:
			plt.savefig("IMG/" + imgName + imgFormat)
	plt.show()



change = round(getTrueBitcoinPriceChange(),6)
print("Average % change in the past year:", round((change*f)*100,3))
for i in range(x):
	if((i+1)%10==0):
		print("Simulation n: ",i+1)
	simulation(currentPrice,i,x)


plot()
