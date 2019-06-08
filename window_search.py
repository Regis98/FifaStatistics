import pandas as pd

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QComboBox
from PyQt5.QtWidgets import QApplication, QTableView

from pandas_model import PandasModel
import copy


class WindowSearch(QWidget):
    def __init__(self, parent, df):
        QWidget.__init__(self, parent=None)

        self.df = copy.copy(self.prepare_df(df))

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        self.search_textbox = QLineEdit(self)
        self.search_textbox.setPlaceholderText("Enter searched name")
        h_layout.addWidget(self.search_textbox)

        self.search_min_age = QLineEdit(self)
        self.search_min_age.setPlaceholderText("Min Age")
        h_layout.addWidget(self.search_min_age)

        self.search_max_age = QLineEdit(self)
        self.search_max_age.setPlaceholderText("Max Age")
        h_layout.addWidget(self.search_max_age)

        self.overall_min = QLineEdit(self)
        self.overall_min.setPlaceholderText("Minimal Overall")
        h_layout.addWidget(self.overall_min)

        self.overall_max = QLineEdit(self)
        self.overall_max.setPlaceholderText("Maximal Overall")
        h_layout.addWidget(self.overall_max)

        self.skill_moves_min = QLineEdit(self)
        self.skill_moves_min.setPlaceholderText("Minimall skill moves")
        h_layout.addWidget(self.skill_moves_min)

        self.skill_moves_max = QLineEdit(self)
        self.skill_moves_max.setPlaceholderText("Max skill moves")
        h_layout.addWidget(self.skill_moves_max)

        self.combo_box_position = QComboBox()
        positions = list(self.df['Position'].dropna().unique())
        self.combo_box_position.addItems(positions)
        h_layout.addWidget(self.combo_box_position)

        self.search_button = QPushButton("Search", self)
        h_layout.addWidget(self.search_button)

        v_layout.addLayout(h_layout)

        self.table = QTableView(self)
        v_layout.addWidget(self.table)

        self.setLayout(v_layout)

        self.model = PandasModel(self.df)
        self.table.setModel(self.model)

        self.search_button.clicked.connect(self.search_clicked)
        self.table.setSortingEnabled(True)

    def search_clicked(self):
        entered_text = self.search_textbox.text()
        print(entered_text)
        entered_position = self.combo_box_position.currentText()
        print(entered_position)
        min_age = float(self.search_min_age.text()) if self.search_min_age.text() != '' else 10
        print(min_age)
        max_age = float(self.search_max_age.text()) if self.search_max_age.text() != '' else 50
        print(max_age)
        min_overall = float(self.overall_min.text()) if self.overall_min.text() != '' else 20
        print(min_overall)
        max_overall = float(self.overall_max.text()) if self.overall_max.text() != '' else 100
        print(max_overall)
        min_skill_moves = float(self.skill_moves_min.text()) if self.skill_moves_min.text() != '' else 1.0
        print(min_skill_moves)
        max_skill_moves = float(self.skill_moves_max.text()) if self.skill_moves_max.text() != '' else 5.0
        print(max_skill_moves)

        result = self.df[
            (self.df['Name'].str.contains(entered_text, na=False)) &
            (self.df['Position'] == entered_position) &
            (self.df['Age'] <= max_age) & (self.df['Age'] >= min_age) &
            (self.df['Skill Moves'] <= max_skill_moves) & (self.df['Skill Moves'] >= min_skill_moves) &
            (self.df['Overall'] < max_overall) & (self.df['Overall'] > min_overall)
        ]

        self.model.update(result)

    @staticmethod
    def prepare_df(df):
        columns = ['Name', 'Age', 'Nationality', 'Overall', 'Club', 'Value',
                   'Wage', 'Skill Moves', 'Position', 'Height', 'Weight']

        return df[columns]

