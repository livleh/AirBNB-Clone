from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

# from .models import SignUp

# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SignUp
#         fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required = True)
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    #id = serializers.AutoField(primary_key=True)
    # password2 = serializers.CharField(write_only = True, required = True)
    #phone_number = serializers.IntegerField()

    class Meta: 
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
#                  'phone_number',
                  'email',
                  'password')

    def validate(self, args):
        email = args.get('email', None)
        #phone_number = args.get('phone_number', None)
        username = args.get('usermame', None)
        # password = args.get('password', None)
        # password2 = args.get('password2', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('username already exists')})
        # if password != password2:
        #     raise serializers.ValidationError({'password': ('passwords do not match')})
        
        return super().validate(args)
    
    def create(self, validated_data):
        # user = User.objects.create(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     first_name=validated_data['first_name'],
        #     last_name=validated_data['last_name']
        # )

        # user.set_password(validated_data['password'])
        # user.save()

        # return user


        return User.objects.create_user(**validated_data)


    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True, validators=[validate_password])
    password1 = serializers.CharField(write_only = True, required = True)
    old_password = serializers.CharField(write_only = True, required = True)
    
    class Meta: 
        model = User
        fields = ('password',
                  'password1',
                  'old_password',
                  )

    def validate(self, args):
        print("hello fayyad")
        print(args)
        password = args.get('password', None)
        password1 = args.get('password1', None)

        if password != password1:
            print("hello reached")
            raise serializers.ValidationError({'password': ('passwords do not match')})
        


        return super().validate(args)

    # def validate_old_password(self, value):
    #     print(self.data)
    #     print ("nsjndasjda")
    #     user = self.user  
    #     print (user.username)
    #     if not user.check_password(value):
    #         raise serializers.ValidationError({"old_password": "Old password is not correct"})
    #     return value

    # def update(self, current, validated_data):
    #     print("fayyad is hungry")
    #     user = self.context['request'].user
    #     #confirm that you are the user 
    #     if user.pk != current.pk:
    #         raise serializers.ValidationError({"Error": "You do not have permissions to change selected user's info"})

    #     current.set_password(validated_data['password'])
    #     current.save()

    #     return current
    
class UpdateProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    class Meta: 
        model = User
        fields = ('email',
                  'first_name',
                  'last_name'
                  )
        
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "email is already being used by a user."})
        return value

    def update(self, current, validated_data):
        user = self.context['request'].user
        if user.pk != current.pk:
            raise serializers.ValidationError({"Error": "You do not have permissions to change selected user's info"})

        current.first_name = validated_data['first_name']
        current.last_name = validated_data['last_name']
        current.email = validated_data['email']

        current.save()
        return current
