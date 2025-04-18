from flask import request, jsonify

class SegmentoController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_segmento(self, data):
        segmento_id = data.get('segmento_id')
        nombre = data.get('nombre')

        if not segmento_id or not nombre:
            return jsonify({
                "message": "'segmento_id' y 'nombre' son requeridos."
            }), 400

        # Verificar si el segmento_id ya existe
        exists = self.models.DIM_SEGMENTO.query.filter_by(segmento_id=segmento_id).first()
        if exists:
            return jsonify({
                "message": f"Ya existe un segmento con ID '{segmento_id}'."
            }), 409

        new_segmento = self.models.DIM_SEGMENTO(
            segmento_id=segmento_id,
            nombre=nombre
        )

        try:
            self.getDb().session.add(new_segmento)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al crear el segmento: {str(e)}"
            }), 500

        return jsonify({
            "message": "Segmento creado correctamente."
        }), 201

    def get_segmento(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        segmentos = self.models.DIM_SEGMENTO.query.paginate(page=page, per_page=per_page, error_out=False)
        if not segmentos.items:
            return jsonify({
                "message": "No hay segmentos registrados."
            }), 404

        return jsonify({
            "segmentos": [s.to_dict() for s in segmentos.items],
            "total": segmentos.total,
            "pagina_actual": segmentos.page,
            "total_paginas": segmentos.pages
        }), 200

    def get_segmento_id(self, id):
        segmento = self.models.DIM_SEGMENTO.query.filter_by(segmento_key=id).first()
        if not segmento:
            return jsonify({
                "message": "Segmento no encontrado por el id requerido."
            }), 404

        return jsonify(segmento.to_dict()), 200

    def put_segmento(self, id, data):
        segmento = self.models.DIM_SEGMENTO.query.filter_by(segmento_key=id).first()
        if not segmento:
            return jsonify({
                "message": "Segmento no encontrado por el id requerido."
            }), 404

        nombre = data.get('nombre')
        if not nombre:
            return jsonify({
                "message": "'nombre' es requerido para actualizar."
            }), 400

        segmento.nombre = nombre

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al actualizar el segmento: {str(e)}"
            }), 500

        return jsonify(segmento.to_dict()), 200
