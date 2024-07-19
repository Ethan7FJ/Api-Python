from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
app.config.from_object(config['config'])

mysql = MySQL(app)

@app.route('/listausu', methods=['GET'])
def lista_usu():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM usuarios "
        cursor.execute(sql)
        datos = cursor.fetchall()

        usuarios = []
        for fila in datos:
            usuario = {
                'codigo': fila[0],
                'nombre': fila[1],
                'apellido': fila[2],
                'email': fila[3],
                'usuario': fila[4],
                'rol': fila[6]
            }
            usuarios.append(usuario)

        cursor.close()  # Cerrar el cursor después de usarlo

        return jsonify({'Usuario': usuarios, 'mensaje': "Listado de usuarios", 'exito': True})

    except Exception as ex:
        return jsonify({'error': str(ex), 'mensaje': "Error al obtener los usuarios", 'exito': False}), 500

@app.route('/buscar_usu/<usuario_u>', methods=['GET'])
def buscar_usuario(usuario_u):
    consulta = "SELECT * FROM usuarios WHERE "
    filtro = []
    parametros = []

    
    if usuario_u:
        filtro.append("usuario_u LIKE %s")
        parametros.append(f"%{usuario_u}%")

    if not filtro:
        return jsonify({"mensaje": "No se proporcionaron parametros validos"}), 400

    consulta += " AND ".join(filtro)
    cursor = mysql.connection.cursor()
    cursor.execute(consulta, parametros)
    datos = cursor.fetchall()

    usuarios = []
    for fila in datos:
        usuario = {
            'codigo': fila[0],
            'nombre': fila[1],
            'apellido': fila[2],
            'email': fila[3],
            'usuario': fila[4],
            'rol': fila[6]
        }
        usuarios.append(usuario)

    cursor.close()  # Cerrar el cursor después de usarlo

    return jsonify(usuarios)

@app.route('/listatare', methods=['GET'])
def lista_tare():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM tareas"
        cursor.execute(sql)
        datos = cursor.fetchall()

        tareas = []
        for fila in datos:
            tarea = {
                'codigo': fila[0],
                'nombre': fila[1],
                'Fecha Inicio': fila[2],
                'Fecha Final': fila[3],
                'Estado': fila[4],
                'Codigo usuario': fila[5]
            }
            tareas.append(tarea)

        cursor.close()  # Cerrar el cursor después de usarlo

        return jsonify({'tareas': tareas, 'mensaje': "Listado de tareas", 'exito': True})

    except Exception as ex:
        return jsonify({'error': str(ex), 'mensaje': "Error al obtener las tareas", 'exito': False}), 500
    
@app.route('/buscar_tare/<nombre_t>', methods=['GET'])
def buscar_tarea(nombre_t):
    consulta = "SELECT * FROM tareas WHERE "
    filtro = []
    parametros = []

    
    if nombre_t:
        filtro.append("nombre_t LIKE %s")
        parametros.append(f"%{nombre_t}%")
    
    fechainicio = request.args.get('fecha_inicio')
    if fechainicio:
        filtro.append("fecha_inicio_t LIKE %s")
        parametros.append(f"%{fechainicio}%")

    if not filtro:
        return jsonify({"mensaje": "No se proporcionaron parametros validos"}), 400

    consulta += " AND ".join(filtro)
    cursor = mysql.connection.cursor()
    cursor.execute(consulta, parametros)
    datos = cursor.fetchall()

    tareas = []
    for fila in datos:
        tarea = {
            'codigo': fila[0],
            'nombre': fila[1],
            'Fecha Inicio': fila[2],
            'Fecha Final': fila[3],
            'Estado': fila[4],
            'Codigo usuario': fila[5]
        }
        tareas.append(tarea)

    cursor.close()  # Cerrar el cursor después de usarlo

    return jsonify(tareas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)