from django import forms

class MemberForm(forms.Form):
    num_members=forms.IntegerField(label="No Of Members",min_value=1)
    joining_package_fee = forms.FloatField(label="Joining Package Fee", min_value=0)
    sponsor_bonus_percent = forms.FloatField(label="Sponsor Bonus (%)", min_value=0)
    binary_bonus_percent = forms.FloatField(label="Binary Bonus (%)", min_value=0)
    matching_bonus_percent = forms.CharField(max_length=255, required=False)
<<<<<<< HEAD

    
    capping_limit = forms.FloatField(label="Capping Limit", min_value=0)
=======
    # matching_bonus_levels = forms.IntegerField(label="Matching Bonus Levels", min_value=0)
    
    # matching_bonus_level_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    # matching_bonus_level_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    # matching_bonus_level_3 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    cap_limit = forms.FloatField(label="Capping Limit", min_value=0)
>>>>>>> 4d56f01fc16c767cc53850b70ca2e313e3429cce
    
    BONUS_TYPE_CHOICES = [
        ('binary', 'Binary Bonus'),
        ('matching', 'Matching Bonus'),
        ('sponsor', 'Sponsor Bonus'),
        ('total', 'Total Bonus'),
    ]
    capping_scope = forms.ChoiceField(choices=BONUS_TYPE_CHOICES)
    
    