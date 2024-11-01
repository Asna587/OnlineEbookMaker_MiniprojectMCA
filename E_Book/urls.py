from E_Book import views
from django.urls import path

urlpatterns = [
    path('',views.home),
    path('login',views.login),
    path('logout',views.logout),
    path('login_post',views.login_post),
    path('admin_home',views.admin_home),
    path('admin_view_users',views.admin_view_users),
    path('block_user/<id>',views.block_user),
    path('unblock_user/<id>',views.unblock_user),
    path('admin_view_published_books',views.admin_view_published_books),
    path('admin_view_feedback',views.admin_view_feedback),
    path('admin_manage_complaints',views.admin_manage_complaints),
    path('add_reply',views.add_reply,name='add_reply'),




    path('user_registration',views.user_registration),
    path('user_home',views.user_home),
    path('manage_book',views.manage_book),
    path('add_new_book',views.add_new_book),
    path('edit_book/<id>',views.edit_book),
    path('delete_book/<id>',views.delete_book),


    path('view_published_books',views.view_published_books),
    path('submit_feedback',views.submit_feedback),
    path('book_edit_request/<id>',views.book_edit_request),
    path('view_edit_request',views.view_edit_request),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('edit_requested_book/<int:book_id>/', views.edit_requested_book, name='edit_requested_book'),
    path('view_accepted_requests', views.view_accepted_requests, name='view_accepted_requests'),


    path('manage_profile', views.manage_profile, name='manage_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('manage_complaint', views.manage_complaint, name='manage_complaint'),
    path('add_new_complaint', views.add_new_complaint, name='add_new_complaint'),


]
