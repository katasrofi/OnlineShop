from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

# Custom login with token email 
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField() 

    def validate(self):
        email = attrs.get("email")
        password = attrs.get("password")
        
        # Authenticate the user 
        user = authenticate(email=email, password=password)

        # Identified user or not 
        if not user:
            raise serializers.ValidationError("Invalid Credentials")

        attrs["user"] = user 
        return super().validate(attrs)
