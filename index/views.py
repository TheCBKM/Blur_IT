from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datauri import DataURI
from base64 import b64encode
import os
import datetime

from . import ipfs
from . import faceblur as fb
from . import compress as cp
from . import restore as rs

from .models import Record

# Create your views here.

def hello(req):
    return render(req, 'index/index.html')

def uploadImage(req):
    return render(req, 'index/upload.html')

def restore(req):
    return render(req, 'index/restore.html')



@csrf_exempt
def uploadBlur(request):

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

    beforeHash = ipfs.uploadIpfs(src)[0]['Hash']
    afterHash = ipfs.uploadIpfs(dest)[0]['Hash']
    print(beforeHash,afterHash)
    os.remove(src)
    os.remove(dest)
    rec = Record.objects.filter(afterhash=afterHash)
    if len(rec) == 0:
        print("unique")
        r = Record(afterhash=afterHash,beforehash=beforeHash, faces=str(face_locations))
        r.save()
        return HttpResponse(afterHash)
    else:
        print("same")
        return HttpResponse(afterHash)

@csrf_exempt
def uploadRestore(request):

    img = request.POST.get('img')
    mask = request.POST.get('mask')
    fname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    user_folder = 'media'
    src = f'{user_folder}/input/{fname}.png'
    maskdir=f'{user_folder}/input/m-{fname}.png'
    dest = f'{user_folder}/output/o-{fname}.png'

    uri=DataURI(img)

    fd=open(src,'wb')
    fd.write(uri.data)
    fd.close()


    uri=DataURI(mask)
    fd=open(maskdir,'wb')
    fd.write(uri.data)
    fd.close()


    cp.saveCompressed(src)
    rs.restore(src,maskdir,dest)   
    output_uri =b64encode(DataURI.from_file(dest).data)

    os.remove(src)
    os.remove(maskdir)
    os.remove(dest)


    return HttpResponse(output_uri)



    








def viewimg(req, hash_id):
    rec = Record.objects.filter(afterhash=hash_id)
    faces = rec[0].faces.strip('[]').strip('()').split('), (')
    print(faces)
    context = {
        'faceNum':len(faces),
        'faces':faces,
        'beforehash':rec[0].beforehash,
        'afterhash':rec[0].afterhash
         }
    return render(req, 'index/viewimg.html',context)


def gallery(req):
    rec = Record.objects.all()
    print(rec)
    return render(req, 'index/gallery.html',{"rec":rec})

    

