from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json
import youtube_dl
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication 

def index(request):
    return render(request, 'index.html', {})


def extract(request):


    if request.POST:
        url = request.POST['url']
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': 'files/%(title)s.%(ext)s',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            format = ydl.extract_info(url , download=False)
            filename = format['title'] + ".mp3"


    resp = {'filename': filename}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def send(request):
    if request.POST:
        url = request.POST['url']
        email = request.POST['email']
        filename = request.POST['name']
        quality = request.POST['quality']
        download_mp3(url, quality, filename)

    mail_host="smtp.gmail.com"  #设置服务器
    mail_user=""    #用户名
    mail_pass=""   #口令 

    sender = 'zxtazur@gmail.com'
    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
     
    message = MIMEMultipart() 
    message["Subject"] = "Your music arrived!"
    message['From'] = Header("HelloTube", 'utf-8')
    message['To'] =  Header(email, 'utf-8')

    part = MIMEApplication(open('files/' + filename,'rb').read()) 
    part.add_header('Content-Disposition', 'attachment', filename=filename) 
    message.attach(part) 

    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()  
    server.starttls()
    server.login("", "")
    server.sendmail(sender, receivers, message.as_string())

    return HttpResponse("Send OK", content_type="application/text")


def create(request):
    if request.POST:
        url = request.POST['url']
        quality = request.POST['quality']
        name = request.POST['name']
        download_mp3(url, quality, name)

    return HttpResponse(name, content_type="application/text")


def download(request, name):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, encoding="latin-1") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break


    the_file_name = "files/" + name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'audio/mpeg'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
    return response

def download_mp3(url, quality, name):
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'outtmpl': 'files/' + name,
        }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

