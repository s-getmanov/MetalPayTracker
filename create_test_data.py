from database import Database
import random

def create_test_data():
    db = Database()
    
    # Очистка таблиц (осторожно!)
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM managers")
    cursor.execute("DELETE FROM clients")
    cursor.execute("DELETE FROM nomenclature")
    db.connection.commit()
    
    # Добавление менеджеров
    managers = [
        ("Иванов Петр Сергеевич", "MAN001"),
        ("Сидорова Анна Владимировна", "MAN002"),
        ("Петров Алексей Иванович", "MAN003")
    ]
    
    for name, code in managers:
        db.add_manager(name, code)
    
    # Добавление клиентов
    clients = [
        ("ООО «МеталлТрейд»", "+7-123-456-7890", "info@metalltrade.ru", "CL001"),
        ("АО «СтройМеталл»", "+7-987-654-3210", "zakaz@stroymetall.ru", "CL002"),
        ("ИП Ковалев А.Б.", "+7-555-123-4567", "kovalev@mail.ru", "CL003"),
        ("ЗАО «МеталлПрофи»", "+7-444-789-0123", "sales@metalprofi.ru", "CL004")
    ]
    
    for name, phone, email, code in clients:
        db.add_client(name, phone, email, code)
    
    # Добавление номенклатуры
    nomenclature = [
        ("Профиль стальной 40x40", "Профиль квадратный", "м", "NOM001"),
        ("Лист стальной 2мм", "Лист горячекатаный", "шт", "NOM002"),
        ("Труба 25x3", "Труба стальная", "м", "NOM003"),
        ("Уголок 50x50", "Уголок стальной", "м", "NOM004"),
        ("Болт М10", "Болт с гайкой", "шт", "NOM005"),
        ("Швеллер 100", "Швеллер стальной", "м", "NOM006")
    ]
    
    for name, desc, unit, code in nomenclature:
        db.add_nomenclature(name, desc, unit, code)
    
    # Создание тестовых заявок
    managers = db.get_managers()
    clients = db.get_clients()
    nom_items = db.get_nomenclature()
    
    for i in range(10):
        manager = random.choice(managers)
        client = random.choice(clients)
        
        order_id = db.create_order(manager[0], client[0])
        
        # Добавление 1-3 позиций в заявку
        for _ in range(random.randint(1, 3)):
            nom = random.choice(nom_items)
            quantity = random.randint(1, 20)
            db.add_order_item(order_id, nom[0], quantity)
    
    print("Тестовые данные созданы успешно!")
    
    # Вывод статистики
    cursor = db.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM managers")
    print(f"Менеджеров: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM clients")
    print(f"Клиентов: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM nomenclature")
    print(f"Номенклатуры: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    print(f"Заявок: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM order_items")
    print(f"Позиций в заявках: {cursor.fetchone()[0]}")

if __name__ == "__main__":
    create_test_data()