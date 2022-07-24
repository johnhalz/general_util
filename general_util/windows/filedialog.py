from win32com.shell.shell import (
    SHBrowseForFolder as browse,
    SHGetPathFromIDList as get_path
)
from win32com.shell import shellcon
import win32gui
import win32con
import pywintypes
from os.path import dirname, splitext, join, isdir


class Win32FileChooser:
    '''A native implementation of NativeFileChooser using the
    Win32 API on Windows.

    Not Implemented features (all dialogs):
    * preview
    * icon

    Not implemented features (in directory selection only - it's limited
    by Windows itself):
    * preview
    * window-icon

    Known issues:
    * non-existins folders such as: Network, Control Panel, My Computer, Trash,
      Library and likes will raise a COM error. The path does not exist, nor
      a user can open from or save to such path.
    '''

    def __init__(self) -> None:
        pass


    def run(self, mode: str, path: str, filters: list, title: str, show_hidden: bool, multiple: bool = False, preview: bool = False):
        self.selection = []
        try:
            if mode != 'dir':
                args = {}

                if path:
                    if isdir(path):
                        args["InitialDir"] = path
                    else:
                        args["InitialDir"] = dirname(path)
                        _, ext = splitext(path)
                        args["File"] = path
                        args["DefExt"] = ext and ext[1:]  # no period

                args["Title"] = title if title else "Pick a file..."
                args["CustomFilter"] = 'Other file types\x00*.*\x00'
                args["FilterIndex"] = 1
                file = ""
                if "File" in args:
                    file = args["File"]
                args["File"] = file + ("\x00" * 4096)

                # e.g. open_file(filters=['*.txt', '*.py'])
                filters = ""
                for f in filters:
                    if type(f) == str:
                        filters += (f + "\x00") * 2
                    else:
                        filters += f[0] + "\x00" + ";".join(f[1:]) + "\x00"
                args["Filter"] = filters

                flags = win32con.OFN_OVERWRITEPROMPT
                flags |= win32con.OFN_HIDEREADONLY

                if multiple:
                    flags |= win32con.OFN_ALLOWMULTISELECT
                    flags |= win32con.OFN_EXPLORER
                if show_hidden:
                    flags |= win32con.OFN_FORCESHOWHIDDEN

                args["Flags"] = flags

                try:
                    if mode == 'open':
                        self.fname, _, _ = win32gui.GetOpenFileNameW(**args)
                    elif mode == 'save':
                        self.fname, _, _ = win32gui.GetSaveFileNameW(**args)
                except pywintypes.error as e:
                    # if canceled, it's not really an error
                    if not e.winerror:
                        self._handle_selection(self.selection)
                        return self.selection
                    raise

                if self.fname:
                    if multiple:
                        seq = str(self.fname).split("\x00")
                        if len(seq) > 1:
                            dir_n, base_n = seq[0], seq[1:]
                            self.selection = [
                                join(dir_n, i) for i in base_n
                            ]
                        else:
                            self.selection = seq
                    else:
                        self.selection = str(self.fname).split("\x00")

            else:  # dir mode
                BIF_EDITBOX = shellcon.BIF_EDITBOX
                BIF_NEWDIALOGSTYLE = 0x00000040
                # From http://goo.gl/UDqCqo
                pidl, name, images = browse(
                    win32gui.GetDesktopWindow(),
                    None,
                    title if title else "Pick a folder...",
                    BIF_NEWDIALOGSTYLE | BIF_EDITBOX, None, None
                )

                # pidl is None when nothing is selected
                # and e.g. the dialog is closed afterwards with Cancel
                if pidl:
                    self.selection = [str(get_path(pidl).decode('utf-8'))]

        except (RuntimeError, pywintypes.error, Exception):
            # Let user know what happened
            import traceback
            traceback.print_exc()
        
        return self.selection
