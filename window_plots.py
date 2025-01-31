import types
from functools import partial

from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox, QWidget, QComboBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from plotter import Plotter
import copy

plot_functions = [x for x in Plotter.__dict__.items() if isinstance(x[1], types.FunctionType) and x[0] != '__init__']
number_of_plots = len(plot_functions)
top_number = None
max_number = None
nationality = "All"
label_top_number_static_text = "Currently showing: {0} lines from nationality: {1}"


class WindowPlots(QWidget):
    def __init__(self, plotter_arg, parent=None):
        super(QWidget, self).__init__(parent)
        self.plotter_all = plotter_arg
        global max_number
        max_number = plotter_arg.df.shape[0]
        self.button_width = 170
        self.button_height = 32
        self.button_distances = 40
        self.canvas = None
        self.textbox_enter_top_number = QLineEdit(self)
        self.combo_box_nationalities = QComboBox(self)

        self.label_top_number = QLabel(self)

        self.my_ui()
        self.set_functions_buttons()
        self.set_change_top_number_button()
        self.set_combo_box_nationalities()

    def my_ui(self):
        self.canvas = Canvas(self, plotter_all=self.plotter_all)
        self.canvas.move(0, 0)

    def set_functions_buttons(self):
        buttons = [None] * number_of_plots
        for i in range(number_of_plots):
            buttons[i] = QPushButton(" ".join(plot_functions[i][0].split('_')), self)
            buttons[i].resize(self.button_width, self.button_height)
            buttons[i].move(1210, 10 + self.button_distances * i)
            buttons[i].clicked.connect(partial(self.on_function_button_click, plot_functions[i][1]))

    def set_change_top_number_button(self):
        self.textbox_enter_top_number.resize(self.button_width, self.button_height)
        self.textbox_enter_top_number.move(1210, 10 + self.button_distances * (number_of_plots + 1))
        self.textbox_enter_top_number.setPlaceholderText("Enter top number")

        button_change_top_number = QPushButton('Change top number', self)
        button_change_top_number.resize(self.button_width, self.button_height)
        button_change_top_number.move(1210, 10 + self.button_distances * (number_of_plots + 2))
        button_change_top_number.clicked.connect(self.on_change_top_number_click)

        button_show_all = QPushButton('Show all', self)
        button_show_all.resize(self.button_width, self.button_height)
        button_show_all.move(1210, 10 + self.button_distances * (number_of_plots + 3))
        button_show_all.clicked.connect(self.set_all)

        self.label_top_number.move(1210, 10 + self.button_distances * (number_of_plots + 4))
        self.label_top_number.resize(self.button_width * 2, self.button_height)
        self.set_label_text()

    def set_label_text(self):
        self.label_top_number.setText(label_top_number_static_text.format(self.canvas.get_df_size(), nationality))

    def set_all(self):
        if max_number:
            global top_number
            top_number = max_number
            self.canvas.update_plot(self.canvas.fun)
            self.set_label_text()

    def set_combo_box_nationalities(self):
        self.combo_box_nationalities.resize(self.button_width, self.button_height)
        self.combo_box_nationalities.move(1210 + self.button_width + 10,
                                          10 + self.button_distances * (number_of_plots + 1))
        nationalities = self.plotter_all.df['Nationality']
        nationalities_distinct = set(nationalities)
        nationalities_list = list(nationalities_distinct)
        nationalities_list.sort()
        self.combo_box_nationalities.addItem("All")
        self.combo_box_nationalities.addItems(nationalities_list)
        self.combo_box_nationalities.activated[str].connect(self.on_combo_box_nationalities_click)

    def on_combo_box_nationalities_click(self, nationality_arg):
        global nationality
        nationality = nationality_arg
        self.canvas.update_plot()
        self.set_label_text()

    def on_function_button_click(self, fun):
        self.canvas.update_plot(fun)
        self.set_label_text()

    def on_change_top_number_click(self):
        global top_number
        entered_text = self.textbox_enter_top_number.text()
        try:
            new_number = int(entered_text)
            if new_number > 0:
                top_number = new_number
        except ValueError:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText('Cannot parse argument: ' + entered_text)
            msg_box.setWindowTitle('Error')
            msg_box.exec()
        finally:
            self.textbox_enter_top_number.setText("")

        self.canvas.update_plot(self.canvas.fun)
        self.set_label_text()


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=12, height=8.7, dpi=100, plotter_all=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plotter_all = plotter_all
        self.modified_plotter = copy.copy(self.plotter_all)
        self.fun = plot_functions[0][1]
        self.update_plot(self.fun)

    def update_plot(self, fun=None):
        self.figure.clear()
        axes = self.figure.add_subplot(111)

        if fun is not None:
            self.fun = fun

        if nationality != "All":
            self.modified_plotter.df = copy.copy(
                self.plotter_all.df[self.plotter_all.df['Nationality'].str.match(nationality)])
        else:
            self.modified_plotter = copy.copy(self.plotter_all)

        if top_number is not None:
            self.modified_plotter.df = copy.copy(self.modified_plotter.df.head(top_number))

        self.fun(self.modified_plotter, ax=axes)

        self.figure.add_axes(axes)
        self.figure.tight_layout()
        self.draw()

    def get_df_size(self):
        return self.modified_plotter.df.shape[0]
