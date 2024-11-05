from django.shortcuts import render
from .forms import MemberForm
from .models import Tree_structure
from django.db.models import F

# def calculate_binary_bonus(nodes, joining_package_fee, binary_bonus_percent):
#     binary_bonus_percent = binary_bonus_percent / 100  
#     total_binary_bonus = 0.0
    
#     for node in nodes:
       
#         left_count = 0
#         right_count = 0
        
#         left_nodes = Tree_structure.objects.filter(lft__gt=node.lft, rgt__lt=node.rgt)
#         left_count = left_nodes.count()

#         right_nodes = Tree_structure.objects.filter(lft__gt=node.lft, rgt__lt=node.rgt)
#         right_count = right_nodes.count()

#         print("Left Count:", left_count)
#         print("Right Count:", right_count)

#         if left_count > 0 and right_count > 0:
#             left_sv = left_count * joining_package_fee
#             right_sv = right_count * joining_package_fee
#             binary_bonus_value = min(left_sv, right_sv) * binary_bonus_percent
#             total_binary_bonus += binary_bonus_value
#             node.binary_bonus = binary_bonus_value
#             node.save()
#         else:
#             node.binary_bonus = 0
#             node.save()

#     return total_binary_bonus

def calculate_binary_bonus(nodes, joining_package_fee, binary_bonus_percent):
    binary_bonus_percent = binary_bonus_percent / 100  
    total_binary_bonus = 0.0
    
    for node in nodes:
        left_count = 0
        right_count = 0
        
        if node.left:
            left_count = 1 + count_subtree_nodes(node.left)
            print("Left Count:",left_count)
        
        if node.right:
            right_count = 1 + count_subtree_nodes(node.right)
            print("Right Count:",right_count)

        if left_count > 0 and right_count > 0:
            left_sv = left_count * joining_package_fee
            right_sv = right_count * joining_package_fee
            binary_bonus_value = min(left_sv, right_sv) * binary_bonus_percent
            total_binary_bonus += binary_bonus_value
            node.binary_bonus = binary_bonus_value
            node.save()
        else:
            node.binary_bonus = 0
            node.save()
            

    return total_binary_bonus


def count_subtree_nodes(node):
    num = Tree_structure.objects.filter(lft__gt=node.lft, rgt__lt=node.rgt).count()
    print("NUM:",num)
    return num


def build_new_tree(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            num_members = form.cleaned_data['num_members']
            joining_package_fee = form.cleaned_data['joining_package_fee']
            sponsor_bonus_percent = form.cleaned_data['sponsor_bonus_percent']
            binary_bonus_percent = form.cleaned_data['binary_bonus_percent']
            values = list(range(1,num_members+1))
            Tree_structure.objects.all().delete()
            for value in values:
                add_node(value)  
                
            nodes = Tree_structure.objects.all()
            for node in nodes:
                parent = None
                if node.parentid:
                    parent = nodes.filter(userid=node.parentid.userid)
                if parent:
                    if node.position == 'left':
                        parent[0].left = node
                    elif node.position == 'right':
                        parent[0].right = node
                    parent[0].save()
                    
            nodes = Tree_structure.objects.all()
            sponsor_bonus = calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee) 
            binary_bonus = calculate_binary_bonus(nodes, binary_bonus_percent, joining_package_fee)
            return render(request, 'display_members.html', {'nodes': nodes,'sponsor_bonus': sponsor_bonus,'binary_bonus': binary_bonus})
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
                if child_count == 0:
                    new_node.position = "left"
                else: 
                    new_node.position = "right"  

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


    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


  

    
# def calculate_binary_bonus(nodes, joining_package_fee, binary_bonus_percent):
#     binary_bonus_percent = binary_bonus_percent / 100 

#     def count_subtree_nodes(node):
#         return Tree_structure.objects.filter(
#             lft__gt=node.lft,
#             rgt__lt=node.rgt
#         ).count()

#     def calculate_for_node(node):
#         left_count = count_subtree_nodes(node.left) if node.left else 0
#         right_count = count_subtree_nodes(node.right) if node.right else 0
        
#         left_count += 1 if node.left else 0
#         right_count += 1 if node.right else 0

#         if left_count == 0 or right_count == 0:
#             node.binary_bonus = 0.0
#         else:
#             left_sv = left_count * joining_package_fee
#             right_sv = right_count * joining_package_fee


#             binary_bonus_value = min(left_sv, right_sv) * binary_bonus_percent
#             node.binary_bonus = binary_bonus_value
#         node.save()

#         if node.left:
#             calculate_for_node(node.left)
#         if node.right:
#             calculate_for_node(node.right)

#     total_binary_bonus = 0.0
#     for node in nodes:
#         node.binary_bonus = 0.0  
#         calculate_for_node(node)  
#         total_binary_bonus += node.binary_bonus  
#     return total_binary_bonus



# def calculate_binary_bonus(nodes, joining_package_fee, binary_bonus_percent):

#     binary_bonus_percent = binary_bonus_percent / 100

#     def calculate_for_node(node):
       
#         left_count = Tree_structure.objects.filter(parentid=node, position='left').count()
#         right_count = Tree_structure.objects.filter(parentid=node, position='right').count()
#         if left_count == 0 or right_count == 0:
#             node.binary_bonus = 0.0
#         else:
#             left_sv = left_count * joining_package_fee
#             right_sv = right_count * joining_package_fee

           
#             binary_bonus_value = min(left_sv, right_sv)
#             node.binary_bonus = binary_bonus_value * binary_bonus_percent

#         if node.left:
#             node.left.binary_bonus += node.binary_bonus
#             calculate_for_node(node.left)

#         if node.right:
#             node.right.binary_bonus += node.binary_bonus
#             calculate_for_node(node.right)

#     total_binary_bonus = 0.0
#     for node in nodes:
#         node.binary_bonus = 0.0
#         calculate_for_node(node)
#         total_binary_bonus += node.binary_bonus

#     return total_binary_bonus


