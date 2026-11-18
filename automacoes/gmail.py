import os
import base64

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Permissão somente para enviar e-mails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "token.json"
)


def conectar_gmail():

    credenciais = None

    if os.path.exists(TOKEN_FILE):
        credenciais = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not credenciais or not credenciais.valid:

        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())

        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credenciais = fluxo.run_local_server(
                port=0
            )

        with open(TOKEN_FILE, "w") as arquivo:
            arquivo.write(credenciais.to_json())

    return build(
        "gmail",
        "v1",
        credentials=credenciais
    )


def enviar_email(destinatario, assunto, mensagem):

    try:

        servico = conectar_gmail()

        email = MIMEText(
            mensagem,
            "plain",
            "utf-8"
        )

        email["to"] = destinatario
        email["subject"] = assunto

        mensagem_codificada = base64.urlsafe_b64encode(
            email.as_bytes()
        ).decode()

        corpo = {
            "raw": mensagem_codificada
        }

        resultado = servico.users().messages().send(
            userId="me",
            body=corpo
        ).execute()

        print("✅ E-mail enviado!")
        print("ID:", resultado["id"])

        return "E-mail enviado com sucesso."

    except Exception as erro:

        print()
        print("❌ ERRO AO ENVIAR E-MAIL")
        print(erro)
        print()

        return "Não consegui enviar o e-mail."