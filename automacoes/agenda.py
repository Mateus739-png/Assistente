import json
import os
import threading
import time
from datetime import datetime, timedelta


ARQUIVO_AGENDA = r"C:\Users\User\Downloads\Assistente\memoria\agenda.json"


def carregar_agenda():
    if not os.path.exists(ARQUIVO_AGENDA):
        return []

    try:
        with open(ARQUIVO_AGENDA, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, list):
            return dados

    except (json.JSONDecodeError, OSError):
        pass

    return []


def salvar_agenda(agenda):
    os.makedirs(
        os.path.dirname(ARQUIVO_AGENDA),
        exist_ok=True
    )

    with open(ARQUIVO_AGENDA, "w", encoding="utf-8") as arquivo:
        json.dump(
            agenda,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def adicionar_compromisso(data_hora, descricao, aviso=0):
    agenda = carregar_agenda()

    compromisso = {
        "id": int(time.time()),
        "data_hora": data_hora,
        "descricao": descricao,
        "aviso": aviso,
        "avisado": False
    }

    agenda.append(compromisso)

    salvar_agenda(agenda)

    return compromisso


def listar_agenda(data=None):
    agenda = carregar_agenda()

    if data:
        resultados = []

        for compromisso in agenda:
            if compromisso["data_hora"].startswith(data):
                resultados.append(compromisso)

        return resultados

    return sorted(
        agenda,
        key=lambda x: x["data_hora"]
    )


def cancelar_compromisso(id_compromisso):
    agenda = carregar_agenda()

    nova_agenda = [
        compromisso
        for compromisso in agenda
        if compromisso["id"] != id_compromisso
    ]

    if len(nova_agenda) == len(agenda):
        return False

    salvar_agenda(nova_agenda)

    return True


def iniciar_monitor_agenda(falar):

    def monitorar():

        while True:

            try:
                agenda = carregar_agenda()

                agora = datetime.now()

                alterou = False

                for compromisso in agenda:

                    if compromisso.get("avisado"):
                        continue

                    horario = datetime.fromisoformat(
                        compromisso["data_hora"]
                    )

                    aviso = compromisso.get("aviso", 0)

                    horario_aviso = horario - timedelta(
                        minutes=aviso
                    )

                    if agora >= horario_aviso:

                        print()
                        print("======================================")
                        print("📅 LEMBRETE DA AGENDA")
                        print("======================================")
                        print(compromisso["descricao"])
                        print()

                        # ==================================
                        # DATA E HORÁRIO DO COMPROMISSO
                        # ==================================

                        data_compromisso = datetime.fromisoformat(
                            compromisso["data_hora"]
                        )

                        dias_semana = [
                            "segunda-feira",
                            "terça-feira",
                            "quarta-feira",
                            "quinta-feira",
                            "sexta-feira",
                            "sábado",
                            "domingo"
                        ]

                        meses = [
                            "janeiro",
                            "fevereiro",
                            "março",
                            "abril",
                            "maio",
                            "junho",
                            "julho",
                            "agosto",
                            "setembro",
                            "outubro",
                            "novembro",
                            "dezembro"
                        ]

                        dia_semana = dias_semana[
                            data_compromisso.weekday()
                        ]

                        mes = meses[
                            data_compromisso.month - 1
                        ]

                        hora = data_compromisso.hour
                        minuto = data_compromisso.minute

                        if minuto == 0:
                            horario_texto = f"{hora} horas"
                        else:
                            horario_texto = (
                                f"{hora} horas e "
                                f"{minuto} minutos"
                            )

                        mensagem = (
                            f"Você tem um compromisso "
                            f"{dia_semana}, "
                            f"dia {data_compromisso.day} "
                            f"de {mes}, "
                            f"às {horario_texto}: "
                            f"{compromisso['descricao']}"
                        )

                        print("🔊 Jarvis:")
                        print(mensagem)
                        print()

                        falar(mensagem)

                        compromisso["avisado"] = True

                        alterou = True

                if alterou:
                    salvar_agenda(agenda)

            except Exception as erro:

                print(
                    "⚠️ Erro no monitor da agenda:",
                    erro
                )

            time.sleep(10)

    threading.Thread(
        target=monitorar,
        daemon=True
    ).start()