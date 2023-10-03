import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import configparser

def cargar_configuracion():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Correo']

def enviar_correo(destinatario, asunto, cuerpo, remitente, password, adjunto=None):
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(cuerpo, 'plain'))

    if adjunto:
        try:
            print("Cargando imagen...")
            attachment = open(adjunto, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {adjunto}')
            msg.attach(part)
        except:
            print("La ruta de imagen no es correcta, asegurate de introducir los datos necesarios y la extension y nombre de la imagen.")
            return 0

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        try:
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
            print("Correo electrónico enviado con éxito.\nGRACIAS POR USAR R3")
            time.sleep(2.5)
        except Exception as e:
            print(f"Ha surgido un error durante el envío del correo electrónico: {e}")
            time.sleep(2.5)

configuracion_correo = cargar_configuracion()

remitente = configuracion_correo['remitente']
password = configuracion_correo['password']
destinatario = input("Gmail al que quieres escribir: ")
asunto = input("Título del gmail: ")
cuerpo = input("Cuerpo del gmail: ")


adjuntar_imagen = input("¿Quieres adjuntar una imagen? (si/no): ").lower()

if adjuntar_imagen == 'si':
    ruta_imagen = input("Ruta de la imagen a adjuntar: ")
    enviar_correo(destinatario, asunto, cuerpo, remitente, password, adjunto=ruta_imagen)
else:
    enviar_correo(destinatario, asunto, cuerpo, remitente, password)