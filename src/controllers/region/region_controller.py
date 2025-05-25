from flask import request, jsonify

class RegionController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    def post_region(self, data):
        region_nombre = data.get('region_nombre')
        if not region_nombre:
            return jsonify({
                "message": "'region_nombre' es requerido."
            }), 400

        # Validar si ya existe una región con ese nombre (sin importar mayúsculas/minúsculas)
        existing = self.models.DIM_REGION.query.filter(
            self.models.DIM_REGION.region_nombre.ilike(region_nombre)
        ).first()
        if existing:
            return jsonify({
                "message": f"La región '{region_nombre}' ya está registrada."
            }), 409

        new_region = self.models.DIM_REGION(region_nombre=region_nombre)
        try:
            self.getDb().session.add(new_region)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al crear la región: {str(e)}"
            }), 500

        return jsonify({
            "message": "Región creada correctamente"
        }), 201

    def get_region(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_region = self.models.DIM_REGION.query.paginate(page=page, per_page=per_page, error_out=False)
        if not all_region.items:
            return jsonify({"message": "No hay regiones registradas."}), 404

        return jsonify({
            "regiones": [reg.to_dict() for reg in all_region.items],
            "total": all_region.total,
            "pagina_actual": all_region.page,
            "total_paginas": all_region.pages
        }), 200

    def put_region(self, id, data):
        region = self.models.DIM_REGION.query.filter_by(region_key=id).first()
        if not region:
            return jsonify({
                "message": "No se ha encontrado la región con el id requerido."
            }), 404

        region_nombre = data.get('region_nombre')
        if not region_nombre:
            return jsonify({
                "message": "El atributo 'region_nombre' es requerido."
            }), 400

        # Verificar si el nuevo nombre ya está en uso por otra región
        existing = self.models.DIM_REGION.query.filter(
            self.models.DIM_REGION.region_nombre.ilike(region_nombre),
            self.models.DIM_REGION.region_key != id
        ).first()
        if existing:
            return jsonify({
                "message": f"Ya existe otra región con el nombre '{region_nombre}'."
            }), 409

        region.region_nombre = region_nombre
        try:
            self.getDb().session.add(region)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios: {str(e)}"
            }), 500

        return jsonify({
            "nombre": region.region_nombre
        }), 200

    def get_region_id(self, id):
        region = self.models.DIM_REGION.query.filter_by(region_key=id).first()
        if not region:
            return jsonify({"message": "Región no encontrada por el id requerido."}), 404

        return jsonify(region.to_dict()), 200
