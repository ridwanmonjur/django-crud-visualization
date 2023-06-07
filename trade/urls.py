from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:index_delete>", views.delete, name="delete"),
    path("add", views.add),
    path("update/<int:index_update>", views.update),
    path("do-update/<int:index_update>", views.do_update),
]
