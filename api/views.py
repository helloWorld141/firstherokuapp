from django.http import JsonResponse, HttpResponse
from .utils.DimensionCalculator import calculateDims
import os, json
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.shortcuts import render
from channels import Group
from django.conf import settings

path = os.path.dirname(os.path.abspath(__file__))
hostname = settings.HOST
def test(req):
	return JsonResponse({"status": "running"})

@csrf_exempt
def dims(req):
	if req.method == 'POST':
		mockArgs = {
			"image": path+ "/resource/img/2.png",
			"width": "1"
		}
		print(req)
		print('Reqest: ', req.FILES, req.POST)
		if ( not req.FILES.get('image') or  not req.POST.get('width')):
			return HttpResponse(content="Bad request. Please include image and width", status=400)
		image = req.FILES['image']
		width = parse(req.POST['width'])
		imgpath = saveImage(image)
		realArgs = {
			"image": imgpath,
			"width": width
		}
		res = calculateDims(realArgs)
		print("Response: ", res)
		Group('staff').send({'text': json.dumps(res)}, immediately=True)
		return JsonResponse({"objects": res})

	if req.method == "GET":
		Group('cam').send({'text': '{"take_picture": true }'}, immediately=True)
		return JsonResponse({'status': 'pending',
			'subscribe_url': 'ws://' + hostname + '/staff/'
			})

def parse(width):
	w = width.split('\r\n')
	print(w)
	return w[0]

#image: class 'django.core.files.uploadedfile.InMemoryUploadedFile'
def saveImage(image):
	imgpath = path+ "/resource/img/" + image.name
	with open(imgpath, 'wb+') as f:
		for chunk in image.chunks():
			f.write(chunk)
	return imgpath

def testWSCam(req):
	return render(req, 'api/cam_ws_init.html')

def testWSStaff(req):
	return render(req, 'api/staff_ws_init.html')