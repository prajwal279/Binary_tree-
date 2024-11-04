from django.shortcuts import render
from .forms import MemberForm
from .models import Tree_structure
from django.db.models import F
from django.db import connection

def build_new_tree(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            num_members = form.cleaned_data['num_members']
            values = list(range(1,num_members+1))
            Tree_structure.objects.all().delete()
            # with connection.cursor() as cursor:
                # cursor.execute("ALTER TABLE placement_tree_structure AUTO_INCREMENT = 1;")
            for value in values:
                add_node(value)
                
            nodes = Tree_structure.objects.all()
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
                else:
                    new_node.lft = parent.lft + 1
                    new_node.rgt = new_node.lft + 1

                Tree_structure.objects.filter(rgt__gte=new_node.lft).update(rgt=F('rgt') + 2)
                Tree_structure.objects.filter(lft__gte=new_node.rgt).update(lft=F('lft') + 2)
                new_node.save()
                return
        curr_level += 1
       




# def add_node(userid, parentid, position, levels, left_count,num_members):
#     if Tree_structure.objects.filter(userid=userid).exists() or num_members <= 0:
#         return
#     lft = left_count[0]
#     rgt = lft + 1from django.db.models import F
#     )
#     new_node.save()
#     left_count[0] = rgt+1
    
#     left_child_node = userid*2
#     right_child_node = userid*2+1
    
#     if left_child_node <= num_members:
#         new_node.rgt=left_count[0]+1
#         num_members = num_members - 1
#         add_node(userid=left_child_node,parentid=new_node,position="left",levels=levels+1,left_count=left_count,num_members=num_members)
    
#     if num_members <= right_child_node:
#         new_node.rgt=left_count[0]+1
#         num_members = num_members - 1
#         add_node(userid=right_child_node,parentid=new_node,position="right",levels=levels+1,left_count=left_count,num_members=num_members)
#     new_node.rgt = left_count[0]
#     new_node.save()            
#     # left_count[0]+=1


# from django.shortcuts import render
# from .forms import MemberForm
# from .models import Tree_structure
# from django.db.models import F

# def build_new_tree(request):
#     if request.method == 'POST':
#         form = MemberForm(request.POST)
#         if form.is_valid():
#             num_members = form.cleaned_data['num_members']
#             values = list(range(1,num_members+1))
#             Tree_structure.objects.all().delete()
#             for value in values:
#                 add_node(value)
                
#             nodes = Tree_structure.objects.all()
#             return render(request, 'display_members.html', {'nodes': nodes})
#     else:
#         form = MemberForm()
#     return render(request, 'input.html', {'form': form})


# def add_node(userid):
#     if Tree_structure.objects.filter(userid=userid).exists():
#         return  
    
#     new_node = Tree_structure(userid=userid)
    
#     if not Tree_structure.objects.exists():
#         new_node.parentid = None 
#         new_node.position = None
#         new_node.levels = 0
#         new_node.lft = 1
#         new_node.rgt = 2
#         new_node.save()
#         return
    
#     curr_level = 0
#     while True:
#         level_node = Tree_structure.objects.filter(levels=curr_level)
        
#         if not level_node.exists():
#             break
        
#         for parents in level_node:
#             child_count = parents.child.count()
#             if child_count < 2:
#                 new_node.parentid = parents
#                 new_node.levels = curr_level + 1
#                 new_node.position = "left" if child_count == 0  else "right"  
                
#                 if child_count == 0:
#                     new_node.lft = parents.lft + 1
#                     new_node.rgt = parents.lft + 2
#                 else:
#                     new_node.lft = parents.rgt
#                     new_node.rgt = parents.rgt + 1
#                 new_node.save()
#                 Tree_structure.objects.filter(rgt__gte = new_node.lft).update(rgt = F('rgt') + 2)
#                 Tree_structure.objects.filter(lft__gte = new_node.rgt).update(lft = F('lft') + 2)
#                 return
#         curr_level += 1           

