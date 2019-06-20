from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json


def index(request):
    return render(request, 'index.html', {})


def extract(request):
    if request.POST:
        url = request.POST['url']
    resp = {'filename': "ttdd", 'size': 'filesize'}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def send(request):
    if request.POST:
        url = request.POST['url']
        email = request.POST['email']
        quality = request.POST['quality']

    return HttpResponse("Send OK", content_type="application/text")


def create(request):
    if request.POST:
        url = request.POST['url']
        quality = request.POST['quality']

    # Wait for 5 seconds
    time.sleep(5)
    
    the_file_name = "test.mp3"
    return HttpResponse(the_file_name, content_type="application/text")


def download(request, name):
    if request.POST:
        url = request.POST['url']
        quality = request.POST['quality']

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, encoding="latin-1") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "files\\" + name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'audio/mpeg'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
    return response


