from flask import request, jsonify

class ClienteController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_cliente(self, data):
        cliente_id = data.get('cliente_id')
        nombre = data.get('cliente_nombre')
        apellido = data.get('cliente_apellido')
        gmail = data.get('cliente_gmail')
        telefono = data.get('cliente_telefono')
        ciudad_id = data.get('ciudad_id')

        # Validación de campos requeridos
        if not cliente_id or not nombre:
            return jsonify({"message": "'cliente_nombre' y 'cliente_id' son requeridos."}), 400
        if not apellido or not gmail:
            return jsonify({"message": "'apellido' y 'cliente_gmail' son requeridos."}), 400
        if not telefono or not ciudad_id:
            return jsonify({"message": "'cliente_telefono' y 'ciudad_id' son requeridos."}), 400

        # Verificar duplicidad por cliente_id, email o teléfono
        if self.models.DIM_CLIENTE.query.filter_by(cliente_id=cliente_id).first():
            return jsonify({"message": f"Ya existe un cliente con el ID '{cliente_id}'."}), 409
        if self.models.DIM_CLIENTE.query.filter_by(email=gmail).first():
            return jsonify({"message": f"Ya existe un cliente con el correo '{gmail}'."}), 409
        if self.models.DIM_CLIENTE.query.filter_by(telefono=telefono).first():
            return jsonify({"message": f"Ya existe un cliente con el teléfono '{telefono}'."}), 409

        # Validar si ya existe por nombre + apellido + email
        if self.models.DIM_CLIENTE.query.filter_by(nombre=nombre, apellido=apellido, email=gmail).first():
            return jsonify({"message": "Ya existe un cliente con ese nombre, apellido y correo."}), 409

        # Validar si existe la ciudad
        previous_ciudad = self.models.DIM_CIUDAD.query.filter_by(ciudad_key=ciudad_id).first()
        if not previous_ciudad:
            return jsonify({"message": f"No se encontró una ciudad con el ID '{ciudad_id}'."}), 404

        new_client = self.models.DIM_CLIENTE(
            cliente_id=cliente_id,
            nombre=nombre,
            apellido=apellido,
            email=gmail,
            telefono=telefono,
            ciudad=previous_ciudad.ciudad_key,
        )

        try:
            self.getDb().session.add(new_client)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear el cliente: {str(e)}"}), 500

        return jsonify({
            "message": "Cliente creado correctamente.",
            "cliente": {
                "cliente_id": cliente_id,
                "cliente_nombre": nombre
            }
        }), 201

    def get_cliente(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_cliente = self.models.DIM_CLIENTE.query.paginate(page=page, per_page=per_page, error_out=False)

        if not all_cliente.items:
            return jsonify({"message": "No hay clientes registrados."}), 404

        return {
            "clientes": [cliente.to_dict() for cliente in all_cliente.items],
            "total": all_cliente.total,
            "pagina_actual": all_cliente.page,
            "total_paginas": all_cliente.pages
        }, 200

    def put_cliente(self, id, data):
        cliente = self.models.DIM_CLIENTE.query.filter_by(cliente_key=id).first()
        if not cliente:
            return jsonify({"message": "No se ha encontrado el cliente con el id establecido."}), 404

        gmail = data.get('cliente_gmail')
        ciudad_id = data.get('cliente_ciudad')
        telefono = data.get('cliente_telefono')
        region = data.get('cliente_region')

        if not gmail or not ciudad_id or not telefono or not region:
            return jsonify({
                "message": "'cliente_gmail', 'cliente_ciudad', 'cliente_telefono' y 'cliente_region' son requeridos."
            }), 400

        # Validar ciudad
        ciudad = self.models.DIM_CIUDAD.query.filter_by(ciudad_key=ciudad_id).first()
        if not ciudad:
            return jsonify({"message": f"No se encontró una ciudad con el ID '{ciudad_id}'."}), 404

        # Validar región
        region_obj = self.models.DIM_REGION.query.filter_by(region_key=region).first()
        if not region_obj:
            return jsonify({"message": f"No se encontró una región con el ID '{region}'."}), 404

        # Validar duplicidad de email o teléfono si se actualizan
        if gmail != cliente.email and self.models.DIM_CLIENTE.query.filter_by(email=gmail).first():
            return jsonify({"message": f"Ya existe un cliente con el correo '{gmail}'."}), 409

        if telefono != cliente.telefono and self.models.DIM_CLIENTE.query.filter_by(telefono=telefono).first():
            return jsonify({"message": f"Ya existe un cliente con el teléfono '{telefono}'."}), 409

        cliente.email = gmail
        cliente.telefono = telefono
        cliente.region = region_obj  # Suponiendo que tienes relación directa
        cliente.ciudad = ciudad.ciudad_key

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al guardar los cambios: {str(e)}"}), 500

        return jsonify({
            "message": "Cliente actualizado correctamente.",
            "cliente": {
                "cliente_id": cliente.cliente_id,
                "cliente_gmail": cliente.email,
                "cliente_telefono": cliente.telefono,
                "cliente_region": region_obj.region_nombre,
                "cliente_ciudad": cliente.ciudad
            }
        }), 200

    def get_cliente_id(self, id):
        cliente = self.models.DIM_CLIENTE.query.filter_by(cliente_key=id).first()
        if not cliente:
            return jsonify({"message": "Cliente no encontrado por el id requerido."}), 404

        return jsonify({
            "nombre": cliente.nombre,
            "apellido": cliente.apellido
        })
