#by R.S
#This code gives constant notification about football world cup 2018 live scores in an specific interval
#usage: python3 football.py -m match_no -t time_in_min

from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import notify2
import sys
import argparse
import time


parser=argparse.ArgumentParser()
parser.add_argument('-m', nargs='?', const=1, type=int,default=58)          #argument for match_no default:58
parser.add_argument('-t', nargs='?', const=1, type=int,default=600)         #argument for interval defauly:10min
args=parser.parse_args()


#data fetching done here
def fetchdata():
	try:

		m_no=args.m
		id='mid1-20596'+str(int(m_no)-14)

	except:
		print('Error in argument')

	try:
		req=Request(url='http://www.livefootball.com/football/world-cup/',headers={'User-Agent': 'Mozilla/5.0'})
		respons=urlopen(req)
		response=respons.read()
		print(respons.getcode())
	except:
		print("connection Error")
		exit()
	if(respons.getcode()==200):
		try:
			soup=BeautifulSoup(response,'html.parser')
			results_pr= soup.body.find('dl',attrs={'id':str(id)}).find_all("dd")
		except:
			print("Error while parsing")
			exit("parsing error")
	stat=results_pr[0].text
	t1=results_pr[1].text
	score=results_pr[2].text
	t2=results_pr[3].text
	print(stat+" "+t1+" "+t2+" "+score)

	return(t1,t2,stat,score)

#for notification
def notify(t1,t2,stat,score):
	notify2.init("Score notification")
	n=notify2.Notification(None,icon = str(str(sys.path[0])+'/football.jpg'))
	n.set_urgency(notify2.URGENCY_NORMAL)
	n.set_timeout(1)
	n.update("    "+(str(t1)+"   vs   "+str(t2))+"      ","|\n|\n|\t\t\t"+str(stat)+"\n|\n|\n\t\t\t"+str(score))
	n.show()


if __name__ == '__main__':

	t1,t2,stat,score=fetchdata()
	notify(t1,t2,stat,score)
	print(stat)

	while(score!='v' and stat!='FT' and stat!='AET'):
		try:
			t1,t2,stat,score=fetchdata()
			notify(t1,t2,stat,score)

		except KeyboardInterrupt:
			print('Football over :(\nCode again!')

		finally:
			time.sleep(args.t*60)
			