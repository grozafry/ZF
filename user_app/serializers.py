from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    otp = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'mobile', 'role', 'otp', 'username')
          

