from django import forms

class MemberForm(forms.Form):
    num_members=forms.IntegerField(label="No Of Members",min_value=1)