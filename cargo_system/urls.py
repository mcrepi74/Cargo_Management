from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('users/', include('users.urls')),
    path('shipments/', include('cargo_app.urls')),
    path('adminpanel/', include('useradmin.urls')),
]
