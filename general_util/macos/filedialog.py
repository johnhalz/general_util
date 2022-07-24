from pyobjus import autoclass, objc_arr, objc_str
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework(INCLUDE.AppKit)
NSURL = autoclass('NSURL')
NSOpenPanel = autoclass('NSOpenPanel')
NSSavePanel = autoclass('NSSavePanel')
NSOKButton = 1


class MacFileChooser:
    '''A native implementation of file chooser dialogs using Apple's API through pyobjus.'''

    def __init__(self) -> None:
        pass

    def run(self, mode: str, path: str, filters: list, title: str, show_hidden: bool, multiple: bool = False, preview: bool = False):
        panel = None
        if mode in ('open', 'dir', 'dir_and_files'):
            panel = NSOpenPanel.openPanel()

            panel.setCanChooseDirectories_(mode != 'open')
            panel.setCanChooseFiles_(mode != 'dir')

            if multiple:
                panel.setAllowsMultipleSelection_(True)
        elif mode == 'save':
            panel = NSSavePanel.savePanel()
        else:
            assert False, mode

        panel.setCanCreateDirectories_(True)
        panel.setShowsHiddenFiles_(show_hidden)

        if title:
            panel.setTitle_(objc_str(title))

        # Mac OS X does not support wildcards unlike the other platforms.
        # This tries to convert wildcards to "extensions" when possible,
        # ans sets the panel to also allow other file types, just to be safe.
        if filters:
            filthies = []
            for f in filters:
                if type(f) == str:
                    f = (None, f)
                for s in f[1:]:
                    pystr = s.strip().split("*")[-1].split(".")[-1]
                    filthies.append(objc_str(pystr))

            ftypes_arr = objc_arr(*filthies)
            # TODO: switch to allowedContentTypes
            panel.setAllowedFileTypes_(ftypes_arr)
            panel.setAllowsOtherFileTypes_(False)

        if path:
            url = NSURL.fileURLWithPath_(path)
            panel.setDirectoryURL_(url)

        selection = None

        if panel.runModal():
            if mode == 'save' or not multiple:
                selection = [panel.filename().UTF8String()]
            else:
                filename = panel.filenames()
                selection = [
                    filename.objectAtIndex_(x).UTF8String()
                    for x in range(filename.count())]

        return selection
