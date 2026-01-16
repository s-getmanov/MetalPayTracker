import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="lmk_fintech.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.connection.cursor()
        
        # Таблица менеджеров
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS managers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code_1c TEXT UNIQUE
            )
        ''')
        
        # Таблица клиентов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                code_1c TEXT UNIQUE
            )
        ''')
        
        # Таблица номенклатуры
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nomenclature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                unit TEXT,
                code_1c TEXT UNIQUE
            )
        ''')
        
        # Таблица заявок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_date DATE NOT NULL,
                manager_id INTEGER,
                client_id INTEGER,
                FOREIGN KEY (manager_id) REFERENCES managers (id),
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')
        
        # Таблица позиций заявки (связь заявки и номенклатуры)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                nomenclature_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (nomenclature_id) REFERENCES nomenclature (id)
            )
        ''')
        
        self.connection.commit()
    
    def add_manager(self, name, code_1c):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO managers (name, code_1c) VALUES (?, ?)", 
                      (name, code_1c))
        self.connection.commit()
        return cursor.lastrowid
    
    def add_client(self, name, phone, email, code_1c):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO clients (name, phone, email, code_1c) VALUES (?, ?, ?, ?)", 
                      (name, phone, email, code_1c))
        self.connection.commit()
        return cursor.lastrowid
    
    def add_nomenclature(self, name, description, unit, code_1c):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO nomenclature (name, description, unit, code_1c) VALUES (?, ?, ?, ?)", 
                      (name, description, unit, code_1c))
        self.connection.commit()
        return cursor.lastrowid
    
    def create_order(self, manager_id, client_id):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO orders (order_date, manager_id, client_id) VALUES (?, ?, ?)", 
                      (datetime.now().strftime("%Y-%m-%d"), manager_id, client_id))
        self.connection.commit()
        return cursor.lastrowid
    
    def add_order_item(self, order_id, nomenclature_id, quantity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO order_items (order_id, nomenclature_id, quantity) VALUES (?, ?, ?)", 
                      (order_id, nomenclature_id, quantity))
        self.connection.commit()
    
    def get_managers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, code_1c FROM managers")
        return cursor.fetchall()
    
    def get_clients(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, phone, email, code_1c FROM clients")
        return cursor.fetchall()
    
    def get_nomenclature(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, description, unit, code_1c FROM nomenclature")
        return cursor.fetchall()
    
    def get_orders_by_manager(self, manager_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT o.id, o.order_date, c.name as client_name, 
                   COUNT(oi.id) as items_count
            FROM orders o
            JOIN clients c ON o.client_id = c.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE o.manager_id = ?
            GROUP BY o.id
        ''', (manager_id,))
        return cursor.fetchall()
    
    def get_order_items(self, order_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT n.name, oi.quantity, n.unit
            FROM order_items oi
            JOIN nomenclature n ON oi.nomenclature_id = n.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        return cursor.fetchall()
    
    def export_orders_to_xml(self, filename="orders_export.xml"):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT o.id, o.order_date, 
                m.id as manager_id, m.name as manager_name, m.code_1c as manager_code_1c,
                c.id as client_id, c.name as client_name, c.code_1c as client_code_1c,
                n.id as item_id, n.name as item_name, n.code_1c as item_code_1c,
                oi.quantity, n.unit
            FROM orders o
            JOIN managers m ON o.manager_id = m.id
            JOIN clients c ON o.client_id = c.id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN nomenclature n ON oi.nomenclature_id = n.id
            ORDER BY o.order_date DESC
        ''')
        
        import xml.etree.ElementTree as ET
        from datetime import datetime
        
        root = ET.Element("Orders")
        root.set("company", "АО «Лискимонтажконструкция»")
        root.set("exportDate", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        current_order_id = None
        order_elem = None
        
        for row in cursor.fetchall():
            if current_order_id != row[0]:
                order_elem = ET.SubElement(root, "Order")
                order_elem.set("id", str(row[0]))
                order_elem.set("date", row[1])
                
                # Менеджер с Code1C
                manager_elem = ET.SubElement(order_elem, "Manager")
                manager_elem.set("id", str(row[2]))
                manager_elem.set("code1c", row[4])
                name_elem = ET.SubElement(manager_elem, "Name")
                name_elem.text = row[3]
                
                # Клиент с Code1C
                client_elem = ET.SubElement(order_elem, "Client")
                client_elem.set("id", str(row[5]))
                client_elem.set("code1c", row[7])
                name_elem = ET.SubElement(client_elem, "Name")
                name_elem.text = row[6]
                
                items_elem = ET.SubElement(order_elem, "Items")
            
            # Позиция заявки с Code1C
            item_elem = ET.SubElement(items_elem, "Item")
            item_elem.set("id", str(row[8]))
            item_elem.set("code1c", row[10])
            
            name_elem = ET.SubElement(item_elem, "Name")
            name_elem.text = row[9]
            
            quantity_elem = ET.SubElement(item_elem, "Quantity")
            quantity_elem.text = str(row[11])
            
            unit_elem = ET.SubElement(item_elem, "Unit")
            unit_elem.text = row[12]
            
            current_order_id = row[0]
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        return filename
    
    