from django.urls import path
from exerhealth.forum import views

app_name = 'forum'

urlpatterns = [
    path('category/<int:category_id>/<int:page_number>/', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/<int:page_number>/', views.thread_detail, name='thread_detail'),
    path('new_thread/<int:category_id>/', views.new_thread, name='new_thread'),
    path('reply_thread/<int:thread_id>/', views.reply_thread, name='reply_thread'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # path('search/', views.search, name='search'),
]
