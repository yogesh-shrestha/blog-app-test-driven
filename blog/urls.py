from django.urls import path, include
from django.views.generic import TemplateView
from . import views


app_name = 'blog'

urlpatterns = [
     path('', views.ListPostView.as_view(), 
          name='index_page'),
     path('profile/', views.show_profile, 
          name='show_profile_page'),
     path('edit-profile/<int:pk>/', views.EditProfileView.as_view(), 
          name='edit_profile_page'),
     path('add-post/', views.AddPostView.as_view(),
          name='add_post_page'),
     path('post-detail/<int:pk>/', views.PostDetailView.as_view(),
          name='post_detail_page'),
     path('category-posts/<int:pk>', views.ListCategoryPostView.as_view(),
          name='category_post_page'),
     path('tag-posts/<int:pk>', views.ListTagPostView.as_view(),
          name='tag_post_page'),
     path('update-post/<int:pk>', views.PostUpdateView.as_view(),
          name='post_update_page'),
     path('contact/', views.ContactView.as_view(),
          name='contact_page'),
     path('thanks/', TemplateView.as_view(template_name='./blog/thank.html'), 
          name='thanks_page'),
     path('thanks-post/', TemplateView.as_view(template_name='./blog/thank_post.html'), 
          name='thanks_post_page'),
]