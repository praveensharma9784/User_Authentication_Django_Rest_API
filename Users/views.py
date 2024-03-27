from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer 
from django.contrib.auth import authenticate
from Users.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#generate token manaully
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView (APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, fromat=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user =serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token' : token, 'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, fromat=None):
        serialzer = UserLoginSerializer(data = request.data)
        if serialzer.is_valid(raise_exception=True):
            email= serialzer.data.get('email')
            password = serialzer.data.get('password')
            user = authenticate ( email=email , password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token' : token , 'msg':'Login Success'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'non_field_errors': ['Email or Password is not vaild']}},status=status.HTTP_404_NOT_FOUND)
        return Response (serialzer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    renderer_classes= [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
        renderer_classes= [UserRenderer]
        permission_classes=[IsAuthenticated]
        def post (self, request, format=None):
             serializer = UserChangePasswordSerializer(data = request.data, context= {'user': request.user})
             if serializer.is_valid(raise_exception=True):
                  return Response({'msg':'Password change Successfully'},status=status.HTTP_200_OK)
             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
class SehdPasswordResetEmailView(APIView):
     renderer_classes = [UserRenderer]
     def post(self, request, format=None) :
          serializer = SendPasswordResetEmailSerializer(data=request.data)

          if serializer.is_valid(raise_exception=True):
               return Response({'msg': 'Password Reset link sendPleasecheck your Email'}, status=status.HTTP_200_OK)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
