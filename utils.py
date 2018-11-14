import tkinter
import tkinter.filedialog
import data_handle


def center_root(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    return size


def right_root(root, width, height, parent_width):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2 + parent_width / 2, (screenheight - height) / 2)
    return size


def select_import_path(import_path):
    path = tkinter.filedialog.askopenfilename()
    import_path.set(path)
    return path


def calc(select, ety_import):
    custom_name = select.get()
    path = ety_import.get()
    data_handle.excel_handle(path, custom_name)