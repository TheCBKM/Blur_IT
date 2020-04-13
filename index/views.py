from django.shortcuts import render
from django.http import HttpResponse
import os
import datetime

from . import ipfs
from . import faceblur as fb
from . import compress as cp

from .models import Record

# Create your views here.


def hello(req):
    return render(req, 'index/index.html')


def upload(request):

    img = request.FILES['f']
    img_extension = os.path.splitext(img.name)[1]
    print(img, img_extension)
    fname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    user_folder = 'media'
    src = f'{user_folder}/input/{fname}{img_extension}'
    dest = f'{user_folder}/output/o-{fname}{img_extension}'

    print(src, dest)

    with open(src, 'wb+') as f:
        for chunk in img.chunks():
            f.write(chunk)

    cp.saveCompressed(src)
    face_locations = fb.face_blur(src, dest)
    print(face_locations)
    os.remove(src)
    res = ipfs.uploadIpfs(dest)
    print(res)
    hash_id = res[0]['Hash']
    os.remove(dest)
    rec = Record.objects.filter(hash=hash_id)
    if len(rec) == 0:
        print("unique")
        r = Record(hash=hash_id, faces=str(face_locations))
        r.save()
        return HttpResponse(hash_id)
    else:
        print("same")
        return HttpResponse(rec[0].hash)


def viewimg(req, hash_id):
    rec = Record.objects.filter(hash=hash_id)
    faces = rec[0].faces.strip('[]').strip('()').split('), (')
    print(faces)
    context = {
        'faceNum':len(faces),
        'faces':faces,
        'hash':rec[0].hash
         }
    return render(req, 'index/viewimg.html',context)


def gallery(req):
    rec = Record.objects.all()
    print(rec)
    return render(req, 'index/gallery.html',{"rec":rec})

    

