from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from customer.chat import get_response,bot_name
from datetime import date, timedelta
import speech_recognition as sr
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from medical import models as CMODEL
from medical import forms as CFORM
from googletrans import Translator
from translate import Translator as trans
from django.views.generic import TemplateView
from django.contrib.auth.models import User


def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()

            # if (models.Customer.user.get_object() == user):
            #     print("SAME")

            print("USER: ", user)
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            
        return HttpResponseRedirect('customerlogin')

    return render(request,'customer/customersignup.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

class eng(TemplateView):
    Template_view="customer/eng.html"
    def get(self,request):
        return render(request,self.Template_view)

    def post(self,request):
        if request.method == 'POST':
            user = request.POST.get('input', False)
            context={"user":user,"bot":get_response(user)}	

        return render(request,self.Template_view,context)

class engm(TemplateView):
    Template_view="customer/engm.html"
    def get(self,request):
        return render(request,self.Template_view)
    def post(self,request):
        if request.method == 'POST':
                        r = sr.Recognizer()
                        print("Please talk")
                        with sr.Microphone() as source:
                        # read the audio data from the default microphone
                                audio_data = r.record(source, duration=6)
                                print("Recognizing...")
                                # convert speech to recognisedSpeech
                                recognisedSpeech = r.recognize_google(audio_data)
                                print("Recognised Speech:" + recognisedSpeech)
                                a=recognisedSpeech
                                translator = Translator()
                                source_lan = "mr"
                                translated_to= "hi"
                                translated_text = translator.translate(recognisedSpeech, src=source_lan, dest = translated_to)
                                res=translated_text.text
                                print(translated_text.text)
                                translator1 = Translator()
                                source_lan1 = "hi"
                                translated_to1= "en"
                                translated_text1 = translator1.translate(res, src=source_lan1, dest = translated_to1)
                        
                                print(translated_text1.text)
                                a_res=translated_text1.text
                                #translator5 = trans(from_lang="en", to_lang="hi")
                                #data3 = translator5.translate(text)
                                #print(data3)
                                result=get_response(a_res)
                                print(result)
                                translator2 = Translator()
                                source_lan2 = "en"
                                translated_to2= "mr"
                                translated_text2 = translator2.translate(result, src=source_lan2, dest = translated_to2)
                        
                                print(translated_text2.text)
                                final=translated_text2.text
                                
                                #print(r)
                                context={"user":res,"bot":final}
                        
                        return render(request,self.Template_view,context)

class engh(TemplateView):
    Template_view="customer/engh.html"
    def get(self,request):
        return render(request,self.Template_view)

    def post(self,request):
        if request.method == 'POST':
            r = sr.Recognizer()
            print("Please talk")

            toEng = ""
            userInput = ""
            with sr.Microphone() as source:
            # read the audio data from the default microphone
                    audio_data = r.record(source, duration=16)
                    print("Recognizing...")
                    # convert speech to recognisedSpeech
                    recognisedSpeech = r.recognize_google(audio_data)
                    print("Recognised Speech: " + recognisedSpeech)
                    userInput = recognisedSpeech

                    translator = Translator()
                    source_lan = "hi"
                    translated_to= "en"
                    translated_text = translator.translate(recognisedSpeech, src=source_lan, dest = translated_to)
                    
                    toEng = translated_text.text

                    res=translated_text.text
                    print(translated_text.text)
                    translator5 = trans(from_lang="en", to_lang="hi")
                    data3 = translator5.translate(recognisedSpeech)
                    print(data3)

            result = get_response(toEng)

            translator6 = trans(from_lang="en", to_lang="hi")
            r = translator6.translate(result)
            print(r)
            context={"user":userInput,"bot":r}

            return render(request, self.Template_view, context)



@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),   
    }
    
    if request.method == 'POST':
        user = request.POST.get('input',False)
        context1={"user":user,"bot":get_response(user)}
			
		
    return render(request,'customer/customer_dashboard.html',context=dict)
''' 
class home(TemplateView):
	Template_view="index.html"

	def get(self,request):
		return render(request,self.Template_view)

	def post(self,request):
		if request.method == 'POST':
			user = request.POST.get('input',False)
			context={"user":user,"bot":get_response(user)}
			
		return render(request,self.Template_view,context)
      
class hindi(TemplateView):
	Template_view="customer/hindi.html"

	def get(self,request):
		return render(request,self.Template_view)

	def post(self,request):
		if request.method == 'POST':
                        r = sr.Recognizer()
                        print("Please talk")
                        with sr.Microphone() as source:
                        # read the audio data from the default microphone
                                audio_data = r.record(source, duration=10)
                                print("Recognizing...")
                                # convert speech to text
                                text = r.recognize_google(audio_data)
                                print("Recognised Speech:" + text)
                                a=text
                                translator = Translator()
                                source_lan = "hi"
                                translated_to= "en"
                                translated_text = translator.translate(text, src=source_lan, dest = translated_to)
                                res=translated_text.text
                                print(translated_text.text)
                                translator5 = trans(from_lang="en", to_lang="hi")
                                data3 = translator5.translate(text)
                                print(data3)
                                result=get_response(res)
                                translator6 = trans(from_lang="en", to_lang="hi")
                                r = translator5.translate(result)
                                print(r)
                                context={"user":data3,"bot":r}
                        return render(request,self.Template_view,context)
class marathi(TemplateView):
	Template_view="customer/marathi.html"

	def get(self,request):
		return render(request,self.Template_view)

	def post(self,request):
		if request.method == 'POST':
			user = request.POST.get('input',False)
			context={"user":user,"bot":get_response(user)}
			
		return render(request,self.Template_view,context)
        '''