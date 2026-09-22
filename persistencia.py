import json
from pathlib import Path

ARQUIVO_DADOS = Path(__file__).with_name("tarefas.json")


def salvar(tarefas, caminho=ARQUIVO_DADOS):
    with Path(caminho).open("w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


def carregar(caminho=ARQUIVO_DADOS):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    try:
        with caminho.open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, list) else []
    except (OSError, json.JSONDecodeError):
        return []
