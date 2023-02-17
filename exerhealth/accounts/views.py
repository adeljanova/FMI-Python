from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from exerhealth.accounts.forms import ProfileForm
from exerhealth.accounts.models import FitnessProfile
from exerhealth.accounts.utils import interpret_bmi
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def home(request):
    return render(request, 'index.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        my_user = authenticate(username=username, password=pass1)
        if my_user is not None:
            login(request, my_user)
            messages.success(request, "Login Successful")
            return redirect('/')
        else:
            messages.error(request, "Username OR Password is not valid")
            return redirect('accounts:login')

    return render(request, "registration/login.html")


def logout_page(request):
    logout(request)
    return redirect("accounts:login")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            messages.info(request, "Password is not Matching")
            return redirect('accounts:signup')

        if User.objects.get(username=username):
            messages.warning(request, "Username is already taken")
            return redirect('accounts:signup')

        if User.objects.get(email=email):
            messages.warning(request, "Email is already taken")
            return redirect('accounts:signup')

        my_user = User.objects.create_user(username, email, pass1)
        my_user.save()
        messages.success(request, "User is Created Please Login")
        return redirect('accounts:login')

    return render(request, "registration/signup.html")


@login_required(login_url=login)
def profile_page(request):
    user = request.user
    try:
        fitness_profile = FitnessProfile.objects.get(user=user)
    except FitnessProfile.DoesNotExist:
        fitness_profile = None
    context = {'fitness_profile': fitness_profile}
    return render(request, 'profile/profile.html', context)


# @login_required(login_url=login)
# def bmi_calculator(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             bmi = profile.weight / (profile.height ** 2)
#             status = interpret_bmi(bmi)
#             chart = {
#                 'type': 'bar',
#                 'data': {
#                     'labels': ['Height', 'Weight', 'BMI', 'status'],
#                     'datasets': [{
#                         'label': 'Profile Data',
#                         'data': [profile.height, profile.weight, bmi, status],
#                         'backgroundColor': ['rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)',
#                                             'rgba(255, 99, 132, 0.2)']
#                     }]
#                 },
#                 'options': {
#                     'scales': {
#                         'y': {
#                             'beginAtZero': True
#                         }
#                     }
#                 }
#             }
#             fig = bmi_plot(bmi_calculator)
#             canvas = FigureCanvas(fig)
#             response = HttpResponse(content_type='image/png')
#             canvas.print_png(response)
#             return response
#     else:
#         form = ProfileForm()
#     return render(request, 'profile/profile.html', {'form': form})

@login_required(login_url=login)
def bmi_calculator(request):
    profile_id = request.GET.get('profile_id')
    profile = FitnessProfile.objects.get(id=profile_id)
    bmi = profile.calculate_bmi
    fig = bmi_plot(bmi)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return render(request, 'profile/bmi.html', {'bmi': bmi, 'plot': response.getvalue()})


@login_required(login_url=login)
def bmi_plot(bmi):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(['BMI'], bmi_calculator)
    ax.set_ylim(0, 40)
    plt.title('BMI Result')
    plt.ylabel('BMI')
    plt.xlabel('Category')
    plt.show()
    return fig
