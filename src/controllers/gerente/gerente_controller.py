from flask import request,jsonify
class GerenteController:
    def __init__(self,db,models):
        self.db=db
        self.models=models
    def getDb(self):
        return self.db
    def post_gerente(self,data):
        data=request.json()
        gerente_id=data.get('gerente_id')
        nombre=data.get('gerente_nombre')
        if not gerente_id or not nombre:
            return jsonify({
                "message": "'gerente_id' y 'gerente_nombre' son requeridos."
            })
        else:
            new_gerente=self.models.DIM_GERENTE(
                gerente_id=gerente_id,
                nombre=nombre
            )
        try:
            self.getDb().session.add(new_gerente)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al crear el gerente: {str(e)}"
            }),500
    def get_gerente(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)

        all_gerente=self.models.DIM_GERENTE.query.paginate(page=page,per_page=per_page,error_out=False)

        if not all_gerente.items:
            return jsonify({
                "message": "No hay gerentes registrados."
            }),404
        else:
            return jsonify({
                "gerentes": [gerente.to_dict() for gerente in all_gerente.items],
                "total": all_gerente.total,
                "pagina_actual": all_gerente.page,
                "total_paginas": all_gerente.pages
            }),200
    def put_gerente(self,id,data):
        gerente=self.models.DIM_GERENTE.query.filter_by(gerente_key=id)
        if not gerente:
            return jsonify({
                "message": "No se ha encontrado el gerente con el id requerido."
            }),404
        if not data.get('gerente_nombre'):
            return jsonify({
                "message": "El atributo 'gerente_nombre' es requerido."
            }),400
        gerente.nombre=data.get('gerente_nombre')
        try:
            self.getDb().session.add(gerente)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios {str(e)}"
            }),500
        return jsonify({
            "nombre": gerente.nombre
        }),200
    def get_gerente_id(self,id):
        gerente=self.models.DIM_GERENTE.query.filter_by(gerente_key=id).first()
        if not gerente:
            return jsonify({
                "message": "Gerente no encontrado por el id requerido."
            }),404
        else:
            return jsonify({
                "gerente_key": gerente.gerente_key,
                "nombre": gerente.nombre
            }),200
        