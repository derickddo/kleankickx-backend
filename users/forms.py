from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username if it exists
        self.fields.pop('username', None)

    def save(self, request):
        user = super().save(request)
        return user
