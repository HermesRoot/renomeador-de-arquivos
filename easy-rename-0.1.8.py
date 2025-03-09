import os
import shutil
import wx
from wx.lib.mixins.listctrl import ColumnSorterMixin

# Variável global para armazenar os arquivos renomeados
renomeacoes = []

# Lista fixa de extensões suportadas (mutável via Editar)
EXTENSOES_SUPORTADAS = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".mp3", ".wav", ".ogg", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".txt", ".pdf", ".docx", ".xlsx"]

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Renomeador de Arquivos", size=(500, 550))
        self.SetMinSize((500, 550))
        self.SetMaxSize((500, 550))

        # Menu
        menu_bar = wx.MenuBar()
        self.SetMenuBar(menu_bar)

        # Menu Arquivo
        arquivo_menu = wx.Menu()
        arquivo_menu.Append(101, "Nova Seleção")
        arquivo_menu.Append(102, "Salvar Log")
        arquivo_menu.Append(103, "Abrir Pasta")
        arquivo_menu.AppendSeparator()
        arquivo_menu.Append(104, "Sair")
        menu_bar.Append(arquivo_menu, "Arquivo")

        # Menu Editar
        editar_menu = wx.Menu()
        editar_menu.Append(201, "Limpar Lista")
        editar_menu.Append(202, "Remover Selecionado")
        editar_menu.Append(203, "Definir Extensões Personalizadas")
        editar_menu.Append(204, "Desfazer Última Renomeação")
        menu_bar.Append(editar_menu, "Editar")

        # Menu Ajuda
        ajuda_menu = wx.Menu()
        ajuda_menu.Append(301, "Instruções")
        ajuda_menu.Append(302, "Sobre")
        menu_bar.Append(ajuda_menu, "Ajuda")

        # Painel principal
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Bloco 1: Seleção de Arquivos
        selecao_box = wx.StaticBox(panel, label="Seleção de Arquivos")
        selecao_sizer = wx.StaticBoxSizer(selecao_box, wx.VERTICAL)
        pasta_sizer = wx.BoxSizer(wx.HORIZONTAL)
        arquivos_label = wx.StaticText(panel, label="Arquivos:")
        pasta_sizer.Add(arquivos_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.pasta_ctrl = wx.TextCtrl(panel, size=(300, 25))
        pasta_sizer.Add(self.pasta_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        btn_selecionar = wx.Button(panel, label="...", size=(30, 25))
        pasta_sizer.Add(btn_selecionar, 0, wx.ALIGN_CENTER_VERTICAL)
        selecao_sizer.Add(pasta_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.Add(selecao_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Bloco 2: Configurações de Renomeação
        config_box = wx.StaticBox(panel, label="Configurações de Renomeação")
        config_sizer = wx.StaticBoxSizer(config_box, wx.VERTICAL)
        
        # Prefixo
        prefixo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        prefixo_label = wx.StaticText(panel, label="Prefixo:")
        prefixo_sizer.Add(prefixo_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.prefixo_ctrl = wx.TextCtrl(panel, size=(300, 25))
        prefixo_sizer.Add(self.prefixo_ctrl, 0, wx.ALIGN_CENTER_VERTICAL)
        config_sizer.Add(prefixo_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Número Inicial e Separador
        contador_sizer = wx.BoxSizer(wx.HORIZONTAL)
        contador_label = wx.StaticText(panel, label="Número Inicial:")
        contador_sizer.Add(contador_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.contador_ctrl = wx.TextCtrl(panel, value="1", size=(50, 25))
        contador_sizer.Add(self.contador_ctrl, 0, wx.RIGHT, 10)
        separador_label = wx.StaticText(panel, label="Separador:")
        contador_sizer.Add(separador_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.separador_ctrl = wx.TextCtrl(panel, size=(50, 25))
        contador_sizer.Add(self.separador_ctrl, 0)
        config_sizer.Add(contador_sizer, 0, wx.ALL | wx.CENTER, 10)
        
        main_sizer.Add(config_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Lista de arquivos
        main_sizer.Add(wx.StaticText(panel, label="Arquivos selecionados:"), 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.lista_arquivos = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_VRULES)
        self.lista_arquivos.InsertColumn(0, "Arquivo Original", width=230)
        self.lista_arquivos.InsertColumn(1, "Novo Nome (Prévia)", width=230)
        main_sizer.Add(self.lista_arquivos, 1, wx.EXPAND | wx.ALL, 5)

        # Botões
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_renomear = wx.Button(panel, label="Renomear", size=(100, 40))
        self.btn_desfazer = wx.Button(panel, label="Desfazer", size=(100, 40))
        btn_sizer.Add(self.btn_renomear, 0, wx.ALL, 10)
        btn_sizer.Add(self.btn_desfazer, 0, wx.ALL, 10)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(main_sizer)

        # Bindings
        self.Bind(wx.EVT_MENU, self.on_nova_selecao, id=101)
        self.Bind(wx.EVT_MENU, self.on_salvar_log, id=102)
        self.Bind(wx.EVT_MENU, self.on_abrir_pasta, id=103)
        self.Bind(wx.EVT_MENU, lambda evt: self.Close(), id=104)
        self.Bind(wx.EVT_MENU, self.on_limpar_lista, id=201)
        self.Bind(wx.EVT_MENU, self.on_remover_selecionado, id=202)
        self.Bind(wx.EVT_MENU, self.on_definir_extensoes, id=203)
        self.Bind(wx.EVT_MENU, self.on_desfazer, id=204)
        self.Bind(wx.EVT_MENU, self.on_instrucoes, id=301)
        self.Bind(wx.EVT_MENU, self.on_sobre, id=302)
        btn_selecionar.Bind(wx.EVT_BUTTON, self.on_nova_selecao)
        self.btn_renomear.Bind(wx.EVT_BUTTON, self.on_renomear)
        self.btn_desfazer.Bind(wx.EVT_BUTTON, self.on_desfazer)
        self.prefixo_ctrl.Bind(wx.EVT_TEXT, self.atualizar_previa)
        self.contador_ctrl.Bind(wx.EVT_TEXT, self.atualizar_previa)
        self.separador_ctrl.Bind(wx.EVT_TEXT, self.atualizar_previa)
        self.lista_arquivos.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def on_nova_selecao(self, event):
        wildcard = "Arquivos suportados (" + ";".join([f"*{ext}" for ext in EXTENSOES_SUPORTADAS]) + ")|" + ";".join([f"*{ext}" for ext in EXTENSOES_SUPORTADAS])
        dlg = wx.FileDialog(self, "Selecione os arquivos", defaultDir=self.pasta_ctrl.GetValue() or "", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            arquivos = dlg.GetPaths()
            if arquivos:
                self.pasta_ctrl.SetValue(os.path.dirname(arquivos[0]))
                self.listar_arquivos(arquivos)
        dlg.Destroy()

    def listar_arquivos(self, arquivos=None):
        self.lista_arquivos.DeleteAllItems()
        if arquivos:
            for i, arquivo in enumerate(arquivos, start=1):
                nome, ext = os.path.splitext(os.path.basename(arquivo))
                novo_nome = self.gerar_preview_nome(nome, ext, i)
                index = self.lista_arquivos.InsertItem(self.lista_arquivos.GetItemCount(), os.path.basename(arquivo))
                self.lista_arquivos.SetItem(index, 1, novo_nome)
            self.atualizar_previa()

    def gerar_preview_nome(self, nome, ext, contador):
        prefixo = self.prefixo_ctrl.GetValue().strip()
        separador = self.separador_ctrl.GetValue().strip()
        try:
            contador_inicial = int(self.contador_ctrl.GetValue().strip())
        except ValueError:
            contador_inicial = 1
        if not prefixo:
            return f"{contador_inicial + contador - 1:02d}{ext}"
        return f"{prefixo}{separador if separador else ''}{contador_inicial + contador - 1:02d}{ext}"

    def atualizar_previa(self, event=None):
        for i in range(self.lista_arquivos.GetItemCount()):
            arquivo = self.lista_arquivos.GetItemText(i, 0)
            nome, ext = os.path.splitext(arquivo)
            novo_nome = self.gerar_preview_nome(nome, ext, i + 1)
            self.lista_arquivos.SetItem(i, 1, novo_nome)

    def on_renomear(self, event):
        global renomeacoes
        pasta = self.pasta_ctrl.GetValue().strip()
        prefixo = self.prefixo_ctrl.GetValue().strip()
        separador = self.separador_ctrl.GetValue().strip()

        try:
            contador_inicial = int(self.contador_ctrl.GetValue().strip())
        except ValueError:
            wx.MessageBox("O contador inicial precisa ser um número válido!", "Atenção", wx.OK | wx.ICON_WARNING)
            return

        if not prefixo:
            wx.MessageBox("Digite um prefixo válido!", "Atenção", wx.OK | wx.ICON_WARNING)
            return

        if self.lista_arquivos.GetItemCount() == 0:
            wx.MessageBox("Nenhum arquivo selecionado!", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        log_path = os.path.join(pasta, "renomeacoes.log")
        renomeacoes = []

        with open(log_path, "w", encoding="utf-8") as log:
            log.write("Iniciando renomeações...\n")
            for i in range(self.lista_arquivos.GetItemCount()):
                arquivo = self.lista_arquivos.GetItemText(i, 0)
                nome, ext = os.path.splitext(arquivo)
                if ext.lower() not in EXTENSOES_SUPORTADAS:
                    continue
                novo_nome = f"{prefixo}{separador if separador else ''}{contador_inicial + i:02d}{ext}"
                caminho_antigo = os.path.join(pasta, arquivo)
                caminho_novo = os.path.join(pasta, novo_nome)
                shutil.move(caminho_antigo, caminho_novo)
                renomeacoes.append((caminho_novo, caminho_antigo))
                self.lista_arquivos.SetItem(i, 1, novo_nome)
                log.write(f'Renomeado "{arquivo}" para "{novo_nome}"\n')
            log.write("Renomeações concluídas.\n")

        wx.MessageBox("Arquivos renomeados com sucesso!", "Concluído", wx.OK | wx.ICON_INFORMATION)

    def on_desfazer(self, event):
        global renomeacoes
        if not renomeacoes:
            wx.MessageBox("Nenhuma renomeação para desfazer.", "Info", wx.OK | wx.ICON_INFORMATION)
            return
        pasta = self.pasta_ctrl.GetValue().strip()
        log_path = os.path.join(pasta, "renomeacoes.log")
        
        with open(log_path, "a", encoding="utf-8") as log:  # Modo "a" para adicionar ao log existente
            log.write("\nIniciando desfazer renomeações...\n")
            for novo, antigo in reversed(renomeacoes):
                shutil.move(novo, antigo)
                log.write(f'Desfeito: "{os.path.basename(novo)}" restaurado para "{os.path.basename(antigo)}"\n')
            log.write("Desfazer concluído.\n")
        
        renomeacoes = []
        self.listar_arquivos()  # Atualiza a lista (embora esteja vazia após desfazer)
        wx.MessageBox("Renomeações desfeitas com sucesso!", "Concluído", wx.OK | wx.ICON_INFORMATION)

    def on_salvar_log(self, event):
        pasta = self.pasta_ctrl.GetValue().strip()
        log_path = os.path.join(pasta, "renomeacoes.log")
        if not pasta or not os.path.exists(log_path):
            wx.MessageBox("Nenhum log disponível para salvar!", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        with wx.FileDialog(self, "Salvar Log", wildcard="Arquivos de Log (*.log)|*.log|Todos os arquivos (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                shutil.copy(log_path, dlg.GetPath())
                wx.MessageBox("Log salvo com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def on_abrir_pasta(self, event):
        pasta = self.pasta_ctrl.GetValue().strip()
        if pasta and os.path.exists(pasta):
            os.startfile(pasta)  # Windows
        else:
            wx.MessageBox("Pasta inválida ou não especificada!", "Atenção", wx.OK | wx.ICON_WARNING)

    def on_limpar_lista(self, event):
        global renomeacoes
        self.lista_arquivos.DeleteAllItems()
        renomeacoes = []
        self.pasta_ctrl.SetValue("")
        self.prefixo_ctrl.SetValue("")
        wx.MessageBox("Lista limpa com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def on_remover_selecionado(self, event):
        selected = self.lista_arquivos.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Nenhum item selecionado!", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        while selected != -1:
            self.lista_arquivos.DeleteItem(selected)
            selected = self.lista_arquivos.GetNextSelected(-1)
        wx.MessageBox("Item(s) removido(s) da lista!", "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def on_key_down(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            self.on_remover_selecionado(event)
        event.Skip()

    def on_definir_extensoes(self, event):
        dlg = wx.Dialog(self, title="Definir Extensões", size=(300, 150))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(dlg, label="Digite as extensões separadas por vírgula (ex: .mp4, .jpg):"), 0, wx.ALL, 5)
        ext_ctrl = wx.TextCtrl(dlg, value=", ".join(EXTENSOES_SUPORTADAS), size=(250, -1))
        sizer.Add(ext_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        btn_salvar = wx.Button(dlg, label="Salvar")
        sizer.Add(btn_salvar, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        dlg.SetSizer(sizer)

        def salvar_extensoes(evt):
            global EXTENSOES_SUPORTADAS
            novas_extensoes = ext_ctrl.GetValue().strip().split(",")
            EXTENSOES_SUPORTADAS = [ext.strip().lower() if ext.startswith(".") else f".{ext.strip().lower()}" for ext in novas_extensoes if ext]
            dlg.Destroy()
            wx.MessageBox("Extensões atualizadas!", "Sucesso", wx.OK | wx.ICON_INFORMATION)

        btn_salvar.Bind(wx.EVT_BUTTON, salvar_extensoes)
        dlg.ShowModal()

    def on_instrucoes(self, event):
        wx.MessageBox("1. Clique em '...' para escolher os arquivos manualmente.\n2. Digite um prefixo e ajuste o contador/separador.\n3. Veja a prévia na lista.\n4. Clique em 'Renomear' para aplicar.\n5. Use 'Desfazer' se necessário.\n6. Pressione 'Delete' para remover arquivos da lista.", "Instruções", wx.OK | wx.ICON_INFORMATION)

    def on_sobre(self, event):
        wx.MessageBox("Renomeador de Arquivos\nPor: HermesRoot\nLicença: MIT\nVersão: 0.1.8", "Sobre", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()