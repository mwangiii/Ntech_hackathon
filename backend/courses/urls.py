from django.urls import path
from . import views

urlpatterns = [
    path("mine/", views.manage_course_list_view, name="manage_course_list"),
    path("create/", views.course_create_view, name="course_create"),
    path("<pk>/edit/", views.course_update_view, name="course_edit"),
    path("<pk>/delete/", views.course_delete_view, name="course_delete"),
    path("<pk>/module/", views.course_module_update_view, name="course_module_update"),
    path(
        "module/<int:module_id>/content/<model_name>/create/",
        views.content_create_update_view,
        name="module_content_create",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/<id>/",
        views.content_create_update_view,
        name="module_content_update",
    ),
    path(
        "content/<int:id>/delete/",
        views.content_delete_view,
        name="module_content_delete",
    ),
    path(
        "module/<int:module_id>/",
        views.module_content_list_view,
        name="module_content_list",
    ),
    path("module/order/", views.module_order_view, name="module_order"),
    path("content/order/", views.content_order_view, name="content_order"),
    path(
        "subject/<slug:subject>/",
        views.course_list_view,
        name="course_list_subject",
    ),
    path("<slug:slug>/", views.course_detail_view, name="course_detail"),
]
