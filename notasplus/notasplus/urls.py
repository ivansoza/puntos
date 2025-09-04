from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página principal
    path('', include('generales.urls')),

    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),

    # Vistas de autenticación
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='generales/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
