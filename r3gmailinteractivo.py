import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import configparser
import tkinter as tk
from tkinter import filedialog
import base64
from PIL import Image, ImageTk
import os

class InterfazCorreo:
    def __init__(self, master):
        self.master = master
        master.title("R3 - EnviaGmail")
        master.geometry("300x215")  # Tamaño ajustado
        master.configure(bg="#2C3E50")  # Fondo azul oscuro

        text_color = "#ECF0F1"  # Color de texto blanco

        self.label_destinatario = tk.Label(master, text="Destinatario:", bg="#2C3E50", fg=text_color)
        self.label_destinatario.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        self.entry_destinatario = tk.Entry(master, width=30, bg="#34495E", fg=text_color)  # Fondo azul oscuro, Texto blanco
        self.entry_destinatario.grid(row=0, column=1, padx=10, pady=5)

        self.label_asunto = tk.Label(master, text="Titulo:", bg="#2C3E50", fg=text_color)
        self.label_asunto.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        self.entry_asunto = tk.Entry(master, width=30, bg="#34495E", fg=text_color)
        self.entry_asunto.grid(row=1, column=1, padx=10, pady=5)

        self.label_cuerpo = tk.Label(master, text="Mensaje:", bg="#2C3E50", fg=text_color)
        self.label_cuerpo.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.entry_cuerpo = tk.Entry(master, width=30, bg="#34495E", fg=text_color)
        self.entry_cuerpo.grid(row=2, column=1, padx=10, pady=5)

        self.var_adjuntar_archivo = tk.IntVar()
        self.check_adjuntar_archivo = tk.Checkbutton(master, text="Adjuntar archivos", variable=self.var_adjuntar_archivo, command=self.toggle_adjuntar, bg="#2C3E50", fg="#000000")
        self.check_adjuntar_archivo.grid(row=3, column=0, columnspan=2, pady=5)

        self.button_adjuntar = tk.Button(master, text="Seleccionar archivos", state=tk.DISABLED, command=self.adjuntar_archivos, bg="#3498DB", fg=text_color)
        self.button_adjuntar.grid(row=4, column=0, columnspan=2, pady=5)

        self.image_label = tk.Label(master, text="Vista previa de la imagen", bg="#2C3E50", fg=text_color)
        self.image_label.grid(row=6, column=0, columnspan=2, pady=5)
        master.minsize(300, 240)

        self.button_enviar = tk.Button(master, text="Enviar correo", command=self.enviar_correo, bg="#E74C3C", fg=text_color)
        self.button_enviar.grid(row=5, column=0, columnspan=2, pady=10)

        self.adjuntos_paths = []  # Inicializar la lista de archivos adjuntos

    def toggle_adjuntar(self):
        if self.var_adjuntar_archivo.get():
            self.button_adjuntar['state'] = tk.NORMAL
        else:
            self.button_adjuntar['state'] = tk.DISABLED

    def adjuntar_archivos(self):
        files = filedialog.askopenfilenames(title="Seleccionar Archivos", filetypes=[("Archivos", "*.*")])
        if files:
            self.adjuntos_paths = list(files)
            self.mostrar_vista_previa()

    def mostrar_vista_previa(self):
        if self.adjuntos_paths:
            img_path = self.adjuntos_paths[0]
            image = Image.open(img_path)
            image.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Ajustar el tamaño de la ventana permitiendo que sea más larga
            width, height = max(image.size[0], 300), max(image.size[1], 385)
            self.master.geometry(f"{width}x{height}")


    def enviar_correo(self):
        destinatario = self.entry_destinatario.get()
        asunto = self.entry_asunto.get()
        cuerpo = self.entry_cuerpo.get()
        adjuntos = self.adjuntos_paths if self.adjuntos_paths else None

        configuracion_correo = cargar_configuracion()
        remitente = configuracion_correo['remitente']
        password = configuracion_correo['password']

        enviar_correo(destinatario, asunto, cuerpo, remitente, password, adjuntos)

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
        for adjunto_path in adjunto:
            try:
                print(f"Cargando archivo adjunto: {adjunto_path}")
                attachment = open(adjunto_path, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={adjunto_path}')
                msg.attach(part)
                print("Archivo adjunto cargado con éxito.")
            except Exception as e:
                print(f"Error al adjuntar el archivo {adjunto_path}: {str(e)}")

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        try:
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
            print("Correo electrónico enviado con éxito.\nGRACIAS POR USAR R3")
            time.sleep(2.5)
        except Exception as e:
            print(f"Ha surgido un error durante el envío del correo electrónico: {str(e)}")
            time.sleep(2.5)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCorreo(root)
    root.mainloop()