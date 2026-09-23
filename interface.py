import wx

from tarefas import GerenciadorTarefas, PRIORIDADES, STATUS_PENDENTE, STATUS_CONCLUIDA
from bandeja import BandejaAgendaTarefas
import persistencia

OPCOES_STATUS = ["Todos", STATUS_PENDENTE, STATUS_CONCLUIDA]
OPCOES_PRIORIDADE_FILTRO = ["Todas"] + PRIORIDADES
COR_AZUL = "#0672CE"
COR_AZUL_ESCURO = "#003B5C"
COR_AZUL_CLARO = "#D9EAF7"
COR_AZUL_MEDIO = "#0B5CAB"
COR_FUNDO = "#F5F7FA"
COR_TEXTO = "#1A1A1A"
COR_PRATA = "#E7EEF5"


class AgendaTarefasFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Agenda de Tarefas", size=(980, 720))
        self.SetMinSize((820, 620))
        self.SetBackgroundColour(wx.Colour(COR_FUNDO))

        self.gerenciador = GerenciadorTarefas()
        self._saida_confirmada = False

        self._criar_interface()
        self._configurar_atalhos()
        self.bandeja = BandejaAgendaTarefas(self)
        self._carregar_tarefas()

        self.Centre()
        self.Show()

    def _criar_interface(self):
        self.painel = wx.Panel(self, style=wx.TAB_TRAVERSAL)
        painel = self.painel
        painel.SetBackgroundColour(wx.Colour(COR_FUNDO))
        painel_sizer = wx.BoxSizer(wx.VERTICAL)

        cabecalho = wx.Panel(painel)
        cabecalho.SetBackgroundColour(wx.Colour(COR_AZUL_ESCURO))
        cabecalho_sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(cabecalho, label="AGENDA DE TAREFAS GABTHUR")
        fonte_titulo = wx.Font(21, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(fonte_titulo)
        titulo.SetForegroundColour(wx.WHITE)
        titulo.SetName("Título da agenda")

        subtitulo = wx.StaticText(cabecalho, label="Organize suas tarefas com clareza e praticidade.")
        subtitulo.SetForegroundColour(wx.Colour(COR_PRATA))
        subtitulo.SetName("Descrição da agenda")
        cabecalho_sizer.Add(titulo, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 16)
        cabecalho_sizer.Add(subtitulo, 0, wx.ALL | wx.ALIGN_CENTER, 8)
        cabecalho.SetSizer(cabecalho_sizer)
        painel_sizer.Add(cabecalho, 0, wx.EXPAND | wx.BOTTOM, 18)

        entrada_sizer = wx.BoxSizer(wx.HORIZONTAL)

        rotulo_tarefa = wx.StaticText(painel, label="&Descrição da tarefa:")
        self.campo_tarefa = wx.TextCtrl(painel, style=wx.TE_PROCESS_ENTER)
        self.campo_tarefa.SetName("Descrição da tarefa")
        self.campo_tarefa.SetHelpText("Digite a descrição da nova tarefa.")
        self.campo_tarefa.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        rotulo_prioridade = wx.StaticText(painel, label="&Prioridade da tarefa:")
        self.combo_prioridade = wx.Choice(painel, choices=PRIORIDADES, size=(150, -1))
        self.combo_prioridade.SetStringSelection("Média")
        self.combo_prioridade.SetName("Prioridade da tarefa")
        self.combo_prioridade.SetHelpText("Escolha a prioridade da nova tarefa.")
        self.combo_prioridade.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.botao_adicionar = wx.Button(painel, label="&Adicionar")
        self.botao_adicionar.SetName("Adicionar tarefa")
        self.botao_adicionar.SetHelpText("Adiciona a tarefa preenchida.")
        self.botao_adicionar.SetBackgroundColour(wx.Colour(COR_AZUL))
        self.botao_adicionar.SetForegroundColour(wx.WHITE)
        self.botao_adicionar.SetMinSize(self.FromDIP((130, 40)))
        self.botao_adicionar.SetSize(self.FromDIP((130, 40)))
        self.botao_adicionar.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        entrada_sizer.Add(rotulo_tarefa, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        entrada_sizer.Add(self.campo_tarefa, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        entrada_sizer.Add(rotulo_prioridade, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        entrada_sizer.Add(self.combo_prioridade, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        entrada_sizer.Add(self.botao_adicionar, 0, wx.ALIGN_CENTER_VERTICAL)
        entrada_caixa = wx.BoxSizer(wx.VERTICAL)
        titulo_entrada = wx.StaticText(painel, label="NOVA TAREFA")
        titulo_entrada.SetForegroundColour(wx.Colour(COR_AZUL_ESCURO))
        titulo_entrada.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        entrada_caixa.Add(titulo_entrada, 0, wx.LEFT | wx.BOTTOM, 4)
        entrada_caixa.Add(entrada_sizer, 1, wx.EXPAND)
        painel_sizer.Add(entrada_caixa, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)

        filtro_sizer = wx.BoxSizer(wx.HORIZONTAL)

        rotulo_status = wx.StaticText(painel, label="Filtro de &status:")
        self.combo_filtro_status = wx.Choice(painel, choices=OPCOES_STATUS, size=(140, -1))
        self.combo_filtro_status.SetStringSelection("Todos")
        self.combo_filtro_status.SetName("Filtrar por status")
        self.combo_filtro_status.SetHelpText("Filtra as tarefas pelo status.")
        self.combo_filtro_status.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        rotulo_filtro_prioridade = wx.StaticText(painel, label="Filtro de &prioridade:")
        self.combo_filtro_prioridade = wx.Choice(
            painel, choices=OPCOES_PRIORIDADE_FILTRO, size=(150, -1)
        )
        self.combo_filtro_prioridade.SetStringSelection("Todas")
        self.combo_filtro_prioridade.SetName("Filtrar por prioridade")
        self.combo_filtro_prioridade.SetHelpText("Filtra as tarefas pela prioridade.")
        self.combo_filtro_prioridade.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        rotulo_busca = wx.StaticText(painel, label="Buscar:")
        self.campo_busca = wx.TextCtrl(painel)
        self.campo_busca.SetName("Buscar tarefa por texto")
        self.campo_busca.SetHelpText("Digite um texto para pesquisar tarefas.")
        self.campo_busca.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.botao_limpar_filtros = wx.Button(painel, label="Limpar filtros")
        self.botao_limpar_filtros.SetName("Limpar filtros")
        self.botao_limpar_filtros.SetHelpText("Remove os filtros aplicados.")
        self.botao_limpar_filtros.SetBackgroundColour(wx.Colour(COR_AZUL_CLARO))
        self.botao_limpar_filtros.SetForegroundColour(wx.Colour(COR_AZUL_ESCURO))
        self.botao_limpar_filtros.SetMinSize(self.FromDIP((145, 40)))
        self.botao_limpar_filtros.SetSize(self.FromDIP((145, 40)))
        self.botao_limpar_filtros.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        filtro_sizer.Add(rotulo_status, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        filtro_sizer.Add(self.combo_filtro_status, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        filtro_sizer.Add(rotulo_filtro_prioridade, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        filtro_sizer.Add(self.combo_filtro_prioridade, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        filtro_sizer.Add(rotulo_busca, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        filtro_sizer.Add(self.campo_busca, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        filtro_sizer.Add(self.botao_limpar_filtros, 0, wx.ALIGN_CENTER_VERTICAL)

        filtro_caixa = wx.BoxSizer(wx.VERTICAL)
        titulo_filtros = wx.StaticText(painel, label="FILTROS")
        titulo_filtros.SetForegroundColour(wx.Colour(COR_AZUL_ESCURO))
        titulo_filtros.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        filtro_caixa.Add(titulo_filtros, 0, wx.LEFT | wx.BOTTOM, 4)
        filtro_caixa.Add(filtro_sizer, 1, wx.EXPAND)
        painel_sizer.Add(filtro_caixa, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)

        rotulo_lista = wx.StaticText(painel, label="&Lista de tarefas:")
        rotulo_lista.SetName("Rótulo da lista de tarefas")
        painel_sizer.Add(rotulo_lista, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        self.lista = wx.ListCtrl(
            painel,
            name="Lista de tarefas",
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES |
            wx.VSCROLL | wx.HSCROLL | wx.BORDER_SUNKEN,
        )
        self.lista.SetHelpText("Lista de tarefas. Use as setas para escolher uma tarefa.")
        self.lista.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.lista.SetMinSize(self.FromDIP((700, 360)))
        self.lista.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.lista.InsertColumn(0, "ID", width=50)
        self.lista.InsertColumn(1, "Descrição da Tarefa", width=350)
        self.lista.InsertColumn(2, "Prioridade", width=110)
        self.lista.InsertColumn(3, "Status", width=120)

        painel_sizer.Add(self.lista, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 15)

        self.botoes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_editar = wx.Button(painel, label="&Editar Tarefa")
        self.botao_concluir = wx.Button(painel, label="&Concluir tarefa")
        self.botao_remover = wx.Button(painel, label="&Remover Tarefa")
        self.botao_editar.SetName("Editar tarefa")
        self.botao_editar.SetHelpText("Edita a tarefa selecionada.")
        self.botao_concluir.SetName("Concluir tarefa")
        self.botao_concluir.SetHelpText("Conclui ou reabre a tarefa selecionada.")
        self.botao_remover.SetName("Remover tarefa")
        self.botao_remover.SetHelpText("Remove a tarefa selecionada.")
        self.botao_editar.SetBackgroundColour(wx.Colour(COR_AZUL_CLARO))
        self.botao_editar.SetForegroundColour(wx.Colour(COR_AZUL_ESCURO))
        self.botao_concluir.SetBackgroundColour(wx.Colour(COR_AZUL_MEDIO))
        self.botao_concluir.SetForegroundColour(wx.WHITE)
        self.botao_remover.SetBackgroundColour(wx.Colour(COR_AZUL_ESCURO))
        self.botao_remover.SetForegroundColour(wx.WHITE)
        fonte_botao = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.botao_editar.SetFont(fonte_botao)
        self.botao_concluir.SetFont(fonte_botao)
        self.botao_remover.SetFont(fonte_botao)
        self.botao_editar.SetMinSize(self.FromDIP((145, 40)))
        self.botao_concluir.SetMinSize(self.FromDIP((175, 40)))
        self.botao_remover.SetMinSize(self.FromDIP((155, 40)))
        self.botao_editar.Hide()
        self.botao_concluir.Hide()
        self.botao_remover.Hide()
        self.botoes_sizer.Add(self.botao_editar, 0, wx.RIGHT, 10)
        self.botoes_sizer.Add(self.botao_concluir, 0, wx.RIGHT, 10)
        self.botoes_sizer.Add(self.botao_remover, 0)
        self.botoes_sizer.SetItemMinSize(self.botao_editar, self.FromDIP((145, 40)))
        self.botoes_sizer.SetItemMinSize(self.botao_concluir, self.FromDIP((175, 40)))
        self.botoes_sizer.SetItemMinSize(self.botao_remover, self.FromDIP((155, 40)))
        painel_sizer.Add(self.botoes_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        painel.SetSizer(painel_sizer)

        self.CreateStatusBar()
        self.SetStatusText("Pronto. Digite uma tarefa e pressione Adicionar.")

        self.botao_adicionar.Bind(wx.EVT_BUTTON, self.ao_adicionar)
        self.campo_tarefa.Bind(wx.EVT_TEXT_ENTER, self.ao_adicionar)
        self.botao_editar.Bind(wx.EVT_BUTTON, self.ao_editar)
        self.botao_concluir.Bind(wx.EVT_BUTTON, self.ao_concluir)
        self.botao_remover.Bind(wx.EVT_BUTTON, self.ao_remover)
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ao_selecionar)
        self.Bind(wx.EVT_CLOSE, self.ao_fechar)

        self.combo_filtro_status.Bind(wx.EVT_CHOICE, self.ao_filtrar)
        self.combo_filtro_prioridade.Bind(wx.EVT_CHOICE, self.ao_filtrar)
        self.campo_busca.Bind(wx.EVT_TEXT, self.ao_filtrar)
        self.botao_limpar_filtros.Bind(wx.EVT_BUTTON, self.ao_limpar_filtros)
        self.lista.Bind(wx.EVT_SIZE, self.ao_redimensionar_lista)

        self._definir_ordem_tab()
        self.campo_tarefa.SetFocus()
        self._ajustar_coluna_status()

    def _definir_ordem_tab(self):
        controles = [
            self.campo_tarefa,
            self.combo_prioridade,
            self.botao_adicionar,
            self.combo_filtro_status,
            self.combo_filtro_prioridade,
            self.campo_busca,
            self.botao_limpar_filtros,
            self.lista,
            self.botao_editar,
            self.botao_concluir,
            self.botao_remover,
        ]
        for anterior, atual in zip(controles, controles[1:]):
            atual.MoveAfterInTabOrder(anterior)

    def _configurar_atalhos(self):
        id_novo = wx.NewIdRef()
        id_remover = wx.NewIdRef()
        id_concluir = wx.NewIdRef()
        id_editar = wx.NewIdRef()

        self.Bind(wx.EVT_MENU, lambda e: self.campo_tarefa.SetFocus(), id=id_novo)
        self.Bind(wx.EVT_MENU, self.ao_remover, id=id_remover)
        self.Bind(wx.EVT_MENU, self.ao_concluir, id=id_concluir)
        self.Bind(wx.EVT_MENU, self.ao_editar, id=id_editar)

        tabela = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord("N"), id_novo),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, id_remover),
            (wx.ACCEL_CTRL, wx.WXK_RETURN, id_concluir),
            (wx.ACCEL_CTRL, ord("E"), id_editar),
        ])
        self.SetAcceleratorTable(tabela)

    def ao_fechar(self, evento):
        if self._saida_confirmada or not evento.CanVeto():
            self.bandeja.RemoveIcon()
            self.bandeja.Destroy()
            self.Destroy()
            return

        evento.Veto()
        self.Hide()
        self.SetStatusText(
            "A Agenda de Tarefas GabThur continua em segundo plano. "
            "Use o ícone na bandeja para reabrir ou sair."
        )

    def sair_definitivamente(self):
        resposta = wx.MessageBox(
            "Deseja realmente sair da Agenda de Tarefas GabThur?",
            "Confirmar saída",
            wx.YES_NO | wx.ICON_QUESTION,
        )
        if resposta == wx.YES:
            self._saida_confirmada = True
            self.Close()

    def ao_adicionar(self, evento):
        try:
            tarefa = self.gerenciador.adicionar(
                self.campo_tarefa.GetValue(), self.combo_prioridade.GetStringSelection()
            )
        except ValueError as erro:
            self.SetStatusText(str(erro))
            self.campo_tarefa.SetFocus()
            return

        persistencia.salvar(self.gerenciador.tarefas)
        self.campo_tarefa.Clear()
        self.SetStatusText(f"Tarefa '{tarefa['descricao']}' adicionada.")
        self._atualizar_lista(tarefa_id=tarefa["id"])
        self.campo_tarefa.SetFocus()

    def ao_selecionar(self, evento):
        tarefa = self.gerenciador.buscar_por_id(self._id_selecionado())
        self._mostrar_botoes(tarefa)
        evento.Skip()

    def _mostrar_botoes(self, tarefa):
        mostrar = tarefa is not None
        self.botao_editar.Show(mostrar)
        self.botao_concluir.Show(mostrar)
        self.botao_remover.Show(mostrar)
        self.botoes_sizer.Show(self.botao_editar, mostrar)
        self.botoes_sizer.Show(self.botao_concluir, mostrar)
        self.botoes_sizer.Show(self.botao_remover, mostrar)
        if tarefa:
            if tarefa["status"] == STATUS_CONCLUIDA:
                self.botao_concluir.SetLabel("&Marcar como pendente")
                self.botao_concluir.SetName("Marcar como pendente")
                self.botao_concluir.SetHelpText("Reabre a tarefa selecionada.")
            else:
                self.botao_concluir.SetLabel("&Concluir tarefa")
                self.botao_concluir.SetName("Concluir tarefa")
                self.botao_concluir.SetHelpText("Conclui a tarefa selecionada.")
        self.painel.Layout()
        self.Layout()

    def ao_editar(self, evento):
        tarefa_id = self._id_selecionado()
        if tarefa_id is None:
            self.SetStatusText("Selecione uma tarefa na lista para editar.")
            return

        tarefa = self.gerenciador.buscar_por_id(tarefa_id)
        dialogo = DialogoEditarTarefa(self, tarefa)
        if dialogo.ShowModal() == wx.ID_OK:
            try:
                self.gerenciador.editar(
                    tarefa_id,
                    nova_descricao=dialogo.obter_descricao(),
                    nova_prioridade=dialogo.obter_prioridade(),
                )
            except ValueError as erro:
                wx.MessageBox(str(erro), "Erro", wx.OK | wx.ICON_ERROR)
            else:
                persistencia.salvar(self.gerenciador.tarefas)
                self.SetStatusText("Tarefa atualizada.")
                self._atualizar_lista(tarefa_id=tarefa_id)
        dialogo.Destroy()

    def ao_concluir(self, evento):
        tarefa_id = self._id_selecionado()
        if tarefa_id is None:
            self.SetStatusText("Selecione uma tarefa na lista.")
            return

        tarefa = self.gerenciador.alternar_status(tarefa_id)
        persistencia.salvar(self.gerenciador.tarefas)
        self.SetStatusText(f"Tarefa marcada como {tarefa['status'].lower()}.")
        self._atualizar_lista(tarefa_id=tarefa["id"])

    def ao_remover(self, evento):
        tarefa_id = self._id_selecionado()
        if tarefa_id is None:
            self.SetStatusText("Selecione uma tarefa na lista para remover.")
            return

        tarefa = self.gerenciador.buscar_por_id(tarefa_id)
        confirmacao = wx.MessageBox(
            f"Remover a tarefa '{tarefa['descricao']}'?",
            "Confirmar remoção",
            wx.YES_NO | wx.ICON_QUESTION,
        )
        if confirmacao == wx.YES:
            self.gerenciador.remover(tarefa_id)
            persistencia.salvar(self.gerenciador.tarefas)
            self.SetStatusText("Tarefa removida.")
            self._atualizar_lista()

    def ao_filtrar(self, evento):
        self._atualizar_lista()

    def ao_redimensionar_lista(self, evento):
        self._ajustar_coluna_status()
        evento.Skip()

    def _ajustar_coluna_status(self):
        largura_lista = self.lista.GetClientSize().width
        largura_fixa = sum(self.lista.GetColumnWidth(coluna) for coluna in range(3))
        largura_status = max(120, largura_lista - largura_fixa - 4)
        self.lista.SetColumnWidth(3, largura_status)

    def ao_limpar_filtros(self, evento):
        self.combo_filtro_status.SetStringSelection("Todos")
        self.combo_filtro_prioridade.SetStringSelection("Todas")
        self.campo_busca.Clear()
        self._atualizar_lista()
        self.SetStatusText("Filtros limpos.")

    def _id_selecionado(self):
        indice = self.lista.GetFirstSelected()
        if indice == -1:
            return None
        return self.lista.GetItemData(indice)

    def _atualizar_lista(self, tarefa_id=None):
        self.lista.DeleteAllItems()
        self._mostrar_botoes(None)
        tarefas_filtradas = self.gerenciador.filtrar(
            status=self.combo_filtro_status.GetStringSelection(),
            prioridade=self.combo_filtro_prioridade.GetStringSelection(),
            texto=self.campo_busca.GetValue(),
        )
        for tarefa in tarefas_filtradas:
            indice = self.lista.InsertItem(self.lista.GetItemCount(), str(tarefa["id"]))
            self.lista.SetItem(indice, 1, tarefa["descricao"])
            self.lista.SetItem(indice, 2, tarefa["prioridade"])
            self.lista.SetItem(indice, 3, tarefa["status"])
            self.lista.SetItemData(indice, tarefa["id"])

            if tarefa["id"] == tarefa_id:
                self.lista.Select(indice)
                self._mostrar_botoes(tarefa)
        self.Layout()
        self.bandeja.atualizar()

    def _carregar_tarefas(self):
        tarefas_salvas = persistencia.carregar()
        self.gerenciador.carregar_lista(tarefas_salvas)
        self._atualizar_lista()


class DialogoEditarTarefa(wx.Dialog):
    def __init__(self, pai, tarefa):
        super().__init__(pai, title="Editar Tarefa", size=(420, 240))
        self.SetBackgroundColour(wx.Colour(COR_FUNDO))

        sizer = wx.BoxSizer(wx.VERTICAL)

        rotulo_descricao = wx.StaticText(self, label="&Descrição da tarefa:")
        self.campo_descricao = wx.TextCtrl(self, value=tarefa["descricao"])
        self.campo_descricao.SetName("Descrição da tarefa para edição")
        self.campo_descricao.SetHelpText("Digite a nova descrição da tarefa.")

        rotulo_prioridade = wx.StaticText(self, label="&Prioridade da tarefa:")
        self.combo_prioridade = wx.Choice(self, choices=PRIORIDADES, size=(260, -1))
        self.combo_prioridade.SetStringSelection(tarefa["prioridade"])
        self.combo_prioridade.SetName("Prioridade da tarefa para edição")
        self.combo_prioridade.SetHelpText("Escolha a nova prioridade da tarefa.")

        sizer.Add(rotulo_descricao, 0, wx.ALL, 10)
        sizer.Add(self.campo_descricao, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer.Add(rotulo_prioridade, 0, wx.ALL, 10)
        sizer.Add(self.combo_prioridade, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        botoes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_salvar = wx.Button(self, id=wx.ID_OK, label="&Salvar")
        self.botao_cancelar = wx.Button(self, id=wx.ID_CANCEL, label="&Cancelar")
        self.botao_salvar.SetName("Salvar alteração")
        self.botao_cancelar.SetName("Cancelar edição")
        self.botao_salvar.SetBackgroundColour(wx.Colour(COR_AZUL))
        self.botao_salvar.SetForegroundColour(wx.WHITE)
        self.botao_cancelar.SetBackgroundColour(wx.Colour(COR_AZUL_CLARO))
        self.botao_cancelar.SetForegroundColour(wx.Colour(COR_AZUL_ESCURO))
        self.botao_salvar.SetMinSize(self.FromDIP((120, 40)))
        self.botao_cancelar.SetMinSize(self.FromDIP((120, 40)))
        self.botao_salvar.SetDefault()
        botoes_sizer.Add(self.botao_salvar, 0, wx.RIGHT, 10)
        botoes_sizer.Add(self.botao_cancelar, 0)
        sizer.Add(botoes_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        self.SetSizer(sizer)
        self.combo_prioridade.MoveAfterInTabOrder(self.campo_descricao)
        self.botao_salvar.MoveAfterInTabOrder(self.combo_prioridade)
        self.botao_cancelar.MoveAfterInTabOrder(self.botao_salvar)
        self.campo_descricao.SetFocus()

    def obter_descricao(self):
        return self.campo_descricao.GetValue()

    def obter_prioridade(self):
        return self.combo_prioridade.GetStringSelection()
