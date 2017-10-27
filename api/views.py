from django.http import JsonResponse, HttpResponse
from .utils.DimensionCalculator import calculateDims
#from .utils.object_size import process_image
import os, json, sys
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.shortcuts import render
from channels import Group
from django.conf import settings
from api.models import Cargo

path = os.path.dirname(os.path.abspath(__file__))
hostname = settings.HOST
def test(req):
	return JsonResponse({"status": "running"})

@csrf_exempt
def dims(req):
	if req.method == 'POST':
		mockArgs = {
			"id": 1401,
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
		if req.GET.get('id'):
			id = req.GET['id']
			Group('cam').send({'text': '{"take_picture": true, "id": "'+ id + '"}'}, immediately=True)
			return JsonResponse({'status': 'pending',
				'subscribe_url': 'ws://' + hostname + '/staff/'
				})
		else:
			return JsonResponse({'message': 'please provide provide id of the cargo'})

def parse(width):
	w = width.split('\r\n')
	print(w)
	return w[0]

#image: class 'django.core.files.uploadedfile.InMemoryUploadedFile'
def saveImage(id, image):
	imgpath = path+ "/resource/img/" + id
	with open(imgpath, 'wb+') as f:
		for chunk in image.chunks():
			f.write(chunk)
	return imgpath

def testWSCam(req):
	return render(req, 'api/cam_ws_init.html')

def testWSStaff(req):
	return render(req, 'api/staff_ws_init.html')

@csrf_exempt
def cargo(req):
	if req.method == 'GET':
		#TODO: get one cargo
		if req.GET.get('id'):
			id = req.GET.get('id')
			cargo = Cargo.objects.filter(id=id).values()
			print(cargo)
			return JsonResponse(list(cargo), safe=False)
		else:
			cargo_list = Cargo.objects.all().values()
			return JsonResponse(list(cargo_list), safe=False)
	if req.method == 'POST':
		try :
			id = req.POST.get('id', '1401')
			dimensions = req.POST.get('dimensions')
			tiltable = json.loads(req.POST.get('tiltable', 'false'))
			stackable = json.loads(req.POST.get('stackable', 'false'))
			pieces = json.loads(req.POST.get('pieces', 1))
			take_picture = json.loads(req.POST.get('take_picture', 'false'))
			print(id, dimensions, tiltable, stackable, take_picture, pieces)
			if not take_picture:
				print('not taking picture')
				Cargo.objects.create(id=id, dims=dimensions, tiltable=tiltable, stackable=stackable, pieces=pieces)
				return JsonResponse({'created': True})
			else:
				Cargo.objects.create(id=id, dims=dimensions, tiltable=tiltable, stackable=stackable, pieces=pieces)
				Group('cam').send({'text': '{"id" :"' + id + '",\
											"take_picture": True}'})
				return JsonResponse({'created': True})
		except:
			e = sys.exc_info()
			print(e)
			return JsonResponse({'created': False})

@csrf_exempt
def picture(req):
	if req.method == 'POST':
		mockArgs = {
			"id": 1401,
			"image": path+ "/resource/img/2.png",
		}
		print(req)
		print('Reqest: ', req.FILES, req.POST)
		if ( not req.FILES.get('image') or  not req.POST.get('id')):
			return HttpResponse(content="Bad request. Please include image and id", status=400)
		image = req.FILES['image']
		print(type(image))
		id = parse(req.POST['id'])
		cargo = Cargo.objects.filter(id=id)
		#cargo['image'].save(image.name, image)
		cargo = list(cargo.values())[0]
		print(cargo)
		imgpath = saveImage(id, image)
		
		height = json.loads(cargo['dims'])[0]
		#TODO: change to real calculateDims
		res = calculateDims(imgpath, height)
		#TODO: update entry in database with calculated dimensions
		print("Response: ", res)
		Group('staff').send({'text': json.dumps({'status': 'done'})}, immediately=True)
		return JsonResponse(res)
	else: 
		return JsonResponse({})

def calculateDims2(picture):
	return {"crop" : [[0,1],[1,1],[1,0],[0,0]],
			"width": 1,
			"height": 1}
		
		