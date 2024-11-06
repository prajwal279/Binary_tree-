from django.db import models

class Tree_structure(models.Model):
    userid = models.IntegerField(unique=True, primary_key=True)
    parentid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    position = models.CharField(max_length=5, choices=[('left', 'left'), ('right', 'right'), ('NULL', 'NULL')], null=True, blank=True)
    levels = models.IntegerField()
    lft = models.IntegerField()
    rgt = models.IntegerField()
    left = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='left_child')
    right = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='right_child')
<<<<<<< HEAD
    sponsor_bonus = models.FloatField(default=0.0)
=======
>>>>>>> 4d56f01fc16c767cc53850b70ca2e313e3429cce
    binary_bonus = models.FloatField(default=0.0)
    matching_bonus = models.FloatField(default=0.0)

    