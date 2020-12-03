from django.urls import path
from . import views

urlpatterns = [
	path('<str:name>/<str:slug>', views.show,name="show"),
    path('<str:name>/<str:slug>/create_comment', views.create_comment,name="create_comment"),
    path('<str:forum>/post/create',views.create_post,name="create"),
    path('<str:slug>/post/lock',views.lock,name="lock"),
    path('<str:slug>/post/move',views.move,name="move"),
]