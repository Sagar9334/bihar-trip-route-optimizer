import sqlite3

conn = sqlite3.connect('trip_database.db')
cursor = conn.cursor()

# 1. Destinations Table (3 budget categories ke sath)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS destinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        low_food INTEGER, low_hotel INTEGER,
        med_food INTEGER, med_hotel INTEGER,
        high_food INTEGER, high_hotel INTEGER
    )
''')

# 2. Routes Table (budget_type filter ke sath)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        transport_mode TEXT,
        cost INTEGER,
        budget_type TEXT
    )
''')

cursor.execute('DELETE FROM destinations')
cursor.execute('DELETE FROM routes')

# Destinations Data (Low, Medium, High budgets for Food/Hotel)
destinations_data = [
    ('Rajgir', 'Historic ruins, Peace Pagoda, Glass Bridge.', 500, 800, 1000, 2000, 2500, 4000),
    ('Bodh Gaya', 'Mahabodhi Temple, Spiritual Journey.', 600, 1000, 1200, 2500, 3000, 5000),
    ('Nalanda', 'Ancient University Ruins.', 400, 700, 800, 1500, 2000, 3500)
]
cursor.executemany('INSERT INTO destinations (name, description, low_food, low_hotel, med_food, med_hotel, high_food, high_hotel) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', destinations_data)

# Routes Data (All over India to Patna, and Patna to destinations)
routes_data = [
    # LOW BUDGET (Sleeper Trains, Normal Buses)
    ('MP', 'Patna', 'Train (Sleeper)', 600, 'Low'),
    ('Delhi', 'Patna', 'Train (Sleeper)', 500, 'Low'),
    ('UP', 'Patna', 'Train (General)', 300, 'Low'),
    ('Maharashtra', 'Patna', 'Train (Sleeper)', 800, 'Low'),
    ('West Bengal', 'Patna', 'Train (Sleeper)', 400, 'Low'),
    ('Patna', 'Rajgir', 'Bus (Non-AC)', 150, 'Low'),
    ('Patna', 'Bodh Gaya', 'Bus (Non-AC)', 200, 'Low'),
    ('Patna', 'Nalanda', 'Bus (Non-AC)', 120, 'Low'),

    # MEDIUM BUDGET (3AC Trains, AC Buses)
    ('MP', 'Patna', 'Train (3AC)', 1500, 'Medium'),
    ('Delhi', 'Patna', 'Train (3AC)', 1400, 'Medium'),
    ('UP', 'Patna', 'Train (3AC)', 800, 'Medium'),
    ('Maharashtra', 'Patna', 'Train (3AC)', 2000, 'Medium'),
    ('West Bengal', 'Patna', 'Train (3AC)', 1000, 'Medium'),
    ('Patna', 'Rajgir', 'Bus (AC Volvo)', 350, 'Medium'),
    ('Patna', 'Bodh Gaya', 'Bus (AC Volvo)', 450, 'Medium'),
    ('Patna', 'Nalanda', 'Bus (AC)', 250, 'Medium'),

    # HIGH BUDGET (Flights, Cabs, 1AC)
    ('MP', 'Patna', 'Flight', 6000, 'High'),
    ('Delhi', 'Patna', 'Flight', 5000, 'High'),
    ('UP', 'Patna', 'Cab / 1AC', 3000, 'High'),
    ('Maharashtra', 'Patna', 'Flight', 7500, 'High'),
    ('West Bengal', 'Patna', 'Flight', 3500, 'High'),
    ('Patna', 'Rajgir', 'Private Cab', 1500, 'High'),
    ('Patna', 'Bodh Gaya', 'Private Cab', 2500, 'High'),
    ('Patna', 'Nalanda', 'Private Cab', 1200, 'High')
]
cursor.executemany('INSERT INTO routes (source, destination, transport_mode, cost, budget_type) VALUES (?, ?, ?, ?, ?)', routes_data)

conn.commit()
conn.close()
print("Updated Database Created with Budget Routes!")