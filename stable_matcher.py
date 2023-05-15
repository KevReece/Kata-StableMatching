class StableMatcher():

    def __init__(self, set_a_preferences: dict, set_b_preferences: dict):

        self.matches = {}

        self._set_a_preferences = set_a_preferences
        self._set_b_preferences = set_b_preferences
        self._set_a_steals = {}
        self._set_b_steals = {}
        self._set_a_items_to_match = list(set_a_preferences.keys())
        self._set_b_items_to_match = list(set_b_preferences.keys())

        while (self._set_a_items_to_match or self._set_b_items_to_match):
            if (self._set_a_items_to_match):
                set_a_item_name = self._set_a_items_to_match.pop()
                self._MatchSetAItem(set_a_item_name)

            if (self._set_b_items_to_match):
                set_b_item_name = self._set_b_items_to_match.pop()
                self._MatchSetBItem(set_b_item_name)

    def _MatchSetAItem(self, set_a_item_name: str):
        for set_a_item_preference in self._set_a_preferences[set_a_item_name]:
            if set_a_item_name in self.matches and self.matches[set_a_item_name] == set_a_item_preference:
                return
            if not self._SetBItemHasBeenMatched(set_a_item_preference):
                self.matches[set_a_item_name] = set_a_item_preference
                return
            current_set_a_match = self._FindSetBCurrentMatchItemName(set_a_item_preference)
            if self._CanSteal(set_a_item_name, current_set_a_match, self._set_b_preferences[set_a_item_preference]):
                self._StealSetBItem(set_a_item_preference, set_a_item_name)
                return

    def _MatchSetBItem(self, set_b_item_name: str):
        for set_b_item_preference in self._set_b_preferences[set_b_item_name]:
            if set_b_item_preference in self.matches and self.matches[set_b_item_preference] == set_b_item_name:
                return
            if not self._SetAItemHasBeenMatched(set_b_item_preference):
                self.matches[set_b_item_preference] = set_b_item_name
                return
            current_set_b_match = self._FindSetACurrentMatchItemName(set_b_item_preference)
            if self._CanSteal(set_b_item_name, current_set_b_match, self._set_a_preferences[set_b_item_preference]):
                self._StealSetAItem(set_b_item_preference, set_b_item_name)
                return

    def _SetAItemHasBeenMatched(self, set_a_item_name: str):
        return (set_a_item_name in self.matches)

    def _SetBItemHasBeenMatched(self, set_b_item_name: str):
        return (set_b_item_name in self.matches.values())

    def _FindSetACurrentMatchItemName(self, set_a_item_name: str):
        if set_a_item_name in self.matches:
            return self.matches[set_a_item_name]
        return None

    def _FindSetBCurrentMatchItemName(self, set_b_item_name: str):
        if not set_b_item_name in list(self.matches.values()):
            return None
        current_match_index = list(self.matches.values()).index(set_b_item_name)
        current_set_a_match_item_name = list(self.matches.keys())[current_match_index]
        return current_set_a_match_item_name

    @staticmethod
    def _CanSteal(stealer_name: str, current_target_match: str, target_item_preferences: list):
        for target_item_preference in target_item_preferences:
            if target_item_preference == stealer_name:
                return True
            if target_item_preference == current_target_match:
                return False

    def _StealSetAItem(self, set_a_item_name_to_steal: str, set_b_item_name: str):
        stolen_from_set_b_item_name = self._FindSetACurrentMatchItemName(set_a_item_name_to_steal)
        if stolen_from_set_b_item_name:
            self._set_b_items_to_match.append(stolen_from_set_b_item_name)
        current_set_a_match_item_name = self._FindSetBCurrentMatchItemName(set_b_item_name)
        if current_set_a_match_item_name:
            self._set_a_items_to_match.append(current_set_a_match_item_name)
            del self.matches[current_set_a_match_item_name]
        self.matches[set_a_item_name_to_steal] = set_b_item_name
        self._RecordSteal(self._set_b_steals, set_b_item_name, current_set_a_match_item_name, set_a_item_name_to_steal, stolen_from_set_b_item_name)

    def _StealSetBItem(self, set_b_item_name_to_steal: str, set_a_item_name: str):
        stolen_from_set_a_item_name = self._FindSetBCurrentMatchItemName(set_b_item_name_to_steal)
        if stolen_from_set_a_item_name:
            self._set_a_items_to_match.append(stolen_from_set_a_item_name)
            del self.matches[stolen_from_set_a_item_name]
        current_set_b_match_item_name = self._FindSetACurrentMatchItemName(set_a_item_name)
        if current_set_b_match_item_name:
            self._set_b_items_to_match.append(current_set_b_match_item_name)
        self.matches[set_a_item_name] = set_b_item_name_to_steal
        self._RecordSteal(self._set_a_steals, set_a_item_name, current_set_b_match_item_name, set_b_item_name_to_steal, stolen_from_set_a_item_name)

    @staticmethod
    def _RecordSteal(set_steals: dict, origin_item: str, orphaned_origin_item: str, target_item: str, orphaned_target_item: str):
        if (not origin_item in set_steals):
            set_steals[origin_item] = []
        steal_actors = (orphaned_origin_item, target_item, orphaned_target_item)
        if (steal_actors in set_steals[origin_item]):
            raise f'steal duplicate: origin_item={origin_item},orphaned_origin_item={steal_actors[0]},target_item={steal_actors[1]},orphaned_target_item={steal_actors[2]}' 
        set_steals[origin_item].append(steal_actors)
