from django.http import JsonResponse
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