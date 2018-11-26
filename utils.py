from tkinter.filedialog import askopenfilename


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
    # path = askopenfilename(defaultextension='xlsx',  filetypes=[('excel', 'xlsx')])
    path = askopenfilename(defaultextension='xlsx')
    import_path.set(path)
    return path
