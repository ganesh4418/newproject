from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from axes.models import AccessAttempt
from axes.attempts import get_cool_off_threshold
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import CustomUser, RequestDemo, Contact, HelpandSupport, UserProfile


User = get_user_model()

class TwoFactorJwtTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if the user has two-factor authentication enabled
        user = self.user
        # if not user.two_factor_enabled:
        #     return data  # Return data as-is if 2FA is not enabled for this user

        # Generate a new access token without the refresh token claim
        refresh = self.get_token(user)
        data['access'] = str(refresh.access_token)

        # Generate a one-time password (OTP) for two-factor authentication
        otp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if otp_device:
            otp = otp_device.generate_otp()
            data['otp'] = otp

        return data

class CustomTokenObtainPairSerializer(TwoFactorJwtTokenObtainPairSerializer):
    default_error_messages = {"no_active_account": ("Login failed. Please check your username or email and password. Note that the password is case-sensitive.")}
    """
    This serves various purposes:
    1. It extends the default TokenObtainPairSerializer2FA to handle 2FA
    2. It adds to add the user's details to the response, saving an additional request after login.
    """

    def check_login_attempt(self, validate_data):
        login_failures_count = (
            AccessAttempt.objects.filter(username=validate_data.get("username"),  attempt_time__gte=get_cool_off_threshold())
            .order_by("username")
            .values("username")
            .annotate(login_failures_count=Sum("failures_since_start"))
            .values("login_failures_count")
        )
        if len(login_failures_count)==0:
            login_failures_count = 0
        else:
            login_failures_count = login_failures_count[0]['login_failures_count']
        if login_failures_count == 1:
            self.error_messages['no_active_account']= (
                "1 failed login attempt: Your account will be locked out for 15 minutes after 1 more failure."
            )
        elif login_failures_count >= 2:
            self.error_messages['no_active_account']= (
                "Your account is locked due to repeated login failures."
            )

    def validate(self, attrs):
        self.check_login_attempt(attrs)
        data = super().validate(attrs)

        # Add user details to response
        data["user"] = UserSerializer(self.user).data

        return data

class BaseUserSerializer( serializers.ModelSerializer):
    """Base serializer for User model"""

    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = CustomUser
        depth = 1
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "user_permissions",
        )
        read_only_fields = (
            "id",
            "updated_by",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "created",
            "modified",
            "user_permissions",
            "intercom_id",
            "parent",
        )

    def validate_email(self, value):
        user_query = User.objects.filter(email=value)
        if hasattr(self, "instance") and self.instance and self.instance.pk:
            user_query = user_query.exclude(pk=self.instance.pk)
        if user_query.exists():
            raise serializers.ValidationError("Email already exists")

        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get("password", None)
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()

        return user

class UserSignupSerializer(BaseUserSerializer):

    class Meta:
        model = CustomUser
        fields = [field.name for field in model._meta.fields]  # "__all__"


    def create(self, validated_data):
        # with transaction.atomic():
        # Create user
        user = super().create(validated_data)
        return user



class UserSerializer(BaseUserSerializer):
    """
    General user serializer
    """

    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Group.objects.all(),
        allow_empty=False,
        required=False,
    )

    class Meta:
        model = BaseUserSerializer.Meta.model
        depth = BaseUserSerializer.Meta.depth
        fields = BaseUserSerializer.Meta.fields + ("groups",)
        read_only_fields = BaseUserSerializer.Meta.read_only_fields

    def validate(self, data):
        # We must have a user
        try:
            user = self.context["request"].user
            if not user or not user.is_authenticated:
                raise serializers.ValidationError("User must be authenticated to update a user.")
        except KeyError:
            raise serializers.ValidationError("User must be authenticated to update a user.")

        return super().validate(data)


class RequestDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDemo
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class HelpandSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpandSupport
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_photo']