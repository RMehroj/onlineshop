from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.contrib.auth.hashers import check_password, make_password 
from . import models 
from django.views import View 



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserWriteSerializer
    authentication_classes = []


class Login(View): 
    return_url = None
  
    def get(self, request): 
        Login.return_url = request.GET.get('return_url') 
        return render(request, 'login.html') 
  
    def post(self, request): 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        user = models.User.get_user_by_email(email) 
        error_message = None
        if user: 
            flag = check_password(password, user.password) 
            if flag: 
                request.session['user'] = user.pk
  
                if Login.return_url: 
                    return HttpResponseRedirect(Login.return_url) 
                else: 
                    Login.return_url = None
                    return redirect('homepage') 
            else: 
                error_message = 'Invalid !!'
        else: 
            error_message = 'Invalid !!'
  
        print(email, password) 
        return render(request, 'login.html', {'error': error_message}) 

  
class SignupAPIView(APIView):
    def get(self, request):
        data = {
            'message': 'Welcome to the signup page!'
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        postData = request.data  # Use request.data to get POST data in DRF
        username = postData.get('username')
        full_name = postData.get('full_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        user = models.User(username=username,
                            full_name=full_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validate_user(user)

        if not error_message:
            user.password = make_password(user.password)
            user.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': {
                    'username': username,
                    'full_name': full_name,
                    'phone': phone,
                    'email': email,
                }
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def validate_user(self, user):
        error_message = None
        if not user.username:
            error_message = "Please Enter your First Name !!"
        elif len(user.username) < 3:
            error_message = 'First Name must be 3 characters long or more'
        elif not user.full_name:
            error_message = 'Please Enter your Last Name'
        elif len(user.full_name) < 3:
            error_message = 'Last Name must be 3 characters long or more'
        elif not user.phone:
            error_message = 'Enter your Phone Number'
        elif len(user.phone) < 10:
            error_message = 'Phone Number must be 10 characters long'
        elif len(user.password) < 5:
            error_message = 'Password must be 5 characters long'
        elif len(user.email) < 5:
            error_message = 'Email must be 5 characters long'
        elif user.isExists():
            error_message = 'Email Address Already Registered..'

        return error_message


# class Signup (View): 
#     def get(self, request): 
#         return render(request, 'signup.html') 
  
#     def post(self, request): 
#         postData = request.POST 
#         username = postData.get('username') 
#         full_name = postData.get('full_name') 
#         phone = postData.get('phone') 
#         email = postData.get('email') 
#         password = postData.get('password') 
#         # validation 
#         value = { 
#             'username': username, 
#             'full_name': full_name, 
#             'phone': phone, 
#             'email': email 
#         } 
#         error_message = None
  
#         user = models.User(username=username, 
#                             full_name=full_name, 
#                             phone=phone, 
#                             email=email, 
#                             password=password) 
#         error_message = self.validateCustomer(user) 
  
#         if not error_message: 
#             print(username, full_name, phone, email, password) 
#             user.password = make_password(user.password) 
#             user.register() 
#             return redirect('homepage') 
#         else: 
#             data = { 
#                 'error': error_message, 
#                 'values': value 
#             } 
#             return render(request, 'signup.html', data) 
  
#     def validateCustomer(self, user): 
#         error_message = None
#         if (not user.username): 
#             error_message = "Please Enter your First Name !!"
#         elif len(user.username) < 3: 
#             error_message = 'First Name must be 3 char long or more'
#         elif not user.full_name: 
#             error_message = 'Please Enter your Last Name'
#         elif len(user.full_name) < 3: 
#             error_message = 'Last Name must be 3 char long or more'
#         elif not user.phone: 
#             error_message = 'Enter your Phone Number'
#         elif len(user.phone) < 10: 
#             error_message = 'Phone Number must be 10 char Long'
#         elif len(user.password) < 5: 
#             error_message = 'Password must be 5 char long'
#         elif len(user.email) < 5: 
#             error_message = 'Email must be 5 char long'
#         elif user.isExists(): 
#             error_message = 'Email Address Already Registered..'
  
#         return error_message 
    
def logout(request): 
    request.session.clear() 
    return redirect('login') 


