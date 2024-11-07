from django.test import TestCase
from django.urls import reverse
from .models import Tree_structure
from .forms import MemberForm
from .views import (
    calculate_sponsor_bonus,
    calculate_binary_bonus,
    calculate_matching_bonus,
    add_node
)

class TreeStructureTests(TestCase):
    def setUp(self):
        self.root_node = Tree_structure.objects.create(userid=1, levels=0, lft=1, rgt=2)
        self.node2 = Tree_structure.objects.create(userid=2, parentid=self.root_node, position="left", levels=1, lft=2, rgt=3)
        self.node3 = Tree_structure.objects.create(userid=3, parentid=self.root_node, position="right", levels=1, lft=4, rgt=5)

    def test_calculate_sponsor_bonus(self):
        nodes = Tree_structure.objects.all()
        sponsor_bonus_percent = 10
        joining_package_fee = 1000
        capping_limit = 5000

        sponsor_bonus = calculate_sponsor_bonus(nodes, sponsor_bonus_percent, joining_package_fee, capping_limit)
        self.assertIsNotNone(sponsor_bonus)
        for node in nodes:
            self.assertLessEqual(node.sponsor_bonus, capping_limit)

    def test_calculate_binary_bonus(self):
        nodes = Tree_structure.objects.all()
        joining_package_fee = 1000
        binary_bonus_percent = 10
        capping_limit = 5000

        binary_bonus = calculate_binary_bonus(nodes, joining_package_fee, binary_bonus_percent, capping_limit)
        self.assertIsNotNone(binary_bonus)
        for node in nodes:
            self.assertLessEqual(node.binary_bonus, capping_limit)

    def test_calculate_matching_bonus(self):
        nodes = Tree_structure.objects.all()
        matching_bonus_percent = {1: 10, 2: 5}
        capping_limit = 5000

        matching_bonus = calculate_matching_bonus(nodes, matching_bonus_percent, capping_limit)
        self.assertIsNotNone(matching_bonus)
        for node in nodes:
            self.assertLessEqual(node.matching_bonus, capping_limit)

    def test_add_node(self):
        initial_count = Tree_structure.objects.count()
        add_node(4)
        self.assertEqual(Tree_structure.objects.count(), initial_count + 1)

    def test_build_new_tree_view(self):
        response = self.client.post(reverse('build_new_tree'), {
            'num_members': 3,
            'joining_package_fee': 1000,
            'sponsor_bonus_percent': 10,
            'binary_bonus_percent': 10,
            'capping_limit': 5000,
            'capping_scope': 'total',
            'matching_bonus_percent': "10,5"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_members.html')
        nodes = Tree_structure.objects.all()
        self.assertGreater(len(nodes), 0)

    # def test_tree_structure_integrity(self):
    #     add_node(6)
    #     nodes = Tree_structure.objects.all()
    #     for node in nodes:
    #         if node.parentid:
    #             self.assertTrue(node.lft > node.parentid.lft)
    #             self.assertTrue(node.rgt > node.parentid.lft)
