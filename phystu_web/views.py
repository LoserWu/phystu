# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from django.http import HttpResponse,Http404
import phyion.models as mo
from django.template import Context
import os
# Create your views here.
#return HttpResponse(function)

head='http://127.0.0.1:8000/'

def Begin(request):
	return render(request,'manage.html',{})
	
def Manage(request,function):
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
			for image,style in zip(ftext[4:9:2],ftext[5:10:2]):
				img.append("{% static 'News\\"+news.split('.')[0]+'\\'+image+"' %}")
				sty.append('"width:'+str(style.split('#')[0])+';height:'+str(style.split('#')[-1])+';"')
			aut='作者:'+ftext[2].split('#')[0]+'\n摄影:'+ftext[2].split('#')[1]
			if len(ftext[2].split('#'))>2 :
				aut=aut+'\n协助编辑:'+ftext[2].split('#')[2]
			new=mo.News(
					title=ftext[0],
					subtitle=ftext[1],
					author=aut,
					timestamp=ftext[3],
					image1=img[0],
					image2=img[1],
					image3=img[2],
					style1=sty[0],
					style2=sty[1],
					style3=sty[2],
					email=ftext[10],
					text='<p>'+'</p><p>'.join(ftext[11:])+'</p>',
					url=head+'news/'+ftext[3].replace('\n','')+'/'+ftext[10].split('@')[0]+'/'
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
				image=os.path.abspath(__file__).replace('views.py','..\\static\\Section\\'+section.split('.')[0]+'\\'+text[1]),
				style='"width:'+text[2].split('#')[0]+';height:'+text[2].split('#')[-1]+';"',
				host=text[3],
				sub=text[4].replace('#','  '),
				email=text[5],
				introduction='<p>'+'</p><p>'.join(text[6:])+'</p>',
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
			url=head+'resource/'+ty+'/'+nam+'/'
		)
		res.save()
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}
	
def ReadActivity(activity):
	try:
		with open(os.path.abspath(__file__).replace('views.pv','..\\static\\Activity\\'+activity.split('.')[0]+'\\'+activity)) as fp:
			text=fp.readlines()
			act=mo.Activity(
				title=text[0],
				timestamp=text[1],
				image="\"{% static 'Acctivity\\activity\\"+activity.split('.')[0]+'\\'+text[2]+"' %}",
				style='"width:'+text[3].split('#')[0]+';height:'+text[3].split('#')[-1]+';"',
				host=text[4],
				undertake=text[5].replace('#','\n'),
				email=text[6],
				introduction='<p>'+'</p><p>'.join(text[7:])+'</p>',
				url=head+'activity/'+timestamp+'/'+email.split('@')[0]+'/'
				)
			act.save()
			
		return {'result':'Succeed!','ps':'Finish.'}
	except Exception, e:
		return {'result':'Fail!','ps':str(e)}

def NewsList(request):
	return render(request,'Newslist.html',{'ActList':mo.News.objects.all()})

def ActivityList(request):
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

def Home(request):
	return render(request,'Home.html',{})
	
def News(request,time,emailaddr):
	#return HttpResponse((mo.News.objects.all()).email)
	return render(request,'News.html',{'news':mo.News.objects.get(email=(emailaddr+'@mail.ustc.edu.cn'))})
	
def Activity(request,time,emailaddr):
	return render(request,'Activity.html',{'activity':mo.Activity.objects.get(email=(emailaddr+'@mail.uxtc.edu.cn'))})
	
def Section(request,emailaddr):
	return render(request,'Section.html',{'section':mo.Section.objects.filter(email=(emailaddr+'@mail.ustc.edu.cn'))})