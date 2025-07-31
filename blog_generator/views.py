from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import yt_dlp
from django.conf import settings
import os
import assemblyai as aai
import requests
from dotenv import load_dotenv
from .models import BlogPost
from django.http import HttpResponse

load_dotenv()


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            # return JsonResponse({'content': yt_link})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        #get yt title
        title = yt_title(yt_link)
        #get yt transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)

        # use GROQAI to generate the blog
        blog_content = generate_blog_from_transcription(transcription )
        if not blog_content:
            return JsonResponse({'error' : "Failed to generate blog article"}, status=500)
        # save blog article to database
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content,
        )
        new_blog_article.save()


        # return blog article as a response
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def yt_title(yt_link):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,  
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_link, download=False)
            return info.get('title', 'No title found')
    except Exception as e:
        return f"Error fetching title: {str(e)}"

    
def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',  
        'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(id)s.%(ext)s'), 
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True, 
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = os.path.join(settings.MEDIA_ROOT, f"{info['id']}.mp3")
            return filename
    except Exception as e:
        print("Download audio error:", e)
        return None

def get_transcription(link):
    audio_file = download_audio(link)
    if not audio_file:
        raise ValueError("Failed to download audio from YouTube link.")

    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY") 

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    return transcript.text



api_key = os.getenv("GROQ_API_KEY")

def generate_blog_from_transcription(transcript):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a professional blog writer."},
            {"role": "user", "content": f"Write a blog post based on this transcript:\n{transcript}"}
        ],
        "model": "llama3-8b-8192"
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("GROQ API error:", e)
        return None

def generate_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog_details.html', {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid  user name or password"
            return render(request, 'login.html', {'error_message':error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message':error_message})
        else:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message':error_message})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')

# def debug_instance(request):
#     instance_name = os.getenv("INSTANCE_NAME", "unknown")
#     return HttpResponse(f"Hello from {instance_name}!")

def home(request):
    server_name = os.environ.get('SERVER_NAME', 'Unknown Server')
    return HttpResponse(f"This response is from {server_name}")
