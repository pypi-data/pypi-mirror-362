from nextcord import ui, Interaction, ButtonStyle
from typing import Union, Callable, Dict, Optional, List

class SmartMenuView(ui.View):
    def __init__(self, menu, path: List[str]):
        super().__init__(timeout=menu.timeout)
        self.menu = menu
        self.path = path
        self.build()

    def build(self):
        self.clear_items()
        node = self.menu.get_node(self.path)

        for label, value in node.items():
            self.add_item(MenuButton(label, value, self.menu, self.path + [label]))

        if self.path:
            self.add_item(BackButton(self.menu, self.path[:-1]))

class MenuButton(ui.Button):
    def __init__(self, label, value, menu, path):
        super().__init__(label=label, style=ButtonStyle.primary)
        self.value = value
        self.menu = menu
        self.path = path

    async def callback(self, interaction: Interaction):
        if callable(self.value):
            await self.value(interaction, self.view)
        elif isinstance(self.value, dict):
            view = SmartMenuView(self.menu, self.path)
            await interaction.response.edit_message(content=self.menu.title_for(self.path), view=view)

class BackButton(ui.Button):
    def __init__(self, menu, path):
        super().__init__(label="🔙 Назад", style=ButtonStyle.secondary)
        self.menu = menu
        self.path = path

    async def callback(self, interaction: Interaction):
        view = SmartMenuView(self.menu, self.path)
        await interaction.response.edit_message(content=self.menu.title_for(self.path), view=view)

class SmartMenu:
    def __init__(
        self,
        title: str,
        structure: Dict[str, Union[Callable, dict]],
        *,
        timeout: int = 180,
        ephemeral: bool = True
    ):
        self.title = title
        self.structure = structure
        self.timeout = timeout
        self.ephemeral = ephemeral

    def get_node(self, path: List[str]):
        node = self.structure
        for key in path:
            node = node[key]
        return node

    def title_for(self, path: List[str]):
        return self.title + (" → " + " → ".join(path) if path else "")

    async def send(self, interaction: Interaction):
        view = SmartMenuView(self, path=[])
        await interaction.response.send_message(
            content=self.title,
            view=view,
            ephemeral=self.ephemeral
        )
