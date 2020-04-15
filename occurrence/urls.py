from django.urls import path, include
from .views import OccurenceList, GenericPOSTAPIView, GenericDetailAPIView, OccurenceOrder 

urlpatterns = [
	path('/', OccurenceList.as_view()),
    path('create/', GenericPOSTAPIView.as_view()),
	path('detail/<int:id>', GenericDetailAPIView.as_view()),
    path('order/', OccurenceOrder.as_view())
]