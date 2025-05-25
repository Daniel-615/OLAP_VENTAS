from flask import request, jsonify

class ClienteSegmentoController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    def post_cliente_segmento(self, data):
        cliente_key = data.get('cliente_key')
        segmento_key = data.get('segmento_key')

        if not cliente_key or not segmento_key:
            return jsonify({"message": "'cliente_key' y 'segmento_key' son requeridos."}), 400

        # Validar existencia de cliente y segmento
        previous_cliente = self.models.DIM_CLIENTE.query.filter_by(cliente_key=cliente_key).first()
        if not previous_cliente:
            return jsonify({"message": "Cliente no encontrado."}), 404

        previous_segmento = self.models.DIM_SEGMENTO.query.filter_by(segmento_key=segmento_key).first()
        if not previous_segmento:
            return jsonify({"message": "Segmento no encontrado."}), 404

        # Validar duplicidad de la relación
        existing_relation = self.models.DIM_CLIENTE_SEGMENTO.query.filter_by(
            cliente_key=cliente_key,
            segmento_key=segmento_key
        ).first()

        if existing_relation:
            return jsonify({
                "message": "El cliente ya está asignado a este segmento."
            }), 409  # Conflicto

        # Crear relación cliente-segmento
        new_rel = self.models.DIM_CLIENTE_SEGMENTO(
            cliente_key=cliente_key,
            segmento_key=segmento_key
        )
        try:
            self.getDb().session.add(new_rel)
            self.getDb().session.commit()
            return jsonify({"message": "Segmento del cliente creado correctamente."}), 201
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear el cliente-segmento: {str(e)}"}), 500

    def get_cliente_segmento(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        pagination = self.models.DIM_CLIENTE_SEGMENTO.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        if not pagination.items:
            return jsonify({"message": "No hay clientes-segmento registrados."}), 404

        return jsonify({
            "clientes_segmento": [rel.to_dict() for rel in pagination.items],
            "total": pagination.total,
            "pagina_actual": pagination.page,
            "total_paginas": pagination.pages
        }), 200

    def put_cliente_segmento(self, id, data):
        segmento_key = data.get('segmento_key')

        if not segmento_key:
            return jsonify({"message": "El atributo 'segmento_key' es requerido."}), 400

        rel = self.models.DIM_CLIENTE_SEGMENTO.query.filter_by(
            cliente_segmento_key=id
        ).first()
        if not rel:
            return jsonify({"message": "No se ha encontrado el cliente-segmento con el id establecido."}), 404

        previous_segmento = self.models.DIM_SEGMENTO.query.filter_by(segmento_key=segmento_key).first()
        if not previous_segmento:
            return jsonify({"message": "Segmento no encontrado."}), 404

        # Validar duplicidad en PUT solo si se cambia el segmento
        if rel.segmento_key != segmento_key:
            exists = self.models.DIM_CLIENTE_SEGMENTO.query.filter_by(
                cliente_key=rel.cliente_key,
                segmento_key=segmento_key
            ).first()
            if exists:
                return jsonify({
                    "message": "Ya existe otra relación para este cliente con el mismo segmento."
                }), 409

        rel.segmento_key = segmento_key
        try:
            self.getDb().session.add(rel)
            self.getDb().session.commit()
            return jsonify({"segmento_key": str(rel.segmento_key)}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al guardar los cambios: {str(e)}"}), 500

    def get_cliente_segmento_id(self, id):
        rel = self.models.DIM_CLIENTE_SEGMENTO.query.filter_by(
            cliente_segmento_key=id
        ).first()
        if not rel:
            return jsonify({"message": "Cliente_segmento no encontrado por el id requerido."}), 404

        return jsonify(rel.to_dict()), 200
