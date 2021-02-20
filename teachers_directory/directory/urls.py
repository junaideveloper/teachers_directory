from django.urls import path

from .views import (
    DirectoryHomeView,
    BulkUploadView,
    TeacherProfileView
)
urlpatterns = [
	path('', DirectoryHomeView.as_view(), name='home'),
    path('upload/', BulkUploadView.as_view(), name="upload"),
    path('teacher/<int:pk>/',TeacherProfileView.as_view(), name='details')
]