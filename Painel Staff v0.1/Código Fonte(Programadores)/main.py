import os

import _tkinter
import unicodedata
import time
import tkinter as tk
import json
from tkinter import messagebox, Text


# =========================================================
# TEMA DO APP
# =========================================================

BG_MAIN = "#090909"
BG_PANEL = "#111111"
BG_PANEL_2 = "#151515"
BG_ENTRY = "#1b1b1b"

GOLD = "#D4AF37"
GOLD_LIGHT = "#F0D477"
GOLD_DARK = "#6F5815"

WHITE = "#F2F2F2"
TEXT = "#CFCFCF"
TEXT_DARK = "#777777"

RED = "#B52A2A"
RED_LIGHT = "#E05252"

GREEN = "#2FBF71"
GREEN_LIGHT = "#5BE398"

BLUE_DARK = "#171717"
BORDER = "#292929"


# =========================================================
# JANELA
# =========================================================

janela = tk.Tk()

try:
    janela.iconbitmap("Icone/RegistroUsuarios.ico")

except _tkinter.TclError:
    messagebox.showerror(
        "Atenção",
        "Você provavelmente apagou o icone OU moveu o executável, "
        "então irá continuar sem.\nCaso o app não abra, olhe na aba de apps abaixo."
    )


# =========================================================
# FUNÇÃO DE LIMPAR
# =========================================================

def limpar_janela(self):
    for widget in janela.winfo_children():
        widget.destroy()


# =========================================================
# LOGIN
# =========================================================

