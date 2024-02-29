from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm, ProfileForm
from common.models import Profile # ,Attendance, PointTokenTransaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from common.forms import CustomPasswordChangeForm
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now, localtime
from synopex.models import Question, Answer, Comment
from django.core.paginator import Paginator

@login_required(login_url='common:login')
def base(request):
    # account settings base page
    if request.method == "POST":
        # Instantiate the form with the posted data and files (if there are any)
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 정상적으로 업데이트 되었습니다!')
            return redirect("common:settings_base")
    else:
        # Instantiate the form with the current user's profile data
        form = ProfileForm(instance=request.user.profile)
    context = {'settings_type': 'base', 'form': form}
    return render(request, 'common/settings/base.html', context)

@login_required(login_url='common:login')
def account_page(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    user_questions = Question.objects.filter(author=user)
    user_answers = Answer.objects.filter(author=user)
    user_comments = Comment.objects.filter(author=user)

    context = {
        'user': user,
        'profile': profile,
        'questions': user_questions,
        'answers': user_answers,
        'comments': user_comments
    }
    return render(request, 'common/account_page.html', context)

@login_required(login_url='common:login')
def user_questions(request, user_id):
    # Fetch the user based on the passed user_id
    user = get_object_or_404(User, pk=user_id)
    questions_list = Question.objects.filter(author=user).order_by('-create_date')
    # Set up pagination
    paginator = Paginator(questions_list, 10)  # 10 questions per page
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)
    profile = user.profile
    return render(request, 'common/user_questions.html', {'questions': questions, 'profile':profile})

@login_required(login_url='common:login')
def user_answers(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    answers_lists = Answer.objects.filter(author=user).order_by('-create_date')
    paginator = Paginator(answers_lists, 10) # 10 answers per page
    page_number = request.GET.get('page')
    answers = paginator.get_page(page_number)
    profile = user.profile
    return render(request, 'common/user_answers.html', {'answers': answers, 'profile': profile})

@login_required(login_url='common:login')
def user_comments(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    comments_list = Comment.objects.filter(author=user).order_by('-create_date')
    paginator = Paginator(comments_list, 10) # 10 comments per page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    profile = user.profile
    return render(request, 'common/user_comments.html', {'comments': comments, 'profile': profile})


@login_required(login_url='common:login')
def profile_modify_image(request):
    if request.method == "POST" and 'profile_picture' in request.FILES:
        profile_picture = request.FILES["profile_picture"]
        try:
            if not profile_picture.name.endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Invalid file type: Accepted file types are .png, .jpg, .jpeg")
            width, height = get_image_dimensions(profile_picture)
            max_dimensions = 800
            if width > max_dimensions or height > max_dimensions:
                raise ValidationError("Invalid image size: Max dimensions are 800x800px")
            # Save image to user's profile
            user_profile = request.user.profile  # assumes a related_name of 'profile'
            user_profile.image = profile_picture
            user_profile.save()

            messages.success(request, "Profile picture updated successfully!")
            return redirect('common:settings_base')  # Redirect to a different view after success
        except ValidationError as e:
            messages.error(request, f"Upload failed: {str(e)}")
    elif request.method == "POST":
        messages.error(request, "Something went wrong.")

    return render(request, 'common/settings/profile_picture.html')  # Render the template for image upload

@login_required(login_url="common:login")
def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '비밀번호가 정상적으로 변경되었습니다.')
            return redirect('common:settings_base')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'common/settings/password_reset.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = UserForm() 
    return render(request, "common/signup.html", {"form":form})

# needed for live run
def page_not_found(request, exception):
    return render(request, 'common/404.html', {})