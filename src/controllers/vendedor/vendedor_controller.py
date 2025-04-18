from flask import request,jsonify
class VendedorController:
    def __init__(self,db,models):
        self.models=models
        self.db=db
    def getDb(self):
        return self.db
    def post_vendedor(self,data):
        vendedor_id=data.get('vendedor_id')
        nombre=data.get('nombre')
        edad=data.get('edad')
        salario=data.get('salario')
        if not vendedor_id or not nombre or not edad or not salario:
            return jsonify({
                "message": "'vendedor_id', 'nombre', 'edad' y 'salario' son requeridos."
            })
        else:
            new_vendedor=self.models.DIM_VENDEDOR(
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
            }),500
        return jsonify({
        "message": "Vendedor creado exitosamente.",
        "vendedor": {
            "vendedor_id": vendedor_id,
            "nombre": nombre
        }
        }), 201
    def get_vendedor(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)

        all_vendedor=self.models.DIM_VENDEDOR.query.paginate(page=page,per_page=per_page,error_out=False)

        if not all_vendedor.items:
            return jsonify({
                "message": "No hay vendedores registrados."
            }),404
        else:
            return jsonify({
                "vendedores": [vendedores.to_dict() for vendedores in all_vendedor.items],
                "total": all_vendedor.total,
                "pagina_actual": all_vendedor.page,
                "total_paginas": all_vendedor.pages
            }),200
    def put_vendedor(self,id,data):
        vendedor=self.models.DIM_VENDEDOR.query.filter_by(vendedor_key=id)
        if not vendedor:
            return{
                "message": "No se ha encontrado el vendedor con el id requerido."
            },404
        if not data.get('salario') or not data.get('edad'):
            return{
                "message": "El atributo 'salario' y 'edad' son requeridos."
            },400
        vendedor.salario=data.get('salario')
        vendedor.edad=data.get('edad')
        try:
            self.getDb().session.add(vendedor)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios {str(e)}"
            }),500
        return jsonify({
            "salario": vendedor.salario,
            "edad": vendedor.edad
        }),200
    def get_vendedor_id(self,id):
        vendedor=self.models.DIM_VENDEDOR.query.filter_by(vendedor_key=id)
        if not vendedor:
            return jsonify({
                "message": "Vendedor no encontrado por el id requerido."
            }),404
        else:
            return jsonify({
                "vendedor_key": vendedor.vendedor_key,
                "activo": vendedor.activo,
                "nombre": vendedor.nombre
            })
    def delete_vendedor(self,id):
        vendedor=self.models.DIM_VENDEDOR.query.filter_by(vendedor_key=id)
        if not vendedor:
            return jsonify({
                "message": "No se ha encontrado el vendedor con el id requerido."
            }),404
        vendedor.activo=False
        try:
            self.getDb().session.add(vendedor)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios {str(e)}"
            }),500
        return jsonify({
            "activo": vendedor.activo
        }),201
        