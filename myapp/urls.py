from django.urls import path
from .views import *

app_name='myapp'

urlpatterns=[
    path("greet_message/",greet),
    path('demo/',demo,name='demo'),
    path("send_email/",send_email_with_attchment,name='email'),
    path("simple_email/",send_simple_email,name='email'),

   
    path("multiple_email/",send_multiple_email,name='email'),
    path("single_email/",send_single_email,name='email'),
    
    path('book/', HomeView.as_view(), name='home'),                  # static home page
    path('students/', StudentListView.as_view(), name='list'),  # list students
    path('students/add/', StudentCreateView.as_view(), name='add'),  # create (class-based)
    path('students/<int:pk>/', StudentDetailView.as_view(), name='detail'),  # detail
    # example function-based view for form processing with custom logic:
    path('students/fbv-add/', add_student_fbv, name='fbv_add'),

    path("register/", RegisterUserAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),

    path("get_all_users/", GetAllUsersAPIView.as_view()),
    path("get_user/", GetUserAPIView.as_view()),
    path("update_user details/", UpdateUserAPIView.as_view()),
    path("delete_user/", DeleteUserAPIView.as_view()),
    path("logout_user/", LogoutAPIView.as_view()),

]
