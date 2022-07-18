import os

class FileLoop:
    def __init__(self, folder: str = '.', file_type = None) -> None:
        self.folder = folder
        self.file_type = file_type
        self.file = None

    def start(self, function, *args, **kwargs):

        self.function = function
        self.args = args
        self.kwargs = kwargs

        for root, _, files in os.walk(self.folder):
            for file in files:
                # Only handle files of certain type
                if self.file_type == '' or self.file_type is None:
                    self.file = os.path.join(root, file)
                else:
                    if file.endswith(self.file_type):
                        self.file = os.path.join(root, file)

                # Perform function
                self.function(*self.args, **self.kwargs)
