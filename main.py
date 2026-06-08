import webview
import sys
import os
import re

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Api:
    def __init__(self):
        self.window = None
        self.expanded_width = 850
        self.expanded_height = 600

    def set_window(self, window):
        self.window = window

    def collapse_window(self):
        try:
            if self.window:
                current_width = int(self.window.width)
                current_height = int(self.window.height)
                self.expanded_width = current_width
                self.expanded_height = current_height
                # To make bingo area a square, width = height
                self.window.resize(current_height, current_height)
        except Exception as e:
            print("Error resizing:", e)

    def expand_window(self):
        try:
            if self.window:
                current_height = int(self.window.height)
                self.window.resize(current_height + 250, current_height)
        except Exception as e:
            print("Error resizing:", e)

    def save_bingo(self, data):
        if self.window:
            result = self.window.create_file_dialog(webview.SAVE_DIALOG, directory='', save_filename='bingo.json', file_types=('JSON Files (*.json)', 'All files (*.*)'))
            if result:
                import os
                if isinstance(result, tuple) or isinstance(result, list):
                    path = result[0]
                else:
                    path = result
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(data)
                    return True
                except Exception as e:
                    print(e)
        return False

    def save_generated_bingo(self, file_name, data):
        try:
            safe_name = re.sub(r'[\\/:*?"<>|]+', '_', str(file_name or 'bingo_custom')).strip()
            safe_name = safe_name.strip(' .') or 'bingo_custom'
            if not safe_name.lower().endswith('.json'):
                safe_name += '.json'

            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.abspath(".")

            save_dir = os.path.join(base_dir, 'save')
            os.makedirs(save_dir, exist_ok=True)
            path = os.path.join(save_dir, safe_name)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)

            return {'ok': True, 'path': path}
        except Exception as e:
            print(e)
            return {'ok': False, 'error': str(e)}

    def load_bingo(self):
        if self.window:
            result = self.window.create_file_dialog(webview.OPEN_DIALOG, directory='', file_types=('JSON Files (*.json)', 'All files (*.*)'))
            if result:
                import os
                if isinstance(result, tuple) or isinstance(result, list):
                    path = result[0]
                else:
                    path = result
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(e)
        return None

if __name__ == '__main__':
    api = Api()
    html_path = get_resource_path('index.html')
    window = webview.create_window('Bingo Editor', url=html_path, js_api=api, width=850, height=600, min_size=(400, 400))
    api.set_window(window)
    # Start webview
    webview.start()
