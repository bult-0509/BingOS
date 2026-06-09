import webview
import sys
import os
import re
import threading

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
        self.sidebar_width = 250
        self.min_grid_size = 400
        self.resize_mode = 'EDIT'
        self.last_width = 850
        self.last_height = 600
        self._resize_guard = False
        self._resize_lock = threading.Lock()

    def set_window(self, window):
        self.window = window
        self.last_width = int(getattr(window, 'initial_width', self.last_width) or self.last_width)
        self.last_height = int(getattr(window, 'initial_height', self.last_height) or self.last_height)

    def on_window_resized(self, width, height):
        try:
            if not self.window:
                return

            width = int(width)
            height = int(height)

            with self._resize_lock:
                if self._resize_guard:
                    self.last_width = width
                    self.last_height = height
                    return

                if getattr(self.window, 'minimized', False) or getattr(self.window, 'maximized', False):
                    self.last_width = width
                    self.last_height = height
                    return

                offset = self.sidebar_width if self.resize_mode == 'EDIT' else 0
                min_width = self.min_grid_size + offset
                min_height = self.min_grid_size

                delta_width = abs(width - self.last_width)
                delta_height = abs(height - self.last_height)

                if delta_width >= delta_height:
                    target_width = max(min_width, width)
                    target_height = max(min_height, target_width - offset)
                    target_width = target_height + offset
                else:
                    target_height = max(min_height, height)
                    target_width = target_height + offset

                if abs(target_width - width) <= 1 and abs(target_height - height) <= 1:
                    self.last_width = width
                    self.last_height = height
                    return

                self._resize_guard = True

            self.window.resize(int(target_width), int(target_height))

            with self._resize_lock:
                self.last_width = int(target_width)
                self.last_height = int(target_height)
                self._resize_guard = False
        except Exception as e:
            with self._resize_lock:
                self._resize_guard = False
            print("Error locking resize ratio:", e)

    def collapse_window(self):
        try:
            if self.window:
                current_width = int(self.window.width)
                current_height = int(self.window.height)
                self.expanded_width = current_width
                self.expanded_height = current_height
                target_size = max(self.min_grid_size, current_height)
                self.resize_mode = 'DRAW'
                self._resize_guard = True
                self.window.resize(target_size, target_size)
                self.last_width = target_size
                self.last_height = target_size
                self._resize_guard = False
        except Exception as e:
            self._resize_guard = False
            print("Error resizing:", e)

    def expand_window(self):
        try:
            if self.window:
                current_height = int(self.window.height)
                target_height = max(self.min_grid_size, current_height)
                target_width = target_height + self.sidebar_width
                self.resize_mode = 'EDIT'
                self._resize_guard = True
                self.window.resize(target_width, target_height)
                self.last_width = target_width
                self.last_height = target_height
                self._resize_guard = False
        except Exception as e:
            self._resize_guard = False
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
    window.events.resized += api.on_window_resized
    # Start webview
    webview.start()
