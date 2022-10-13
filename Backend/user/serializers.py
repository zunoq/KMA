from rest_framework import serializers
from user.hashers import make_password, validate_password
from user.models import User, CustomerHandlerRequest
from user.otp_verify import verify_otp


class CustomerHandlerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHandlerRequest
        fields = (
            "id",
            "method",
            "data",
            "status",
            "owner",
            "customer_id",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "method": {"required": True},
            "data": {"required": True},
            "status": {"read_only": True},
            "owner": {"read_only": True},
            "customer_id": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": True},
            "email": {"required": True},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"required": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": False},
            "date_joined": {"read_only": True},
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
            "description",
            "price",
            "number_of_surveys",
            "number_of_surveys_question",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": True},
            "email": {"required": True},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"required": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": False},
            "date_joined": {"read_only": True},
            "description": {"required": False},
            "price": {"required": False},
            "number_of_surveys": {"required": False},
            "number_of_surveys_question": {"required": False},
        }


class CreateStaffSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "confirm_password",
            "id",
            "username",
            "password",
            "email",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": True},
            "password": {"write_only": True},
            "email": {"required": True},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"required": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": True},
            "date_joined": {"read_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password") and not attrs.get("confirm_password"):
            raise serializers.ValidationError("Please confirm your password")
        elif not attrs.get("password") and attrs.get("confirm_password"):
            raise serializers.ValidationError("Please enter your password")
        elif attrs.get("password") and attrs.get("confirm_password"):
            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError(
                    "Password and confirm password do not match"
                )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return User(**validated_data)


class CreateCustomerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "confirm_password",
            "id",
            "username",
            "password",
            "email",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
            "description",
            "price",
            "number_of_surveys",
            "number_of_surveys_question",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": True},
            "password": {"write_only": True},
            "email": {"required": True},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"required": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": True},
            "date_joined": {"read_only": True},
            "confirm_password": {"write_only": True},
            "description": {"required": False},
            "price": {"required": False},
            "number_of_surveys": {"required": False},
            "number_of_surveys_question": {"required": False},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password") and not attrs.get("confirm_password"):
            raise serializers.ValidationError("Please confirm your password")
        elif not attrs.get("password") and attrs.get("confirm_password"):
            raise serializers.ValidationError("Please enter your password")
        elif attrs.get("password") and attrs.get("confirm_password"):
            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError(
                    "Password and confirm password do not match"
                )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return User(**validated_data)


class UpdateSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
            "email": {"read_only": True},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"read_only": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"read_only": False},
            "date_joined": {"read_only": True},
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = (
            "password",
            "current_password",
            "new_password",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "current_password": {"write_only": True, "required": True},
            "new_password": {"write_only": True, "required": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not "current_password" or not "new_password" in attrs:
            raise serializers.ValidationError(
                "Current password and new password is required"
            )
        if not validate_password(attrs["current_password"], self.instance.password):
            raise serializers.ValidationError("Current password is incorrect")
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data["new_password"])
        validated_data.pop("current_password")
        validated_data.pop("new_password")
        return instance


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(max_length=255)

    def is_valid_otp(self, otp):
        return bool(verify_otp(otp))

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.is_valid_otp(attrs["otp"]):
            raise serializers.ValidationError("Invalid OTP")
        return attrs


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
            "description",
            "price",
            "number_of_surveys",
            "number_of_surveys_question",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": False},
            "email": {"required": False},
            "password": {"write_only": True, "required": False},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"read_only": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": False},
            "date_joined": {"read_only": True},
            "description": {"required": False},
            "price": {"required": False},
            "number_of_surveys": {"required": False},
            "number_of_surveys_question": {"required": False},
        }

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        for field in self.get_fields().keys():
            setattr(
                instance, field, validated_data.get(field, getattr(instance, field))
            )
        return instance


class UpdateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": False},
            "email": {"required": False},
            "password": {"write_only": True, "required": False},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"read_only": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": False},
            "date_joined": {"read_only": True},
        }

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        for field in self.get_fields().keys():
            setattr(
                instance, field, validated_data.get(field, getattr(instance, field))
            )
        return instance


class CreateCustomerRequestSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
            "description",
            "price",
            "number_of_surveys",
            "number_of_surveys_question",
            "confirm_password",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": True},
            "password": {"required": True},
            "confirm_password": {"required": True},
            "email": {"required": True},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"required": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": True},
            "date_joined": {"read_only": True},
            "description": {"required": False},
            "price": {"required": False},
            "number_of_surveys": {"required": False},
            "number_of_surveys_question": {"required": False},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password") and not attrs.get("confirm_password"):
            raise serializers.ValidationError("Please confirm your password")
        elif not attrs.get("password") and attrs.get("confirm_password"):
            raise serializers.ValidationError("Please enter your password")
        elif attrs.get("password") and attrs.get("confirm_password"):
            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError(
                    "Password and confirm password do not match"
                )
        return attrs
    

class UpdateCustomerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "address",
            "full_name",
            "role",
            "gender",
            "phone_number",
            "is_active",
            "date_joined",
            "description",
            "price",
            "number_of_surveys",
            "number_of_surveys_question",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"required": False},
            "email": {"required": False},
            "password": {"required": False},
            "address": {"required": False},
            "full_name": {"required": False},
            "role": {"read_only": True},
            "gender": {"required": False},
            "phone_number": {"required": False},
            "is_active": {"required": False},
            "date_joined": {"read_only": True},
            "description": {"required": False},
            "price": {"required": False},
            "number_of_surveys": {"required": False},
            "number_of_surveys_question": {"required": False},
        }
