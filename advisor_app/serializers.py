from rest_framework import serializers
from user_app.models import User

class AdvisorUserSerializer(serializers.ModelSerializer):
    
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'mobile', 'role', 'otp')
        
    
