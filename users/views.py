from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, LoginSerializer, UserDataSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import OneTimePassword


class GetUserDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDataSerializer
    queryset = User.objects.all()

    def get(self, request):
        user_data = request.user
        serializer = self.serializer_class(user_data)
        return Response({"data": serializer.data, "status": "success"}, status=status.HTTP_200_OK)


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        # print(user_data)
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])
            # send email function
            return Response({
                'data': user,
                'message': f"hi {user['first_name']} thank for signing up"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get("otp")
        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()

                return Response({
                    'message':  'account verified successfully'
                }, status=status.HTTP_200_OK)
            return Response({'message': 'account already verified'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        except OneTimePassword.DoesNotExist:
            return Response({'message': 'passcode not provided'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestRoute(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'msg': "It works"
            }, status=status.HTTP_200_OK
        )
