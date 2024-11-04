from django.shortcuts import render
from .forms import MemberForm
from .models import Tree_structure
from django.db.models import F
from django.db.models import Max

def build_new_tree(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            num_members = form.cleaned_data['num_members']
            joining_package_fee = form.cleaned_data['joining_package_fee']
            sponsor_bonus_percent = form.cleaned_data['sponsor_bonus_percent']
            # binary_bonus_percent = form.cleaned_data['binary_bonus_percent']
            # matching_bonus_percent = form.cleaned_data['matching_bonus_percent']
            # matching_bonus_levels = form.cleaned_data['matching_bonus_levels']
            # capping_scope=form.cleaned_data['bonus_type']
            # cap_limit = form.cleaned_data['cap_limit']
            
            values = list(range(1,num_members+1))
            Tree_structure.objects.all().delete()
            for value in values:
                add_node(value)
                
            nodes = Tree_structure.objects.all()
            
            sponsor_bonus = calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee)
            print(sponsor_bonus)
            
            return render(request, 'display_members.html', {'nodes': nodes})
    else:
        form = MemberForm()
    return render(request, 'input.html', {'form': form})


def add_node(userid):
   
    if Tree_structure.objects.filter(userid=userid).exists():
        return  

    new_node = Tree_structure(userid=userid)
    
    
    if not Tree_structure.objects.exists():
        new_node.parentid = None  
        new_node.position = None  
        new_node.levels = 0       
        new_node.lft = 1         
        new_node.rgt = 2          
        new_node.save()
        return
    
   
    curr_level = 0
    while True:
        level_nodes = Tree_structure.objects.filter(levels=curr_level)
        
        if not level_nodes.exists():
            break 
        
        
        for parent in level_nodes:
            child_count = parent.child.count()
            if child_count < 2:
                new_node.parentid = parent
                new_node.levels = curr_level + 1
                new_node.position = "left" if child_count == 0 else "right"  
                
                if child_count == 1:
                    new_node.lft = parent.rgt
                    new_node.rgt = new_node.lft + 1
                    parent.right = new_node
                else:
                    parent.left = new_node
                    new_node.lft = parent.lft + 1
                    new_node.rgt = new_node.lft + 1

                Tree_structure.objects.filter(rgt__gte=new_node.lft).update(rgt=F('rgt') + 2)
                Tree_structure.objects.filter(lft__gte=new_node.rgt).update(lft=F('lft') + 2)
                new_node.save()
                parent.save()
                return
        curr_level += 1
        
def calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee):
    bonus = 0
    for node in nodes:
        child_count = node.child.count()
        bonus += child_count * sponsor_bonus_percent/100 * joining_package_fee
    return bonus
    

def customized_preorder(curr):
    if curr is None or curr.left is None and curr.right is None:
        return []
    return [curr.userid] + customized_preorder(curr.left) + customized_preorder(curr.right)
       