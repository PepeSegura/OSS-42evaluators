from django import forms
from fetch_data.models import Cursus, Project, ClusterLocation
from fetch_data.models import User as OurUser

class FavoriteUsersForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[('add', 'Add'), ('delete', 'Delete')], widget=forms.HiddenInput())

    class Meta:
        model = OurUser
        fields = ['login', 'favorite_users']
