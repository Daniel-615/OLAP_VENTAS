from flask import request, jsonify

class CiudadController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_ciudad(self, data):
        ciudad_nombre = data.get('ciudad_nombre')
        region_key = data.get('region_key')

        if not ciudad_nombre or not region_key:
            return jsonify({"message": "El nombre de la ciudad y la región son requeridos."}), 400

        # Verificar si ya existe una ciudad con ese nombre (ignorar mayúsculas/minúsculas)
        existing_city = self.models.DIM_CIUDAD.query.filter(
            self.models.DIM_CIUDAD.ciudad_nombre.ilike(ciudad_nombre)
        ).first()

        if existing_city:
            return jsonify({
                "message": f"La ciudad '{ciudad_nombre}' ya está registrada."
            }), 409

        # Validar que la región exista
        previous_region = self.models.DIM_REGION.query.filter_by(region_key=region_key).first()
        if not previous_region:
            return jsonify({"message": "Región no encontrada entre los registros."}), 404

        new_city = self.models.DIM_CIUDAD(
            ciudad_nombre=ciudad_nombre,
            region_key=previous_region.region_key
        )

        try:
            self.getDb().session.add(new_city)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear la ciudad: {str(e)}"}), 500

        return jsonify({"message": "Ciudad creada exitosamente."}), 201

    def get_ciudad(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_ciudad = self.models.DIM_CIUDAD.query.paginate(page=page, per_page=per_page, error_out=False)

        if not all_ciudad.items:
            return jsonify({"message": "No hay ciudades registradas."}), 404

        return jsonify({
            "ciudades": [ciudad.to_dict() for ciudad in all_ciudad.items],
            "total": all_ciudad.total,
            "pagina_actual": all_ciudad.page,
            "total_paginas": all_ciudad.pages
        }), 200

    def put_ciudad(self, id, data):
        ciudad = self.models.DIM_CIUDAD.query.filter_by(ciudad_key=id).first()

        if not ciudad:
            return jsonify({"message": "No se ha encontrado la ciudad con el ID establecido."}), 404

        if not data.get('ciudad_nombre'):
            return jsonify({"message": "El atributo 'ciudad_nombre' es requerido."}), 400

        ciudad.ciudad_nombre = data.get('ciudad_nombre')

        try:
            self.getDb().session.add(ciudad)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al guardar los cambios: {str(e)}"}), 500

        return jsonify({"nombre": ciudad.ciudad_nombre}), 200

    def get_ciudad_id(self, id):
        ciudad = self.models.DIM_CIUDAD.query.filter_by(ciudad_key=id).first()
        if not ciudad:
            return jsonify({"message": "Ciudad no encontrada por el id requerido."}), 404

        return jsonify({"ciudad_nombre": ciudad.ciudad_nombre}), 200
