from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path("eggs_list/", views.eggs_list, name="eggs_list"),
    path("eggs_list/<int:minus_days>/", views.eggs_list, name="eggs_list"),
    path("eggs_delete/<int:year>/<int:month>/<int:day>/", views.eggs_delete),
    path(
        "eggs_delete/<int:year>/<int:month>/<int:day>/<str:group>/<str:error>/",
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
