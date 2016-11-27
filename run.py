import sqlite3
import urllib
import operator
import time
from BeautifulSoup import *

start = time.time()
print "Let's begin"
print "------------"

url =  "https://unacademy.in/user/alchemist95"
page = urllib.urlopen(url).read()
soup = BeautifulSoup(page)
figures = soup("span", {"class": "_2OSJuLMgr0cQ1lUZKGMPhl"})
print figures[2].contents[0]+" followers till now !!"
conn = sqlite3.connect('unacademy.sqlite')

cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Videos (videoName TEXT, plays INTEGER)')
cur.execute('DROP TABLE IF EXISTS Courses')
cur.execute('CREATE TABLE Courses (courseName TEXT, plays INTEGER)')	

stackCount = 0
codingCount = 0
acmCount = 0
newViews = 0
myUrl = "https://unacademy.in/lesson/"
myFile = open("videolist.txt", "r")
myList = myFile.read().split("\n")
newUrl = ""
videoName = ""
numberInt = 0
myD = dict()
count = 0
totalViews = 0
courseName = ""
for video in myList:
	count = count+1
	newUrl = myUrl + video
	page =  urllib.urlopen(newUrl).read()
	soup = BeautifulSoup(page)
	plays = soup("div", {"color":"tertiary", "style": "display:flex;align-content:space-between;font-size:1.5rem;line-height:2.1rem;color:rgb(180, 180, 180);"})
	number = plays[0].contents[0].contents[0]
	numberInt = int(number.split(" ")[0])
	videoName = video.split("/")[0]
	#print "Video Name :",videoName	
	cur.execute('SELECT videoName FROM Videos where videoName = ?', (videoName, ))

	try:
		data = cur.fetchone()[0]
		cur.execute('SELECT plays FROM Videos where videoName = ?',(videoName,))
		plays = cur.fetchone()[0]
		#print "Plays:",plays
		if numberInt != int(plays):
			print "For Video:",videoName,
			print "Plays increased from",plays,"to",numberInt
			print "\n"
			myD[videoName] = numberInt - plays	
			newViews = newViews + numberInt - plays
			cur.execute('UPDATE Videos SET plays = ? where videoName = ?', (numberInt, videoName))
	except:
		cur.execute('INSERT INTO Videos(videoName, plays) VALUES(?,?)', (videoName, numberInt))

	totalViews = totalViews + numberInt
	if count==8:
		courseName = "Understanding Stack for Coding Interviews"
		stackCount = totalViews
		cur.execute('INSERT INTO Courses(courseName, plays) VALUES(?,?)',(courseName, totalViews))
	elif count==16:
		courseName = "Top Coding Interview Questions and Solutions"
		codingCount = totalViews - stackCount
		cur.execute('INSERT INTO Courses(courseName, plays) VALUES(?,?)',(courseName,codingCount))
	elif count==21:
		courseName = "Solutions to ACM ICPC 2014 Problems"
		acmCount = totalViews - stackCount - codingCount
		cur.execute('INSERT INTO Courses(courseName, plays) VALUES(?,?)',(courseName,acmCount))
		
print "Total Views:",totalViews
print "Stack Course:",stackCount
print "Coding Interview Count:", codingCount
print "ACM Series Count:",acmCount
print "New plays:",newViews

if bool(myD):
	myD = sorted(myD.items(), key=operator.itemgetter(1), reverse=True)
	print "Most watched video of the day so far:",myD[0][0].upper()," watched",myD[0][1],"times"
end = time.time()
m, s = divmod(end-start, 60)
h, m = divmod(m, 60)
print "------------"
print "Total time taken is %d:%02d:%02d" % (h, m, s)
conn.commit()
cur.close()