# -*- coding: utf-8 -*-
'''
#title = 'IUPUI ET career job crawler (JS verison)'
#author = 'D Jin'

               ┏┓      ┏┓
              ┏┛┻━━━━━━┛┻┓
              ┃          ┃
              ┃  ┳┛  ┗┳  ┃
              ┃     ┻    ┃
              ┗━┓      ┏━┛
                ┃      ┗━━━━┓
                ┃  神兽保佑  ┣┓
                ┃　永无BUG！ ┏┛
                ┗━┓┓┏━━┳┓┏━━┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛

'''
from bs4 import BeautifulSoup  
from ghost import Ghost, Session
import re

class Crawler:
	
	def __init__(self,login_url,user_name,pass_word,job_url,referer_joblist):		
		self._username2 = user_name
		self._password2 = pass_word		
		self.joburl = job_url
		self.jobheader = {'Referer': referer_joblist, 'Connection': 'keep-alive'}
	
	def login(self):
		se.set_field_value("#username",self._username2)
		se.set_field_value("#password",self._password2)
		se.click(".btn_go",btn=0)

	def checkend(self):
		sss = BeautifulSoup(se.content, "html.parser")
		shres = sss.find(text="End of Jobs")
		print (shres)

		if (shres==None):
			print ("loop once")
			return 1
		else:
			print ("stop loop")
			return 0
	
	def openpage(self):
		se.open(self.joburl,headers=self.jobheader,user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36') 
		self.login() 
		se.wait_for_selector(".sumlist-body",timeout=None)		
		
		while (self.checkend()==1):
			se.evaluate("window.scroll(0, 20000)")
			print ("while loop")
			se.show()
		print ("All pages loaded")
		return se.content

	def Collecturl(self):
		allloadpage = self.openpage()
		finalpage = BeautifulSoup(allloadpage, 'html.parser')
		joburllist = []
		jobbaseurl = 'https://iupui-pset-csm.symplicity.com/students/index.php'
		joburlfind = finalpage.fina_all("a", class_="act")
		for alljob in joburlfind:
			href = alljob.get('href')
			joburllist.append(jobbaseurl+href)
		return joburllist

	def Autoapply(self):
		urllist = self.Collecturl()
		for jobinlist in urllist:
			se.open(jobinlist,headers=self.jobheader,user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
			se.wait_for_selector('#sb_timeline')
			cont = se.content()
			if se.exists(".buttons-td"):
				se.click('[name="dnf_opt_submit"]',btn=0)
			else:
				print ('这个得自己上网申请')
		print ('都申请好了')

	
login_url = 'https://iupui-pset-csm.symplicity.com/sso/students'
job_url = 'https://iupui-pset-csm.symplicity.com/students/index.php?s=jobs&ss=jobmatches&mode=list'
referer_joblist = 'https://iupui-pset-csm.symplicity.com/students/index.php?s=home'
user_name = input('username: ')
pass_word = input('password: ')

ghost = Ghost()
se = Session(ghost,wait_timeout=666,user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')

kaishi = Crawler(login_url,user_name,pass_word,job_url,referer_joblist)
kaishi.Autoapply()