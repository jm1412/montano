# urls.py
from django.contrib import admin
from django.urls import path, include
from montano import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Homepage and static pages
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('login/<str:from_app>', views.login_view, name='login_with_redirect'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register'),
    path('register/<str:from_app>', views.register_view, name='register_with_redirect'),
    path('admin/', admin.site.urls),
    
    # Application-specific URLs
    path('apps/', views.apps_index, name='apps_index'),
    path('calendar/', include('app_calendar.urls')),
    path('todo/', include('todolist.urls')),
    path('blog/', include('blog.urls')),
    path('skc/', include('skc.urls')),
    path('ipon_goodbot/', include('ipon_goodbot.urls')),
    path('sudoku/', include('sudoku.urls')),
    
    # Authentication and API URLs
    path('accounts/', include('accounts.urls')),  # Ensure 'accounts.urls' has the appropriate endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
