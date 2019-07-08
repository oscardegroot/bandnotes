from ..forms import UserForm, LoginForm, ProfileForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib import messages

def logout_view(request):
    logout(request)
    return redirect('home')

# Log a user in
class LoginFormView(View):
    form_class = LoginForm
    template_name = 'musicnotes/login_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('musicnotes:index')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

                if user.is_active:
                    login(request, user)
                    redirect_to = self.request.GET.get('next')
                    if(redirect_to):
                        return redirect(redirect_to)
                    else:
                        return redirect('musicnotes:index')
        else:
            messages.error(request, 'User could not be logged in');
            return render(request, self.template_name, {'form': request.POST})


# Register a user
class UserFormView(View):
    template_name = 'musicnotes/registration_form.html'

    # On submit
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        # If the data is valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()

            profile.user = user

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Account created!')
                    return redirect('musicnotes:index')
                else:
                    messages.error(request, 'User is not active!')
                    return render(request, self.template_name, {
                        'user_form': user_form,
                        'profile_form': profile_form,
                    })

        else:
            messages.error(request, 'Invalid data')
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form,
            })

    # Loading the page first, give them an empty form
    def get(self, request):
        user_form = UserForm(None)
        profile_form = ProfileForm(None)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })