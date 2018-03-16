import os
from django.shortcuts import render,redirect
from dashboard.forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm
from dashboard.models import UserModel,PostModel,SessionToken,LikeModel,CommentModel
from django.http import HttpResponse,JsonResponse
from datetime import timedelta,datetime
from myapp.settings import BASE_DIR,IMGUR_CLIENT_ID,IMGUR_CLIENT_SECRET

from imgurpython import ImgurClient

from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

def signup_view(request):
    now_time=datetime.now()
    if request.method=="POST":

        form=SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            #encrpyt the password
            password=make_password(password)

            #saving data to DB
            user=UserModel(name=name,username=username,email=email,password=password)
            user.save()
            return render(request,'success.html')
        
    else:
        form=SignUpForm()
    return render(request,'signUp.html',{'now':now_time,'form':form})

def login_view(request):
    #response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            error_msg=""
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #read data from Db  
            user = UserModel.objects.filter(username=username).first()

            if user:
                #compare password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    #ewdirect to feed
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    error_msg = 'Incorrect Password! Please try again!'
                    return render(request,'login.html',{'error_msg':error_msg})              
    else:
        
        form = LoginForm()
        return render(request, 'login.html', {'login_form':form})


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                new_post = PostModel(user=user, image=image, caption=caption)
                new_post.save()

                #path = str(BASE_DIR + new_post.image.url)
                path = os.path.join(BASE_DIR, new_post.image.url)
                client = ImgurClient(IMGUR_CLIENT_ID,IMGUR_CLIENT_SECRET)
                new_post.image_url = client.upload_from_path(path,anon=True)['link']
                
                new_post.save()

                return redirect('/feed')
                #return HttpResponse('Image Saved')
        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post=post, user=user).first()
            if existing_like:
                #post is already liked
                post.is_liked = True
            
        return render(request, 'feed.html',{'posts':posts})
    else:

        return redirect('/login/')

def logout_view(request):
    response = redirect("/")
    response.delete_cookie("session_token")
    return response

def like_view(request):
    user=check_validation(request)
    if user:
        #user is logged in
        if request.method == 'GET':
            return redirect('/feed/')
        else:
            #form is submitted
            like_form = LikeForm(request.POST)
            if like_form.is_valid():
                post_id = like_form.cleaned_data.get('post')

                existing_like = LikeModel.objects.filter(post=post_id,user=user).first()
                #when only we need to check if value exists or not we use .exists()with the result of database
                if not existing_like:
                    #post is not liked
                    LikeModel.objects.create(post=post_id, user=user)#this is a new way to save data without using save method
                else:
                    #post is already liked
                    existing_like.delete()
                return redirect("/feed/")
            else:
                return HttpResponse("Form Data is invalid")
    else:
        return redirect("/login/")


def comment_view(request):
    user=check_validation(request)
    if user:
         #user already loged in
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                post_id = comment_form.cleaned_data.get('post')
                comment_text = comment_form.cleaned_data.get('comment')


                #save this data in Database
                CommentModel.objects.create(post=post_id,user=user,comment=comment_text)
                return redirect("/feed/")

        else:
            pass
    else:
        #user not loged in
        return redirect("/login/")



def home_view(request):
    user=check_validation(request)
    if user:
        return redirect('/feed/')

    return render(request,'home.html')


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
        else:
            return None