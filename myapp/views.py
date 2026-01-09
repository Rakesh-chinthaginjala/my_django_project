from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .models import Student, User
from .forms import StudentForm
from .serializers import UserSerializer, LoginSerializer, IdSerializer
from .utils import get_tokens_for_user


def greet(request):
    return HttpResponse("hello all welcome to django project")

def demo(request):
    return HttpResponse("let start with django")

def send_email_with_attchment(request):

    # creating an email object
    email = EmailMessage(
        subject='Regarding email sending with attachment',
        body='Welcome to the django project handling the files',
        from_email='rakesh.chinthaginjala26@gmail.com',
        to=['nb6684@gmail.com']
    )

    # adding the attachment to the email
    email.attach(
        filename='krishna.txt',
        content='Folk Tales & Fables: Often feature animals or magical elements with clear morals, teaching lessons about honesty, cleverness, or bravery (e.g., the monkey and crocodile)',
        mimetype='text/plain'
    )

    # finally sending the email
    email.send()
    return HttpResponse('Email sent successfully with attachment')

def send_simple_email(request):
    send_mail(
        subject='welcome to diamonds class',
        message='hi everyone,Good moring,this is a simple email',
        from_email='rakesh.chinthaginjala26@gmail.com',
        recipient_list=['mleelakrishna37@gmail.com'],
        fail_silently=False,
    
    )
    return HttpResponse('Email sent successfully')

def send_sample_email(request):
    send_mail(
        subject='sample mail',
        message='hi srinadh chinthaginjala,this mail is working please check yourself ',
        from_email='rakesh.chinthaginjala26@gmail.com',
        recipient_list=['c.srinadh@outlook.com'],
        fail_silently=False,
    
    )
    return HttpResponse('Email sent successfully')

def send_multiple_email(request):
    my_message1=(
        'tommorrow having a exam',
        'the',
        'rakesh.chinthaginjala26@gmail.com',
        ['chrakesh664@gmail.com'],
    )
    my_message2=(
        'tommorrow having a exam',
        'fhiyufyef',
        'rakesh.chinthaginjala26@gmail.com',
        ['mleelakrishna37@gmail.com'],
    )
    send_mass_mail((my_message1,my_message2),fail_silently=False)
    return HttpResponse('messege successfully sending')


def send_single_email(request):
    send_mail(
        subject='sample email',
        message='hi sir ,this email is working please check once manually ',
        from_email='rakesh.chinthaginjala26@gmail.com',
        recipient_list=['c.srinadh@outlook.com'],
        fail_silently=False,
    )
    return HttpResponse('sucessfully sending email')

# Static Home page (Generic TemplateView)
class HomeView(TemplateView):
    template_name = 'student/home.html'

# ListView: lists students (pagination optional)
class StudentListView(ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    paginate_by = 10  # optional

# DetailView: show single student
class StudentDetailView(DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

# CreateView: uses ModelForm automatically
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    # on success will use get_absolute_url of the model

# Function-based view example for manual form processing (shows explicit handling of request.FILES)
# def add_student_fbv(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             student = form.save()
#             return redirect(student.get_absolute_url())
#     else:
#         form = StudentForm()
#     return render(request, 'student/student_form.html', {'form': form})


def add_student_fbv(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # or wherever you want to go
    else:
        form = StudentForm()
    return render(request, 'student/student_form.html', {'form': form})



class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # User is inactive on register
        serializer.save(is_active=False)

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )


class UserSignupAPIView(APIView):
    """Provides a form schema via GET and accepts signup via POST."""
    permission_classes = [AllowAny]

    def get(self, request):
        schema = {
            "title": "User Signup",
            "fields": [
                {"name": "username", "type": "string", "required": True, "max_length": 100},
                {"name": "email", "type": "email", "required": True},
                {"name": "password", "type": "password", "required": True, "min_length": 8},
            ]
        }
        return Response(schema)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create user inactive by default
        serializer.save(is_active=False)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                username=serializer.validated_data["username"]
            )
        except User.DoesNotExist:
            return Response(
                {"error": "USer not found in db"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(
            serializer.validated_data["password"],
            user.password
        ):
            return Response(
                {"error": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ACTIVATE USER ON LOGIN
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        return Response({
            "message": "Login successful",
            "token": get_tokens_for_user(user),
            "is_active": user.is_active
        })
    
class GetAllUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = IdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(id=serializer.validated_data["id"]).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        return Response(UserSerializer(user).data)
    
class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Convert QueryDict → normal dict
        data = request.data.dict() if hasattr(request.data, "dict") else dict(request.data)

        user_id = data.get("id")

        if not user_id:
            return Response(
                {"error": "id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove id before checking update fields
        data.pop("id", None)

        # CRITICAL VALIDATION
        if len(data.keys()) == 0:
            return Response(
                {"error": "At least one field is required to update"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(
            user,
            data=data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "User updated successfully",
            "updated_fields": serializer.validated_data
        })

class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = IdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(id=serializer.validated_data["id"]).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response({"message": "User deleted successfully"})

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = IdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["id"]

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.is_active = False
        user.save(update_fields=["is_active"])

        return Response({
            "message": "Logout successful",
            "is_active": user.is_active
        })


#   write an API that takes location as input and gets its latitude and longitude  
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_lat_long(request):
    location = request.GET.get('location')

    if not location:
        return Response(
            {"error": "Location parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json"
    }

    response = requests.get(
        url, params=params, headers={"User-Agent": "django-app"}
    )

    data = response.json()

    if not data:
        return Response(
            {"error": "Location not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "location": location,
        "latitude": data[0]["lat"],
        "longitude": data[0]["lon"]
    })
    