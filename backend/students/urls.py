from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    path(
        "register/",
        views.student_registration_view,
        name="student_registration",
    ),
    path(
        "enroll-course/",
        views.student_enroll_course_view,
        name="student_enroll_course",
    ),
    path("courses/", views.student_course_list_view, name="student_course_list"),
    path(
        "course/<pk>/",
        cache_page(60 * 15)(views.student_course_detail_view),
        name="student_course_detail",
    ),
    path(
        "course/<pk>/<module_id>/",
        cache_page(60 * 15)(views.student_course_detail_view),
        name="student_course_detail_module",
    ),
]
