from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash_y_session'

usuarios_registrados = []

@app.route('/')
def home():
    if 'usuario' in session:
        return render_template('index.html', nombre=session['usuario']['nombre'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        repetir_correo = request.form.get('repetir_correo')
        contrasena = request.form.get('contrasena')
        genero = request.form.get('genero')

        if correo != repetir_correo:
            flash('Los correos no coinciden.')
            return redirect(url_for('register'))

        if any(usuario['correo'] == correo for usuario in usuarios_registrados):
            flash('Este correo ya está registrado.')
            return redirect(url_for('register'))

        usuarios_registrados.append({
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contrasena': contrasena,
            'genero': genero
        })

        flash('Registro exitoso, por favor inicia sesión.')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        usuario = next((u for u in usuarios_registrados if u['correo'] == correo and u['contrasena'] == contrasena), None)

        if usuario:
            session['usuario'] = usuario
            return redirect(url_for('home'))
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('login'))

    return render_template('inicio.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
