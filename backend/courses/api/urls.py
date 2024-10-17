from django.urls import path, include
from .views import (
    subject_list_view,
    subject_detail_view,
    course_list_view,
    course_detail_view,
    enroll_in_course_view,
    course_contents_view,
)

app_name = "courses"

urlpatterns = [
    path("subjects/", subject_list_view, name="subject_list"),
    path("subjects/<pk>/", subject_detail_view, name="subject_detail"),
    path("courses/", course_list_view, name="course_list"),
    path("courses/<pk>/", course_detail_view, name="course_detail"),
    path("courses/<pk>/enroll/", enroll_in_course_view, name="course_enroll"),
    path("courses/<pk>/contents/", course_contents_view, name="course_contents"),
]
