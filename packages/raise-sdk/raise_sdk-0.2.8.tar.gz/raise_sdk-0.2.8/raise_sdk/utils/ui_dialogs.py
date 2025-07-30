import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QTreeView, QPushButton, QMessageBox


class FileDialog(QFileDialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)  # Allows file selection
        self.setViewMode(QFileDialog.List)    # Set view mode for better accessibility

        # Find and customize the "Open" button to capture selected items
        btns = self.findChildren(QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)

        # Access the file tree view to process selections
        self.tree = self.findChild(QTreeView)
        
        # Initialize empty lists for selected files and folders
        self.selectedFiles = []
        self.selectedFolders = []

    def openClicked(self):
        # Process selected files and folders from the tree view
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        folders = []
        for i in inds:
            if i.column() == 0:  # If the selection is on the first column (file/folder name)
                selected_path = os.path.join(str(self.directory().absolutePath()), str(i.data()))
                if os.path.isfile(selected_path):
                    files.append(selected_path)
                elif os.path.isdir(selected_path):
                    folders.append(selected_path)

        self.selectedFiles = files
        self.selectedFolders = folders
        
        self.hide()

    def filesSelected(self):
        # Return both selected files and folders
        # all_items = self.selectedFiles
        # for root, dirs, files in self.selectedFolders:
        #     all_items += [root + file for file in files]
        return self.selectedFiles + self.selectedFolders


def select_files(title="Select files", filetypes=[("All Files", "*.*")]):
    """
    Opens a file selection dialog and allows the user to select a multiple files.

    Args:
        title (str): The title of the file dialog window.
        filetypes (list): A list of tuples specifying the allowed file types.

    Returns:
        tuple: A tuple containing the paths of the selected files.
    """
    
    app     = QApplication([])  # Create an instance of the application
    options = QFileDialog.Options()
    # Handle the case where filetypes might be a list of a single tuple
    if len(filetypes) == 1 and isinstance(filetypes[0], tuple):
        file_filter = f"{filetypes[0][0]} ({filetypes[0][1]})"
    else:
        # Convert filetypes into the correct string format
        file_filter = ";;".join([f"{name} ({pattern})" for name, pattern in filetypes])
    # Open the file dialog
    file_paths, _ = QFileDialog.getOpenFileNames(None, title, "", file_filter, options=options)

    # Raise an error if no files were selected
    if not file_paths:
        raise FileNotFoundError(f"No files were selected.")

    return file_paths


def show_popup(title="", message=""):
    """
    Show a PyQt5 dialog box asking the user if they want to proceed without Docker.

    Returns:
        bool: True if the user clicks "Yes", False if they click "No".
    """
    app = QApplication([])  # Create a PyQt5 application instance
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    
    # Execute the dialog and return True for "Yes", False for "No"
    response = msg_box.exec_()
    return response == QMessageBox.Yes