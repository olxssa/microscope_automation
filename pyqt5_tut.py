# PyQt5 tutorial
# codemy.com PyQT5 GUI Thursdays

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # title
        self.setWindowTitle('Microscope Automation')

        # geometry
        self.setGeometry(0, 0, 1500, 1000)

        # layout
        self.setLayout(qtw.QHBoxLayout())

        # label
        label = qtw.QLabel('Hello! What`s your name?')
        # change font size of label
        label.setFont(qtg.QFont('SansSerif', 10))
        self.layout().addWidget(label)

        # create entry box
        entry = qtw.QLineEdit()
        entry.setObjectName('name_field')
        entry.setText('')
        self.layout().addWidget(entry)

        # combo box
        combo = qtw.QComboBox(self)
        combo.addItem('A', 2)
        combo.addItem('B', 3)
        self.layout().addWidget(combo)

        # spin box (for integers), double spin box (for floats)
        spin = qtw.QDoubleSpinBox(self,
                                  value = 10,
                                  maximum = 100,
                                  minimum = 0,
                                  singleStep = 5,
                                  prefix = '#',
                                  suffix = ' Order')
        self.layout().addWidget(spin)


        # create a button
        button = qtw.QPushButton('Press me!', clicked = lambda: press_it())
        self.layout().addWidget(button)

        button2 = qtw.QPushButton('Press me!', clicked=lambda: press_it2())
        self.layout().addWidget(button2)

        button_spin = qtw.QPushButton('Press me!', clicked=lambda: press_it_spin())
        self.layout().addWidget(button_spin)

        # show the app
        self.show()

        def press_it():
            label.setText(f'Hello {entry.text()}!')
            entry.setText('')
        def press_it2():
            label.setText(f'You picked {combo.currentData()}!') # Text, Data, Index
        def press_it_spin():
            label.setText(f'You picked #{spin.value()} Order!')


app = qtw.QApplication([])
mw = MainWindow()

app.exec_()