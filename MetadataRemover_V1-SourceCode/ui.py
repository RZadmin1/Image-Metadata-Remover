from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class MetadataRemoverUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Metadata Remover")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select Input and Output Folders")
        layout.addWidget(self.label)

        self.input_btn = QPushButton("Select Input Folder")
        self.input_btn.clicked.connect(self.select_input_folder)
        layout.addWidget(self.input_btn)

        self.output_btn = QPushButton("Select Output Folder")
        self.output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_btn)

        self.run_btn = QPushButton("Remove Metadata")
        self.run_btn.clicked.connect(self.remove_metadata)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.controller.set_input_folder(folder)
            self.label.setText(f"Input Folder: {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.controller.set_output_folder(folder)
            self.label.setText(f"Output Folder: {folder}")

    def remove_metadata(self):
        status = self.controller.run_metadata_removal()
        self.label.setText(status)