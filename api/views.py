from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#generate token menually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):
    def post(self, request, format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user=serializer.save()
                token=get_tokens_for_user(user)
            
                return Response({'token':token,'msg': 'registration success'},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserLogin(APIView):
    def post(self,request,format = None):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email=serializer.data.get('email')
                password=serializer.data.get('password')
                user = authenticate(email=email,password=password)

                if  user is not None:
                    token=get_tokens_for_user(user)
                    return Response({'token':token,'msg':'login succsess'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
                

        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user = request.user  
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            serializer =ChangePasswordSerializer(data=request.data,context = {'user':request.user})
            if serializer.is_valid(raise_exception=True):
                return Response({'msg':'password change successfully '})
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
