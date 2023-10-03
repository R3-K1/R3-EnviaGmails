import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser

def cargar_configuracion():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Correo']

def enviar_correo(destinatario, asunto, cuerpo, remitente, password):
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(cuerpo, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        try:
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
            print("Correo electrónico enviado con éxito.\nGRACIAS POR USAR R3")
            time.sleep(2.5)
        except:
            print("Ha surgido un error durante el envío del correo electrónico, verifica las credenciales otorgadas.")
            time.sleep(2.5)

# Cargar configuración desde el archivo
configuracion_correo = cargar_configuracion()

remitente = configuracion_correo['remitente']
password = configuracion_correo['password']
destinatario = input("Gmail al que quieres escribir: ")
asunto = input("Título del gmail: ")
cuerpo = input("Cuerpo del gmail: ")

enviar_correo(destinatario, asunto, cuerpo, remitente, password)