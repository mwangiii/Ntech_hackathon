from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.db.models import Count
from django.forms.models import modelform_factory
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from django.views.generic.base import TemplateResponseMixin
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .forms import ModuleFormSet
from .models import Course, Module, Content, Subject
from students.forms import CourseEnrollForm


def get_owner_queryset(queryset, user):
    return queryset.filter(owner=user)


@login_required
@permission_required("courses.view_course")
def manage_course_list_view(request):
    courses = get_owner_queryset(Course.objects.all(), request.user)
    return JsonResponse({"courses": list(courses.values())})


@login_required
@permission_required("courses.add_course")
def course_create_view(request):
    if request.method == "POST":
        formset = ModuleFormSet(data=request.POST)
        if formset.is_valid():
            course = Course(owner=request.user)
            course.save()
            modules = formset.save(commit=False)
            for module in modules:
                module.course = course
                module.save()
            return JsonResponse({"success": True, "redirect": "manage_course_list"})
        return JsonResponse({"success": False, "errors": formset.errors}, status=400)
    else:
        formset = ModuleFormSet()
    return JsonResponse({"formset": formset.errors})


@login_required
@permission_required("courses.change_course")
def course_update_view(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    if request.method == "POST":
        formset = ModuleFormSet(instance=course, data=request.POST)
        if formset.is_valid():
            formset.save()
            return JsonResponse({"success": True, "redirect": "manage_course_list"})
        return JsonResponse({"success": False, "errors": formset.errors}, status=400)
    else:
        formset = ModuleFormSet(instance=course)
    return JsonResponse({"formset": formset.errors})


@login_required
@permission_required("courses.delete_course")
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    course.delete()
    return JsonResponse({"success": True, "redirect": "manage_course_list"})


@login_required
def course_module_update_view(request, pk):
    course = get_object_or_404(Course, id=pk, owner=request.user)
    if request.method == "POST":
        formset = ModuleFormSet(instance=course, data=request.POST)
        if formset.is_valid():
            formset.save()
            return JsonResponse({"success": True, "redirect": "manage_course_list"})
        return JsonResponse({"success": False, "errors": formset.errors}, status=400)
    formset = ModuleFormSet(instance=course)
    return JsonResponse({"formset": formset.errors})


@login_required
def content_create_update_view(request, module_id, model_name, id=None):
    module = get_object_or_404(Module, id=module_id, course__owner=request.user)
    model = apps.get_model(app_label="courses", model_name=model_name)
    obj = get_object_or_404(model, id=id, owner=request.user) if id else None

    if request.method == "POST":
        form = modelform_factory(
            model, exclude=["owner", "order", "created", "updated"]
        )(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=module, item=obj)
            return JsonResponse(
                {
                    "success": True,
                    "redirect": "module_content_list",
                    "module_id": module.id,
                }
            )
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    form = modelform_factory(model, exclude=["owner", "order", "created", "updated"])(
        instance=obj
    )
    return JsonResponse({"form": form.errors})


@login_required
def content_delete_view(request, id):
    content = get_object_or_404(Content, id=id, module__course__owner=request.user)
    module = content.module
    content.item.delete()
    content.delete()
    return JsonResponse(
        {"success": True, "redirect": "module_content_list", "module_id": module.id}
    )


@login_required
def module_content_list_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__owner=request.user)
    return JsonResponse({"module": module})


@login_required
def module_order_view(request):
    if request.method == "POST":
        for id, order in request.POST.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return JsonResponse({"saved": "OK"})


@login_required
def content_order_view(request):
    if request.method == "POST":
        for id, order in request.POST.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(
                order=order
            )
        return JsonResponse({"saved": "OK"})


def course_list_view(request):
    all_courses = Course.objects.annotate(total_modules=Count("modules"))
    subject = request.GET.get("subject")
    if subject:
        subject = get_object_or_404(Subject, slug=subject)
        courses = all_courses.filter(subject=subject)
    else:
        courses = all_courses
    subjects = cache.get("all_subjects")
    if not subjects:
        subjects = Subject.objects.annotate(total_courses=Count("courses"))
        cache.set("all_subjects", subjects)
    return JsonResponse(
        {
            "courses": list(courses.values()),
            "subjects": list(subjects.values()),
            "subject": subject,
        }
    )


def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enroll_form = CourseEnrollForm(initial={"course": course})
    return JsonResponse(
        {
            "course": {
                "id": course.id,
                "title": course.title,
                "overview": course.overview,
                # Add other course fields as needed
            },
            "enroll_form": enroll_form.as_p(),  
        }
    )
