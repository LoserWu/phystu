# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from django.http import HttpResponse,Http404,StreamingHttpResponse
import phyion.models as mo
from django.template import Context
import os
# Create your views here.
#return HttpResponse(function)

head='http://127.0.0.1:8000/'

def Begin(request):
	return render(request,'manage.html',{})

def Manage(request,function):
	#return HttpResponse(function)
	return render(request,'Result.html',eval(function))

def Init():
	initlist=['Section','News','Activity','Resource']
	namelist=[]
	try:
		for name in initlist:
			for parent,dirnames,filenames in os.walk(os.path.dirname(os.path.abspath(__file__).replace('views.py','..\\static\\'+name+'\\'))):
				for filename in  filenames:
					#namelist.append(filename)
					eval('Read'+name+'("'+filename+'")')
		return {'result':'Succeed!','ps':'Finish'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def ReadNews(news):
	try:
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\News\\'+news.split('.')[0]+'\\'+news),'r') as fp:
			ftext=fp.readlines()
			img=[]
			sty=[]
			for image in ftext[4:6]:
				img.append("/static/News/"+news.split('.')[0]+'/'+image)
				
			aut='<p align=\"center\">作者:'+ftext[2].split('#')[0]+'</p><p align=\"center\">摄影:'+ftext[2].split('#')[1]+'</p>'
			if len(ftext[2].split('#'))>2 :
				aut=aut+'<p align="center">协助编辑:'+ftext[2].split('#')[2]+'</p>'
			new=mo.News(
					title=ftext[0],
					subtitle=ftext[1],
					author=aut,
					timestamp=ftext[3].split('\n')[0],
					image1=img[0],
					image2=img[1],
					email=ftext[6].split('\n')[0],
					text='<p>'+'</p><p>'.join(ftext[7:])+'</p>',
					url=head+'news/'+ftext[3].split('\n')[0]
				)
			new.save()
			
			return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def ReadSection(section):
	try:
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\Section\\'+section.split('.')[0]+'\\'+section),'r') as fp:
			text=fp.read().split('\n')
			sec=mo.Section(
				Name=text[0],
				image='/static/Section/'+section.split('.')[0]+'/'+text[1],
				host=text[2],
				sub=text[3].replace('#','  '),
				email=text[4],
				introduction='<p>'+'</p><p>'.join(text[5:])+'</p>',
			)
			sec.save()
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def ReadResource(resource):
	vedio=['mp4','mkv','rm','rmvb','3gp','avi','wmv','mp3','wav','wma','ogg','ape','acc','cda','flac','aac']
	picture=['bmp','jpg','gif','jpeg','tiff','psd','png','swf','svg','dxf''eps']
	sty='Defualt'
	try:
		nam=resource
		if resource.split('.')[-1] in vedio:
			ty='vedio'
		elif resource.split('.')[-1] in picture:
			ty='picture'
		else:
			ty='doc'
			sty=resource.split('-')[0]
			nam=resource.split('-')[1]
		
		res=mo.Resource(
			name=nam,
			type=ty,
			style=sty,
			url=head+'download/'+resource
		)
		res.save()
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def DeleteSection(section):
	try:
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\Section\\'+section.split('.')[0]+'\\'+section),'r') as fp:
			text=fp.read().split('\n')
			mo.Section.get(Name=text[0]).delete()
		return {'result':'Succeed!','ps':'Finish!'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def DeleteResource(resource):
	vedio=['mp4','mkv','rm','rmvb','3gp','avi','wmv','mp3','wav','wma','ogg','ape','acc','cda','flac','aac']
	picture=['bmp','jpg','gif','jpeg','tiff','psd','png','swf','svg','dxf''eps']
	try:
		nam=resource
		if resource.split('.')[-1] in vedio:
			ty='vedio'
		elif resource.split('.')[-1] in picture:
			ty='picture'
		else:
			ty='doc'
			sty=resource.split('-')[0]
			nam=resource.split('-')[1]
		mo.Resource.get(name=nam).delete()
		for parent,dirnames,filenames in os.walk(os.path.dirname(os.path.abspath(__file__).replace('views.py','..\\static\\Resource\\'+resource.split('.')[0]))):
			for filename in  filenames:
				os.remove(os.path.abspath(__file__).replace('views.py','..\\static\\Resource\\'+resource.split('.')[0]+'\\'+filename))
		os.rmdir(os.path.abspath(__file__).replace('views.py','..\\static\\Resource\\'+resource.split('.')[0]))
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def DeleteNews(news):
	try:
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\News\\'+news.split('.')[0]+'\\'+news),'r') as fp:
			text=fp.readlines()
			mo.News.get(title=text[0]).delete()
			for parent,dirnames,filenames in os.walk(os.path.dirname(os.path.abspath(__file__).replace('views.py','..\\static\\News\\'+news.split('.')[0]))):
				for filename in  filenames:
					os.remove(os.path.abspath(__file__).replace('views.py','..\\static\\News\\'+news.split('.')[0]+'\\'+filename))
			os.rmdir(os.path.abspath(__file__).replace('views.py','..\\static\\News\\'+news.split('.')[0]))
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def DeleteActivity(activity):
	try:
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\Activity\\'+activity.split('.')[0]+'\\'+activity),'r') as fp:
			text=fp.readlines()
			mo.News.get(title=text[0]).delete()
			for parent,dirnames,filenames in os.walk(os.path.dirname(os.path.abspath(__file__).replace('views.py','..\\static\\Activity\\'+activity.split('.')[0]))):
				for filename in  filenames:
					os.remove(os.path.abspath(__file__).replace('views.py','..\\static\\Activity\\'+activity.split('.')[0]+'\\'+filename))
			os.rmdir(os.path.abspath(__file__).replace('views.py','..\\static\\Activity\\'+activity.split('.')[0]))
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def ReadActivity(activity):

	try:
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\Activity\\'+activity.split('.')[0]+'\\'+activity),'r') as fp:
			text=fp.read().split('\n')
			act=mo.Activity(
				title=text[0],
				timestamp=text[1].split('\n')[0],
				image="/static/Activity/"+activity.split('.')[0]+'/'+text[2],
				host=text[3],
				undertake=text[4].replace('#',' ； '),
				email=text[5].split('\n')[0],
				introduction='<p>'+'</p><p>'.join(text[6:])+'</p>',
				url=head+'activity/'+text[1].split('\n')[0]
				)
			act.save()
			return {'result':'Succeed!','ps':'Finish!'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def NewsList(request):
	return render(request,'Newslist.html',{'ActList':mo.News.objects.all()})

def ActivityList(request):
	#return HttpResponse(mo.Activity.objects.all())
	return render(request,'Activitylist.html',{'ActivityList':mo.Activity.objects.all()})
	
def ResourceList(request):
	return render(request,'Resourcelist.html',{'VedioList':mo.Resource.objects.filter(type='vedio'),'PictureList':mo.Resource.objects.filter(type='picture'),'DocList':mo.Resource.objects.filter(type='doc')})
	
def Mail(request):
	me=request.Get.get('sub')+'<1367190098@qq.com>'
	context='<p>Name:'+request.Get.get('name')+'</p><p>Email:'+request.Get.get('email')+'</p><p>Student ID:'+request.Get.get('studentid')+'</p><p>Phone:'+request.Get.get('phone')+'</p>'
	if request.Get.get('sub')=='意见反馈' :
		context=context+'<p>'+request.Get.get('suggest')+'</p>'
	msg = MIMEText(context,'html','utf-8')
	msg['Subject'] = Header(sub,'utf-8')
	msg['From'] = me
	msg['To'] = ','+(request.Get.get('tomail'))
	
	try:
		server=smtplib.SMTP_SSL("smtp.qq.com",465)
		server.connect("smtp.qq.com")
		server.login('1367190098',"uqhmihabuowlidjb" )
		server.sendmail(me,request.Get.get('tomail'),msg.as_string())
		server.quit()
		return render(request,'Result.html',{'result':'Succeed!','ps':'Thanks!'})
	except Exception, e:
		print str(e)
		return render(request,'Result.html',{'result':'Fail!','ps':'Pleause send mail to '+request.Get.get('tomail')+'by yourself. Thanks.'})

def UploadFile(request):
	if request.method=="POST" :
		myFile=request.FILES.get("myfile",None)
	if myFile==None:
		return render(request,'Result.html',{'result':'Fail!','ps':"no files for upload!"})
	if not os.path.exists(os.path.abspath(__file__).replace('views.py','..\\static\\'+myFile.name.split('.')[0]+'\\'+myFile.name.split('.')[1])):
		os.mkdir(os.path.abspath(__file__).replace('views.py','..\\static\\'+myFile.name.split('.')[0]+'\\'+myFile.name.split('.')[1]))
	
	try:		
		with open(os.path.abspath(__file__).replace('views.py','..\\static\\'+str(myFile.name.split('.')[0])+'\\'+str(myFile.name.split('.')[1])+'\\'+'.'.join(myFile.name.split('.')[2:])),'wb+') as des:
			for chunk in myFile.chunks():
				des.write(chunk)
			return render(request,'Result.html',{'result':'Succeed!','ps':'The file has been uploaded successfully!'})
	except Exception, e:
		return render(request,'Result.html',{'result':'Fail!','ps':str(e)})

def DownloadFile(request,filename):		
	#return HttpResponse(filename)
	response=StreamingHttpResponse(ReadFile(os.path.abspath(__file__).replace('views.py','..\\static\\Resource\\'+filename)))
	response['Content-Type']='application/octet-stream'
	response['Content-Disposition']='attachment;filename="{0}"'.format(filename)
	return response

def ReadFile(filename,chunk_size=512):
	with open(filename,'rb') as f:
		while True:
			c=f.read(chunk_size)
			if c:
				yield c
			else:
				break
		
def Home(request):
	return render(request,'Home.html',{})
	
def News(request,time):
	return render(request,'News.html',{'news':mo.News.objects.filter(timestamp=time),})
	
def Activity(request,time):
	return render(request,'Activity.html',{'activity':mo.Activity.objects.get(timestamp=time)})
	
def Section(request,emailaddr):
	emailaddr=emailaddr+'@mail.ustc.edu.cn'
	return render(request,'Section.html',{'sec':mo.Section.objects.filter(email=emailaddr),})