from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .serializers import PropertySerializer, ImageSerializer
from .models import Property, Image
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt # Need to remove this line when validation is proper
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class PropertyList(ListAPIView):
	serializer_class = PropertySerializer
	pagination_class = PageNumberPagination
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		query_set = Property.objects.all()

		uid = self.request.GET.get('uid')
		if uid:
			query_set = query_set.filter(owner__id=uid)

		city = self.request.GET.get('city')
		if city:
			query_set = query_set.filter(city=city)

		num_guests = self.request.GET.get('num_guests')
		if num_guests:
			query_set = query_set.filter(num_guests__gte=num_guests)

		num_beds = self.request.GET.get('num_beds')
		if num_beds:
			query_set = query_set.filter(num_beds__gte=num_beds)

		num_baths = self.request.GET.get('num_baths')
		if num_baths:
			query_set = query_set.filter(num_baths__gte=num_baths)

		wifi = self.request.GET.get('wifi')
		if wifi:
			query_set = query_set.filter(wifi=wifi)

		free_parking = self.request.GET.get('free_parking')
		if free_parking:
			query_set = query_set.filter(free_parking=free_parking)
		
		sort_by = self.request.GET.get('sort_by')
		ordering = self.request.GET.get('ordering')

		if sort_by:
			if ordering:
				if ordering.lower() == 'desc':
					sort_by = '-' + sort_by
			query_set = query_set.order_by(sort_by)

		return query_set


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def property_detail(request, pid):

	try:
		property_ = Property.objects.get(pid=pid)
	except Property.DoesNotExist:
		return Response({'details': 'Property not found'}, status=404)

	if request.method == 'GET':
		serializer = PropertySerializer(property_)
		return Response(serializer.data)

	elif request.method == 'PATCH':
		if request.user != property_.owner:
			return Response({'details': 'Forbidden from editing this property'}, status=403)
		
		data = request.data
		serializer = PropertySerializer(property_, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=400)

	elif request.method == 'DELETE':
		if request.user != property_.owner:
			return Response({'details': 'Forbidden from deleting this property'}, status=403)
		
		property_.delete()
		return Response({'details': 'Property was deleted'}, status=200)
	return Response({'details': 'Something went wrong with the request'}, status=400)
	

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def property_create(request):
	if request.method == 'POST':
		data = request.POST.dict()

		#data['owner'] = request.user
		
		serializer = PropertySerializer(data=data)
		if serializer.is_valid():
			property_ = serializer.save(owner=request.user)
			images = request.FILES.getlist("images")
			if images:
				num_images = property_.image_counter
				for image in images:
					name = str(property_.pid) + '_' + str(num_images)
					Image.objects.create(name=name, image_property=property_, image=image)
					num_images += 1
				serializer.save(image_counter=num_images)
			return Response(data=serializer.data)
		return Response(serializer.errors, status=400)

	return Response({'details': 'Something went wrong with the request'}, status=400)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def image_add(request, pid):
	if request.method == 'POST':
		try:
			property_ = Property.objects.get(pid=pid)
		except Property.DoesNotExist:
			return Response({'details': 'Property not found'}, status=404)
		
		images = request.FILES.getlist("images")
		if images:
			num_images = property_.image_counter
			for image in images:
				name = str(property_.pid) + '_' + str(num_images)
				Image.objects.create(name=name, image_property=property_, image=image)
				num_images += 1
				property_.image_counter = num_images
				property_.save()
			return Response({'details': 'Images were added'}, status=200)

	return Response({'details': 'Something went wrong with the request'}, status=400)


class PropertyImages(ListAPIView):
	serializer_class = ImageSerializer
	pagination_class = PageNumberPagination
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		pid = self.kwargs['pid']
		query_set = Image.objects.filter(image_property__pid=pid).order_by('id')
		return query_set
	

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def image_delete(request, image_id):
	try:
		image = Image.objects.get(pk=image_id)
	except Image.DoesNotExist:
		return Response({'details': 'Image not found'}, status=404)

	if request.method == 'DELETE':
		if request.user != image.image_property.owner:
			return Response({'details': 'Forbidden from deleting this image'}, status=403)
		
		image.delete()
		return Response({'details': 'Image was deleted'}, status=200)
	return Response({'details': 'Something went wrong with the request'}, status=400)
