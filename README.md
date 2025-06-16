python myenv env 
env\Scripts\activate
pip install -r requirements.txt

Tunelizacion:
https://microservicio_ventas.serveo.net

Configuración del tunel:
Ir a main.py y configurar el servidor flask para que host=0.0.0.0 y port=5000
ssh -R microservicio_ventas:80:192.168.1.21:5000 serveo.net
ssh-keygen -t rsa -b 4096 -C "tucorreo@gmail.com"
Luego de hacer estos 2 pasos volver a ejecutar el comando ssh -R.
Y autenticarse y listo. 

Probando :D