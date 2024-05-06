class Configurations():
    def __init__(self) -> None:
        self.behaviors = {
            "SHOW_POPUP" : 0,
            "DO_NOT_TRIGGER":1
        }
        self.hotkey = ""
        self.behavior_of_reserve_menu_detector = self.behaviors["SHOW_POPUP"]
    def set_key_binding(self,keys: str):
        self.hotkey = keys
    
    def set_reserve_menu_detector_behavior(self,behavior:str):
        result = self.behaviors.get(behavior)
        if result is None:
            raise ValueError(f"Undefined behavior '{behavior}' for when program detects 'Select Option' window")
        self.behavior_of_reserve_menu_detector = self.behaviors[behavior]