class Login:

    def __init__(self):

        self.password = self.carregar_senha()
        self.tentativas = 0

        self.status = tk.Label(
            janela,
            text="Insira a senha do administrador",
            bg=BG_MAIN,
            fg=TEXT,
            font=("Arial", 9)
        )

        self.logado = False

    # -----------------------------------------------------
    # CARREGAR SENHA
    # -----------------------------------------------------

    def carregar_senha(self):

        try:
            with open("Funcionarios/senha.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            senha = data.get("senha")

            if isinstance(senha, str) and senha:
                return senha

        except (FileNotFoundError, json.JSONDecodeError):
            pass

        return "0000"

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    def react_login(self, entrada):

        if not self.logado:

            if entrada == "" or entrada == "Digite a senha admin...":
                self.status.config(
                    text="Preencha os campos.",
                    fg=RED_LIGHT
                )
                return

            if self.tentativas >= 2:

                messagebox.showerror(
                    "Painel de funcionários",
                    "Você foi deslogado do servidor pois acabou as tentativas!"
                )

                self.status.config(
                    text="Bloqueado!",
                    fg=RED_LIGHT
                )

                janela.destroy()
                return

            if entrada == self.password:

                messagebox.showinfo(
                    "Painel de funcionários",
                    "Você logou no painel de funcionários com sucesso!"
                )

                self.status.configure(
                    text="Logado com sucesso!",
                    fg=GREEN_LIGHT
                )

                self.logado = True

                time.sleep(1)

                painel = Painel()
                painel.start()

                self.status.config(
                    text="Painel aberto com sucesso!",
                    fg=GREEN_LIGHT
                )

            else:

                messagebox.showerror(
                    "Painel de funcionários",
                    "Você errou a senha admin!"
                )

                self.tentativas += 1

                self.status.configure(
                    text=f"Senha inválida ({self.tentativas}/3)",
                    fg=RED_LIGHT
                )

                if self.tentativas == 2:

                    messagebox.showwarning(
                        "Painel de funcionários",
                        "Atenção, está é a sua ultima tentativa."
                    )

                    pass

        else:

            messagebox.showerror(
                "Painel de funcionarios",
                "Você já está logado."
            )

    # -----------------------------------------------------
    # DISPLAY LOGIN
    # -----------------------------------------------------

    def login_dysplay(self):

        janela.title("Registro de Usuários - Login")
        janela.geometry("800x380")

        janela.configure(
            bg=BG_MAIN
        )

        janela.resizable(
            False,
            False
        )

        # linha dourada

        goldline = tk.Frame(
            janela,
            bg=GOLD,
            height=3
        )

        goldline.place(
            x=0,
            y=0,
            relwidth=1
        )

        # título

        titulo = tk.Label(
            janela,
            text="REGISTRO DE USUÁRIOS",
            bg=BG_MAIN,
            fg=GOLD,
            font=("Segoe Script", 22, "bold")
        )

        titulo.place(
            x=0,
            y=45,
            width=800
        )

        # subtítulo

        subtitle = tk.Label(
            janela,
            text="ACESSO RESTRITO AO ADMINISTRADOR",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Arial", 8, "bold")
        )

        subtitle.place(
            x=0,
            y=87,
            width=800
        )

        # status

        self.status.place(
            x=0,
            y=145,
            width=800
        )

        # entrada

        texto = tk.StringVar(
            value="Digite a senha admin..."
        )

        getpass = tk.Entry(
            janela,
            textvariable=texto,
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            bd=1,
            relief="solid",
            width=30,
            justify="center",
            font=("Arial", 10)
        )

        getpass.place(
            x=275,
            y=185,
            width=250,
            height=34
        )

        # detalhe dourado abaixo

        entryline = tk.Frame(
            janela,
            bg=GOLD,
            height=1,
            width=250
        )

        entryline.place(
            x=275,
            y=219
        )

        # login

        login = tk.Button(
            janela,
            text="ENTRAR",
            fg=BG_MAIN,
            bg=GOLD,
            activebackground=GOLD_LIGHT,
            activeforeground=BG_MAIN,
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief="flat",
            bd=0,
            command=lambda: self.react_login(
                texto.get()
            )
        )

        login.place(
            x=325,
            y=245,
            width=150,
            height=38
        )

        # rodapé

        footer = tk.Label(
            janela,
            text="Registro de Usuários • Painel Administrativo",
            bg=BG_MAIN,
            fg="#555555",
            font=("Arial", 7)
        )

        footer.place(
            x=0,
            y=345,
            width=800
        )

        janela.mainloop()


# =========================================================
# PAINEL
# =========================================================

class Painel:

    def __init__(self):
        self.subtitulo = "sla"

    # -----------------------------------------------------
    # REMOVER DISPLAY
    # -----------------------------------------------------

    def delete_display(self):

        limpar_janela(self)

        janela.geometry(
            "430x240"
        )

        janela.config(
            bg=BG_MAIN
        )

        janela.title(
            "Remover - PAINEL"
        )

        janela.resizable(
            False,
            False
        )

        # topo

        top = tk.Frame(
            janela,
            bg=BG_PANEL,
            height=60
        )

        top.place(
            x=0,
            y=0,
            relwidth=1
        )

        line = tk.Frame(
            janela,
            bg=GOLD,
            height=3
        )

        line.place(
            x=0,
            y=0,
            relwidth=1
        )

        titulo = tk.Label(
            janela,
            text="REMOÇÃO",
            font=("Segoe Script", 15, "bold"),
            bg=BG_PANEL,
            fg=GOLD
        )

        titulo.place(
            x=0,
            y=14,
            width=430
        )

        self.subtitulo = tk.Label(
            janela,
            text="Digite o nome completo para removê-lo.",
            font=("Arial", 8),
            bg=BG_MAIN,
            fg=TEXT
        )

        self.subtitulo.place(
            x=0,
            y=75,
            width=430
        )

        # entrada

        textt = tk.StringVar(
            value="Digite o nome do usuário..."
        )

        getname = tk.Entry(
            janela,
            bd=1,
            relief="solid",
            textvariable=textt,
            width=50,
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            justify="center",
            font=("Arial", 9)
        )

        getname.place(
            x=40,
            y=105,
            width=350,
            height=34
        )

        # botão

        confirm = tk.Button(
            janela,
            text="CONFIRMAR REMOÇÃO",
            bg=RED,
            fg=WHITE,
            activebackground=RED_LIGHT,
            activeforeground=WHITE,
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief="flat",
            command=lambda: self.func_delete(
                getname.get(),
                self.subtitulo
            )
        )

        confirm.place(
            x=110,
            y=155,
            width=210,
            height=35
        )

        # voltar

        exit2 = tk.Button(
            janela,
            text="←",
            fg=GOLD,
            bg=BG_PANEL,
            activebackground=BG_PANEL_2,
            activeforeground=GOLD_LIGHT,
            cursor="hand2",
            relief="flat",
            font=("Arial", 13, "bold"),
            command=lambda: Painel().start()
        )

        exit2.place(
            x=10,
            y=12,
            width=35,
            height=30
        )

        janela.mainloop()

    # -----------------------------------------------------
    # ANEXAR CARGO
    # -----------------------------------------------------

    def func_confirm_anex(self, name, cargo):

        name = ''.join(
            c for c in unicodedata.normalize('NFD', name)
            if unicodedata.category(c) != 'Mn'
        ).upper()

        cargo = ''.join(
            c for c in unicodedata.normalize('NFD', cargo)
            if unicodedata.category(c) != 'Mn'
        ).upper()

        if name == "INSIRA O NOME COMPLETO..." or cargo == "INSIRA O CARGO PARA ANEXAR.":

            messagebox.showerror(
                "AVISO - PAINEL",
                "Apague o texto nos campos dos dados e os preencha corretamente."
            )

            return

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                data = json.load(f)

            func = data['funcionarios']

            if name in func:

                func.remove(name)

                toup = f"{name} - {cargo}"

                func.append(toup)

                with open(
                    "Funcionarios/dat.json",
                    "w"
                ) as f:

                    toup0 = {
                        "funcionarios": func
                    }

                    json.dump(
                        toup0,
                        f,
                        indent=4
                    )

                messagebox.showinfo(
                    "AVISO - Inserir Cargos",
                    f"Cargo {cargo} anexado no usuário {name} com sucesso.\n"
                    "Clique no X para sair."
                )

            else:

                messagebox.showerror(
                    "AVISO - Distribuição de cargos",
                    "Este usuário não está na sua lista."
                )

                return

        except FileNotFoundError:

            messagebox.showerror(
                "AVISO - Distribuição de cargos",
                "Você não possui o DATA/STORAGE de funcionários, portanto\n"
                "Você provavelmente não tem usuários registrados."
            )

    def func_anexarcargo(self):

        limpar_janela(self)

        janela.geometry(
            "430x250"
        )

        janela.config(
            bg=BG_MAIN
        )

        janela.title(
            "Anexar cargo - PAINEL"
        )

        # topo

        topbox = tk.Frame(
            janela,
            bg=BG_PANEL,
            width=430,
            height=55
        )

        topbox.place(
            x=0,
            y=0
        )

        goldline = tk.Frame(
            janela,
            bg=GOLD,
            width=430,
            height=3
        )

        goldline.place(
            x=0,
            y=0
        )

        titulo = tk.Label(
            janela,
            text="INSERIR CARGO",
            bg=BG_PANEL,
            fg=GOLD,
            font=("Segoe Script", 15, "bold")
        )

        titulo.place(
            x=0,
            y=10,
            width=430
        )

        subtitulo = tk.Label(
            janela,
            text="ADICIONE UM NOME E ABAIXO O CARGO",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Arial", 7, "bold")
        )

        subtitulo.place(
            x=0,
            y=68,
            width=430
        )

        # nome

        place = tk.StringVar(
            value="Insira o nome completo..."
        )

        getname = tk.Entry(
            janela,
            bd=1,
            relief="solid",
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            textvariable=place,
            width=50,
            justify="center",
            font=("Arial", 9)
        )

        getname.place(
            x=50,
            y=100,
            width=330,
            height=32
        )

        # cargo

        place2 = tk.StringVar(
            value="Insira o cargo para anexar."
        )

        getrole = tk.Entry(
            janela,
            bd=1,
            relief="solid",
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            textvariable=place2,
            width=50,
            justify="center",
            font=("Arial", 9)
        )

        getrole.place(
            x=50,
            y=142,
            width=330,
            height=32
        )

        # confirmar

        confirmar = tk.Button(
            janela,
            text="CONFIRMAR",
            bg=GOLD,
            fg=BG_MAIN,
            activebackground=GOLD_LIGHT,
            activeforeground=BG_MAIN,
            relief="flat",
            font=("Arial", 9, "bold"),
            command=lambda: self.func_confirm_anex(
                getname.get(),
                getrole.get()
            ),
            cursor="hand2"
        )

        confirmar.place(
            x=145,
            y=185,
            width=140,
            height=35
        )

        # voltar

        exit = tk.Button(
            janela,
            text="←",
            bg=BG_PANEL,
            fg=GOLD,
            activebackground=BG_PANEL,
            activeforeground=GOLD_LIGHT,
            font=("Arial", 13, "bold"),
            command=lambda: Painel().start(),
            cursor="hand2",
            relief="flat"
        )

        exit.place(
            x=10,
            y=10,
            width=35,
            height=30
        )

        janela.mainloop()

    # -----------------------------------------------------
    # DELETE FUNCIONÁRIO
    # -----------------------------------------------------

    def func_delete(self, name, sub):

        name = ''.join(
            c for c in unicodedata.normalize('NFD', name)
            if unicodedata.category(c) != 'Mn'
        ).upper()

        if len(name) < 5:

            sub.config(
                text="Adicione o nome completo.",
                fg=RED_LIGHT
            )

            return

        if name == "Digite o nome do usuário...":

            messagebox.showwarning(
                "Remoção - PAINEL",
                "Remova o texto da caixa e substitua-o pelo nome do funcionário."
            )

            return

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                dat = json.load(f)

            funcs = dat['funcionarios']

            if name not in funcs:

                messagebox.showerror(
                    "PAINEL - REMOÇÃO",
                    "Este nome não está na sua lista.\n\n"
                    "Caso o mesmo possua um cargo, adicione junto. "
                    "EX: João César - Admin"
                )

            else:

                funcs.remove(name)

                with open(
                    "Funcionarios/dat.json",
                    "w"
                ) as f:

                    datup = {
                        "funcionarios": funcs
                    }

                    json.dump(
                        datup,
                        f
                    )

                    messagebox.showinfo(
                        "PAINEL - REMOÇÃO",
                        f"Usuário {name} removido com sucesso."
                    )

                return self.start()

        except FileNotFoundError:

            sub.config(
                text="Você não tem funcionários cadastrados.",
                fg=RED_LIGHT
            )

    # -----------------------------------------------------
    # GERENCIAMENTO DE SENHA
    # -----------------------------------------------------

    def alterar_senha(self):

        limpar_janela(self)

        janela.geometry("430x300")
        janela.title("Alterar senha - PAINEL")
        janela.config(bg=BG_MAIN)
        janela.resizable(False, False)

        top = tk.Frame(
            janela,
            bg=BG_PANEL,
            height=60
        )

        top.place(
            x=0,
            y=0,
            relwidth=1
        )

        goldline = tk.Frame(
            janela,
            bg=GOLD,
            height=3
        )

        goldline.place(
            x=0,
            y=0,
            relwidth=1
        )

        titulo = tk.Label(
            janela,
            text="ALTERAR SENHA",
            bg=BG_PANEL,
            fg=GOLD,
            font=("Segoe Script", 16, "bold")
        )

        titulo.place(
            x=0,
            y=12,
            width=430
        )

        atual_var = tk.StringVar()
        nova_var = tk.StringVar()
        confirmar_var = tk.StringVar()

        tk.Label(
            janela,
            text="SENHA ATUAL",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Arial", 8, "bold")
        ).place(
            x=40,
            y=75,
            width=350
        )

        atual = tk.Entry(
            janela,
            textvariable=atual_var,
            show="*",
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            bd=1,
            relief="solid",
            justify="center",
            font=("Arial", 9)
        )

        atual.place(
            x=40,
            y=95,
            width=350,
            height=32
        )

        tk.Label(
            janela,
            text="NOVA SENHA",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Arial", 8, "bold")
        ).place(
            x=40,
            y=138,
            width=350
        )

        nova = tk.Entry(
            janela,
            textvariable=nova_var,
            show="*",
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            bd=1,
            relief="solid",
            justify="center",
            font=("Arial", 9)
        )

        nova.place(
            x=40,
            y=158,
            width=350,
            height=32
        )

        tk.Label(
            janela,
            text="CONFIRMAR NOVA SENHA",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Arial", 8, "bold")
        ).place(
            x=40,
            y=201,
            width=350
        )

        confirmar = tk.Entry(
            janela,
            textvariable=confirmar_var,
            show="*",
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            bd=1,
            relief="solid",
            justify="center",
            font=("Arial", 9)
        )

        confirmar.place(
            x=40,
            y=221,
            width=350,
            height=32
        )

        def salvar():

            atual_senha = atual_var.get()
            nova_senha = nova_var.get()
            confirmacao = confirmar_var.get()

            if not atual_senha or not nova_senha or not confirmacao:
                return messagebox.showwarning(
                    "Alterar senha",
                    "Preencha todos os campos."
                )

            if atual_senha != play.password:
                return messagebox.showerror(
                    "Alterar senha",
                    "A senha atual está incorreta."
                )

            if nova_senha != confirmacao:
                return messagebox.showerror(
                    "Alterar senha",
                    "A confirmação da nova senha não confere."
                )

            if len(nova_senha) < 4:
                return messagebox.showwarning(
                    "Alterar senha",
                    "A nova senha deve possuir pelo menos 4 caracteres."
                )

            try:
                os.makedirs("Funcionarios", exist_ok=True)

                with open(
                    "Funcionarios/senha.json",
                    "w",
                    encoding="utf-8"
                ) as f:
                    json.dump(
                        {"senha": nova_senha},
                        f,
                        indent=4
                    )

                play.password = nova_senha

                messagebox.showinfo(
                    "Alterar senha",
                    "Senha alterada com sucesso."
                )

                self.start()

            except OSError as erro:

                messagebox.showerror(
                    "Alterar senha",
                    f"Não foi possível salvar a nova senha.\n\n{erro}"
                )

        confirmar_btn = tk.Button(
            janela,
            text="SALVAR SENHA",
            bg=GOLD,
            fg=BG_MAIN,
            activebackground=GOLD_LIGHT,
            activeforeground=BG_MAIN,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            command=salvar
        )

        confirmar_btn.place(
            x=140,
            y=265,
            width=150,
            height=32
        )

        voltar = tk.Button(
            janela,
            text="←",
            fg=GOLD,
            bg=BG_PANEL,
            activebackground=BG_PANEL_2,
            activeforeground=GOLD_LIGHT,
            cursor="hand2",
            relief="flat",
            font=("Arial", 13, "bold"),
            command=self.start
        )

        voltar.place(
            x=10,
            y=12,
            width=35,
            height=30
        )

        janela.mainloop()

    # -----------------------------------------------------
    # START
    # -----------------------------------------------------

    def start(self):

        limpar_janela(self)

        janela.geometry(
            "800x430"
        )

        janela.title(
            "Inicio - Painel"
        )

        janela.resizable(
            False,
            False
        )

        self.aba_main()

        janela.mainloop()

    # -----------------------------------------------------
    # ABA PRINCIPAL
    # -----------------------------------------------------

    def aba_main(self):

        janela.configure(
            bg=BG_MAIN
        )

        # topo

        topbox = tk.Frame(
            janela,
            bg=BG_PANEL,
            width=800,
            height=65
        )

        topbox.place(
            x=0,
            y=0
        )

        goldline = tk.Frame(
            janela,
            bg=GOLD,
            width=800,
            height=3
        )

        goldline.place(
            x=0,
            y=0
        )

        # esquerda

        leftbox = tk.Frame(
            janela,
            bg=BG_PANEL,
            width=100,
            height=365
        )

        leftbox.place(
            x=0,
            y=65
        )

        # título

        self.titulo = tk.Label(
            janela,
            text="PAINEL",
            bg=BG_PANEL,
            fg=GOLD,
            font=("Segoe Script", 20, "bold")
        )

        self.titulo.place(
            x=100,
            y=10,
            width=700
        )

        # registrar

        registrar = tk.Button(
            janela,
            text="REGISTRAR",
            font=("Arial", 8, "bold"),
            bg=GOLD,
            fg=BG_MAIN,
            activebackground=GOLD_LIGHT,
            activeforeground=BG_MAIN,
            relief="flat",
            command=lambda: Registro().func_registrar(),
            cursor="hand2"
        )

        registrar.place(
            x=12,
            y=85,
            width=76,
            height=28
        )

        # remover

        delete = tk.Button(
            janela,
            text="REMOVER",
            bg=RED,
            fg=WHITE,
            activebackground=RED_LIGHT,
            activeforeground=WHITE,
            font=("Arial", 8, "bold"),
            relief="flat",
            command=self.delete_display,
            cursor="hand2"
        )

        delete.place(
            x=12,
            y=120,
            width=76,
            height=28
        )

        # cargo

        ac = tk.Button(
            janela,
            text="CARGO",
            font=("Arial", 8, "bold"),
            bg=BG_PANEL_2,
            fg=GOLD,
            activebackground="#222222",
            activeforeground=GOLD_LIGHT,
            cursor="hand2",
            relief="flat",
            command=self.func_anexarcargo
        )

        ac.place(
            x=12,
            y=155,
            width=76,
            height=28
        )

        # senha

        senha_btn = tk.Button(
            janela,
            text="SENHA",
            bg=BG_PANEL_2,
            font=("Arial", 8, "bold"),
            fg=GOLD,
            activebackground="#222222",
            activeforeground=GOLD_LIGHT,
            cursor="hand2",
            relief="flat",
            command=self.alterar_senha
        )

        senha_btn.place(
            x=12,
            y=225,
            width=76,
            height=28
        )

        # blacklist

        change_aba_for_blacklist = tk.Button(
            janela,
            text="BLACK LIST",
            bg=BG_PANEL_2,
            font=("Arial", 8, "bold"),
            fg=RED_LIGHT,
            activebackground="#222222",
            activeforeground="#FF7777",
            cursor="hand2",
            relief="flat",
            command=lambda: PainelBlack().startpanel()
        )

        change_aba_for_blacklist.place(
            x=8,
            y=190,
            width=84,
            height=30
        )

        # subtitulo

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                dat = json.load(f)

            subtittle = tk.Label(
                janela,
                text=f"Funcionários cadastrados: {len(dat['funcionarios'])}",
                bg=BG_MAIN,
                fg=TEXT,
                font=("Arial", 12, "bold")
            )

        except FileNotFoundError:

            subtittle = tk.Label(
                janela,
                text="Funcionários cadastrados: 0",
                bg=BG_MAIN,
                fg=TEXT,
                font=("Arial", 12, "bold")
            )

        subtittle.place(
            x=120,
            y=75,
            width=650
        )

        # área lista

        lista_bg = tk.Frame(
            janela,
            bg=BG_PANEL,
            bd=1,
            relief="solid"
        )

        lista_bg.place(
            x=120,
            y=110,
            width=650,
            height=270
        )

        lfuncionarios = tk.Label(
            lista_bg,
            text="Analisando dados...",
            width=40,
            relief="flat",
            height=15,
            bg=BG_PANEL,
            fg=TEXT,
            font=("Arial", 10),
            justify="center",
            anchor="center"
        )

        lfuncionarios.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                data = json.load(f)

                funcioarios = data["funcionarios"]

            todos = []

            for funcionario in funcioarios:

                todos.append(
                    funcionario
                )

            lfuncionarios.config(
                text="\n".join(todos)
            )

        except FileNotFoundError:

            lfuncionarios.config(
                text="Nenhum funcionário registrado.",
                fg=RED_LIGHT
            )

            register = tk.Button(
                janela,
                text="Clique aqui para registrar seu primeiro funcionário",
                bg=GOLD,
                fg=BG_MAIN,
                activebackground=GOLD_LIGHT,
                activeforeground=BG_MAIN,
                font=("Arial", 8, "bold"),
                relief="flat",
                command=lambda: Registro().func_registrar()
            )

            register.place(
                x=310,
                y=330
            )


# =========================================================
# REGISTRO
# =========================================================

class Registro:

    def __init__(self):

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                data = json.load(f)

            if len(data["funcionarios"]) >= 15:

                messagebox.showerror(
                    "AVISO - Registro",
                    "MÁXIMO DE MEMBROS ATINGIDO!\n\n\n\n"
                    "O que fazer? É simples!:\n"
                    "Aperte com o botão direito do mouse em cima do app, "
                    "depois aperta em copiar.\n"
                    "Vá até outra pasta e aperte CTRL + V.\n"
                    "Após isso o sistema irá criar um json novo, sem funcionarios."
                )

                return

        except FileNotFoundError:

            pass

        limpar_janela(self)

        janela.geometry(
            "430x250"
        )

        janela.config(
            bg=BG_MAIN
        )

        janela.title(
            "REGISTRO - PAINEL"
        )

    # -----------------------------------------------------
    # CONFIRMAR
    # -----------------------------------------------------

    def func_confirmar(self, name, titulo):

        name = ''.join(
            c for c in unicodedata.normalize('NFD', name)
            if unicodedata.category(c) != 'Mn'
        ).upper()

        if len(name) < 5:

            titulo.config(
                text="Coloque o nome completo.",
                fg=RED_LIGHT
            )

            return

        if name == "DIGITE O NOME COMPLETO DO FUNCIONARIO.":

            titulo.config(
                text="Apague o texto do campo e preencha com o nome.",
                fg=RED_LIGHT
            )

            return

        os.makedirs(
            "Funcionarios",
            exist_ok=True
        )

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                data = json.load(f)

        except FileNotFoundError:

            data = {
                "funcionarios": []
            }

        funcionarios = data["funcionarios"]

        if name in funcionarios:

            titulo.config(
                text="Este nome já está cadastrado.",
                fg=RED_LIGHT
            )

            return

        funcionarios.append(name)

        with open(
            "Funcionarios/dat.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        titulo.config(
            text="Funcionário registrado com sucesso.",
            fg=GREEN_LIGHT
        )

        messagebox.showinfo(
            "AVISO - REGISTRO",
            f"Usuário {name} adicionado com sucesso."
        )

        return Painel().start()

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def func_registrar(self):

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                data = json.load(f)

            if len(data["funcionarios"]) >= 15:
                return

        except FileNotFoundError:

            pass

        titulo = tk.Label(
            janela,
            text="REGISTRO",
            font=("Segoe Script", 17, "bold"),
            width=20,
            bg=BG_PANEL,
            fg=GOLD
        )

        titulo.place(
            x=0,
            y=15,
            width=430,
            height=45
        )

        linha = tk.Frame(
            janela,
            bg=GOLD,
            height=3
        )

        linha.place(
            x=0,
            y=0,
            width=430
        )

        subtitle = tk.Label(
            janela,
            text="Preencha os dados abaixo.",
            font=("Arial", 9),
            bg=BG_MAIN,
            fg=TEXT
        )

        subtitle.place(
            x=0,
            y=75,
            width=430
        )

        texto = tk.StringVar(
            value="Digite o nome completo do funcionário."
        )

        getname = tk.Entry(
            janela,
            textvariable=texto,
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            bd=1,
            relief="solid",
            width=40,
            font=("Arial", 9),
            justify="center"
        )

        getname.place(
            x=40,
            y=110,
            width=350,
            height=34
        )

        confirm = tk.Button(
            janela,
            text="CONFIRMAR",
            bg=GOLD,
            fg=BG_MAIN,
            activebackground=GOLD_LIGHT,
            activeforeground=BG_MAIN,
            font=("Arial", 9, "bold"),
            relief="flat",
            command=lambda: self.func_confirmar(
                getname.get(),
                subtitle
            ),
            cursor="hand2"
        )

        confirm.place(
            x=140,
            y=165,
            width=150,
            height=36
        )

        exit = tk.Button(
            janela,
            text="←",
            fg=GOLD,
            font=("Arial", 13, "bold"),
            bg=BG_PANEL,
            activebackground=BG_PANEL_2,
            activeforeground=GOLD_LIGHT,
            relief="flat",
            command=lambda: Painel().start(),
            cursor="hand2"
        )

        exit.place(
            x=10,
            y=12,
            width=35,
            height=30
        )

        janela.mainloop()


# =========================================================
# BLACK LIST
# =========================================================

class PainelBlack:

    def __init__(self):
        pass

    # -----------------------------------------------------
    # START BLACK LIST
    # -----------------------------------------------------

    def startpanel(self):

        limpar_janela(self)

        janela.geometry(
            "700x600"
        )

        janela.title(
            "Black List - Painel"
        )

        janela.configure(
            bg=BG_MAIN
        )

        janela.resizable(
            False,
            False
        )

        # =================================================
        # TOPO
        # =================================================

        topbox = tk.Frame(
            janela,
            bg=BG_PANEL,
            width=700,
            height=80
        )

        topbox.place(
            x=0,
            y=0
        )

        goldline = tk.Frame(
            janela,
            bg=GOLD,
            width=700,
            height=3
        )

        goldline.place(
            x=0,
            y=0
        )

        titulo = tk.Label(
            janela,
            text="BLACK LIST",
            bg=BG_PANEL,
            fg=GOLD,
            font=("Segoe Script", 24, "bold")
        )

        titulo.place(
            x=0,
            y=10,
            width=700
        )

        subtitulo = tk.Label(
            janela,
            text="PAINEL DE CONTROLE",
            bg=BG_PANEL,
            fg="#777777",
            font=("Arial", 7, "bold")
        )

        subtitulo.place(
            x=0,
            y=52,
            width=700
        )

        # =================================================
        # DIVISÓRIA
        # =================================================

        leftline = tk.Frame(
            janela,
            width=2,
            height=480,
            bg=GOLD_DARK
        )

        leftline.place(
            x=220,
            y=95
        )

        # =================================================
        # CENTRO
        # =================================================

        centerbox = tk.Frame(
            janela,
            width=435,
            height=450,
            bg=BG_PANEL,
            bd=1,
            relief="solid"
        )

        centerbox.place(
            x=245,
            y=100
        )

        centerline = tk.Frame(
            janela,
            width=435,
            height=2,
            bg=GOLD
        )

        centerline.place(
            x=245,
            y=100
        )

        listtitle = tk.Label(
            janela,
            text="FUNCIONÁRIOS NA BLACK LIST",
            bg=BG_PANEL,
            fg=GOLD,
            font=("Arial", 10, "bold")
        )

        listtitle.place(
            x=245,
            y=115,
            width=435
        )

        listsubtitle = tk.Label(
            janela,
            text="USUÁRIOS BLOQUEADOS",
            bg=BG_PANEL,
            fg="#666666",
            font=("Arial", 7)
        )

        listsubtitle.place(
            x=245,
            y=138,
            width=435
        )

        # =================================================
        # NOMES
        # =================================================

        nomesinblack = tk.Label(
            centerbox,
            text="Verificando usuários...",
            bg=BG_PANEL,
            fg=WHITE,
            justify="center",
            anchor="center",
            font=("Arial", 10)
        )

        nomesinblack.place(
            relx=0.5,
            rely=0.52,
            anchor="center"
        )

        try:

            with open(
                "Funcionarios/blacklist.json",
                "r"
            ) as f:

                data = json.load(f)

            funcionarios = data["funcionarios"]

            if funcionarios:

                nomesinblack.config(
                    text="\n".join(funcionarios),
                    justify="center"
                )

            else:

                nomesinblack.config(
                    text="Nenhum funcionário\nna BLACK LIST.",
                    fg=TEXT_DARK
                )

        except FileNotFoundError:

            nomesinblack.config(
                text="Nenhum funcionário\nna BLACK LIST.",
                fg=TEXT_DARK
            )

        # =================================================
        # ÁREA ESQUERDA - ADICIONAR
        # =================================================

        addtitle = tk.Label(
            janela,
            text="ADICIONAR",
            bg=BG_MAIN,
            fg=GOLD,
            font=("Arial", 9, "bold")
        )

        addtitle.place(
            x=15,
            y=105,
            width=190
        )

        # nome

        place = tk.StringVar(
            value="Nome completo"
        )

        getname = tk.Entry(
            janela,
            relief="solid",
            bd=1,
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            textvariable=place,
            justify="center",
            font=("Arial", 9)
        )

        getname.place(
            x=15,
            y=135,
            width=190,
            height=32
        )

        # cargo

        place2 = tk.StringVar(
            value="Cargo (Se tiver)"
        )

        getrole = tk.Entry(
            janela,
            relief="solid",
            bd=1,
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            textvariable=place2,
            justify="center",
            font=("Arial", 9)
        )

        getrole.place(
            x=15,
            y=177,
            width=190,
            height=32
        )

        # adicionar

        confirm = tk.Button(
            janela,
            text="ADICIONAR",
            font=("Arial", 8, "bold"),
            bg=GOLD,
            fg=BG_MAIN,
            activebackground=GOLD_LIGHT,
            activeforeground=BG_MAIN,
            relief="flat",
            cursor="hand2",
            command=lambda: self.react_confirm(
                getname.get(),
                getrole.get()
            )
        )

        confirm.place(
            x=50,
            y=220,
            width=120,
            height=34
        )

        # =================================================
        # LINHA
        # =================================================

        divider = tk.Frame(
            janela,
            bg=BORDER,
            width=190,
            height=1
        )

        divider.place(
            x=15,
            y=280
        )

        # =================================================
        # REMOÇÃO
        # =================================================

        removetitle = tk.Label(
            janela,
            text="REMOÇÃO",
            bg=BG_MAIN,
            fg=RED_LIGHT,
            font=("Arial", 9, "bold")
        )

        removetitle.place(
            x=15,
            y=300,
            width=190
        )

        remover_var = tk.StringVar(
            value="Nome para remover"
        )

        remover_entry = tk.Entry(
            janela,
            relief="solid",
            bd=1,
            bg=BG_ENTRY,
            fg=WHITE,
            insertbackground=GOLD,
            textvariable=remover_var,
            justify="center",
            font=("Arial", 9)
        )

        remover_entry.place(
            x=15,
            y=330,
            width=190,
            height=32
        )

        # remover blacklist

        rem = tk.Button(
            janela,
            text="REMOVER",
            font=("Arial", 8, "bold"),
            bg=RED,
            fg=WHITE,
            activebackground=RED_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            command=lambda: self.remover_blacklist(
                remover_entry.get()
            )
        )

        rem.place(
            x=50,
            y=372,
            width=120,
            height=34
        )

        # remover cadastro

        tirar_dat = tk.Button(
            janela,
            text="REMOVER DO CADASTRO",
            font=("Arial", 7, "bold"),
            bg=GOLD_DARK,
            fg=GOLD_LIGHT,
            activebackground="#806719",
            activeforeground=GOLD_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: self.remover_dat(
                remover_entry.get()
            )
        )

        tirar_dat.place(
            x=20,
            y=414,
            width=180,
            height=32
        )

        # =================================================
        # VOLTAR
        # =================================================

        voltar = tk.Button(
            janela,
            text="←  VOLTAR",
            font=("Arial", 8, "bold"),
            bg=BG_PANEL,
            fg=GOLD,
            activebackground=BG_PANEL_2,
            activeforeground=GOLD_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: Painel().start()
        )

        voltar.place(
            x=15,
            y=550,
            width=100,
            height=30
        )

        janela.mainloop()

    # -----------------------------------------------------
    # REACT CONFIRM
    # -----------------------------------------------------

    def react_confirm(self, nome, cargo=None):

        nome = ''.join(
            c for c in unicodedata.normalize('NFD', nome)
            if unicodedata.category(c) != 'Mn'
        ).upper()

        if cargo is not None:

            cargo = ''.join(
                c for c in unicodedata.normalize('NFD', cargo)
                if unicodedata.category(c) != 'Mn'
            ).upper()

        if cargo == "CARGO (SE TIVER)" or cargo is None:

            try:

                with open(
                    "Funcionarios/blacklist.json",
                    "r"
                ) as f:

                    data = json.load(f)

                try:

                    with open(
                        "Funcionarios/dat.json",
                        "r"
                    ) as f:

                        funcionarios = json.load(f)

                    func2 = funcionarios["funcionarios"]

                except FileNotFoundError:

                    messagebox.showerror(
                        "AVISO EXTREMO",
                        "Erro ao carregar storage funcionarios.\n"
                        "Cadastre um primeiro."
                    )

                    return

                if not nome in func2:

                    messagebox.showerror(
                        "AVISO - Black List PAINEL",
                        "Este nome não está na sua lista de funcionários."
                    )

                    return

                func = data["funcionarios"]

                if nome in func:

                    messagebox.showwarning(
                        "AVISO - Black List PAINEL",
                        "Este nome já está registrado na BLACK LIST."
                    )

                    return

                if len(nome) < 5:

                    messagebox.showerror(
                        "AVISO - Black Lisr PAINEL",
                        "Coloque o nome completo."
                    )

                    return

                with open(
                    "Funcionarios/blacklist.json",
                    "w"
                ) as fl:

                    data["funcionarios"].append(
                        nome
                    )

                    json.dump(
                        data,
                        fl,
                        indent=4
                    )

                messagebox.showinfo(
                    "AVISO - Black List PAINEL",
                    f"Usuario {nome} registrado com sucesso na black list."
                )

                return self.startpanel()

            except FileNotFoundError:

                with open(
                    "Funcionarios/blacklist.json",
                    "w"
                ) as f:

                    toup = {
                        "funcionarios": []
                    }

                    toup["funcionarios"].append(
                        nome
                    )

                    json.dump(
                        toup,
                        f,
                        indent=4
                    )

                messagebox.showinfo(
                    "AVISO - Black List PAINEL",
                    f"Usuario {nome} registrado com sucesso na black list."
                )

                return self.startpanel()

        else:

            try:

                with open(
                    "Funcionarios/blacklist.json",
                    "r"
                ) as f:

                    data = json.load(f)

                funcb = data["funcionarios"]

                try:

                    with open(
                        "Funcionarios/dat.json",
                        "r"
                    ) as f:

                        funcionarios = json.load(f)

                    func2 = funcionarios["funcionarios"]

                except FileNotFoundError:

                    return messagebox.showerror(
                        "AVISO EXTREMO",
                        "Erro ao carregar storage dos funcionários.\n"
                        "Cadastre um primeiro."
                    )

                namewithrole = f"{nome} - {cargo}"

                if len(nome) < 5:

                    return messagebox.showerror(
                        "AVISO - Black Lisr PAINEL",
                        "Coloque o nome completo."
                    )

                if not namewithrole in func2:

                    return messagebox.showerror(
                        "AVISO - Black List PAINEL",
                        "Este funcionário não está registrado."
                    )

                if namewithrole in funcb:

                    return messagebox.showwarning(
                        "AVISO - Black List PAINEL",
                        "Este nome já está registrado na BLACK LIST."
                    )

                with open(
                    "Funcionarios/blacklist.json",
                    "w"
                ) as f:

                    funcb.append(
                        namewithrole
                    )

                    data["funcionarios"] = funcb

                    json.dump(
                        data,
                        f,
                        indent=4
                    )

                messagebox.showinfo(
                    "AVISO - Black List PAINEL",
                    f"Usuario {namewithrole} registrado com sucesso na black list."
                )

                return self.startpanel()

            except FileNotFoundError:

                namewithrole = f"{nome} - {cargo}"

                with open(
                    "Funcionarios/blacklist.json",
                    "w"
                ) as f:

                    data = {
                        "funcionarios": []
                    }

                    data["funcionarios"].append(
                        namewithrole
                    )

                    json.dump(
                        data,
                        f,
                        indent=4
                    )

                messagebox.showinfo(
                    "AVISO - Black List PAINEL",
                    f"Usuario {namewithrole} registrado com sucesso na black list."
                )

                return self.startpanel()

    # -----------------------------------------------------
    # REMOVER DA BLACKLIST
    # -----------------------------------------------------

    def remover_blacklist(self, nome):

        if nome == "Nome para remover" or len(nome) < 5:

            return messagebox.showerror(
                "AVISO - Black List PAINEL",
                "Digite o nome completo para remover."
            )

        try:

            with open(
                "Funcionarios/blacklist.json",
                "r"
            ) as f:

                data = json.load(f)

            funcionarios = data["funcionarios"]

            if nome not in funcionarios:

                return messagebox.showerror(
                    "AVISO - Black List PAINEL",
                    "Este funcionário não está na BLACK LIST."
                )

            funcionarios.remove(
                nome
            )

            with open(
                "Funcionarios/blacklist.json",
                "w"
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4
                )

            messagebox.showinfo(
                "AVISO - Black List PAINEL",
                f"{nome} removido da BLACK LIST com sucesso."
            )

            return self.startpanel()

        except FileNotFoundError:

            return messagebox.showerror(
                "AVISO - Black List PAINEL",
                "A BLACK LIST ainda não foi criada."
            )

    # -----------------------------------------------------
    # REMOVER DO DAT
    # -----------------------------------------------------

    def remover_dat(self, nome):

        if nome == "Nome para remover" or len(nome) < 5:

            return messagebox.showerror(
                "AVISO - Black List PAINEL",
                "Digite o nome completo."
            )

        try:

            with open(
                "Funcionarios/dat.json",
                "r"
            ) as f:

                data = json.load(f)

            funcionarios = data["funcionarios"]

            if nome not in funcionarios:

                return messagebox.showerror(
                    "AVISO - Black List PAINEL",
                    "Este funcionário não está cadastrado no dat.json."
                )

            funcionarios.remove(
                nome
            )

            with open(
                "Funcionarios/dat.json",
                "w"
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4
                )

            messagebox.showinfo(
                "AVISO - Black List PAINEL",
                f"{nome} removido do cadastro de funcionários."
            )

            return self.startpanel()

        except FileNotFoundError:

            return messagebox.showerror(
                "AVISO - Black List PAINEL",
                "O dat.json ainda não foi criado."
            )


# =========================================================
# INICIAR
# =========================================================

play = Login()
play.login_dysplay()
