import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QComboBox, QPushButton, QFileDialog, QLineEdit,
                               QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

#### Step 4.2 import my model
from models.my_analysis import MyModel
#### ENd Step 4.2 import my model

# Step1. Define MyMainWindow
class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        #### Step 4.2 Set My Model 
        self.my_model = MyModel()
        #### End Step 4.2 Set My Model 

        ## Step 2 Main Layout ---------------------------------------
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        ## End Step 2 Main Layout -------------------------------------------

        ## Step 2.CSV File Selector ----------------------------------
        self.file_widget = QWidget()
        self.file_layout = QHBoxLayout(self.file_widget)

        self.file_line = QLineEdit()
        self.file_line.setPlaceholderText("파일을 선택해주세요.")
        self.file_line.setReadOnly(True)
        self.file_layout.addWidget(self.file_line)

        self.open_button = QPushButton("Open File", self)
        self.file_layout.addWidget(self.open_button)

        self.layout.addWidget(self.file_widget)
        ## End Step 2.CSV File Selector ------------------------------

        ## Step 2.Combo Box ----------------------------------------
        self.combo_box1 = QComboBox(self)
        self.combo_box2 = QComboBox(self)
        self.layout.addWidget(self.combo_box1)
        self.layout.addWidget(self.combo_box2)
        self.combo_box1.setPlaceholderText("로드된 데이터가 없습니다.")
        self.combo_box2.setPlaceholderText("로드된 데이터가 없습니다.")
        ## End Step 2. Combo Box -----------------------------------------

        ## Step2.Draw Plot -----------------------------------------
        self.canvas = FigureCanvas(Figure())
        self.layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot(111)
        ## End Draw Plot ----------------------------------------

        ## Step 2. My Analysis Model ---------------------------------
        self.my_model_label = QLabel("분석 결과(상관관계)")
        self.my_model_line = QLineEdit()
        self.layout.addWidget(self.my_model_label)
        self.layout.addWidget(self.my_model_line)
        ## End Step 2. My Analysis --------------------------------

        ### Step 3. Connect File Open Event ------------------
        self.open_button.clicked.connect(self.open_file)
        ### End Step 3. Connect File Open Event   --------------

        ###### 6.4 Combo Box Connect Event --------------------------------------
        self.combo_box1.currentIndexChanged.connect(self.update_board)
        self.combo_box2.currentIndexChanged.connect(self.update_board)
        # End 6.4 Combo Box Connect Event --------------------------------

    ### Step 3. Open File Dialog -----------------
    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")

        if file_dialog.exec():
            selected_csv_file = file_dialog.selectedFiles()[0]
            self.file_line.setText(selected_csv_file)
    ### Hoding Step 3  
            #### 4.2 Call read_data
            self.read_data(selected_csv_file)   
            ##### 5. Call set_columns
            self.set_columns()
    ### End Step 3. 3Open File Dialog --------------

    #### Step 4.2 Read Data --------------------------
    def read_data(self, selected_csv_file):
        if selected_csv_file != "":
            self.my_model.set_data(data=pd.read_csv(selected_csv_file))
    #### End Step 4.2 Read Data ----------------------

    ##### Step 5. Set columns from data -------------
    def set_columns(self):
        if self.my_model.data is not None :
            self.combo_box1.clear()
            self.combo_box1.setPlaceholderText("컬럼을 선택해주세요.")
            self.combo_box1.addItems(self.my_model.data.columns)

            self.combo_box2.clear()
            self.combo_box2.setPlaceholderText("컬럼을 선택해주세요.")
            self.combo_box2.addItems(self.my_model.data.columns)
    ##### End Step 5 Set columns --------------------

    ###### Step 6.1 Draw Canvas ------------------
    def draw_plot(self, selected_column1:str, selected_column2:str):
        self.ax.clear() 
        self.ax.scatter(self.my_model.data[selected_column1], self.my_model.data[selected_column2])
        self.ax.set_xlabel(selected_column1)
        self.ax.set_ylabel(selected_column2)
        self.ax.set_title(f'Scatter Plot: {selected_column1} vs {selected_column2}')
        self.canvas.draw()
    ###### End 6.1 Draw Canvas --------------
        
    ###### 6.2 My models calc corr -----------
    def my_analysis(self, selected_column1:str, selected_column2:str) :
        corr_result = self.my_model.calc_corr(ca1=selected_column1, ca2=selected_column2)
        self.my_model_line.setText(f"{corr_result:.2f}")
    ###### End Step 6.2 My models ------------
        
    ###### 6.3 Data select board ----------
    def update_board(self):
        selected_column1 = self.combo_box1.currentText()
        selected_column2 = self.combo_box2.currentText()
        if selected_column1 and selected_column2 :
            self.draw_plot(selected_column1, selected_column2)
            self.my_analysis(selected_column1, selected_column2)
    ###### End 6.3 Data select board -----------
        

# Step1. Define main
def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())

# Step1. Main
if __name__ == '__main__':
    main()

