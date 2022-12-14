from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User as AuthUser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import *
from .models import *
from rest_framework import generics

from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = AuthUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

for user in AuthUser.objects.all():
    Token.objects.get_or_create(user=user)


# ****** Competition *******


@api_view(['GET'])
def competitions_list(request):
    if request.method == 'GET':
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def competitions_add(request):

    if not request.user.is_superuser:
        return Response({'response': 'You dont have permission to create that.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == 'POST':
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

@api_view(['GET'])
def competitions_detail(request, pk):
    try:
        competition = Competition.objects.get(pk=pk)
    except Competition.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def competitions_update(request, pk):
    try:
        competition = Competition.objects.get(pk=pk)
    except Competition.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_superuser:
        return Response({'response': 'You dont have permission to update that.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == 'PUT':
        serializer = CompetitionSerializer(competition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def competitions_delete(request, pk):
    try:
        competition = Competition.objects.get(pk=pk)
    except Competition.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_superuser:
        return Response({'response': 'You dont have permission to delete that.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == 'DELETE':
        competition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ****** User Details *******

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details_add(request, username):

    if request.user.is_superuser:
        return Response({'response': 'You dont need to create that, cause you are admin, not a skateboarder!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif username != request.user.username:
        return Response({'response': 'You cant add user details of another user!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        queryset = AuthUser.objects.get(username=username)
        user_details = User_detail.objects.get(user=queryset.id)
    except User_detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = User_detail_Serializer(user_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ****** Registration *******

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrations_list_of_all_users(request):

    if not request.user.is_superuser:
        return Response({'response': 'You cant see registrations of all users!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == 'GET':
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrations_list_by_status(request, state):

    if not request.user.is_superuser:
        return Response({'response': 'You cant see registrations of all users!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # if status != 'SEND' or status != 'OK' or status != 'NOT':
    #     return Response({'response': 'There is no status like that!'},
    #                     status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == 'GET':
        registrations = Registration.objects.all().filter(status=state)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrations_add(request, username):

    if request.user.is_superuser:
        return Response({'response': 'You dont need to create that, cause you are admin, not a skateboarder!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif username != request.user.username:
        return Response({'response': 'You cant add registration of another user!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        queryset = AuthUser.objects.get(username=username)
        if Registration.objects.filter(id_competition=request.data['id_competition'], id_user=queryset).exists():
            return Response({'response': 'Your registration for that competition already exists!'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        registration = Registration.objects.create(status="SEND", id_user=queryset)
    except AuthUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrations_list(request, username):

    if username != request.user.username and not request.user.is_superuser:
        return Response({'response': 'You cant view registrations of another user!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        queryset = AuthUser.objects.get(username=username)
        registrations = Registration.objects.all().filter(id_user=queryset.id)
    except AuthUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrations_detail(request, username, pk):

    if username != request.user.username and not request.user.is_superuser:
        return Response({'response': 'You cant view registrations of another user!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        registration = Registration.objects.get(pk=pk)
    except Registration.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrations_change_status(request, pk):

    if not request.user.is_superuser:
        return Response({'response': 'You cant change status of any registration!'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        registration = Registration.objects.get(pk=pk)
    except Registration.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = RegistrationSerializer(registration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)