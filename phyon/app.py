from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista en memoria para almacenar los datos temporalmente
data_store = []

@app.route('/')
def index():
    """Página principal que muestra todos los elementos"""
    return render_template('index.html', items=data_store)

@app.route('/add', methods=['POST'])
def add_item():
    """Agregar un nuevo elemento"""
    new_item = {
        'id': len(data_store) + 1,
        'name': request.form['name'],
        'description': request.form['description']
    }
    data_store.append(new_item)
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """Editar un elemento existente"""
    item = next((item for item in data_store if item['id'] == item_id), None)
    if request.method == 'POST' and item:
        item['name'] = request.form['name']
        item['description'] = request.form['description']
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """Eliminar un elemento por su ID"""
    global data_store
    data_store = [item for item in data_store if item['id'] != item_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
