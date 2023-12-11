from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import   RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer, UserRetrieveSerializer
from rest_framework import permissions, generics, status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .models import UserProfile
from django.http import Http404

# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (permissions.AllowAny, )
#     serializer_class = MyTokenObtainPairSerializer

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserRetrieveSerializer
    lookup_field = 'pk'
    def get_object(self):
        
        user_id = self.kwargs['pk']

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise Http404("UserProfile not found.")
        
        return user_profile.user
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UpdateUserSerializer

class LogoutView(APIView):
    permission_classes= (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAllView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)