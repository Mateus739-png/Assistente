
from pathlib import Path
from datetime import datetime

pasta = Path(__file__).resolve().parent
arquivo = pasta / "interface.py"

if not arquivo.exists():
    raise FileNotFoundError(f"Não encontrei: {arquivo}")

codigo = arquivo.read_text(encoding="utf-8")

if "PERFIL_PUBLICO_ADICIONADO" in codigo:
    raise RuntimeError("O perfil público já foi adicionado.")

# Backup antes de alterar
backup = pasta / f"interface_backup_{datetime.now():%Y%m%d_%H%M%S}.py"
backup.write_text(codigo, encoding="utf-8")

def substituir(antigo, novo, descricao):
    global codigo
    if antigo not in codigo:
        raise RuntimeError(
            f"Não encontrei o trecho necessário: {descricao}. "
            "O arquivo original não será sobrescrito."
        )
    codigo = codigo.replace(antigo, novo, 1)

substituir(
    "        self.tarefas_lock = threading.Lock()\n",
    "        self.tarefas_lock = threading.Lock()\n"
    "        self.perfil_atual = 'Privado'\n"
    "        # PERFIL_PUBLICO_ADICIONADO\n",
    "inicialização do perfil",
)

substituir(
    '        self.status_label.pack(side="right", pady=8)\n',
    '        self.status_label.pack(side="right", pady=8)\n'
    '\n'
    '        tk.Label(\n'
    '            cabecalho, text="Perfil:",\n'
    '            font=("Segoe UI", 10), fg="#c9d1d9", bg="#0b0f14"\n'
    '        ).pack(side="right", padx=(12, 5))\n'
    '\n'
    '        self.seletor_perfil = ttk.Combobox(\n'
    '            cabecalho, values=("Privado", "Público"),\n'
    '            state="readonly", width=10\n'
    '        )\n'
    '        self.seletor_perfil.set("Privado")\n'
    '        self.seletor_perfil.pack(side="right", pady=8)\n'
    '        self.seletor_perfil.bind(\n'
    '            "<<ComboboxSelected>>", self.alterar_perfil\n'
    '        )\n',
    "seletor de perfil no cabeçalho",
)

substituir(
    "    # ======================================================\n"
    "    # STATUS\n"
    "    # ======================================================\n",
    "    def alterar_perfil(self, evento=None):\n"
    "        self.perfil_atual = self.seletor_perfil.get()\n"
    "        if self.perfil_atual == 'Público':\n"
    "            self.atualizar_status(\n"
    "                '🌐 PERFIL PÚBLICO',\n"
    "                'Modo público: conversa com a IA. Comandos e análise de tela bloqueados.'\n"
    "            )\n"
    "        else:\n"
    "            self.atualizar_status(\n"
    "                '🔒 PERFIL PRIVADO',\n"
    "                'Modo privado ativado.'\n"
    "            )\n"
    "\n"
    "    # ======================================================\n"
    "    # STATUS\n"
    "    # ======================================================\n",
    "método de alteração de perfil",
)

substituir(
    "    def processar_texto(self, texto):\n"
    "        try:\n"
    "            self.atualizar_estado(\"⚙️ EXECUTANDO\")\n"
    "\n"
    "            resultado = executar_comando(texto)\n",
    "    def processar_texto(self, texto):\n"
    "        try:\n"
    "            if self.perfil_atual == 'Público':\n"
    "                # Neste ramo, não chamar executar_comando nem memória privada.\n"
    "                self.atualizar_estado('🧠 PENSANDO')\n"
    "                resposta = perguntar(texto)\n"
    "            else:\n"
    "                self.atualizar_estado('⚙️ EXECUTANDO')\n"
    "                resultado = executar_comando(texto)\n"
    "                if resultado:\n"
    "                    logging.info('COMANDO | %s | RESULTADO | %s', texto, resultado)\n"
    "                    resposta = resultado\n"
    "                else:\n"
    "                    logging.info('QWEN | %s', texto)\n"
    "                    self.atualizar_estado('🧠 PENSANDO')\n"
    "                    resposta = perguntar(texto)\n",
    "roteamento seguro do processamento",
)

# O bloco antigo de resultado ainda ficou abaixo da substituição?
# Removemos somente a duplicação exata que existia no código original.
duplicado = (
    "\n"
    "            if resultado:\n"
    "                logging.info(\"COMANDO | %s | RESULTADO | %s\", texto, resultado)\n"
    "                resposta = resultado\n"
    "            else:\n"
    "                logging.info(\"QWEN | %s\", texto)\n"
    "                self.atualizar_estado(\"🧠 PENSANDO\")\n"
    "                resposta = perguntar(texto)\n"
)
if duplicado in codigo:
    codigo = codigo.replace(duplicado, "\n", 1)

substituir(
    "    def iniciar_analise_print(self):\n"
    "        self.iniciar_tarefa()\n",
    "    def iniciar_analise_print(self):\n"
    "        if self.perfil_atual == 'Público':\n"
    "            self.adicionar_mensagem(\n"
    "                'JARVIS', 'A análise de tela está bloqueada no perfil público.'\n"
    "            )\n"
    "            return\n"
    "        self.iniciar_tarefa()\n",
    "bloqueio de análise de tela",
)

# Valida a sintaxe antes de gravar
compile(codigo, str(arquivo), "exec")
arquivo.write_text(codigo, encoding="utf-8")

print("Perfil Público adicionado.")
print(f"Backup salvo em: {backup}")
print("O perfil público conversa com o Qwen e bloqueia automações.")
print("A pesquisa na internet será conectada na próxima etapa.")
input("Pressione Enter para sair...")
