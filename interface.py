import tkinter as tk
from tkinter import ttk

import threading
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime
import os
import logging

from automacoes import (
    executar_comando,
    tirar_print,
    obter_ultimo_print,
)

from ia.qwen import (
    perguntar,
    analisar_imagem,
)

from ia.tts import falar

from audio.gravacao import gravar_audio, gravar_aula_teams, classificar_comando_aula, gravar_aula_continua
from ia.whisper import transcrever

# ==========================================================
# LOG DO JARVIS
# ==========================================================

PASTA_LOGS = os.path.join(
    os.path.dirname(__file__),
    "logs",
)

os.makedirs(PASTA_LOGS, exist_ok=True)

ARQUIVO_LOG = os.path.join(
    PASTA_LOGS,
    "jarvis.log",
)

logging.basicConfig(
    filename=ARQUIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

LARGURA = 1000
ALTURA = 700


class JarvisInterface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)

        try:
            self.root.state("zoomed")
        except Exception:
            pass

        self.executor = ThreadPoolExecutor(max_workers=4)
        self.tts_lock = threading.Lock()
        self.tarefas_ativas = 0
        self.tarefas_lock = threading.Lock()
        self.gravacao_aula_thread = None
        self.gravacao_aula_stop = None

        self.criar_estilo()
        self.criar_interface()
        self.atualizar_status("🟢 ONLINE", "Pronto para receber comandos.")

    # ======================================================
    # ESTILO
    # ======================================================

    def criar_estilo(self):
        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except Exception:
            pass

        estilo.configure(
            "Jarvis.TButton",
            font=("Segoe UI", 11),
            padding=10,
        )

        estilo.configure(
            "Jarvis.TEntry",
            font=("Segoe UI", 12),
        )

    # ======================================================
    # INTERFACE
    # ======================================================

    def criar_interface(self):
        self.root.configure(bg="#0b0f14")
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        # CABEÇALHO
        cabecalho = tk.Frame(self.root, bg="#0b0f14")
        cabecalho.grid(row=0, column=0, sticky="ew", padx=35, pady=(25, 10))

        titulo = tk.Label(
            cabecalho,
            text="JARVIS",
            font=("Segoe UI", 26, "bold"),
            fg="#f0f6fc",
            bg="#0b0f14",
        )
        titulo.pack(side="left")

        self.status_label = tk.Label(
            cabecalho,
            text="● ONLINE",
            font=("Segoe UI", 11, "bold"),
            fg="#7ee787",
            bg="#0b0f14",
        )
        self.status_label.pack(side="right", pady=8)

        # ÁREA CENTRAL
        centro = tk.Frame(self.root, bg="#0b0f14")
        centro.grid(row=1, column=0, sticky="nsew", padx=35, pady=10)
        centro.grid_rowconfigure(0, weight=1)
        centro.grid_rowconfigure(1, weight=0)
        centro.grid_rowconfigure(2, weight=0)
        centro.grid_columnconfigure(0, weight=1)

        # INDICADOR CENTRAL
        indicador_frame = tk.Frame(centro, bg="#0b0f14")
        indicador_frame.grid(row=0, column=0, sticky="n", pady=(30, 15))

        self.indicador = tk.Label(
            indicador_frame,
            text="◉",
            font=("Segoe UI", 42),
            fg="#7ee787",
            bg="#0b0f14",
        )
        self.indicador.pack()

        self.estado_central = tk.Label(
            indicador_frame,
            text="ONLINE",
            font=("Segoe UI", 13, "bold"),
            fg="#8b949e",
            bg="#0b0f14",
        )
        self.estado_central.pack()

        self.descricao_central = tk.Label(
            indicador_frame,
            text="Pronto para receber comandos",
            font=("Segoe UI", 10),
            fg="#6e7681",
            bg="#0b0f14",
        )
        self.descricao_central.pack(pady=(5, 0))

        # CHAT
        self.chat = tk.Text(
            centro,
            bg="#11161d",
            fg="#d8dee9",
            insertbackground="white",
            font=("Segoe UI", 11),
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=25,
            pady=20,
            state="disabled",
        )
        self.chat.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # STATUS DOS SISTEMAS
        status_frame = tk.Frame(centro, bg="#0b0f14")
        status_frame.grid(row=2, column=0, sticky="ew", pady=(12, 12))

        status_texto = tk.Label(
            status_frame,
            text="Qwen  •  Whisper  •  Piper  •  Automação",
            font=("Segoe UI", 9),
            fg="#6e7681",
            bg="#0b0f14",
        )
        status_texto.pack()

        # ÁREA DE DIGITAÇÃO
        entrada_frame = tk.Frame(centro, bg="#0b0f14")
        entrada_frame.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        entrada_frame.grid_columnconfigure(0, weight=1)

        self.entrada = tk.Entry(
            entrada_frame,
            bg="#161b22",
            fg="#f0f6fc",
            insertbackground="white",
            font=("Segoe UI", 12),
            relief="flat",
            borderwidth=0,
        )
        self.entrada.grid(row=0, column=0, sticky="ew", ipady=14, padx=(0, 8))
        self.entrada.insert(0, "Digite um comando...")
        self.entrada.bind("<FocusIn>", lambda evento: self.limpar_placeholder())
        self.entrada.bind("<Return>", lambda evento: self.enviar_texto())

        botao_enviar = tk.Button(
            entrada_frame,
            text="➤",
            command=self.enviar_texto,
            bg="#238636",
            fg="white",
            activebackground="#2ea043",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 14, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
        )
        botao_enviar.grid(row=0, column=1, padx=4)

        botao_voz = tk.Button(
            entrada_frame,
            text="🎤",
            command=self.iniciar_voz,
            bg="#1f6feb",
            fg="white",
            activebackground="#388bfd",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 13),
            padx=14,
            pady=8,
            cursor="hand2",
        )
        botao_voz.grid(row=0, column=2, padx=4)

        botao_aula = tk.Button(
            entrada_frame,
            text="📚",
            command=self.iniciar_aula_teams,
            bg="#f08800",
            fg="white",
            activebackground="#ff9f1c",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 13),
            padx=14,
            pady=8,
            cursor="hand2",
        )
        botao_aula.grid(row=0, column=3, padx=4)

        botao_print = tk.Button(
            entrada_frame,
            text="📸",
            command=self.iniciar_analise_print,
            bg="#8957e5",
            fg="white",
            activebackground="#a371f7",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 13),
            padx=14,
            pady=8,
            cursor="hand2",
        )
        botao_print.grid(row=0, column=4, padx=4)

        rodape = tk.Label(
            self.root,
            text="Jarvis Local",
            font=("Segoe UI", 8),
            fg="#484f58",
            bg="#0b0f14",
        )
        rodape.grid(row=2, column=0, pady=(0, 10))

        # STATUS INDICADORES
        status_indicadores = tk.Frame(centro, bg="#0d1117")
        status_indicadores.grid(row=2, column=0, sticky="ew", pady=(12, 8))

        self.criar_status(status_indicadores, "🧠 Qwen", "ONLINE").pack(side="left", padx=5)
        self.criar_status(status_indicadores, "🎤 Whisper", "ONLINE").pack(side="left", padx=5)
        self.criar_status(status_indicadores, "🔊 Piper", "ONLINE").pack(side="left", padx=5)
        self.criar_status(status_indicadores, "⚙️ Automação", "ONLINE").pack(side="left", padx=5)

    # ======================================================
    # STATUS
    # ======================================================

    def criar_status(self, parent, nome, estado):
        frame = tk.Frame(parent, bg="#161b22", padx=10, pady=7)

        tk.Label(
            frame,
            text=nome,
            font=("Segoe UI", 9, "bold"),
            fg="#c9d1d9",
            bg="#161b22",
        ).pack(side="left")

        tk.Label(
            frame,
            text=f"  ● {estado}",
            font=("Segoe UI", 9),
            fg="#7ee787",
            bg="#161b22",
        ).pack(side="left")

        return frame

    def limpar_placeholder(self):
        if self.entrada.get() == "Digite um comando...":
            self.entrada.delete(0, "end")
            self.entrada.configure(fg="#f0f6fc")

    def atualizar_status(self, estado, descricao=""):
        self.root.after(0, lambda: self.status_label.config(text=estado))
        if descricao:
            self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", descricao))

    def atualizar_estado(self, estado):
        if not hasattr(self, "status_label"):
            return

        def atualizar():
            self.status_label.config(text=estado)

            if "OUVINDO" in estado:
                icone = "🎤"
                texto = "OUVINDO"
                descricao = "Estou ouvindo você..."
                cor = "#58a6ff"
            elif "PENSANDO" in estado or "EXECUTANDO" in estado:
                icone = "◌"
                texto = "PENSANDO"
                descricao = "Processando sua solicitação..."
                cor = "#d29922"
            elif "FALANDO" in estado:
                icone = "🔊"
                texto = "FALANDO"
                descricao = "Estou respondendo..."
                cor = "#a371f7"
            elif "ERRO" in estado:
                icone = "!"
                texto = "ERRO"
                descricao = "Algo deu errado."
                cor = "#f85149"
            else:
                icone = "◉"
                texto = "ONLINE"
                descricao = "Pronto para receber comandos."
                cor = "#7ee787"

            if hasattr(self, "indicador"):
                self.indicador.config(text=icone, fg=cor)
            if hasattr(self, "estado_central"):
                self.estado_central.config(text=texto, fg=cor)
            if hasattr(self, "descricao_central"):
                self.descricao_central.config(text=descricao)

        self.root.after(0, atualizar)

    def iniciar_tarefa(self):
        with self.tarefas_lock:
            self.tarefas_ativas += 1
            tarefas = self.tarefas_ativas

        self.atualizar_estado(f"🟡 PROCESSANDO ({tarefas})")

    def finalizar_tarefa(self):
        with self.tarefas_lock:
            self.tarefas_ativas = max(0, self.tarefas_ativas - 1)
            tarefas = self.tarefas_ativas

        if tarefas == 0:
            self.atualizar_estado("🟢 ONLINE")
        else:
            self.atualizar_estado(f"🟡 PROCESSANDO ({tarefas})")

    # ======================================================
    # CHAT
    # ======================================================

    def adicionar_mensagem(self, autor, mensagem):
        logging.info("TEXTO | %s", mensagem)

        horario = datetime.now().strftime("%H:%M")
        self.chat.config(state="normal")

        if autor == "VOCÊ":
            prefixo = f"\n[{horario}] VOCÊ:\n"
        else:
            prefixo = f"\n[{horario}] JARVIS:\n"

        self.chat.insert("end", prefixo)
        self.chat.insert("end", mensagem + "\n")
        self.chat.see("end")
        self.chat.config(state="disabled")

    # ======================================================
    # TEXTO
    # ======================================================

    def enviar_texto(self):
        texto = self.entrada.get().strip()

        if not texto:
            return

        self.entrada.delete(0, "end")
        self.adicionar_mensagem("VOCÊ", texto)
        self.iniciar_tarefa()
        self.executor.submit(self.processar_texto, texto)

    # ======================================================
    # PROCESSAR TEXTO
    # ======================================================

    def processar_texto(self, texto):
        try:
            comando_aula = classificar_comando_aula(texto)

            if comando_aula == "iniciar":
                if self.gravacao_aula_thread is not None and self.gravacao_aula_thread.is_alive():
                    self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", "A gravação da aula já está ativa."))
                    return

                self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", "Gravação da aula iniciada. Diga 'parar gravação da aula' para encerrar."))
                self.gravacao_aula_stop = threading.Event()
                self.gravacao_aula_thread = threading.Thread(
                    target=gravar_aula_continua,
                    args=(r"C:\Users\User\Downloads\Assistente\aula_teams.wav", self.gravacao_aula_stop),
                    daemon=True,
                )
                self.gravacao_aula_thread.start()
                return

            if comando_aula == "parar":
                if self.gravacao_aula_thread is not None and self.gravacao_aula_thread.is_alive():
                    self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", "Encerrando gravação da aula..."))
                    self.gravacao_aula_stop.set()
                    self.gravacao_aula_thread.join(timeout=15)
                    caminho = r"C:\Users\User\Downloads\Assistente\aula_teams.wav"
                    transcricao = transcrever(caminho)
                    resumo = perguntar(
                        "Você é um assistente acadêmico brasileiro. "
                        "Resuma esta aula em português do Brasil, em tópicos, conceitos e tarefas.\n\n"
                        f"TRANSCRIÇÃO:\n{transcricao}"
                    )
                    self.root.after(0, lambda r=resumo: self.adicionar_mensagem("JARVIS", r),)
                    with self.tts_lock:
                        falar(resumo)
                    self.gravacao_aula_thread = None
                    self.gravacao_aula_stop = None
                    return

                self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", "Não há gravação da aula ativa."))
                return

            self.atualizar_estado("⚙️ EXECUTANDO")

            resultado = executar_comando(texto)

            if resultado:
                logging.info("COMANDO | %s | RESULTADO | %s", texto, resultado)
                resposta = resultado
            else:
                logging.info("QWEN | %s", texto)
                self.atualizar_estado("🧠 PENSANDO")
                resposta = perguntar(texto)

            self.root.after(
                0,
                lambda r=resposta: self.adicionar_mensagem("JARVIS", r),
            )

            self.atualizar_estado("🔊 FALANDO")

            with self.tts_lock:
                falar(resposta)

        except Exception as erro:
            mensagem = f"Erro ao processar comando:\n{erro}"
            self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", mensagem))
            self.atualizar_estado("🔴 ERRO")
        finally:
            self.finalizar_tarefa()

    # ======================================================
    # VOZ
    # ======================================================

    def iniciar_voz(self):
        self.iniciar_tarefa()
        self.executor.submit(self.processar_voz)

    def processar_voz(self):
        try:
            self.atualizar_estado("🔴 OUVINDO")
            audio = gravar_audio()
            self.atualizar_estado("📝 TRANSCRIBINDO")

            texto = transcrever(audio)
            logging.info("VOZ | %s", texto)

            if not texto:
                self.finalizar_tarefa()
                return

            self.root.after(
                0,
                lambda t=texto: self.adicionar_mensagem("VOCÊ", t),
            )

            self.processar_texto(texto)

        except Exception as erro:
            mensagem = f"Erro no microfone:\n{erro}"
            self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", mensagem))
            self.atualizar_estado("🔴 ERRO")
            self.finalizar_tarefa()

    # ======================================================
    # AULA DO TEAMS
    # ======================================================

    def iniciar_aula_teams(self):
        self.iniciar_tarefa()
        self.executor.submit(self.processar_aula_teams)

    def processar_aula_teams(self):
        try:
            self.atualizar_estado("🎧 GRAVANDO AULA")
            audio = gravar_aula_teams(tempo_maximo=600)
            self.atualizar_estado("📝 TRANSCRIBINDO AULA")

            texto = transcrever(audio)
            logging.info("AULA | %s", texto)

            if not texto:
                self.root.after(
                    0,
                    lambda: self.adicionar_mensagem("JARVIS", "Não consegui extrair áudio da aula."),
                )
                self.finalizar_tarefa()
                return

            self.root.after(
                0,
                lambda t=texto: self.adicionar_mensagem("VOCÊ", "Transcrição da aula:\n" + t[:5000]),
            )

            self.atualizar_estado("🧠 RESUMINDO AULA")

            prompt = (
                "Você é um assistente acadêmico brasileiro. "
                "Resuma esta aula em português do Brasil. "
                "Use estrutura clara: tema principal, tópicos, conceitos-chave, "
                "resumo em 5 itens e tarefas ou pendências. "
                "Se houver algo mal explicado ou incompleto, deixe explícito.\n\n"
                f"TRANSCRIÇÃO:\n{texto}"
            )

            resumo = perguntar(prompt)

            self.root.after(
                0,
                lambda r=resumo: self.adicionar_mensagem("JARVIS", r),
            )

            self.atualizar_estado("🔊 FALANDO")

            with self.tts_lock:
                falar(resumo)

        except Exception as erro:
            mensagem = f"Erro ao gravar e resumir a aula:\n{erro}"
            self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", mensagem))
            self.atualizar_estado("🔴 ERRO")
        finally:
            self.finalizar_tarefa()

    # ======================================================
    # ANÁLISE DE PRINT
    # ======================================================

    def iniciar_analise_print(self):
        self.iniciar_tarefa()
        self.executor.submit(self.processar_analise_print)

    def processar_analise_print(self):
        try:
            self.root.after(0, lambda: self.status_label.config(text="📸 TIRANDO PRINT"))
            tirar_print()
            self.root.after(0, lambda: self.status_label.config(text="🧠 ANALISANDO"))

            ultimo_print = obter_ultimo_print()

            if ultimo_print is None:
                self.root.after(
                    0,
                    lambda: self.adicionar_mensagem("JARVIS", "Não encontrei o print para analisar."),
                )
                self.finalizar_tarefa()
                return

            resposta = analisar_imagem(
                ultimo_print,
                "Analise este print cuidadosamente e me diga o que aparece nele. "
                "Se houver erros, mensagens ou informações importantes, explique "
                "de forma clara e direta.",
            )

            self.root.after(
                0,
                lambda r=resposta: self.adicionar_mensagem("JARVIS", r),
            )
            self.root.after(0, lambda: self.status_label.config(text="🔵 FALANDO"))

            with self.tts_lock:
                falar(resposta)

            self.finalizar_tarefa()

        except Exception as erro:
            mensagem = f"Erro ao analisar o print:\n{erro}"
            self.root.after(0, lambda: self.adicionar_mensagem("JARVIS", mensagem))
            self.finalizar_tarefa()

    # ======================================================
    # INICIAR
    # ======================================================

    def iniciar(self):
        self.adicionar_mensagem("JARVIS", "Interface iniciada. Estou pronto.")
        self.root.mainloop()


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    interface = JarvisInterface()
    interface.iniciar()
