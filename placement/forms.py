from django import forms

class MemberForm(forms.Form):
    num_members=forms.IntegerField(label="No Of Members",min_value=1)
    joining_package_fee = forms.FloatField(label="Joining Package Fee", min_value=0)
    sponsor_bonus_percent = forms.FloatField(label="Sponsor Bonus (%)", min_value=0)
    binary_bonus_percent = forms.FloatField(label="Binary Bonus (%)", min_value=0)
    matching_bonus_percent = forms.CharField(max_length=255, required=False)
    
    capping_limit = forms.FloatField(label="Capping Limit", min_value=0)

    BONUS_TYPE_CHOICES = [
        ('binary', 'Binary Bonus'),
        ('matching', 'Matching Bonus'),
        ('sponsor', 'Sponsor Bonus'),
        ('total', 'Total Bonus'),
    ]
    capping_scope = forms.ChoiceField(choices=BONUS_TYPE_CHOICES)
    
    