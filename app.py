from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
        conn.close()

# CRITICAL: Call init_db to recreate the database with the new schema.
# This will delete all existing grocery items.
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    # Fetch all columns including category and notes
    groceries = conn.execute('SELECT * FROM groceries ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', groceries=groceries)

@app.route('/add', methods=['POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        quantity_str = request.form.get('quantity', '1')
        units = request.form.get('units', '').strip()
        category = request.form.get('category', '').strip() # New: Get category
        notes = request.form.get('notes', '').strip()       # New: Get notes

        # Safely convert quantity to integer
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        if item_name:
            conn = get_db_connection()
            # Insert item with quantity, units, category, and notes
            conn.execute('INSERT INTO groceries (name, quantity, units, category, notes, purchased) VALUES (?, ?, ?, ?, ?, ?)',
                         (item_name, quantity, units, category, notes, 0)) # 0 for false (not purchased)
            conn.commit()
            conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:item_id>')
def toggle_purchased(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT purchased FROM groceries WHERE id = ?', (item_id,)).fetchone()
    if item:
        new_status = 1 if item['purchased'] == 0 else 0
        conn.execute('UPDATE groceries SET purchased = ? WHERE id = ?',
                     (new_status, item_id))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM groceries WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)