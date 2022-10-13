from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Q
from util.permissions import AdminPermission, StaffPermission, CustomerPermission
from user.models import User, CustomerHandlerRequest
from user.otp_verify import generate_otp
from user.serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    OTPVerifySerializer,
    ResetPasswordSerializer,
    UpdateSelfSerializer,
    CreateStaffSerializer,
    CreateCustomerSerializer,
    CustomerSerializer,
    UpdateCustomerSerializer,
    UpdateStaffSerializer,
    CustomerHandlerRequestSerializer,
    CreateCustomerRequestSerializer,
    UpdateCustomerRequestSerializer,
)


class UserView(APIView):
    permission_classes = [AdminPermission | StaffPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AdminPermission | StaffPermission]
        else:
            permission_classes = [AdminPermission]
        return [permission() for permission in permission_classes]

    def get(self, request, page=None, size=None, active=None):
        page = request.GET.get("page", None)
        size = request.GET.get("size", None)
        active = request.GET.get("active", None)

        if active and active not in ("true", "false"):
            message = {"message": "Invalid active", "status_code": 400}
            return JsonResponse(message, status=400)

        if self.request.user.role == "staff":
            users = User.objects.filter(role="customer")
        else:
            users = User.objects.filter(Q(role="staff") | Q(role="customer"))
        if active:
            users = users.filter(is_active=str(active).capitalize())

        if page and size:
            paginator = PageNumberPagination()
            paginator.page_size = size
            users = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(users, many=True)
        output = {
            "users": serializer.data,
            "page": int(page if page else 1),
            "size": int(size if size else len(users)),
            "total": len(users),
        }
        return JsonResponse(output, status=200)

    def post(self, request):
        if not request.data.get('role'):
            message = {"message": "Role is required", "status_code": 400}
            return JsonResponse(message, status=400)
        if request.data.get("role") == "admin":
            message = {
                "message": "Don't have permission to create admin",
                "status_code": 400,
            }
            return JsonResponse(message, status=400)

        if request.data.get("role") == "staff":
            serializer = CreateStaffSerializer(data=request.data)
        elif request.data.get("role") == "customer":
            serializer = CreateCustomerSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.save()
            output = UserSerializer(user).data
            return JsonResponse(output, status=200)
        else:
            message = {
                "message": serializer.errors,
                "status_code": 400,
            }
            return JsonResponse(message, status=400)


class UserByIdView(APIView):
    permission_classes = [AdminPermission | StaffPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AdminPermission | StaffPermission]
        else:
            permission_classes = [AdminPermission]
        return [permission() for permission in permission_classes]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=str(user_id).strip())
        except User.DoesNotExist:
            message = {"message": "User does not exist", "status_code": 404}
            return JsonResponse(message, status=404)

        if self.request.user.role == "staff" and (
            user.role == "admin" or user.role == "staff"
        ):
            message = {
                "message": "Don't have permission to view this user",
                "status_code": 403,
            }
            return JsonResponse(message, status=403)

        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, status=200)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=str(user_id).strip())
        except User.DoesNotExist:
            message = {"message": "User does not exist", "status_code": 404}
            return JsonResponse(message, status=404)

        if user.role == "admin":
            message = {
                "message": "Don't have permission to update admin",
                "status_code": 400,
            }
            return JsonResponse(message, status=400)

        elif user.role == "staff":
            serializer = UpdateStaffSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.save()
                return JsonResponse(serializer.data, status=200)
            else:
                message = {"message": serializer.errors, "status_code": 400}
                return JsonResponse(message, status=400)

        elif user.role == "customer":
            serializer = UpdateCustomerSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.save()
                output = CustomerSerializer(user).data
                return JsonResponse(output, status=200)
            else:
                message = {"message": serializer.errors, "status_code": 400}
                return JsonResponse(message, status=400)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=str(user_id).strip())
        except User.DoesNotExist:
            message = {"message": "User does not exist", "status_code": 404}
            return JsonResponse(message, status=404)

        user.delete()
        message = {"message": "User deleted successfully", "status_code": 200}
        return JsonResponse(message, status=204)


