from typing import Callable, Optional, Union, Dict

class SmartAction:
    def __init__(
        self,
        callback: Callable,
        *,
        label: Optional[Union[str, Dict[str, str]]] = None,
        description: Optional[Union[str, Dict[str, str]]] = None,
        condition: Optional[Callable] = None
    ):
        self.callback = callback
        self.label = label
        self.description = description
        self.condition = condition  # lambda interaction: bool

    def is_visible(self, interaction):
        return self.condition(interaction) if self.condition else True

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)
