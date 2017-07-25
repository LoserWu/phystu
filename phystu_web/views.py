from django.shortcuts import render

# Create your views here.

def mainpage(request):
	context = {}
	return render(request,'phystu_web/mainpage.html',context)
