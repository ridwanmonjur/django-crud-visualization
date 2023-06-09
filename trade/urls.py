from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:index_delete>", views.delete, name="delete"),
    path("add", views.add),
    path("chart", views.get_chart_page),
    path("get_chart", views.get_chart),
    path("seed", views.seed),
    path("update/<int:id_update>", views.update),
    path("do-update/<int:id_update>", views.do_update),
]
