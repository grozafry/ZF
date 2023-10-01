from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError

import uuid

from .models import AdvisorClientMapping, User, ProductLink
from .serializers import AdvisorUserSerializer
from .permisssions import IsAdvisor

from user_app.serializers import UserSerializer
from admin_app.models import Product


class AdvisorRegistration(APIView):
    def post(self, request):
        request.data["role"] = "Advisor"
        serializer = AdvisorUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdvisorLogin(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        
        try:
            user = User.objects.get(mobile=mobile)
            if user.role != "Advisor":
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

class AdvisorClientRegistration(APIView):

    permission_classes=[IsAdvisor, IsAuthenticated]

    def post(self, request):
        request.data["role"] = "User"
        advisor = request.user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            AdvisorClientMapping.objects.create(
                advisor=advisor,
                client=user
            )

            users_added_by_advisor = User.objects.filter(user_client__advisor=advisor)
            user_serializer = UserSerializer(users_added_by_advisor, many=True)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdvisorProductPurchase(APIView):
    
    permission_classes=[IsAdvisor, IsAuthenticated]
    
    def post(self, request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        advisor = request.user
        try:
            product = Product.objects.get(id=product_id)
            user = User.objects.get(id=user_id)
            
            if not AdvisorClientMapping.objects.filter(
                advisor=advisor,
                client=user
            ).exists():
                return Response({'error': 'Advisor can purchase for his/her users only'}, status=status.HTTP_400_BAD_REQUEST)
            
            product_link=str(uuid.uuid4())

            try:
                ProductLink.objects.create(
                    product=product,
                    client=user,
                    advisor=advisor,
                    product_link=product_link
                )
            except IntegrityError:
                return Response({'error': 'This user has already purchased this product'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'product_link': product_link}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
