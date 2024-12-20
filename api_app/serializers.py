from rest_framework import serializers
from user_app.models import *
from django.core.exceptions import ValidationError
import re
from datetime import datetime

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'address', 'phone_number', 'd_o_b', 'gender', 'image']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate_image(self, value):
        if value:
            valid_image_formats = ['image/png', 'image/jpeg', 'image/jpg']
            if value.content_type not in valid_image_formats:
                raise ValidationError("Only PNG, JPG, and JPEG image formats are allowed.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character.")
        
        return value
    
    def validate_d_o_b(self, value):
        if value:
            try:
                parsed_date = datetime.strptime(str(value), '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Date of Birth must be in the format yyyy/mm/dd.")
        return value
    
    def validate_phone_number(self, value):
        if not value.isdigit():
            raise ValidationError("Phone number must only contain digits.")
        if len(value) != 10:
            raise ValidationError("Phone number must be exactly 10 digits long.")
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
            d_o_b=validated_data.get('d_o_b'),
            gender=validated_data['gender'],
            image=validated_data.get('image')
        )
        return user