# File Class

## Description

The `File` class is meant to be able to handle files quickly and easily through functions in python. Current functionalities include:

- Checking if a file or folder exists
- Get the home directory path
- Rename file or folder
- Append string to filename
- Create folder
- Create file
- Get file extension
    - Separate extension from filename
    - Check if extension is the same as a given string
    - Retrieve only the filename from a path (filename + extension)
- Count the number of files in folder
- Delete file or folder

----------------------------

## Class Methods

### `path_exists()`

**Description:** Checking if a file or folder exists

**Inputs:**

- `input_path` (`str`): File path
- `with_error` (`bool`): Print error to console if file path does not exist (Default = `False`)

**Returns:** Boolean value to indicate if the path exists or not

### `home_dir()`

**Description:** Return the path of the home directory

**Inputs:** (None)

**Returns:** String with the home directory path

### `separate_extension()`

**Description:** Separate the file extension from the filename.

**Input:**

- `input_path` (`str`): Input path

**Returns:** Tuple containing the filename in first position and the extension in second position.

### `rename()`

**Description:** Rename path.

**Inputs:**

- `input_path` (`str`): Current path
- `new_name` (`str`): New name to give to `input_path`

**Returns:** (None)

### `append_to_filename()`

**Description:** Append string to filename.

**Inputs:**

- `input_path` (`str`): Current path
- `append_string` (`str`): String to append to filename

**Returns:** (None)

### `create_dir()`

**Description:** Create new directory at a given path.

**Inputs:**

- `dir_name` (`str`): Full directory path (or relative from where the python script is run from)

**Returns:** (None)

### `create_file()`

**Description:** Create new file at a given path.

**Inputs:**

- `filename` (`str`): Full file path (or relative from where the python script is run from)

**Returns:** (None)

### `get_file_extension()`

**Description:** Get filename extension.

**Inputs:**

- `input_path` (`str`): Input path of file

**Returns:** String containing file extension

### `count_files()`

**Description:** Count the number of files in folder.

**Inputs:**

- `input_path` (`str`): Path where to count files

**Returns:** Integer equal to the number of files in folder path

### `remove()`

**Description:** Delete file of folder

**Inputs:**

- `input_path` (`str`): Path of file/folder to delete

**Returns:** (None)

### `only_filename()`

**Description:** Return filename without parent path.

**Inputs:**

- `input_path` (`str`): Full input path
- `with_extension` (`bool`): Return filename with extension (Default: `True`)

**Returns:** String with desired filename.
