from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, Category
from .serializers import ProductSerializer
from .permissions import IsAdmin

from user_app.models import User
from user_app.serializers import UserSerializer

class AdminRegistration(APIView):
    def post(self, request):
        request.data["role"] = "Admin"
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLogin(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        
        try:
            user = User.objects.get(mobile=mobile)
            if user.role != "Admin":
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED) 

        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        def check_user_otp(user, otp):
            #OTP validation logic
            return True

        if check_user_otp(user, otp):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class AdminProductCreation(APIView):

    permission_classes = [IsAdmin]

    def post(self, request):
        product_name = request.data.get('product_name')
        description = request.data.get('description')
        category_name = request.data.get('category')

        category, created = Category.objects.get_or_create(name=category_name)
        product = Product.objects.create(
            name=product_name,
            description=description,
            category=category
        )

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


