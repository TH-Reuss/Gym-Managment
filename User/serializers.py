from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ()

    def create(self, validated_data):
        user = Users(
            email               = validated_data['email'],
            username            = validated_data['username'],
            gym                 = validated_data['gym'],
            is_superuser        = validated_data['is_superuser'],
            rut                 = validated_data['rut'],
            first_name          = validated_data['first_name'],
            last_name           = validated_data['last_name'],
            is_staff            = validated_data['is_staff'],
            is_active           = validated_data['is_active'],
            last_login          = validated_data['last_login'],
            userType            = validated_data['userType'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user