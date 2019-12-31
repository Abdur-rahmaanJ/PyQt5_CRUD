import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from models import Product
from base import Session, engine, Base
from utils import app_path, layout_addWidget


Base.metadata.create_all(engine)
session = Session()


class AddProduct(QtWidgets.QWidget):

    def __init__(self, view_product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_product = view_product
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.barcode_label = QtWidgets.QLabel('Enter barcode')
        self.barcode_entry = QtWidgets.QLineEdit()
        self.name_label = QtWidgets.QLabel('Enter Name')
        self.name_entry = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton('Add')


        self.button.clicked.connect(self.button_clicked)

        layout_addWidget(self.layout, [
            self.barcode_label, 
            self.barcode_entry, 
            self.name_label, 
            self.name_entry,
            self.button
            ])

        self.setLayout(self.layout)

    def clear_textboxes(self):
        self.barcode_entry.setText('')
        self.name_entry.setText('')

    def button_clicked(self):
        product = Product(
            barcode=self.barcode_entry.text(), 
            name=self.name_entry.text())
        session.add(product)
        session.commit()

        self.view_product.display_products()
        self.clear_textboxes()


class EditProduct(QtWidgets.QWidget):

    def __init__(self, view_product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_product = view_product
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.old_barcode_label = QtWidgets.QLabel('Enter old barcode')
        self.old_barcode_entry = QtWidgets.QLineEdit()
        self.new_barcode_label = QtWidgets.QLabel('Enter new barcode')
        self.new_barcode_entry = QtWidgets.QLineEdit()
        self.name_label = QtWidgets.QLabel('Enter Name')
        self.name_entry = QtWidgets.QLineEdit()
        self.load_button = QtWidgets.QPushButton('Load')
        self.edit_button = QtWidgets.QPushButton('Edit')

        self.load_button.clicked.connect(self.load_button_clicked)
        self.edit_button.clicked.connect(self.edit_button_clicked)
        
        layout_addWidget(self.layout, [
            self.old_barcode_label, 
            self.old_barcode_entry, 
            self.new_barcode_label, 
            self.new_barcode_entry,
            self.name_label, 
            self.name_entry,
            self.load_button,
            self.edit_button
            ])

        self.setLayout(self.layout)

    def clear_textboxes(self):
        self.old_barcode_entry.setText('')
        self.new_barcode_entry.setText('')
        self.name_entry.setText('')

    def load_button_clicked(self):
        check_barcode = self.old_barcode_entry.text()
        record = session.query(Product).filter(Product.barcode == check_barcode).first()
        self.new_barcode_entry.setText(check_barcode)
        self.name_entry.setText(record.name)

    def edit_button_clicked(self):
        check_barcode = self.old_barcode_entry.text()
        record = session.query(Product).filter(Product.barcode == check_barcode).first()
        
        record.barcode = self.new_barcode_entry.text()
        record.name = self.name_entry.text()

        self.view_product.display_products()
        self.clear_textboxes()


class DeleteProduct(QtWidgets.QWidget):

    def __init__(self, view_product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_product = view_product
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.barcode_label = QtWidgets.QLabel('Enter barcode')
        self.barcode_entry = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton('Delete')

        self.button.clicked.connect(self.button_clicked)

        layout_addWidget(self.layout, [
            self.barcode_label, 
            self.barcode_entry,
            self.button
            ])

        self.setLayout(self.layout)

    def clear_textboxes(self):
        self.barcode_entry.setText('')

    def button_clicked(self):
        check_barcode = self.barcode_entry.text()
        session.query(Product).filter(Product.barcode == check_barcode).delete()
        self.clear_textboxes()
        self.view_product.display_products()


class ViewProduct(QtWidgets.QWidget):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignTop)
        

        self.data_area = QtWidgets.QWidget()
        self.data_area_layout = QtWidgets.QVBoxLayout(self.data_area)
        self.data_area_layout.setAlignment(QtCore.Qt.AlignTop)
        self.display_products()

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.data_area)
        self.scroll_area.setWidgetResizable(True)

        layout.addWidget(self.scroll_area)

    def clear_area(self):
        for i in reversed(range(self.data_area_layout.count())): 
            self.data_area_layout.itemAt(i).widget().setParent(None)

    def display_products(self):
        self.clear_area()
        products = session.query(Product).all()

        record_string = '''
        <table>
            <tr>
                <th>id</th>
                <th>barcode</th>
                <th>name</th>
            </tr>
        '''
        self.data_area_layout.addWidget(QtWidgets.QLabel('PRODUCTS'))

        for product in products:
            record_string += '''
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            '''.format(product.id, product.barcode, product.name)
        record_string += '''
        </table>'''
        self.data_area_layout.addWidget(QtWidgets.QLabel(record_string))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        # win initialisations
        self.layout = QtWidgets.QGridLayout()
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
        self.setWindowTitle('Products')
        self.setWindowIcon(QtGui.QIcon(app_path('pics/icon.png'))) 

        self.view_product_widget = ViewProduct()
        self.add_product_widget = AddProduct(self.view_product_widget)
        self.edit_product_widget = EditProduct(self.view_product_widget)
        self.delete_product_widget = DeleteProduct(self.view_product_widget)

        layout_addWidget(self.layout, [
            (self.add_product_widget, 0, 0),
            (self.edit_product_widget, 0, 1),
            (self.delete_product_widget, 0, 2),
            (self.view_product_widget, 0, 3),
            ])



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())

