from sys import platform
import logging as log

from sys import path
from os.path import dirname, join, abspath
path.append(abspath(join(dirname(__file__), 'file_dialog')))

class FileDialog:
    def __init__(self) -> None:

        if platform == 'darwin':
            from .macos.filedialog import MacFileChooser
            self.filechooser = MacFileChooser()

        elif platform == 'win32':
            from .windows.filedialog import Win32FileChooser
            self.filechooser = Win32FileChooser()

        elif platform == 'linux':
            from .linux.filedialog import LinuxFileChooser
            self.filechooser = LinuxFileChooser()


    def open_file(self, path: str = None,
                        multiple: bool = True,
                        filters: list = [],
                        preview: bool = False,
                        title: str = None,
                        show_hidden: bool = False):
        
        selected_path: list = self.filechooser.run(mode='open',
                                                   path=path,
                                                   multiple=multiple,
                                                   filters=filters,
                                                   preview=preview,
                                                   title=title,
                                                   show_hidden=show_hidden)

        if len(selected_path) == 1:
            return selected_path[0]

        else:
            return selected_path


    def save_file(self, path: str = None,
                        filters: list = [],
                        title: str = None,
                        show_hidden: bool = False):
        
        save_path: list = self.filechooser.run(mode='save',
                                               path=path,
                                               filters=filters,
                                               title=title,
                                               show_hidden=show_hidden)

        if save_path is None:
            return None

        else:
            return save_path[0]


    def open_dir(self, path: str = None,
                       multiple: bool = True,
                       filters: list = [],
                       preview: bool = False,
                       title: str = None,
                       show_hidden: bool = False):
        
        selected_path: list = self.filechooser.run(mode='dir',
                                                   path=path,
                                                   multiple=multiple,
                                                   filters=filters,
                                                   preview=preview,
                                                   title=title,
                                                   show_hidden=show_hidden)

        if len(selected_path) == 1:
            return selected_path[0]

        else:
            return selected_path
