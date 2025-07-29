from nextcord import ui, Interaction, ButtonStyle
from typing import Union, Callable, Dict, Optional, List
from .localization import LocalizationContext

Localizable = Union[str, Dict[str, str]]
MenuAction = Union[Callable, dict]

class SmartMenuView(ui.View):
    def __init__(self, menu, path: List[str], locale: str):
        super().__init__(timeout=menu.timeout)
        self.menu = menu
        self.path = path
        self.locale = locale
        self.ctx = LocalizationContext(locale=locale, fallback=menu.default_locale)
        self.build()

    def build(self):
        self.clear_items()
        node = self.menu.get_node(self.path)

        for key, value in node.items():
            # Если value — подменю со структурой с мета-полями
            label = self.ctx.translate(value.get("__label__") if isinstance(value, dict) and "__label__" in value else key)
            self.add_item(MenuButton(label, value, self.menu, self.path + [key], self.locale))

        if self.path:
            self.add_item(BackButton(self.menu, self.path[:-1], self.locale, self.ctx))

class MenuButton(ui.Button):
    def __init__(self, label, value, menu, path, locale):
        super().__init__(label=label, style=ButtonStyle.primary)
        self.value = value
        self.menu = menu
        self.path = path
        self.locale = locale

    async def callback(self, interaction: Interaction):
        if callable(self.value):
            await self.value(interaction, self.view)
        elif isinstance(self.value, dict):
            action = self.value.get("__action__")
            if callable(action):
                await action(interaction, self.view)
            else:
                view = SmartMenuView(self.menu, self.path, self.locale)
                await interaction.response.edit_message(content=self.menu.title_for(self.path, self.locale), view=view)

class BackButton(ui.Button):
    def __init__(self, menu, path, locale, ctx: LocalizationContext):
        label = ctx.translate({"en": "🔙 Back", "ru": "🔙 Назад"})
        super().__init__(label=label, style=ButtonStyle.secondary)
        self.menu = menu
        self.path = path
        self.locale = locale

    async def callback(self, interaction: Interaction):
        view = SmartMenuView(self.menu, self.path, self.locale)
        await interaction.response.edit_message(content=self.menu.title_for(self.path, self.locale), view=view)

class SmartMenu:
    def __init__(
        self,
        title: Localizable,
        structure: Dict[str, MenuAction],
        *,
        timeout: int = 180,
        ephemeral: bool = True,
        default_locale: str = "en"
    ):
        self.title = title
        self.structure = structure
        self.timeout = timeout
        self.ephemeral = ephemeral
        self.default_locale = default_locale

    def get_node(self, path: List[str]):
        node = self.structure
        for key in path:
            node = node[key]
        return node

    def title_for(self, path: List[str], locale: str):
        ctx = LocalizationContext(locale, fallback=self.default_locale)
        base_title = ctx.translate(self.title)
        return base_title + (" → " + " → ".join(path) if path else "")

    async def send(self, interaction: Interaction):
        locale = interaction.locale.value if interaction.locale else self.default_locale
        view = SmartMenuView(self, path=[], locale=locale)
        await interaction.response.send_message(
            content=self.title_for([], locale),
            view=view,
            ephemeral=self.ephemeral
        )
