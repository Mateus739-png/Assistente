from audio.gravacao import classificar_comando_aula


def test_comando_iniciar():
    assert classificar_comando_aula("iniciar gravação da aula") == "iniciar"
    assert classificar_comando_aula("começar aula do teams") == "iniciar"


def test_comando_parar():
    assert classificar_comando_aula("parar gravação") == "parar"
    assert classificar_comando_aula("encerrar gravação da aula") == "parar"


def test_comando_nao_reconhecido():
    assert classificar_comando_aula("qual é a capital do brasil") is None
