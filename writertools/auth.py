from allauth.account.adapter import DefaultAccountAdapter


class ProjectAuthAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True
