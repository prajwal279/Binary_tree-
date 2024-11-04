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
    
    def __str__(self):
        return f"Node: {self.userid}, Levels: {self.levels}"
