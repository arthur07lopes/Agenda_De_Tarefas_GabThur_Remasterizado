import wx
import wx.adv

from tarefas import STATUS_PENDENTE

NOME_PROGRAMA = "Agenda de Tarefas GabThur"
COR_AZUL_ESCURO = "#003B5C"
COR_AZUL = "#0672CE"
COR_BRANCO = "#FFFFFF"


def _criar_icone():
    """Desenha um ícone quadrado azul (estilo Dell) com uma marca de tarefa concluída."""
    tamanho = 32
    bitmap = wx.Bitmap(tamanho, tamanho, 32)
    bitmap.UseAlpha()
    contexto_dc = wx.MemoryDC(bitmap)
    contexto_dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0, 0)))
    contexto_dc.Clear()

    gc = wx.GraphicsContext.Create(contexto_dc)
    gc.SetBrush(wx.Brush(wx.Colour(COR_AZUL_ESCURO)))
    gc.SetPen(wx.TRANSPARENT_PEN)
    gc.DrawRoundedRectangle(1, 1, tamanho - 2, tamanho - 2, 7)

    gc.SetBrush(wx.Brush(wx.Colour(COR_AZUL)))
    gc.DrawRoundedRectangle(5, 5, tamanho - 10, 9, 3)

    caminho = gc.CreatePath()
    caminho.MoveToPoint(8, 21)
    caminho.AddLineToPoint(14, 27)
    caminho.AddLineToPoint(24, 13)
    gc.SetPen(wx.Pen(wx.Colour(COR_BRANCO), 3))
    gc.StrokePath(caminho)

    contexto_dc.SelectObject(wx.NullBitmap)

    icone = wx.Icon()
    icone.CopyFromBitmap(bitmap)
    return icone


class BandejaAgendaTarefas(wx.adv.TaskBarIcon):
    """Ícone de bandeja do sistema que mantém a Agenda de Tarefas GabThur em segundo plano."""

    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.SetIcon(_criar_icone(), self._texto_dica(0))

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.ao_ativar)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.ao_ativar)

    def _texto_dica(self, quantidade_pendentes):
        if quantidade_pendentes <= 0:
            return f"{NOME_PROGRAMA} - tudo em dia"
        if quantidade_pendentes == 1:
            return f"{NOME_PROGRAMA} - 1 tarefa pendente"
        return f"{NOME_PROGRAMA} - {quantidade_pendentes} tarefas pendentes"

    def _quantidade_pendentes(self):
        return sum(
            1 for tarefa in self.frame.gerenciador.tarefas
            if tarefa["status"] == STATUS_PENDENTE
        )

    def atualizar(self):
        quantidade = self._quantidade_pendentes()
        self.SetIcon(_criar_icone(), self._texto_dica(quantidade))

    def ao_ativar(self, evento):
        self.restaurar_janela()

    def restaurar_janela(self):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show()
        self.frame.Raise()
        self.frame.SetFocus()

    def CreatePopupMenu(self):
        menu = wx.Menu()

        item_abrir = menu.Append(wx.ID_ANY, "&Abrir programa")
        self.Bind(wx.EVT_MENU, lambda evento: self.restaurar_janela(), item_abrir)

        menu.AppendSeparator()

        quantidade = self._quantidade_pendentes()
        if quantidade <= 0:
            texto_quantidade = "Tudo em dia"
        elif quantidade == 1:
            texto_quantidade = "1 tarefa pendente"
        else:
            texto_quantidade = f"{quantidade} tarefas pendentes"
        item_quantidade = menu.Append(wx.ID_ANY, texto_quantidade)
        item_quantidade.Enable(False)

        menu.AppendSeparator()

        item_sair = menu.Append(wx.ID_ANY, f"&Sair da {NOME_PROGRAMA}")
        self.Bind(wx.EVT_MENU, lambda evento: self.frame.sair_definitivamente(), item_sair)

        return menu
