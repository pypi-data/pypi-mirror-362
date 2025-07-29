from nicegui import ui

class SettingsPanel:
    def __init__(self):
        with ui.column().classes('items-center q-pa-xl'):

            # Header
            ui.label("Settings").style('font-size: 32px; font-weight: bold; color: #2e3b4e')

            # Settings card
            with ui.card().style('max-width: 400px; width: 100%; padding: 20px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1)'):

                self._setting_group("Account Settings", [
                    ("Enable notifications", True),
                    ("Allow email updates", False),
                ])

                ui.separator().style("margin: 20px 0")

                self._setting_group("Privacy", [
                    ("Location tracking", False),
                    ("Data sharing", True),
                ])

    def _setting_group(self, title: str, settings: list[tuple[str, bool]]):
        ui.label(title).style('font-size: 18px; font-weight: 500; margin-bottom: 10px; color: #333')

        for label_text, default_value in settings:
            with ui.row().style('justify-content: space-between; align-items: center; margin-bottom: 12px'):
                ui.label(label_text).style("font-size: 14px; color: #555")
                ui.switch(value=default_value)
