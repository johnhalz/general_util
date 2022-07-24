from distutils.spawn import find_executable as which
import os
import subprocess as sp
import time


class LinuxFileChooser:
    '''FileChooser implementation for GNu/Linux. Accepts one additional
    keyword argument, *desktop_override*, which, if set, overrides the
    back-end that will be used. Set it to "gnome" for Zenity, to "kde"
    for KDialog and to "yad" for YAD (Yet Another Dialog).
    If set to None or not set, a default one will be picked based on
    the running desktop environment and installed back-ends.
    '''

    def __init__(self, desktop_override: str = None) -> None:
        self.executable = ''    # The name of the executable of the back-end.
        self.separator = '|'    # The separator used by the back-end. Override this for automatic splitting, or override _split_output.
        self.successretcode = 0 # The return code which is returned when the user doesn't close thedialog without choosing anything, or when the app doesn't crash.
        
        self._process = None

        # Determine desktop
        self.desktop = None
        if (str(os.environ.get("XDG_CURRENT_DESKTOP")).lower() == "kde"
                and which("kdialog")):
            self.desktop = "kde"
        
        elif (str(os.environ.get("DESKTOP_SESSION")).lower() == "trinity"
                and which('kdialog')):
            self.desktop = "kde"
        
        elif which("yad"):
            self.desktop = "yad"
        
        elif which("zenity"):
            self.desktop = "gnome"


    @staticmethod
    def _handle_selection(selection):
        '''
        Dummy placeholder for returning selection from chooser.
        '''
        return selection


    def _run_command(self, cmd):
        self._process = sp.Popen(cmd, stdout=sp.PIPE)
        while True:
            ret = self._process.poll()
            if ret is not None:
                if ret == self.successretcode:
                    out = self._process.communicate()[0].strip().decode('utf8')
                    return self._set_and_return_selection(
                        self._split_output(out))
                else:
                    return self._set_and_return_selection(None)
            time.sleep(0.1)


    def _set_and_return_selection(self, value):
        self.selection = value
        self._handle_selection(value)
        return value


    def _split_output(self, out):
        '''This methods receives the output of the back-end and turns
        it into a list of paths.
        '''
        return out.split(self.separator)


    def run(self, mode: str, path: str, filters: list, title: str, show_hidden: bool = False, multiple: bool = False, preview: bool = False):
        if self.desktop == 'yad':
            command = self._gen_cmdline_yad(mode, path, filters, title, show_hidden, multiple, preview)
        elif self.desktop == 'kde':
            command = self._gen_cmdline_kdialog(mode, path, filters, title, show_hidden, multiple, preview)
        elif self.desktop == 'gnome':
            command = self._gen_cmdline_zenity(mode, path, filters, title, show_hidden, multiple, preview)

        print(command)
        return self._run_command(command)


    def _gen_cmdline_zenity(self, mode: str, path: str, filters: list, title: str, show_hidden: bool = False, multiple: bool = False, preview: bool = False):
        '''A FileChooser implementation using Zenity (on GNU/Linux).

        Not implemented features:
        * show_hidden
        * preview
        '''

        self.executable = "zenity"
        self.separator = "|"
        self.successretcode = 0

        cmdline = [
            which(self.executable),
            "--file-selection",
            "--confirm-overwrite"
        ]
        if multiple:
            cmdline += ["--multiple"]
        if mode == 'save':
            cmdline += ["--save"]
        elif mode == 'dir':
            cmdline += ["--directory"]
        if path:
            cmdline += ["--filename", path]
        if title:
            cmdline += ["--name", title]
        for f in filters:
            if type(f) == str:
                cmdline += ["--file-filter", f]
            else:
                cmdline += [
                    "--file-filter",
                    "{name} | {flt}".format(name=f[0], flt=" ".join(f[1:]))
                ]

        return cmdline


    def _gen_cmdline_kdialog(self, mode: str, path: str, filters: list, title: str, show_hidden: bool = False, multiple: bool = False, preview: bool = False):
        self.executable = "kdialog"
        self.separator = "\n"
        self.successretcode = 0

        cmdline = [which(self.executable)]

        filt = []

        for f in filters:
            if type(f) == str:
                filt += [f]
            else:
                filt += list(f[1:])

        if mode == "dir":
            cmdline += [
                "--getexistingdirectory",
                (path if path else os.path.expanduser("~"))
            ]
        elif mode == "save":
            cmdline += [
                "--getsavefilename",
                (path if path else os.path.expanduser("~")),
                " ".join(filt)
            ]
        else:
            cmdline += [
                "--getopenfilename",
                (path if path else os.path.expanduser("~")),
                " ".join(filt)
            ]
        if multiple:
            cmdline += ["--multiple", "--separate-output"]
        if title:
            cmdline += ["--title", self.title]

        return cmdline


    def _gen_cmdline_yad(self, mode: str, path: str, filters: list, title: str, show_hidden: bool = False, multiple: bool = False, preview: bool = False):
        self.executable = "yad"
        self.separator = "|?|"
        self.successretcode = 0

        cmdline = [
            which(self.executable),
            '--file-selection',
            '--confirm-overwrite',
            '--geometry',
            '800x600+150+150'
        ]

        if multiple:
            cmdline += ['--multiple', '--separator', self.separator]
        if mode == 'save':
            cmdline += ['--save']
        elif mode == 'dir':
            cmdline += ['--directory']
        if preview:
            cmdline += ['--add-preview']
        if path:
            cmdline += ['--filename', path]
        if title:
            cmdline += ['--name', title]
        for f in filters:
            if type(f) == str:
                cmdline += ['--file-filter', f]
            else:
                cmdline += [
                    '--file-filter',
                    '{name} | {flt}'.format(name=f[0], flt=' '.join(f[1:]))
                ]

        return cmdline
