from flask import request, jsonify

class VendedorTiendaController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_vendedor_tienda(self, data):
        data = request.json
        vendedor_key = data.get('vendedor_key')
        tienda_key = data.get('tienda_key')
        if not vendedor_key or not tienda_key:
            return jsonify({
                "message": "'vendedor_key' y 'tienda_key' son requeridos."
            })
        else:
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
                "message": f"Error al vendedor_tienda: {str(e)}"
            }), 500
        return jsonify({
            "message": "Vendedor Tienda creado correctamente"
        })

    def get_vendedor_tienda(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_vendedor_tienda = self.models.DIM_GERENTE.query.paginate(page=page, per_page=per_page, error_out=False)
        if not all_vendedor_tienda.items:
            return jsonify({
                "message": "No hay vendedor_tienda registrados."
            }), 404
        else:
            return jsonify({
                "vendedor_tienda": [vendedor_tienda.to_dict() for vendedor_tienda in all_vendedor_tienda.items],
                "total": all_vendedor_tienda.total,
                "pagina_actual": all_vendedor_tienda.page,
                "total_paginas": all_vendedor_tienda.pages
            }), 200

    def put_vendedor_tienda(self, id, data):
        vendedor_tienda = self.models.DIM_VENDEDOR_TIENDA.query.filter_by(id=id).first()
        if not vendedor_tienda:
            return jsonify({
                "message": "No se ha encontrado con el gerente con el id requerido."
            }), 404
        if not data.get('fecha_renuncia'):
            return jsonify({
                "message": "El atributo 'fecha_renuncia' es requerido."
            }), 400
        else:
            vendedor_tienda.fecha_renuncia = data.get('fecha_renuncia')
            vendedor_tienda.activo = False
            try:
                self.getDb().session.add(vendedor_tienda)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return jsonify({
                    "message": f"Error al guardar los cambios {str(e)}"
                }), 500
        return jsonify({
            "activo": vendedor_tienda.activo
        }), 200

    def get_vendedor_tienda_id(self, id):
        vendedor_tienda = self.models.DIM_VENDEDOR_TIENDA.query.filter_by(id=id).first()
        if not vendedor_tienda:
            return jsonify({
                "message": "Vendedor_tienda no encontrado por el id requerido."
            }), 400
        else:
            return jsonify({
                "vendedor": vendedor_tienda.vendedor,
                "tienda": vendedor_tienda.tienda
            })