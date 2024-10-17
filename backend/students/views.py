from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from courses.models import Course
from .forms import CourseEnrollForm

# Student Registration View
def student_registration_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticate(username=user.username, password=form.cleaned_data["password1"])
            login(request, user)
            return JsonResponse({'success': True, 'redirect': reverse_lazy("student_course_list")})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = UserCreationForm()
    
    return JsonResponse({'form': form.errors})  # For GET request, show empty form errors

# Student Enroll Course View
@login_required
def student_enroll_course_view(request):
    if request.method == "POST":
        form = CourseEnrollForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data["course"]
            course.students.add(request.user)
            return JsonResponse({'success': True, 'redirect': reverse_lazy("student_course_detail", args=[course.id])})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CourseEnrollForm()
    
    return JsonResponse({'form': form.errors})  # For GET request, show empty form errors

# Student Course List View
@login_required
def student_course_list_view(request):
    courses = Course.objects.filter(students=request.user).values()  # Use values() for a simple JSON response
    return JsonResponse({'courses': list(courses)})

# Student Course Detail View
@login_required
def student_course_detail_view(request, pk, module_id=None):
    course = get_object_or_404(Course, pk=pk, students=request.user)
    module = course.modules.get(id=module_id) if module_id else course.modules.first()

    response_data = {
        "course": {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            # Add other course fields as needed
        },
        "module": {
            "id": module.id,
            "name": module.name,
            # Add other module fields as needed
        } if module else None,
    }
    
    return JsonResponse(response_data)
