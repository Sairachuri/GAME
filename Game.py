from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder='templates')

# Configure your MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="harshdb"
)

cursor = db.cursor()

# Create the table if it doesn't exist
table_creation_query = """
    CREATE TABLE IF NOT EXISTS game (
        id INT AUTO_INCREMENT PRIMARY KEY,
        attribute_name VARCHAR(255) NOT NULL,
        attribute_value TEXT NOT NULL
    )
"""
cursor.execute(table_creation_query)
db.commit()

# Hardcoded data (you should replace this with data from your database)
attributes = {
    'Color': ['Red', 'Blue', 'Green'],
    'Size': ['Small', 'Medium', 'Large'],
    'Brand': ['Brand A', 'Brand B', 'Brand C']
}

@app.route('/')
def index():
    return render_template('index.html', attributes=attributes)

@app.route('/edit/<attribute>')
def edit_attribute(attribute):
    if attribute in attributes:
        return render_template('edit.html', attribute=attribute, values=attributes[attribute])
    else:
        return redirect(url_for('index'))

@app.route('/update/<attribute>', methods=['POST'])
def insert_attribute(attribute):
    if attribute in attributes:
        new_values = request.form.getlist('value')
        attributes[attribute] = new_values

        # insert in the database (you need to adapt this based on your actual database structure)
        insert_query = "UPDATE game SET attribute_value = %s WHERE attribute_name = %s"
        cursor.execute(insert_query, (', '.join(new_values), attribute))
        db.commit()

    return redirect(url_for('index'))

@app.route('/update/<attribute>', methods=['POST'])
def update_attribute(attribute):
    if attribute in attributes:
        new_values = request.form.getlist('value')
        attributes[attribute] = new_values

        # Update the database (you need to adapt this based on your actual database structure)
        update_query = "UPDATE game SET attribute_value = %s WHERE attribute_name = %s"
        cursor.execute(update_query, (', '.join(new_values), attribute))
        db.commit()

    return redirect(url_for('index'))



# Add a route to handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Add a route to handle 500 errors
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Add a route for a generic error page
@app.route('/error')
def show_error():
    # You can customize this route for specific error handling
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
