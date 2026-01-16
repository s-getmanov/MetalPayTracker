from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QTableWidget, QTableWidgetItem,
                            QPushButton, QLabel, QLineEdit, QTextEdit,
                            QComboBox, QSpinBox, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle("АО «Лискимонтажконструкция» - Система заявок")
        self.setGeometry(100, 100, 900, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Вкладка заявок
        self.order_tab = QWidget()
        self.tabs.addTab(self.order_tab, "Новая заявка")
        self.setup_order_tab()
        
        # Вкладка менеджеров
        self.managers_tab = QWidget()
        self.tabs.addTab(self.managers_tab, "Менеджеры")
        self.setup_managers_tab()
        
        # Вкладка клиентов
        self.clients_tab = QWidget()
        self.tabs.addTab(self.clients_tab, "Клиенты")
        self.setup_clients_tab()
        
        # Вкладка номенклатуры
        self.nomenclature_tab = QWidget()
        self.tabs.addTab(self.nomenclature_tab, "Номенклатура")
        self.setup_nomenclature_tab()
        
        # Вкладка отчетов
        self.reports_tab = QWidget()
        self.tabs.addTab(self.reports_tab, "Отчеты")
        self.setup_reports_tab()
        
        # Кнопка экспорта
        export_btn = QPushButton("Экспорт заявок в XML")
        export_btn.clicked.connect(self.export_to_xml)
        main_layout.addWidget(export_btn)
    
    def setup_order_tab(self):
        layout = QVBoxLayout(self.order_tab)
        
        # Выбор менеджера
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Менеджер:"))
        self.manager_combo = QComboBox()
        hbox1.addWidget(self.manager_combo)
        layout.addLayout(hbox1)
        
        # Выбор клиента
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Клиент:"))
        self.client_combo = QComboBox()
        hbox2.addWidget(self.client_combo)
        layout.addLayout(hbox2)
        
        # Таблица позиций заявки
        layout.addWidget(QLabel("Позиции заявки:"))
        self.order_items_table = QTableWidget(0, 3)
        self.order_items_table.setHorizontalHeaderLabels(["Номенклатура", "Количество", "Действие"])
        layout.addWidget(self.order_items_table)
        
        # Добавление позиции
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("Номенклатура:"))
        self.nomenclature_combo = QComboBox()
        hbox3.addWidget(self.nomenclature_combo)
        hbox3.addWidget(QLabel("Количество:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(1000)
        hbox3.addWidget(self.quantity_spin)
        add_item_btn = QPushButton("Добавить позицию")
        add_item_btn.clicked.connect(self.add_order_item)
        hbox3.addWidget(add_item_btn)
        layout.addLayout(hbox3)
        
        # Кнопка создания заявки
        create_order_btn = QPushButton("Создать заявку")
        create_order_btn.clicked.connect(self.create_order)
        layout.addWidget(create_order_btn)
    
    def setup_managers_tab(self):
        layout = QVBoxLayout(self.managers_tab)
        
        # Форма добавления менеджера
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Добавить менеджера:"))
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("ФИО:"))
        self.manager_name_input = QLineEdit()
        hbox1.addWidget(self.manager_name_input)
        form_layout.addLayout(hbox1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Код 1С:"))
        self.manager_code_input = QLineEdit()
        hbox2.addWidget(self.manager_code_input)
        form_layout.addLayout(hbox2)
        
        add_manager_btn = QPushButton("Добавить")
        add_manager_btn.clicked.connect(self.add_manager)
        form_layout.addWidget(add_manager_btn)
        
        layout.addLayout(form_layout)
        
        # Таблица менеджеров
        self.managers_table = QTableWidget()
        self.managers_table.setColumnCount(3)
        self.managers_table.setHorizontalHeaderLabels(["ID", "ФИО", "Код 1С"])
        layout.addWidget(self.managers_table)
    
    def setup_clients_tab(self):
        layout = QVBoxLayout(self.clients_tab)
        
        # Форма добавления клиента
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Добавить клиента:"))
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Название:"))
        self.client_name_input = QLineEdit()
        hbox1.addWidget(self.client_name_input)
        form_layout.addLayout(hbox1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Телефон:"))
        self.client_phone_input = QLineEdit()
        hbox2.addWidget(self.client_phone_input)
        form_layout.addLayout(hbox2)
        
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("Email:"))
        self.client_email_input = QLineEdit()
        hbox3.addWidget(self.client_email_input)
        form_layout.addLayout(hbox3)
        
        hbox4 = QHBoxLayout()
        hbox4.addWidget(QLabel("Код 1С:"))
        self.client_code_input = QLineEdit()
        hbox4.addWidget(self.client_code_input)
        form_layout.addLayout(hbox4)
        
        add_client_btn = QPushButton("Добавить")
        add_client_btn.clicked.connect(self.add_client)
        form_layout.addWidget(add_client_btn)
        
        layout.addLayout(form_layout)
        
        # Таблица клиентов
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels(["ID", "Название", "Телефон", "Email", "Код 1С"])
        layout.addWidget(self.clients_table)
    
    def setup_nomenclature_tab(self):
        layout = QVBoxLayout(self.nomenclature_tab)
        
        # Форма добавления номенклатуры
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Добавить номенклатуру:"))
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Наименование:"))
        self.nom_name_input = QLineEdit()
        hbox1.addWidget(self.nom_name_input)
        form_layout.addLayout(hbox1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Описание:"))
        self.nom_desc_input = QTextEdit()
        self.nom_desc_input.setMaximumHeight(60)
        hbox2.addWidget(self.nom_desc_input)
        form_layout.addLayout(hbox2)
        
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("Ед. измерения:"))
        self.nom_unit_input = QLineEdit()
        hbox3.addWidget(self.nom_unit_input)
        form_layout.addLayout(hbox3)
        
        hbox4 = QHBoxLayout()
        hbox4.addWidget(QLabel("Код 1С:"))
        self.nom_code_input = QLineEdit()
        hbox4.addWidget(self.nom_code_input)
        form_layout.addLayout(hbox4)
        
        add_nom_btn = QPushButton("Добавить")
        add_nom_btn.clicked.connect(self.add_nomenclature)
        form_layout.addWidget(add_nom_btn)
        
        layout.addLayout(form_layout)
        
        # Таблица номенклатуры
        self.nomenclature_table = QTableWidget()
        self.nomenclature_table.setColumnCount(5)
        self.nomenclature_table.setHorizontalHeaderLabels(["ID", "Наименование", "Описание", "Ед. изм.", "Код 1С"])
        layout.addWidget(self.nomenclature_table)
    
    def setup_reports_tab(self):
        layout = QVBoxLayout(self.reports_tab)
        
        # Панель управления отчетом
        report_controls = QHBoxLayout()
        
        # Выбор менеджера для отчета
        report_controls.addWidget(QLabel("Менеджер:"))
        self.report_manager_combo = QComboBox()
        self.report_manager_combo.currentIndexChanged.connect(self.load_manager_report)
        report_controls.addWidget(self.report_manager_combo)
        
        # Кнопка обновления отчета
        self.refresh_report_btn = QPushButton("Обновить")
        self.refresh_report_btn.clicked.connect(self.load_manager_report)
        report_controls.addWidget(self.refresh_report_btn)
        
        # Добавляем панель в основной layout
        layout.addLayout(report_controls)
        
        # Таблица отчетов
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(["ID заявки", "Дата", "Клиент", "Кол-во позиций"])
        layout.addWidget(self.report_table)
    
    def load_data(self):
        # Загрузка менеджеров
        self.manager_combo.clear()
        self.report_manager_combo.clear()
        managers = self.db.get_managers()
        self.managers_table.setRowCount(len(managers))
        for i, (id, name, code_1c) in enumerate(managers):
            self.manager_combo.addItem(f"{name} ({code_1c})", id)
            self.report_manager_combo.addItem(f"{name} ({code_1c})", id)
            self.managers_table.setItem(i, 0, QTableWidgetItem(str(id)))
            self.managers_table.setItem(i, 1, QTableWidgetItem(name))
            self.managers_table.setItem(i, 2, QTableWidgetItem(code_1c))
        
        # Загрузка клиентов
        self.client_combo.clear()
        clients = self.db.get_clients()
        self.clients_table.setRowCount(len(clients))
        for i, (id, name, phone, email, code_1c) in enumerate(clients):
            self.client_combo.addItem(f"{name} ({code_1c})", id)
            self.clients_table.setItem(i, 0, QTableWidgetItem(str(id)))
            self.clients_table.setItem(i, 1, QTableWidgetItem(name))
            self.clients_table.setItem(i, 2, QTableWidgetItem(phone))
            self.clients_table.setItem(i, 3, QTableWidgetItem(email))
            self.clients_table.setItem(i, 4, QTableWidgetItem(code_1c))
        
        # Загрузка номенклатуры
        self.nomenclature_combo.clear()
        nomenclature = self.db.get_nomenclature()
        self.nomenclature_table.setRowCount(len(nomenclature))
        for i, (id, name, description, unit, code_1c) in enumerate(nomenclature):
            self.nomenclature_combo.addItem(f"{name} ({code_1c})", id)
            self.nomenclature_table.setItem(i, 0, QTableWidgetItem(str(id)))
            self.nomenclature_table.setItem(i, 1, QTableWidgetItem(name))
            self.nomenclature_table.setItem(i, 2, QTableWidgetItem(description))
            self.nomenclature_table.setItem(i, 3, QTableWidgetItem(unit))
            self.nomenclature_table.setItem(i, 4, QTableWidgetItem(code_1c))
        
        self.order_items = []
        self.update_order_items_table()
    
    def add_manager(self):
        name = self.manager_name_input.text()
        code = self.manager_code_input.text()
        
        if not name or not code:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        try:
            self.db.add_manager(name, code)
            self.load_data()
            self.manager_name_input.clear()
            self.manager_code_input.clear()
            QMessageBox.information(self, "Менеджер", "Менеджер добавлен")
        except Exception as e:
            QMessageBox.critical(self, "Менеджер", f"Ошибка добавления: {str(e)}")
    
    def add_client(self):
        name = self.client_name_input.text()
        phone = self.client_phone_input.text()
        email = self.client_email_input.text()
        code = self.client_code_input.text()
        
        if not name or not code:
            QMessageBox.warning(self, "Ошибка", "Заполните название и код 1С")
            return
        
        try:
            self.db.add_client(name, phone, email, code)
            self.load_data()
            self.client_name_input.clear()
            self.client_phone_input.clear()
            self.client_email_input.clear()
            self.client_code_input.clear()
            QMessageBox.information(self, "Клиент", "Клиент добавлен")
        except Exception as e:
            QMessageBox.critical(self, "Клиент", f"Ошибка добавления: {str(e)}")
    
    def add_nomenclature(self):
        name = self.nom_name_input.text()
        description = self.nom_desc_input.toPlainText()
        unit = self.nom_unit_input.text()
        code = self.nom_code_input.text()
        
        if not name or not code:
            QMessageBox.warning(self, "Ошибка", "Заполните наименование и код 1С")
            return
        
        try:
            self.db.add_nomenclature(name, description, unit, code)
            self.load_data()
            self.nom_name_input.clear()
            self.nom_desc_input.clear()
            self.nom_unit_input.clear()
            self.nom_code_input.clear()
            QMessageBox.information(self, "Добавление номенклатуры", "Номенклатура добавлена")
        except Exception as e:
            QMessageBox.critical(self, "Добавление номенклатуры", f"Ошибка добавления: {str(e)}")
    
    def add_order_item(self):
        nom_id = self.nomenclature_combo.currentData()
        quantity = self.quantity_spin.value()
        
        if not nom_id:
            QMessageBox.warning(self, "Номенклатура", "Выберите номенклатуру")
            return
        
        self.order_items.append({
            'nomenclature_id': nom_id,
            'name': self.nomenclature_combo.currentText(),
            'quantity': quantity
        })
        
        self.update_order_items_table()
        self.quantity_spin.setValue(1)
    
    def update_order_items_table(self):
        self.order_items_table.setRowCount(len(self.order_items))
        for i, item in enumerate(self.order_items):
            self.order_items_table.setItem(i, 0, QTableWidgetItem(item['name']))
            self.order_items_table.setItem(i, 1, QTableWidgetItem(str(item['quantity'])))
            
            remove_btn = QPushButton("Удалить")
            remove_btn.clicked.connect(lambda checked, idx=i: self.remove_order_item(idx))
            self.order_items_table.setCellWidget(i, 2, remove_btn)
    
    def remove_order_item(self, index):
        self.order_items.pop(index)
        self.update_order_items_table()
    
    def create_order(self):
        manager_id = self.manager_combo.currentData()
        client_id = self.client_combo.currentData()
        
        if not manager_id or not client_id:
            QMessageBox.warning(self, "Менеджер", "Выберите менеджера и клиента")
            return
        
        if not self.order_items:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы одну позицию")
            return
        
        try:
            order_id = self.db.create_order(manager_id, client_id)
            
            for item in self.order_items:
                self.db.add_order_item(order_id, item['nomenclature_id'], item['quantity'])
            
            self.order_items = []
            self.update_order_items_table()
            #Ошибка - не обновляются отчеты
            #Добавлено - автообновление отчета //16.12.2025
            self.load_manager_report()
            
            QMessageBox.information(self, "Заявка", f"Заявка #{order_id} создана")
        except Exception as e:
            QMessageBox.critical(self, "Заявка", f"Ошибка создания заявки: {str(e)}")
    
    def load_manager_report(self):
        manager_id = self.report_manager_combo.currentData()
        if not manager_id:
            return
        
        orders = self.db.get_orders_by_manager(manager_id)
        self.report_table.setRowCount(len(orders))
        
        for i, (order_id, order_date, client_name, items_count) in enumerate(orders):
            self.report_table.setItem(i, 0, QTableWidgetItem(str(order_id)))
            self.report_table.setItem(i, 1, QTableWidgetItem(order_date))
            self.report_table.setItem(i, 2, QTableWidgetItem(client_name))
            self.report_table.setItem(i, 3, QTableWidgetItem(str(items_count)))
    
    def export_to_xml(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт заявок", "orders_export.xml", "XML Files (*.xml)"
        )
        
        if filename:
            try:
                exported_file = self.db.export_orders_to_xml(filename)
                QMessageBox.information(self, "Выгрузка файла обмена с 1С", f"Заявки экспортированы в {exported_file}")
            except Exception as e:
                QMessageBox.critical(self, "Выгрузка файла обмена с 1С", f"Ошибка экспорта: {str(e)}")