from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .models import Occurrence
from .serializers import OccurrenceSerializer, OccurrenceSerializerPost, OccurrenceSerializerPut
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
# Create your views here.

class OccurenceList(generics.ListAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['author', 'category_of_occur', 'location']

class OccurenceOrder(generics.ListAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['author', 'category_of_occur', 'location']
    ordering = ['author']

class GenericDetailAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
	mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

	serializer_class = OccurrenceSerializerPut
	queryset = Occurrence.objects.all()
	lookup_field = 'id'
	authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)	
		else:
			return self.list(request)

	def put(self, request, id=id):
		if request.user.is_staff:
			return self.update(request, id)
		return HttpResponseForbidden({'response: "You dont have permission to edit it"'})

	def delete(self, request, id=id):
		if request.user.is_staff:
			return self.destroy(request, id)
		return HttpResponseForbidden({'response: "You dont have permission to delete it"'})

class GenericPOSTAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
	mixins.RetrieveModelMixin):
	
	serializer_class = OccurrenceSerializerPost
	queryset = Occurrence.objects.all()
	lookup_field = 'id'
	authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
	permission_classes = [IsAuthenticated]
	
	def post(self, request, id=None):
		return self.create(request)

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)
		else:
			return self.list(request)
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)
 