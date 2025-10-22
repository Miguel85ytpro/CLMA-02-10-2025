from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.secret_key = 'secreto'

usuarios = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']

        for u in usuarios:
            if u['correo'] == correo:
                flash('El correo ya está registrado')
                return redirect('/registro')

        usuarios.append({'nombre': nombre, 'correo': correo})
        return redirect('/')

    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
