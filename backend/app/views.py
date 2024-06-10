from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from app.forms import UserEditForm
from .models import Event
from .serializer import EventRegistrationSerializer, UserRegisterSerializer, UserLoginSerializer, UserSerializer, EventSerializer
from .validations import custom_validation, validate_email, validate_password
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseServerError
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import viewsets
from django.contrib.auth.models import User
from .forms import EventForm
from .models import Event, Event_Registration
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin




#rejestracja uzytkownikow
User = get_user_model()

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data.copy()
            validated_data.pop('csrfmiddlewaretoken', None)
            user = User.objects.create_user(**validated_data)
            return redirect('/login')
        else:
            return render(request, 'register.html', {'error': 'Registration failed'})
        

#logowanie uzytkownikow
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            if user.is_superuser:
                return redirect('/start')
            else:
                return redirect('/start')  
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})



#wylogowywanie uzytkowwnikow
class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        logout(request)
        return redirect('home')

    def post(self, request):
        logout(request)
        return redirect('home')


#uzytkownicy
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(get_user_model(), pk=pk)
            serializer = UserSerializer(user)
        else:
            users = get_user_model().objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#strona startowa
def home_view(request):
    return render(request, 'home.html')



#panel administratora
def admin_check(user):
    return user.is_superuser

@login_required
@csrf_exempt
def admin_dashboard(request):
    User = get_user_model()
    users = User.objects.all()
    events = Event.objects.all()
    
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            return redirect('admin_dashboard')
    else:
        event_form = EventForm()
    
    return render(request, 'admin_dashboard.html', {'users': users, 'events': events, 'event_form': event_form})



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#edycja uzytkownika
@login_required
@csrf_exempt
def edit_user(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_detail', user_id=user_id)
    else:
        user_form = UserEditForm(instance=user)

    return render(request, 'edit_user.html', {'user_form': user_form, 'user_id': user_id})

#usuwanie uzytkownika
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('admin_dashboard')

#detale uzytkownika
@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    events_joined = Event_Registration.objects.filter(user_ID=user)
    return render(request, 'user_detail.html', {'user': user, 'events_joined': events_joined})




#edycja wydarzenia
@login_required
@csrf_exempt
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('admin_dashboard')
    else:
        event_form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'event_form': event_form, 'event_id': event_id})

#usuwanie wydarzenia
@login_required
@csrf_exempt
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('admin_dashboard')

#tworzenie wydarzenia
@login_required
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            return redirect('admin_dashboard')
    else:
        event_form = EventForm()
    return render(request, 'create_event.html', {'event_form': event_form})


class JoinEventView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not Event_Registration.objects.filter(event_ID=event, user_ID=request.user).exists():
            Event_Registration.objects.create(event_ID=event, user_ID=request.user)
            messages.success(request, f'You have been signed up for the event: {event.title}')
        return redirect('events')

class LeaveEventView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        registration = get_object_or_404(Event_Registration, event_ID=event, user_ID=request.user)
        registration.delete()
        messages.success(request, f'You have been written out of the event: {event.title}')
        return redirect('events')


#wydarzenia
class EventView(APIView):
    def get(self, request, event_id=None):
        if event_id:
            event = Event.objects.get(pk=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

#lista wydarzen
class EventListView(View):
    def get(self, request):
        events = Event.objects.all()
        if request.user.is_authenticated:
            user_registrations = Event_Registration.objects.filter(user_ID=request.user)
            user_registered_events = {registration.event_ID for registration in user_registrations}
        else:
            user_registered_events = set()
        
        context = {
            'events': events,
            'user_registered_events': user_registered_events,
        }
        return render(request, 'events.html', context)
    

#detale wydarzen
class EventDetailView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        is_registered = False
        if request.user.is_authenticated:
            is_registered = Event_Registration.objects.filter(event_ID=event, user_ID=request.user).exists()
        
        context = {
            'event': event,
            'is_registered': is_registered,
        }
        return render(request, 'event_detail.html', context)