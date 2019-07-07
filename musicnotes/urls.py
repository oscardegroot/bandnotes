from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'musicnotes'

urlpatterns = [
    # musicnotes/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^song/detail/(?P<pk>[0-9]+)/$', views.SongDetailView.as_view(), name='song-detail'),

    url(r'^song/add/1$', views.addSongStep1, name='add-song-1'),
    url(r'^song/add/2$', views.addSongStep2, name='add-song-2'),
    url(r'^song/add/3$', views.addSongStep3, name='add-song-3'),
    url(r'^song/finish/$', views.finishSong, name='finish-song'),

    url(r'^songpart/add/(?P<type_nr>[0-9]+)/', views.addSongPart, name='add-song-part'),
    url(r'^songpart/add_existing/(?P<pk>[0-9]+)/', views.addExistingSongPart, name='add-existing-song-part'),
    url(r'^songpart/remove/(?P<pk>[0-9]+)/', views.removeSongPart, name='remove-song-part'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login')
]

    # picnic/list/order/#
    # url(r'^list/order/(?P<pk>[0-9]+)/$', views.OverviewOrderView.as_view(), name='list-order'),