class SelfInfoView(APIView):
    permission_classes = [AdminPermission | StaffPermission | CustomerPermission]

    def get(self, request):
        user = self.request.user
        if user.role in ("admin", "staff"):
            serializer = UserSerializer(user, many=False)
        else:
            serializer = CustomerSerializer(user, many=False)
        return JsonResponse(serializer.data, status=200)

    def put(self, request):
        serializer = UpdateSelfSerializer(self.request.user, data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.save()
            if user.role == "admin" or user.role == "staff":
                output = UserSerializer(user).data
            elif user.role == "customer":
                output = CustomerSerializer(user).data
            return JsonResponse(output, status=200)
        else:
            message = {"message": serializer.errors, "status_code": 400}
            return JsonResponse(message, status=400)


class ChangePasswordView(APIView):
    permission_classes = [AdminPermission | StaffPermission | CustomerPermission]

    def put(self, request):
        serializer = ChangePasswordSerializer(self.request.user, data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.save()
            message = {
                "message": "Password changed successfully",
                "status_code": 200,
            }
            return JsonResponse(message, status=200)
        else:
            message = {
                "message": serializer.errors,
                "status_code": 400,
            }
            return JsonResponse(message, status=400)


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            User.objects.get(email=serializer.data["email"])
        except User.DoesNotExist:
            message = {
                "message": "User with email does not exist",
                "status_code": 404,
            }
            return JsonResponse(message, status=404)

        subject = "Cung cấp mã OTP để đặt lại mật khẩu"
        html_content = render_to_string("otp_verify.html", {"otp": str(generate_otp())})
        recipient_list = [serializer.data["email"]]
        email = EmailMultiAlternatives(subject)
        email.attach_alternative(html_content, "text/html")
        email.to = recipient_list
        email.send()

        message = {
            "message": "OTP has been sent",
            "status_code": 200,
        }
        return JsonResponse(message, status=200)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data.get("email"))
        except User.DoesNotExist:
            message = {
                "message": "User with this email does not exist",
                "status_code": 404,
            }
            return JsonResponse(message, status=404)

        user.set_password(serializer.data.get("new_password"))
        user.save()
        message = {
            "message": "Password reset successfully",
            "status_code": 200,
        }
        return JsonResponse(message, status=200)


class StaffRequestView(APIView):
    permission_classes = [AdminPermission | StaffPermission]

    def get(self, request, page=None, size=None, status=None):
        page = request.GET.get("page", None)
        size = request.GET.get("size", None)
        status = request.GET.get("status", None)

        if status and status not in ("pending", "approved", "rejected"):
            message = {"message": "Invalid status", "status_code": 400}
            return JsonResponse(message, status=400)

        if status:
            requests = CustomerHandlerRequest.objects.filter(status=status)
        else:
            requests = CustomerHandlerRequest.objects.all()
        
        if self.request.user.role != 'admin':
            requests = requests.filter(owner=self.request.user.id)

        if page and size:
            paginator = PageNumberPagination()
            paginator.page_size = size
            requests = paginator.paginate_queryset(requests, request)

        serializer = CustomerHandlerRequestSerializer(requests, many=True)
        output = {
            "requests": serializer.data,
            "page": page if page else 1,
            "size": size if size else int(len(requests)),
            "total": int(len(requests)),
        }
        return JsonResponse(output, status=200)


class StaffRequestByIdView(APIView):
    permission_classes = [AdminPermission | StaffPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AdminPermission | StaffPermission]
        else:
            permission_classes = [AdminPermission]
        return [permission() for permission in permission_classes]

    def get(self, request, request_id):
        try:
            req = CustomerHandlerRequest.objects.get(id=str(request_id).strip())
        except CustomerHandlerRequest.DoesNotExist:
            message = {"message": "Request does not exist", "status_code": 404}
            return JsonResponse(message, status=404)
        
        if self.request.user.role == 'staff' and req.owner != self.request.user:
            message = {"message": "Don't have permission to view this request", "status_code": 403}
            return JsonResponse(message, status=403)
        
        serializer = CustomerHandlerRequestSerializer(req, many=False)
        return JsonResponse(serializer.data, status=200)

    def put(self, request, request_id):
        try:
            req = CustomerHandlerRequest.objects.get(id=str(request_id).strip())
        except CustomerHandlerRequest.DoesNotExist:
            message = {"message": "Request does not exist", "status_code": 404}
            return JsonResponse(message, status=404)

        if not request.data.get('status'):
            message = {'message': 'Status is required', 'status_code': 400}
            return JsonResponse(message, status=400)
        if request.data.get('status') not in ('approved', 'rejected'):
            message = {'message': 'Invalid status', 'status_code': 400}
            return JsonResponse(message, status=400)
        
        if request.data.get('status') == 'approved':
            req.status = 'approved'
            req.save()
            if req.method == 'post':
                serializer = CreateCustomerSerializer(data=req.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.save()
                message = {'message': 'Customer created successfully', 'status_code': 200}
                return JsonResponse(message, status=200)
            if req.method == 'put':
                user = User.objects.get(id=req.customer_id)
                serializer = UpdateCustomerSerializer(user, data=req.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.save()
                message = {'message': 'Customer updated successfully', 'status_code': 200}
                return JsonResponse(message, status=200)
            if req.method == 'delete':
                user = User.objects.get(id=req.customer_id)
                user.delete()
                message = {'message': 'Customer deleted', 'status_code': 200}
                return JsonResponse(message, status=200)
        else:
            req.status = 'rejected'
            req.save()
            output = CustomerHandlerRequestSerializer(req).data
            return JsonResponse(output, status=200)

    def delete(self, request, request_id):
        try:
            req = CustomerHandlerRequest.objects.get(id=str(request_id).strip())
        except CustomerHandlerRequest.DoesNotExist:
            message = {"message": "Request does not exist", "status_code": 404}
            return JsonResponse(message, status=404)

        req.delete()
        message = {"message": "Request deleted successfully", "status_code": 204}
        return JsonResponse(message, status=204)


class StaffCreateRequestView(APIView):
    permission_classes = [StaffPermission]

    def post(self, request):
        if request.data.get('role') != 'customer':
            message = {'message': 'Only customer role is allowed', 'status_code': 400}
            return JsonResponse(message, status=400)
        
        serializer = CreateCustomerRequestSerializer(data=request.data)
        if serializer.is_valid():
            req = CustomerHandlerRequest(
                data=serializer.data,
                status="pending",
                owner=self.request.user,
                method="post",
            )
            req.save()
            output = CustomerHandlerRequestSerializer(req).data
            return JsonResponse(output, status=200)
        else:
            message = {"message": serializer.errors, "status_code": 400}
            return JsonResponse(message, status=400)


class StaffUpdateRequestView(APIView):
    permission_classes = [StaffPermission]
    
    def post(self, request, customer_id):
        try:
            user = User.objects.get(id=str(customer_id).strip())
        except User.DoesNotExist:
            message = {'message': 'User does not exist', 'status_code': 404}
            return JsonResponse(message, status=404)
        
        if user.role != 'customer':
            message = {'message': 'Only customer role is allowed', 'status_code': 400}
            return JsonResponse(message, status=400)
        
        serializer = UpdateCustomerRequestSerializer(data=request.data)
        if serializer.is_valid():
            req = CustomerHandlerRequest(
                data=serializer.data,
                status="pending",
                owner=self.request.user,
                method="put",
                customer_id=customer_id,
            )
            req.save()
            output = CustomerHandlerRequestSerializer(req).data
            return JsonResponse(output, status=200)
        else:
            message = {"message": serializer.errors, "status_code": 400}
            return JsonResponse(message, status=400)


class StaffDeleteRequest(APIView):
    permission_classes = [StaffPermission]
    
    def post(self, request, customer_id):
        try:
            user = User.objects.get(id=str(customer_id).strip())
        except User.DoesNotExist:
            message = {'message': 'User does not exist', 'status_code': 404}
            return JsonResponse(message, status=404)
        
        if user.role != 'customer':
            message = {'message': 'Only customer role is allowed', 'status_code': 400}
            return JsonResponse(message, status=400)
        
        req = CustomerHandlerRequest(method="delete", status="pending", owner=self.request.user, customer_id=customer_id)
        req.save()
        
        output = CustomerHandlerRequestSerializer(req).data
        return JsonResponse(output, status=200)
