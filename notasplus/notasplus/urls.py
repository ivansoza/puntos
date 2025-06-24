from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- LOGIN en la ruta raíz ---
    path(
        '',
        auth_views.LoginView.as_view(
            template_name='generales/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),

    # Logout: usará LOGOUT_REDIRECT_URL
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),

    # Tu app de home /dashboard protegido
    path('home/', include('generales.urls')),
]
