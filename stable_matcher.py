class StableMatcher():

    def __init__(self, set_a_preferences: dict, set_b_preferences: dict):

        self.set_a_preferences = set_a_preferences
        self.set_b_preferences = set_b_preferences
        self.matches = {}
        self.set_a_steals = {}
        self.set_b_steals = {}
        self.set_a_items_to_match = list(set_a_preferences.keys())
        self.set_b_items_to_match = list(set_b_preferences.keys())

        while (self.set_a_items_to_match or self.set_b_items_to_match):
            if (self.set_a_items_to_match):
                set_a_item_name = self.set_a_items_to_match.pop()
                self.MatchSetAItem(set_a_item_name)

            if (self.set_b_items_to_match):
                set_b_item_name = self.set_b_items_to_match.pop()
                self.MatchSetBItem(set_b_item_name)

    def MatchSetAItem(self, set_a_item_name: str):
        for set_a_item_preference in self.set_a_preferences[set_a_item_name]:
            if set_a_item_name in self.matches and self.matches[set_a_item_name] == set_a_item_preference:
                return
            if not self.SetBItemHasBeenMatched(set_a_item_preference):
                self.matches[set_a_item_name] = set_a_item_preference
                return
            current_set_a_match = self.FindSetBCurrentMatchItemName(set_a_item_preference)
            if self.CanSteal(set_a_item_name, current_set_a_match, self.set_b_preferences[set_a_item_preference]):
                self.StealSetBItem(set_a_item_preference, set_a_item_name)
                return

    def MatchSetBItem(self, set_b_item_name: str):
        for set_b_item_preference in self.set_b_preferences[set_b_item_name]:
            if set_b_item_preference in self.matches and self.matches[set_b_item_preference] == set_b_item_name:
                return
            if not self.SetAItemHasBeenMatched(set_b_item_preference):
                self.matches[set_b_item_preference] = set_b_item_name
                return
            current_set_b_match = self.FindSetACurrentMatchItemName(set_b_item_preference)
            if self.CanSteal(set_b_item_name, current_set_b_match, self.set_a_preferences[set_b_item_preference]):
                self.StealSetAItem(set_b_item_preference, set_b_item_name)
                return

    def SetAItemHasBeenMatched(self, set_a_item_name: str):
        return (set_a_item_name in self.matches)

    def SetBItemHasBeenMatched(self, set_b_item_name: str):
        return (set_b_item_name in self.matches.values())

    def FindSetACurrentMatchItemName(self, set_a_item_name: str):
        if set_a_item_name in self.matches:
            return self.matches[set_a_item_name]
        return None

    def FindSetBCurrentMatchItemName(self, set_b_item_name: str):
        if not set_b_item_name in list(self.matches.values()):
            return None
        current_match_index = list(self.matches.values()).index(set_b_item_name)
        current_set_a_match_item_name = list(self.matches.keys())[current_match_index]
        return current_set_a_match_item_name

    @staticmethod
    def CanSteal(stealer_name: str, current_target_match: str, target_item_preferences: list):
        for target_item_preference in target_item_preferences:
            if target_item_preference == stealer_name:
                return True
            if target_item_preference == current_target_match:
                return False

    def StealSetAItem(self, set_a_item_name_to_steal: str, set_b_item_name: str):
        stolen_from_set_b_item_name = self.FindSetACurrentMatchItemName(set_a_item_name_to_steal)
        if stolen_from_set_b_item_name:
            self.set_b_items_to_match.append(stolen_from_set_b_item_name)
        current_set_a_match_item_name = self.FindSetBCurrentMatchItemName(set_b_item_name)
        if current_set_a_match_item_name:
            self.set_a_items_to_match.append(current_set_a_match_item_name)
            del self.matches[current_set_a_match_item_name]
        self.matches[set_a_item_name_to_steal] = set_b_item_name
        self.record_steal(self.set_b_steals, set_b_item_name, current_set_a_match_item_name, set_a_item_name_to_steal, stolen_from_set_b_item_name)

    def StealSetBItem(self, set_b_item_name_to_steal: str, set_a_item_name: str):
        stolen_from_set_a_item_name = self.FindSetBCurrentMatchItemName(set_b_item_name_to_steal)
        if stolen_from_set_a_item_name:
            self.set_a_items_to_match.append(stolen_from_set_a_item_name)
            del self.matches[stolen_from_set_a_item_name]
        current_set_b_match_item_name = self.FindSetACurrentMatchItemName(set_a_item_name)
        if current_set_b_match_item_name:
            self.set_b_items_to_match.append(current_set_b_match_item_name)
        self.matches[set_a_item_name] = set_b_item_name_to_steal
        self.record_steal(self.set_a_steals, set_a_item_name, current_set_b_match_item_name, set_b_item_name_to_steal, stolen_from_set_a_item_name)

    @staticmethod
    def record_steal(set_steals: dict, origin_item: str, orphaned_origin_item: str, target_item: str, orphaned_target_item: str):
        if (not origin_item in set_steals):
            set_steals[origin_item] = []
        steal_actors = (orphaned_origin_item, target_item, orphaned_target_item)
        if (steal_actors in set_steals[origin_item]):
            raise f'steal duplicate: origin_item={origin_item},orphaned_origin_item={steal_actors[0]},target_item={steal_actors[1]},orphaned_target_item={steal_actors[2]}' 
        set_steals[origin_item].append(steal_actors)
