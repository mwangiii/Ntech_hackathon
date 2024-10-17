from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer, CourseSerializer
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer


@api_view(["GET"])
def subject_list_view(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def subject_detail_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    serializer = SubjectSerializer(subject)
    return Response(serializer.data)


@api_view(["POST"])
def course_enroll_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.students.add(request.user)
    return Response({"enrolled": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def course_list_view(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(["POST"])
def enroll_in_course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.students.add(request.user)
    return Response({"enrolled": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def course_contents_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    serializer = CourseWithContentsSerializer(course)
    return Response(serializer.data)
