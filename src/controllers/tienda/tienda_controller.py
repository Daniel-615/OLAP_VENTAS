from flask import request, jsonify

class TiendaController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_tienda(self, data):
        tienda_id = data.get('tienda_id')
        nombre_tienda = data.get('nombre_tienda')
        direccion = data.get('direccion')
        ciudad_id = data.get('ciudad')
        tamaño_m2 = data.get('tamaño_m2')
        horario_apertura = data.get('horario_apertura')
        horario_cierre = data.get('horario_cierre')
        gerente_key = data.get('gerente_key')

        # Validaciones requeridas
        if not gerente_key:
            return jsonify({"message": "'gerente_key' es requerido."}), 400

        if not tienda_id or not nombre_tienda or not direccion or not ciudad_id or not tamaño_m2 or not horario_apertura or not horario_cierre:
            return jsonify({
                "message": "'tienda_id', 'nombre_tienda', 'direccion', 'ciudad', 'tamaño_m2', 'horario_apertura' y 'horario_cierre' son requeridos."
            }), 400

        # Validación de duplicidad compuesta
        tienda_existente = self.models.DIM_TIENDA.query.filter_by(
            nombre_tienda=nombre_tienda,
            direccion=direccion,
            ciudad=ciudad_id
        ).first()

        if tienda_existente:
            return jsonify({
                "message": "Ya existe una tienda con el mismo nombre, dirección y ciudad."
            }), 409

        # Validación de claves foráneas
        gerente = self.models.DIM_GERENTE.query.filter_by(gerente_key=gerente_key).first()
        if not gerente:
            return jsonify({"message": "Gerente no encontrado."}), 404

        ciudad = self.models.DIM_CIUDAD.query.filter_by(ciudad_key=ciudad_id).first()
        if not ciudad:
            return jsonify({"message": "Ciudad no encontrada."}), 404

        # Crear tienda
        nueva_tienda = self.models.DIM_TIENDA(
            tienda_id=tienda_id,
            nombre_tienda=nombre_tienda,
            direccion=direccion,
            ciudad=ciudad_id,
            tamaño_m2=tamaño_m2,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre,
            gerente_key=gerente_key
        )

        try:
            self.getDb().session.add(nueva_tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear la tienda: {str(e)}"}), 500

        return jsonify({
            "message": "Tienda creada correctamente.",
            "tienda": nueva_tienda.to_dict()
        }), 201

    def get_tienda(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_tienda = self.models.DIM_TIENDA.query.paginate(page=page, per_page=per_page, error_out=False)
        if not all_tienda.items:
            return jsonify({"message": "No hay tiendas registradas."}), 404

        return jsonify({
            "tiendas": [t.to_dict() for t in all_tienda.items],
            "total": all_tienda.total,
            "pagina_actual": all_tienda.page,
            "total_paginas": all_tienda.pages
        }), 200

    def put_tienda(self, id, data):
        tienda = self.models.DIM_TIENDA.query.filter_by(tienda_key=id).first()
        if not tienda:
            return jsonify({"message": "No se ha encontrado la tienda con el id requerido."}), 404

        horario_apertura = data.get('horario_apertura')
        horario_cierre = data.get('horario_cierre')

        if not horario_apertura or not horario_cierre:
            return jsonify({
                "message": "Los atributos 'horario_apertura' y 'horario_cierre' son requeridos."
            }), 400

        tienda.horario_apertura = horario_apertura
        tienda.horario_cierre = horario_cierre

        try:
            self.getDb().session.add(tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al guardar los cambios: {str(e)}"}), 500

        return jsonify({
            "horario_apertura": tienda.horario_apertura.strftime("%H:%M") if tienda.horario_apertura else None,
            "horario_cierre": tienda.horario_cierre.strftime("%H:%M") if tienda.horario_cierre else None
        }), 200

    def get_tienda_id(self, id):
        tienda = self.models.DIM_TIENDA.query.filter_by(tienda_key=id).first()
        if not tienda:
            return jsonify({
                "message": "Tienda no encontrada por el id requerido."
            }), 404

        return jsonify(tienda.to_dict()), 200
