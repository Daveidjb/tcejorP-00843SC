from django.urls import path
from . import views

urlpatterns = [
    path('',                      views.reading_list,   name='reading_list'),
    path('add/',                  views.reading_create, name='reading_create'),
    path('edit/<int:pk>/',        views.reading_edit,   name='reading_edit'),
    path('delete/<int:pk>/',      views.reading_delete, name='reading_delete'),
    path('report/',               views.report,         name='report'),
    path('books/',                views.book_list,      name='book_list'),
    path('books/add/',            views.book_create,    name='book_create'),
    path('books/edit/<int:pk>/',  views.book_edit,      name='book_edit'),
    path('books/delete/<int:pk>/',views.book_delete,    name='book_delete'),
    path('authors/add/',          views.author_create,  name='author_create'),
    path('members/',              views.member_list,    name='member_list'),
    path('members/add/',              views.member_create,  name='member_create'),
    path('members/edit/<int:pk>/',    views.member_edit,    name='member_edit'),
    path('members/delete/<int:pk>/',  views.member_delete,  name='member_delete'),   
]