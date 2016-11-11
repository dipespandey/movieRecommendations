from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.movie_list, name='movie_list'),
    url(r'^movie_detail/(?P<id>[0-9]+)/$', views.movie_detail, name='movie_detail'),
    url(r'^refined_similarities/$',views.train_user, name='train_user'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^search/$', views.search, name='search'),
    url(r'^categories/(?P<id>[0-9]+)$', views.categories, name='categories'),
    # url(r'^product_detail/(?P<slug>[\w\-]+)$',views.product_detail, name='product_detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^profile/dashboard/$',views.dashboard, name='dashboard'),

]
