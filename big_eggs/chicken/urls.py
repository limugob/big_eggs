from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path("eggs_list/", lambda request: redirect("eggs_list", "10"), name="eggs_list"),
    path("eggs_list/<int:minus_days>/", views.eggs_list, name="eggs_list"),
    path(
        "eggs_list/<int:minus_days>/stats.png",
        views.eggs_list,
        {"stats": True},
        name="eggs_list_stats",
    ),
    path(
        "eggs_delete/<uuid:id>/",
        views.eggs_delete,
        name="eggs_delete",
    ),
    path(
        "eggs_delete/<int:year>/<int:month>/<int:day>/",
        views.eggs_delete,
        name="eggs_delete",
    ),
    path("chicken_list/", views.ChickenList.as_view(), name="chicken_list"),
    path("chicken/add/", views.ChickenCreate.as_view(), name="chicken_add"),
    path(
        "chicken/update/<uuid:pk>/",
        views.ChickenUpdate.as_view(),
        name="chicken_update",
    ),
    path(
        "chicken/delete/<uuid:pk>/",
        views.ChickenDelete.as_view(),
        name="chicken_delete",
    ),
    path(
        "chickengroup_list/", views.ChickenGroupList.as_view(), name="chickengroup_list"
    ),
    path(
        "chickengroup/add/", views.ChickenGroupCreate.as_view(), name="chickengroup_add"
    ),
    path(
        "chickengroup/update/<uuid:pk>/",
        views.ChickenGroupUpdate.as_view(),
        name="chickengroup_update",
    ),
    path(
        "chickengroup/delete/<uuid:pk>/",
        views.ChickenGroupDelete.as_view(),
        name="chickengroup_delete",
    ),
]
