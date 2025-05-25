from flask import request, jsonify

class VendedorController:
    def __init__(self, db, models):
        self.models = models
        self.db = db

    def getDb(self):
        return self.db

    def post_vendedor(self, data):
        vendedor_id = data.get('vendedor_id')
        nombre = data.get('nombre')
        edad = data.get('edad')
        salario = data.get('salario')

        if not vendedor_id or not nombre or edad is None or salario is None:
            return jsonify({
                "message": "'vendedor_id', 'nombre', 'edad' y 'salario' son requeridos."
            }), 400

        if not isinstance(edad, int) or edad < 18 or edad > 65:
            return jsonify({
                "message": "La edad debe ser un número entero entre 18 y 65 años."
            }), 400

        if not isinstance(salario, (int, float)) or salario < 3000:
            return jsonify({
                "message": "El salario debe ser mayor o igual a 3000."
            }), 400

        # Validar duplicidad por vendedor_id
        if self.models.DIM_VENDEDOR.query.filter_by(vendedor_id=vendedor_id).first():
            return jsonify({
                "message": f"Ya existe un vendedor con el ID '{vendedor_id}'."
            }), 409

        # Validar duplicidad por combinación lógica (opcional)
        duplicado = self.models.DIM_VENDEDOR.query.filter_by(
            nombre=nombre, edad=edad, salario=salario
        ).first()
        if duplicado:
            return jsonify({
                "message": "Ya existe un vendedor registrado con el mismo nombre, edad y salario."
            }), 409

        new_vendedor = self.models.DIM_VENDEDOR(
            vendedor_id=vendedor_id,
            nombre=nombre,
            edad=edad,
            salario=salario
        )

        try:
            self.getDb().session.add(new_vendedor)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al crear el vendedor: {str(e)}"
            }), 500

        return jsonify({
            "message": "Vendedor creado exitosamente.",
            "vendedor": new_vendedor.to_dict()
        }), 201

    def get_vendedor(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        all_vendedor = self.models.DIM_VENDEDOR.query.filter_by(activo=True).paginate(
            page=page, per_page=per_page, error_out=False
        )

        if not all_vendedor.items:
            return jsonify({"message": "No hay vendedores registrados."}), 404

        return jsonify({
            "vendedores": [v.to_dict() for v in all_vendedor.items],
            "total": all_vendedor.total,
            "pagina_actual": all_vendedor.page,
            "total_paginas": all_vendedor.pages
        }), 200

    def put_vendedor(self, id, data):
        vendedor = self.models.DIM_VENDEDOR.query.filter_by(vendedor_key=id).first()
        if not vendedor:
            return jsonify({
                "message": "No se ha encontrado el vendedor con el id requerido."
            }), 404

        edad = data.get('edad')
        salario = data.get('salario')

        if edad is None or salario is None:
            return jsonify({
                "message": "Los atributos 'edad' y 'salario' son requeridos."
            }), 400

        if not isinstance(edad, int) or edad < 18 or edad > 65:
            return jsonify({
                "message": "La edad debe ser un número entero entre 18 y 65 años."
            }), 400

        if not isinstance(salario, (int, float)) or salario < 3000:
            return jsonify({
                "message": "El salario debe ser mayor o igual a 3000."
            }), 400

        vendedor.edad = edad
        vendedor.salario = salario

        try:
            self.getDb().session.add(vendedor)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios: {str(e)}"
            }), 500

        return jsonify({
            "message": "Vendedor actualizado correctamente.",
            "vendedor": vendedor.to_dict()
        }), 200

    def get_vendedor_id(self, id):
        vendedor = self.models.DIM_VENDEDOR.query.filter_by(vendedor_key=id).first()

        if not vendedor:
            return jsonify({
                "message": "Vendedor no encontrado por el id requerido."
            }), 404

        if not vendedor.activo:
            return jsonify({
                "message": "El vendedor existe pero se encuentra desactivado."
            }), 403

        return jsonify(vendedor.to_dict()), 200

    def delete_vendedor(self, id):
        vendedor = self.models.DIM_VENDEDOR.query.filter_by(vendedor_key=id).first()
        if not vendedor:
            return jsonify({
                "message": "No se ha encontrado el vendedor con el id requerido."
            }), 404

        vendedor.activo = False

        try:
            self.getDb().session.add(vendedor)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios: {str(e)}"
            }), 500

        return jsonify({
            "message": "Vendedor desactivado correctamente.",
            "activo": vendedor.activo
        }), 200
