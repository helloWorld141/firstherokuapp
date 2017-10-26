from django.http import JsonResponse, HttpResponse
from .utils.DimensionCalculator import calculateDims
import os, json
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

path = os.path.dirname(os.path.abspath(__file__))

def test(req):
	return JsonResponse({"status": "running"})

@csrf_exempt
def dims(req):
	mockArgs = {
		"image": path+ "/resource/img/2.png",
		"width": "1"
	}
	print('Reqest: ', req.FILES, req.POST)
	if ( not req.FILES.get('image') or  not req.POST.get('width')):
		return HttpResponse(content="Bad request. Please include image and width", status=400)
	image = req.FILES['image']
	imgpath = saveImage(image)
	realArgs = {
		"image": imgpath,
		"width": req.POST['width']
	}
	res = calculateDims(realArgs)
	print("Response: ", res)
	return JsonResponse({"objects": res})

#image: class 'django.core.files.uploadedfile.InMemoryUploadedFile'
def saveImage(image):
	imgpath = path+ "/resource/img/" + image.name
	with open(imgpath, 'wb+') as f:
		for chunk in image.chunks():
			f.write(chunk)
	return imgpath