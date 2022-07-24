from general_util.file_chooser import FileDialog

file_dialog = FileDialog()

files = file_dialog.save_file()
print(files)