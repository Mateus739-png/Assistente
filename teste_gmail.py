from automacoes.gmail import enviar_email


destinatario = "mateusoli764@gmail.com"

enviar_email(
    destinatario,
    "Teste do Jarvis",
    "Olá! Este é um teste de envio de e-mail pelo Jarvis."
)