# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cookielib
import urllib
import urllib2

BASE_URL = "http://www.kfckoreasurvey.com/";
Q_URL = "https://s.kfcvisit.com/kor/"

jar = cookielib.FileCookieJar("cookies")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

request_num = 0

def init():
	code = raw_input('스마트 코드를 입력해주세요 : ')
	print "초기화중입니다. 잠시만 기다려주세요."
	raw = opener.open(BASE_URL)
	read = raw.read()
	parsed = BeautifulSoup(read)
	data = {"JavaScriptEnabled":"1","FIP":"True","AcceptCookies":"True"}
	data = urllib.urlencode(data)
	req = urllib2.Request(Q_URL+str(parsed.find("form")['action']), data)
	raw = opener.open(req)
	read = raw.read()
	parsed = BeautifulSoup(read)
	data = {"JavaScriptEnabled":"1","FIP":"True","InputCouponNum":code}
	data = urllib.urlencode(data)
	req = urllib2.Request(Q_URL+str(parsed.find("form")['action']), data)
	nextStep(req)

def nextStep(req):
	global request_num
	request_num += 1
	print "Request #"+str(request_num)
	raw = opener.open(req)
	read = raw.read()
	parsed = BeautifulSoup(read)
	if not parsed.find("div", { "class" : "Error" }):
		vc = parsed.find("p", { "class" : "ValCode" })
		if vc:
			print vc.getText()
		else:
			data = {}
			fns = parsed.find(attrs={"name": "PostedFNS"})['value']
			fns_list = fns.split('|')
			for posted in fns_list:
				data[posted] = 2
			ionf = parsed.find(attrs={"name": "IoNF"})['value']
			data["IoNF"] = ionf
			data["PostedFNS"] = fns
			data = urllib.urlencode(data)
			req = urllib2.Request(Q_URL+str(parsed.find("form")['action']), data)
			nextStep(req)
	else:
		print "잘못된 코드입니다. 다시 시도해주세요. :("
		init()
init()
