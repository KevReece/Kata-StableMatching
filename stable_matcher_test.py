import unittest
from stable_matcher import StableMatcher
#from gale_shapley_stable_matcher import GaleShapleyStableMatcher as StableMatcher

class StableMatcherTests(unittest.TestCase):

    def test_single_pair_match(self):

        set_a_preferences = {'cheddar': ['rioja']}
        set_b_preferences = {'rioja': ['cheddar']}

        matches = StableMatcher(set_a_preferences, set_b_preferences).matches

        self.assertDictEqual(matches, {'cheddar': 'rioja'})

    def test_dominant_pair_match(self):

        set_a_preferences = {
                'cheddar': ['chardonnay','chianti'],
                'gruyere': ['chardonnay','chianti'],
            }
        set_b_preferences = {
                'chardonnay': ['cheddar','gruyere'],
                'chianti': ['cheddar','gruyere'],
            }

        matches = StableMatcher(set_a_preferences, set_b_preferences).matches

        self.assertDictEqual(matches, {
                'cheddar': 'chardonnay',
                'gruyere': 'chianti',
            })
        
    def test_swap_for_set_a_preferences(self):

        set_a_preferences = {
                'cheddar': ['chardonnay','chianti','rioja'], # matches chardonnay
                'gruyere': ['chardonnay','chianti','rioja'], # matches chianti
                'stilton': ['chianti','chardonnay','rioja'], # steals chianti
            }
        set_b_preferences = {
                'chardonnay': ['cheddar','gruyere','stilton'],
                'chianti': ['stilton','cheddar','gruyere'],
                'rioja': ['gruyere','stilton','cheddar'],
            }

        matches = StableMatcher(set_a_preferences, set_b_preferences).matches

        self.assertDictEqual(matches, {
                'cheddar': 'chardonnay',
                'gruyere': 'rioja',
                'stilton': 'chianti',
            })
        
    def test_swap_for_set_b_preferences(self):

        set_a_preferences = {
                'cheddar': ['chardonnay','chianti'], # matches chardonnay
                'gruyere': ['chardonnay','chianti'], # matches chianti 
            }
        set_b_preferences = {
                'chardonnay': ['gruyere','cheddar'], # steals gruyere
                'chianti': ['cheddar','gruyere'],
            }

        matches = StableMatcher(set_a_preferences, set_b_preferences).matches

        self.assertDictEqual(matches, {
                'cheddar': 'chianti',
                'gruyere': 'chardonnay',
            })
        
    def test_verify_matching(self):

        set_a_preferences = {
                'cheddar': ['rioja','chianti','chardonnay'], # matches rioja
                'gruyere': ['chianti','rioja','chardonnay'], # matches chianti
                'stilton': ['rioja','chardonnay','chianti'], # matches chardonnay
            }
        set_b_preferences = {
                'chardonnay': ['gruyere','stilton','cheddar'],
                'chianti': ['gruyere','rioja','cheddar'],
                'rioja': ['stilton','gruyere','cheddar'], # steals stilton
            }

        matches = StableMatcher(set_a_preferences, set_b_preferences).matches

        self.assertDictEqual(matches, {
                'cheddar': 'chardonnay',
                'gruyere': 'chianti',
                'stilton': 'rioja',
            })
        
    def test_arbitary(self):

        set_a_preferences = {
                'cheddar': ['chardonnay','chianti'], # matches chardonnay
                'gruyere': ['chianti','chardonnay'], # matches chianti 
            }
        set_b_preferences = {
                'chardonnay': ['gruyere','cheddar'],
                'chianti': ['cheddar','gruyere'],
            }

        matches = StableMatcher(set_a_preferences, set_b_preferences).matches

        self.assertDictEqual(matches, {
                'cheddar': 'chardonnay',
                'gruyere': 'chianti',
            })
        # equally could swap matchings

if __name__ == '__main__':
    unittest.main()