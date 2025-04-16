from flask import request

class CiudadController:
    def __init__(self, db,models):
        self.models =models
        self.db=db
    def getDb(self):
        return self.db
    def post_ciudad(self,data):
        data = request.get_json()

        ciudad_nombre=data['ciudad_nombre']
        region_key=data['region_key']
        if not ciudad_nombre or not region_key:
            return {"message": "Nombre y Región son requeridos."}, 400
        else:
            previous_region = self.models.DIM_REGION.query.filter_by(region_key=region_key).first()
            if not previous_region:
                return {"message": "Región no encontrada entre los registros."}, 404
            new_city = self.models.DIM_CIUDAD(ciudad_nombre=ciudad_nombre, region_key=previous_region)
            try:
                self.getDb().session.add(new_city)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return {"message": f"Error al crear la ciudad: {str(e)}"}, 500
            return {"message": "Ciudad creada exitosamente."}, 201
    def get_ciudad(self):
        page = request.args.get('page',default=1,type=int)
        per_page = request.args.get('per_page',default=10,type=int)  # Número de elementos por página por defecto

        all_ciudad = self.models.DIM_CIUDAD.query.paginate(page=page, per_page=per_page, error_out=False)

        if not all_ciudad.items:
            return {
                "message": "No hay ciudades registradas."
                }, 404
        else:
            return {
            "ciudades": [ciudad.to_dict() for ciudad in all_ciudad.items],
            "total": all_ciudad.total,
            "pagina_actual": all_ciudad.page,
            "total_paginas": all_ciudad.pages
            }, 200
    def put_ciudad(self, id, data):
        ciudad = self.models.DIM_CIUDAD.query.filter_by(ciudad_key=id).first()
        
        # Validar si la ciudad existe
        if not ciudad:
            return {"message": "No se ha encontrado la ciudad con el ID establecido."}, 404
        
        # Validar si 'ciudad_nombre' está en los datos
        if not data['ciudad_nombre']:
            return {
                "message": "El atributo 'ciudad_nombre' es requerido."
                }, 400
        
        ciudad.nombre = data['ciudad_nombre']
        
        # Guardar los cambios
        try:
            self.getDb().session.add(ciudad)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return {
                "message": f"Error al guardar los cambios: {str(e)}"
                }, 500
        
        # Respuesta exitosa
        return {
            "nombre": ciudad.nombre
        }, 200
    def get_ciudad_id(self,id):
        ciudad=self.models.DIM_CIUDAD.query.filter_by(ciudad_key=id)
        if not ciudad:
            return {
                "message": "Ciudad no encontrada por el id requerido."
            },404
        else:
            return{
                "ciudad_nombre": ciudad.nombre 
            },200