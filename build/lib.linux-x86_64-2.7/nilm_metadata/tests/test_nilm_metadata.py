#!/usr/bin/env python
from __future__ import print_function
import unittest
from copy import deepcopy
from ..object_concatenation import get_appliance_types

class TestNilmMetadata(unittest.TestCase):

    def test_appliance_types(self):
        types = get_appliance_types()

        # COLD APPLIANCE
        cold = types['cold appliance']
        cold_answers = {'n_ancestors': 1, 
                        'categories': {'traditional': 'cold', 'size': 'large'}}
        for k, v in cold_answers.iteritems():        
            self.assertEqual(cold[k], v)

        # FRIDGE
        fridge = types['fridge']
        fridge_answers = {'n_ancestors': 2, 
                          'categories': {'traditional': 'cold', 
                                         'size': 'large',
                                         'electrical': ['single-phase induction motor']},
                          'subtypes': ['chest', 'upright']}
        for k, v in fridge_answers.iteritems():
            self.assertEqual(fridge[k], v)
            
        fridge_dists = fridge['distributions']
        self.assertEqual(fridge_dists.keys(), ['rooms'])
        rooms = fridge_dists['rooms']
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0]['distance'], 1)
        self.assertEqual(rooms[0]['from_appliance_type'], 'cold appliance')

        # FREEZER
        freezer = types['freezer']
        freezer_dists = freezer['distributions']
        self.assertEqual(freezer_dists.keys(), ['rooms'])
        rooms = freezer_dists['rooms']
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0]['distance'], 2)
        self.assertEqual(rooms[0]['from_appliance_type'], 'cold appliance')
        freezer_answers = deepcopy(fridge_answers)
        freezer_answers.update({'n_ancestors': 3})
        for k, v in freezer_answers.iteritems():
            self.assertEqual(freezer[k], v)

if __name__ == '__main__':
    unittest.main()
