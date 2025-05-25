from flask import request, jsonify

class VendedorTiendaController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_vendedor_tienda(self, data):
        vendedor_key = data.get('vendedor_key')
        tienda_key = data.get('tienda_key')

        if not vendedor_key or not tienda_key:
            return jsonify({
                "message": "'vendedor_key' y 'tienda_key' son requeridos."
            }), 400

        # Validar si ya existe ese vínculo (activo o inactivo)
        existing = self.models.DIM_VENDEDOR_TIENDA.query.filter_by(
            vendedor_key=vendedor_key,
            tienda_key=tienda_key
        ).first()

        if existing:
            return jsonify({
                "message": "El vendedor ya ha sido asignado anteriormente a esta tienda. No se permite duplicidad."
            }), 409

        new_vendedor_tienda = self.models.DIM_VENDEDOR_TIENDA(
            vendedor_key=vendedor_key,
            tienda_key=tienda_key
        )

        try:
            self.getDb().session.add(new_vendedor_tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al registrar vendedor en tienda: {str(e)}"
            }), 500

        return jsonify({
            "message": "Vendedor-Tienda creado correctamente.",
            "vinculo": new_vendedor_tienda.to_dict()
        }), 201

    def get_vendedor_tienda(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_vendedor_tienda = self.models.DIM_VENDEDOR_TIENDA.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        if not all_vendedor_tienda.items:
            return jsonify({
                "message": "No hay relaciones vendedor-tienda registradas."
            }), 404

        return jsonify({
            "vendedor_tienda": [vt.to_dict() for vt in all_vendedor_tienda.items],
            "total": all_vendedor_tienda.total,
            "pagina_actual": all_vendedor_tienda.page,
            "total_paginas": all_vendedor_tienda.pages
        }), 200

    def put_vendedor_tienda(self, id, data):
        vendedor_tienda = self.models.DIM_VENDEDOR_TIENDA.query.filter_by(id=id).first()

        if not vendedor_tienda:
            return jsonify({
                "message": "No se ha encontrado la relación vendedor-tienda con el id requerido."
            }), 404

        fecha_renuncia = data.get('fecha_renuncia')
        if not fecha_renuncia:
            return jsonify({
                "message": "El atributo 'fecha_renuncia' es requerido."
            }), 400

        vendedor_tienda.fecha_renuncia = fecha_renuncia
        vendedor_tienda.activo = False

        try:
            self.getDb().session.add(vendedor_tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios: {str(e)}"
            }), 500

        return jsonify({
            "message": "Vinculación vendedor-tienda actualizada y desactivada.",
            "activo": vendedor_tienda.activo
        }), 200

    def get_vendedor_tienda_id(self, id):
        vendedor_tienda = self.models.DIM_VENDEDOR_TIENDA.query.filter_by(id=id).first()

        if not vendedor_tienda:
            return jsonify({
                "message": "Vinculación vendedor-tienda no encontrada por el id requerido."
            }), 404

        return jsonify(vendedor_tienda.to_dict()), 200
