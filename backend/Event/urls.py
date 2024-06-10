from django.conf.urls import include
from django.middleware import csrf
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
from app.views import EventListView, EventDetailView, EventView, UserRegister, UserLogin, UserViewSet, UserLogout, UserView, home_view, admin_dashboard, edit_user, delete_user, user_detail, edit_event, delete_event, create_event, JoinEventView, LeaveEventView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('start/', home_view, name='home'),
    
    #wydarzenia 
    path('create_event/', create_event, name='create_event'),
    path('edit_event/<int:event_id>/', edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    
    path('events/', EventListView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/join/', JoinEventView.as_view(), name='join_event'),
    path('events/<int:pk>/leave/', LeaveEventView.as_view(), name='leave_event'),
    
    #logowanie/rejestracja
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    
    #uzytkownicy 
    path('users/<int:pk>/', UserView.as_view(), name='user_detail'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('user_detail/<int:user_id>/', user_detail, name='user_detail'),
    
    #panel admina 
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]
