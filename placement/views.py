from django.shortcuts import render
from .forms import MemberForm
from .models import Tree_structure
from django.db.models import F
from decimal import Decimal
# def calculate_matching_bonus(nodes, matching_bonus_percent, joining_package_fee, matching_bonus_levels):
#     total_matching_bonus = 0
#     nodes=Tree_structure.objects.all()
#     for node in nodes:
#         if node.binary_bonus and node.parentid:
#             parent = node.parentid
#             matching_bonus = (node.binary_bonus * matching_bonus_percent) / 100
#             parent.matching_bonus = matching_bonus
#             parent.save()
def calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee, capping_limit=2147483647):
    bonus = 0
    node_sponsor_bonus = 0
    for node in nodes:
        child_count = node.child.count()
        node_sponsor_bonus += child_count * sponsor_bonus_percent/100 * joining_package_fee
        if node_sponsor_bonus >= capping_limit:
            node_sponsor_bonus = capping_limit
        
        bonus += node_sponsor_bonus
        node.sponsor_bonus = node_sponsor_bonus
        node.save()
    return bonus
     

def calculate_binary_bonus(nodes, joining_package_fee, binary_bonus_percent, capping_limit=2147483647):
    binary_bonus_percent = binary_bonus_percent / 100  
    total_binary_bonus = 0.0
    
    for node in nodes:
        left_count = 0
        right_count = 0
        
        if node.left:
            left_count =  count_subtree_nodes(node.left)
        
        if node.right:
            right_count =  count_subtree_nodes(node.right)

        if left_count > 0 and right_count > 0:
            left_sv = left_count * joining_package_fee
            right_sv = right_count * joining_package_fee
            binary_bonus_value = min(left_sv, right_sv) * binary_bonus_percent

            if binary_bonus_value >= capping_limit:
                binary_bonus_value = capping_limit

            total_binary_bonus += binary_bonus_value
            node.binary_bonus = binary_bonus_value
            node.save()
        else:
            node.binary_bonus = 0
            node.save()
            

    return total_binary_bonus

def count_subtree_nodes(node):
    num = Tree_structure.objects.filter(lft__gte=node.lft, rgt__lte=node.rgt).count()
    return num

def calculate_matching_bonus(nodes, matching_bonus_percent, capping_limit=2147483647):
    for node in nodes:
        node.matching_bonus = 0
        node.save()

    node_levels = {}
    for node in nodes:
        if node.levels not in node_levels:
            node_levels[node.levels] = []
        node_levels[node.levels].append(node)

    max_level = max(node_levels.keys())
    for level in range(max_level, -1, -1):
        for node in node_levels[level]:
            current_node = node
            
            for i in range(1, max(matching_bonus_percent.keys()) + 1):
                if i in matching_bonus_percent:
                    bonus_percent = matching_bonus_percent[i]
                    if current_node.parentid:
                        parent = Tree_structure.objects.get(userid=current_node.parentid.userid)
                        matching_bonus = (float(node.binary_bonus) * float(bonus_percent)) / 100
                        old_matching_bonus = parent.matching_bonus
                        if old_matching_bonus + matching_bonus >= capping_limit:
                            parent.matching_bonus = capping_limit
                        else:
                            parent.matching_bonus = old_matching_bonus + matching_bonus
                        parent.save()
                        current_node = parent
                    else:
                        break
    return sum(node.matching_bonus for node in nodes)

def build_new_tree(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            num_members = form.cleaned_data['num_members']
            joining_package_fee = form.cleaned_data['joining_package_fee']
            sponsor_bonus_percent = form.cleaned_data['sponsor_bonus_percent']
            binary_bonus_percent = form.cleaned_data['binary_bonus_percent']
            capping_limit = form.cleaned_data['capping_limit']
            capping_scope = form.cleaned_data['capping_scope']
            matching_bonus_percents = [int(level.strip()) for level in form.cleaned_data['matching_bonus_percent'].split(",")]
            matching_bonus_percent = {index + 1: value for index, value in enumerate(matching_bonus_percents)}
                    
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
            nodes = Tree_structure.objects.all()
            binary_bonus = calculate_binary_bonus(nodes, binary_bonus_percent, joining_package_fee)
            nodes = Tree_structure.objects.all()
            matching_bonus = calculate_matching_bonus(nodes, matching_bonus_percent)
            if capping_scope == 'binary':
                nodes = Tree_structure.objects.all()
                binary_bonus = calculate_binary_bonus(nodes, binary_bonus_percent, joining_package_fee, capping_limit)
            elif capping_scope == 'sponsor':
                nodes = Tree_structure.objects.all()
                sponsor_bonus = calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee, capping_limit) 
            elif capping_scope == 'matching':
                nodes = Tree_structure.objects.all()
                matching_bonus = calculate_matching_bonus(nodes, matching_bonus_percent, capping_limit)
            elif capping_scope == 'total':
                nodes = Tree_structure.objects.all()
                binary_bonus = calculate_binary_bonus(nodes, binary_bonus_percent, joining_package_fee, capping_limit)
                nodes = Tree_structure.objects.all()
                sponsor_bonus = calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee, capping_limit)
                nodes = Tree_structure.objects.all()
                matching_bonus = calculate_matching_bonus(nodes, matching_bonus_percent, capping_limit)
            nodes = Tree_structure.objects.all()
            return render(request, 'display_members.html', {'nodes': nodes,'sponsor_bonus': sponsor_bonus,'binary_bonus': binary_bonus, 'matching_bonus': matching_bonus})
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