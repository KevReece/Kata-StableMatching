Problem
---
Match pairs from two equal sized sets of items. 
Each item has preferences of matchings, as an ordered list of the other set items.
The resulting pairs should be stable. It is not stable when two unpaired items would prefer to pair together rather than stay in their current pairings

Normally this is as hetrosexual monogomous preferences between a set of women and men. But could equally be cheeses and wines.

The goal is to find a stable matching, or to identify an unstable data set.

Note: The following is a personal attempt to solve the problem and notably wasn't the most efficient, however the official Gale-Shapley solution is also below

Run
---
```python
from stable_matcher import StableMatcher 
StableMatcher(set_a_preferences_lookup, set_b_preferences_lookup).matches
```

Test
---
`python stable_matcher_test.py`

Example data
---

Set preferences
```python
set_a_preferences = {
    'stilton': ['rioja','chardonnay','chianti'],
    'gruyere': ['chianti','rioja','chardonnay'],
    'cheddar': ['rioja','chianti','chardonnay']
}
```

Run Gale Shapley alternative
---
```python
from gale_shapley_stable_matcher import GaleShapleyStableMatcher as StableMatcher 
StableMatcher(set_a_preferences_lookup, set_b_preferences_lookup).matches
```

Test Gale Shapley alternative
---
1. Edit `stable_matcher_test.py` with `from gale_shapley_stable_matcher import GaleShapleyStableMatcher as StableMatcher`
2. `python stable_matcher_test.py`
