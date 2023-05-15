class GaleShapleyStableMatcher():

    def __init__(self, set_a_preferences: dict, set_b_preferences: dict):

        self.matches = {}

        self._set_a_preferences = set_a_preferences
        self._set_b_preferences = set_b_preferences
        self._set_a_preference_ranks = self._MapPreferencesToPreferenceRanks(set_a_preferences)
        self._set_b_preference_ranks =  self._MapPreferencesToPreferenceRanks(set_b_preferences)
        self._item_preferences_to_match = list(map(lambda item_name: (item_name, 0), set_a_preferences.keys()))

        while (self._item_preferences_to_match):
            item_name, preference_index = self._item_preferences_to_match.pop()
            self._MatchItem(item_name, preference_index)

    def _MatchItem(self, item_name: str, preference_index: int):
        item_preferences = self._set_a_preferences[item_name]
        desired_item = item_preferences[preference_index]
        if item_name in self.matches and self.matches[item_name] == desired_item:
            return
        if not desired_item in self.matches.values():
            self.matches[item_name] = desired_item
            return
        current_set_a_match = self._FindSetBCurrentMatchItemName(desired_item)
        if self._CanSteal(item_name, current_set_a_match, self._set_b_preference_ranks[desired_item]):
            self._StealItem(desired_item, item_name)
            return
        self._item_preferences_to_match.append((item_name, preference_index+1))

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
    def _CanSteal(stealer_name: str, current_target_match: str, target_item_preference_ranks: list):
        target_rank_of_stealer = target_item_preference_ranks[stealer_name]
        target_rank_of_current = target_item_preference_ranks[current_target_match]
        return target_rank_of_stealer < target_rank_of_current

    def _StealItem(self, set_b_item_name_to_steal: str, set_a_item_name: str):
        stolen_from_set_a_item_name = self._FindSetBCurrentMatchItemName(set_b_item_name_to_steal)
        if stolen_from_set_a_item_name:
            self._item_preferences_to_match.append((
                    stolen_from_set_a_item_name, 
                    self._set_a_preference_ranks[stolen_from_set_a_item_name][set_b_item_name_to_steal]+1)) 
            del self.matches[stolen_from_set_a_item_name]
        current_set_b_match_item_name = self._FindSetACurrentMatchItemName(set_a_item_name)
        if current_set_b_match_item_name:
            self._item_preferences_to_match.append((
                    current_set_b_match_item_name,
                    self._set_b_preference_ranks[current_set_b_match_item_name][set_a_item_name]+1))
        self.matches[set_a_item_name] = set_b_item_name_to_steal

    @staticmethod
    def _MapPreferencesToPreferenceRanks(preferences: dict):
        return {
                item_name: {
                    preference_name: index 
                    for index, preference_name in enumerate(item_preferences)
                } 
                for item_name, item_preferences in preferences.items()
            }
