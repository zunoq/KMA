from user.hashers import make_password, validate_password
from django.db import models
import uuid


class User(models.Model):
    ROLE_CHOICES = [
        ("admin", "Quản trị viên"),
        ("staff", "Nhân viên kinh doanh"),
        ("customer", "Khách hàng"),
    ]
    GENDER_CHOICES = [
        ("male", "Nam"),
        ("female", "Nữ"),
    ]
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = "username"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=255)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=255, null=True, blank=True
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    number_of_surveys = models.IntegerField(null=True, blank=True)
    number_of_surveys_question = models.IntegerField(null=True, blank=True)

    @property
    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return validate_password(password, self.password)


class CustomerHandlerRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Đang chờ"),
        ("approved", "Đã duyệt"),
        ("rejected", "Đã từ chối"),
    ]
    METHOD_CHOICES = [
        ("post", "Thêm"),
        ("put", "Sửa"),
        ("delete", "Xóa"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(
        max_length=255, choices=METHOD_CHOICES, null=True, blank=True
    )
    data = models.JSONField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default="pending")
