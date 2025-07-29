from nicegui import ui
from typing import List, Callable
from common import config_settings
from datetime import datetime


class NiceGUIConsole:
    def __init__(self):
        self.init_footer_log()
        self.log_area = ui.column().style('max-height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px')
        self.counter_label = ui.label()

    def init_footer_log(self):
        with ui.element('div').style('''
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #2e3b4e;
            text-align: center;
            padding: 4px 8px;  /* meno padding verticale */
            font-size: 14px;
            line-height: 18px;
            z-index: 1000;
        ''') as footer:
            self.footer_label = ui.label("Ready.").style("color: white; margin: 0")

    def log_message(self, message: str, color: str = "#ffffff"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        """
        with self.log_area:
            ui.label(f"[{timestamp}] {message}").style(f'color: {color}; white-space: pre-wrap')
        """
        self.footer_label.text = f"${timestamp}$ {message}"
        self.footer_label.style(f"color: {color}")


    def panel_message(self, message: str, color: str = "#ccc"):
        with ui.card().style(f'background-color: {color}; color: white'):
            ui.label(message).style("text-align: center")

    def bot_log(self, message: str):
        self._add_log(message, config_settings.console_options.NORMAL_COLOR)

    def bot_error_log(self, message: str):
        self._add_log(f'❌ {message}', config_settings.console_options.ERROR_COLOR)

    def bot_warning_log(self, message: str):
        self._add_log(f'⚠️ {message}', config_settings.console_options.QUESTION_MESSAGE_COLOR)

    def bot_input_log(self, message: str):
        self._add_log(message, config_settings.console_options.NORMAL_COLOR)

    def bot_question_log(self, message: str):
        self._add_log(message, config_settings.console_options.QUESTION_MESSAGE_COLOR)

    def bot_counter_log(self, message: str):
        self.counter_label.set_text(message)
        self.counter_label.style(f'color: {config_settings.console_options.QUESTION_MESSAGE_COLOR}')

    def bot_process_table_log(self, content: List):
        ui.label("Here is your files list" if content else "There are no files here")
        ui.table(columns=[
            {'name': 'pack', 'label': 'Torrent Pack', 'field': 'pack'},
            {'name': 'category', 'label': 'Media', 'field': 'category'},
            {'name': 'path', 'label': 'Path', 'field': 'path'},
        ], rows=[
            {
                'pack': 'Yes' if item.torrent_pack else 'No',
                'category': item.category,
                'path': item.torrent_path,
            } for item in content
        ])

    def bot_process_table_pw(self, content: List):
        ui.label("Here is your files list" if content else "There are no files here")
        ui.table(columns=[
            {'name': 'category', 'label': 'Category', 'field': 'category'},
            {'name': 'indexer', 'label': 'Indexer', 'field': 'indexer'},
            {'name': 'title', 'label': 'Title', 'field': 'title'},
            {'name': 'size', 'label': 'Size', 'field': 'size'},
            {'name': 'seeders', 'label': 'Seeders', 'field': 'seeders'},
        ], rows=[
            {
                'category': item.categories[0]['name'],
                'indexer': item.indexer,
                'title': item.title,
                'size': str(item.size),
                'seeders': str(item.seeders),
            } for item in content
        ])

    def bot_tmdb_table_log(self, result, title: str, media_info_language: List[str]):
        media_info_audio_languages = ", ".join(media_info_language).upper()
        self.panel_message(f"Results for {title.upper()}")

        ui.table(columns=[
            {'name': 'tmdb_id', 'label': 'TMDB ID', 'field': 'tmdb_id'},
            {'name': 'language', 'label': 'LANGUAGE', 'field': 'language'},
            {'name': 'poster', 'label': 'TMDB POSTER', 'field': 'poster'},
            {'name': 'backdrop', 'label': 'TMDB BACKDROP', 'field': 'backdrop'},
        ], rows=[{
            'tmdb_id': str(result.video_id),
            'language': media_info_audio_languages,
            'poster': result.poster_path,
            'backdrop': result.backdrop_path,
        }])

    def wait_for_user_confirmation(self, message: str, on_confirm: Callable):
        self.bot_error_log(message)
        with ui.row():
            ui.button("OK", on_click=on_confirm)
            ui.button("Cancel",
                      on_click=lambda: self.bot_error_log("Operation cancelled. Please update your config file."))

    def user_input(self, message: str, on_submit: Callable[[int], None]):
        with ui.row():
            input_field = ui.input(label=message, placeholder="Enter TMDB ID").props("type=number")
            ui.button("Submit", on_click=lambda: self._validate_and_submit(input_field.value, on_submit))

    def user_input_str(self, message: str, on_submit: Callable[[str], None]):
        with ui.row():
            input_field = ui.input(label=message, placeholder="Enter text")
            ui.button("Submit", on_click=lambda: on_submit(input_field.value or "0"))

    def _add_log(self, message: str, color: str = "#fff"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        with self.log_area:
            ui.label(f"[{timestamp}] {message}").style(f'color: {color}; white-space: pre-wrap')

    def _validate_and_submit(self, value: str, on_submit: Callable[[int], None]):
        try:
            if value.isdigit():
                user_id = int(value)
                on_submit(user_id if user_id < 9999999 else 0)
            else:
                self.bot_error_log("Please enter a valid number.")
        except Exception as e:
            self.bot_error_log(f"Error: {str(e)}")
