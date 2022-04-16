from email import message
import imp
import re
from django.forms import forms
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group,User
from .forms import PostForm, SignUpForm, LoginForm ,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post


# Home
def home(request):
	posts=Post.objects.all()
	return render(request, 'blog/home.html',{'posts':posts})

# About


def about(request):
	return render(request, 'blog/about.html')

# Contact


def contact(request):
	return render(request, 'blog/contact.html')

# Dashboard


def dashboard(request):
	if request.user.is_authenticated:
		posts=Post.objects.all()
		user = request.user
		full_name = user.get_full_name()
		gps = user.groups.all()
		return render(request,'blog/dashboard.html',{"posts":posts,'user':user,'fname':full_name,'groups':gps})
	else:
		return HttpResponseRedirect('/login/')
        
# postdetail
def postdetail(request,id):
	post=Post.objects.get(pk=id)
	return render(request, 'blog/postdetail.html',{'post':post})

# Login


def user_login(request):
	if not request.user.is_authenticated:
		if request.method=="POST":
			form= LoginForm(request=request,data=request.POST)
			if form.is_valid():
				uname=form.cleaned_data['username']
				upass=form.cleaned_data['password']
				user=authenticate(username=uname,password=upass)
				if user is not None:
					login(request,user)
					messages.success(request,"Login Successfull !!!")
					return HttpResponseRedirect('/dashboard/')
		else:
			form=LoginForm()
		return render(request,'blog/login.html',{'form':form})
	else:
		return HttpResponseRedirect('/dashboard/')

	
	

# Signup
def signup(request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			messages.success(request,"Congratulation!! you have become an AUTHOR")
			user = form.save()
			group = Group.objects.get(name="Author")
			user.groups.add(group)
	else:
		form=SignUpForm()
	return render(request,'blog/signup.html',{'form':form})

# Logout
def user_logout(request):
	logout(request)
	messages.success(request,'Logout Successfull')
	return HttpResponseRedirect('/')

#add post
def addpost(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			form=PostForm(request.POST)
			if form.is_valid():
				title = form.cleaned_data['title']
				desc = form.cleaned_data['description']
				pst = Post(title=title,description=desc)
				pst.save()
				form = PostForm()
				messages.success(request,"Post Added Successfully !!!")
				return HttpResponseRedirect('/dashboard/')
		else:
			form = PostForm()
			return render(request,'blog/addpost.html',{'form':form}) 
	else:
		return HttpResponseRedirect("/login/")
def updatepost(request,id):
	if request.user.is_authenticated:
		if request.method=="POST":
			pi=Post.objects.get(pk=id)
			form=PostForm(request.POST,instance=pi)
			if form.is_valid():
				form.save()
				messages.success(request,"Post Updated Successfully !!!")
				return HttpResponseRedirect('/dashboard/')
		else:
			pi=Post.objects.get(pk=id)
			form=PostForm(instance=pi)
			return render(request,'blog/updatepost.html',{'form':form})

	else:
		return HttpResponseRedirect('/login/')
def deletepost(request,id):
	if request.user.is_authenticated:
		if request.method=="POST":
			pi=Post.objects.get(pk=id)
			pi.delete()
			messages.success(request,"Post Deleted Successfully !!!")
			return HttpResponseRedirect("/dashboard/")
		else:
			return HttpResponseRedirect('/login/')
		    
	else:
		return HttpResponseRedirect("/login/")
	  
	





