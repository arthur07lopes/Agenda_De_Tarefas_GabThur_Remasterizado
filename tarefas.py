PRIORIDADES = ["Baixa", "Média", "Alta"]
STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"


class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = []
        self.proximo_id = 1

    def adicionar(self, descricao, prioridade):
        descricao = descricao.strip()
        if not descricao:
            raise ValueError("A descrição não pode estar vazia.")

        tarefa = {
            "id": self.proximo_id,
            "descricao": descricao,
            "prioridade": prioridade,
            "status": STATUS_PENDENTE,
        }
        self.tarefas.append(tarefa)
        self.proximo_id += 1
        return tarefa

    def editar(self, tarefa_id, nova_descricao=None, nova_prioridade=None):
        tarefa = self.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise ValueError("Tarefa não encontrada.")

        if nova_descricao is not None:
            nova_descricao = nova_descricao.strip()
            if not nova_descricao:
                raise ValueError("A descrição não pode estar vazia.")
            tarefa["descricao"] = nova_descricao

        if nova_prioridade is not None:
            tarefa["prioridade"] = nova_prioridade

        return tarefa

    def alternar_status(self, tarefa_id):
        tarefa = self.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise ValueError("Tarefa não encontrada.")
        if tarefa["status"] == STATUS_CONCLUIDA:
            tarefa["status"] = STATUS_PENDENTE
        else:
            tarefa["status"] = STATUS_CONCLUIDA
        return tarefa

    def remover(self, tarefa_id):
        tarefa = self.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise ValueError("Tarefa não encontrada.")
        self.tarefas.remove(tarefa)

    def buscar_por_id(self, tarefa_id):
        for tarefa in self.tarefas:
            if tarefa["id"] == tarefa_id:
                return tarefa
        return None

    def filtrar(self, status=None, prioridade=None, texto=None):
        resultado = self.tarefas

        if status and status != "Todos":
            resultado = [t for t in resultado if t["status"] == status]

        if prioridade and prioridade != "Todas":
            resultado = [t for t in resultado if t["prioridade"] == prioridade]

        if texto:
            texto = texto.lower()
            resultado = [t for t in resultado if texto in t["descricao"].lower()]

        return resultado

    def carregar_lista(self, lista_tarefas):
        self.tarefas = lista_tarefas
        if self.tarefas:
            self.proximo_id = max(t["id"] for t in self.tarefas) + 1
