import re
import tkinter as tk
from controller.OrderController import OrderController
from controller.EmployeeController import EmployeeController
from datetime import datetime
sql_injection_prevention_flag = True

class FormularioPedidoDinamico:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Formulário de Pedido")

        self.itens = []

        self.using_orm_flag = tk.BooleanVar(value=True)
        self.sql_injection_enabled_flag = tk.BooleanVar(value=False)

        frame_opcoes = tk.Frame(self.janela)
        frame_opcoes.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky="w")

        tk.Checkbutton(
            frame_opcoes,
            text="Usar o SQLAlchemy (ORM)",
            variable=self.using_orm_flag
        ).pack(anchor="w")

        tk.Checkbutton(
            frame_opcoes,
            text="Habilitar SQL Injection",
            variable=self.sql_injection_enabled_flag
        ).pack(anchor="w")
        
        self.atualizar_controller()

        self.criar_campo("Nome do Cliente:", 0)
        self.criar_campo("Nome do Vendedor:", 1)
        self.criar_campo_texto("Dados do Pedido:", 2)

        tk.Label(self.janela, text="Itens do Pedido:").grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.frame_itens = tk.Frame(self.janela)
        self.frame_itens.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.adicionar_item() 

        botao_adicionar = tk.Button(self.janela, text="+ Adicionar Item", command=self.adicionar_item)
        botao_adicionar.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        botao_remover = tk.Button(self.janela, text="- Remover Item", command=self.remover_item)
        botao_remover.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        botao_enviar = tk.Button(self.janela, text="Enviar", command=self.enviar)
        botao_enviar.grid(row=6, column=0, columnspan=4, padx=5, pady=10)

        self.entry_order_id = tk.Entry(self.janela)
        self.entry_order_id.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        tk.Label(self.janela, text="ID do Pedido para relatório:").grid(row=7, column=0, padx=5, pady=5, sticky="w")

        botao_relatorio = tk.Button(self.janela, text="📄 Ver Detalhes do Pedido", command=self.ver_relatorio_pedido)
        botao_relatorio.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.entry_data_inicial = tk.Entry(self.janela)
        self.entry_data_inicial.grid(row=10, column=1, padx=5, pady=5, sticky="ew")
        tk.Label(self.janela, text="Data Inicial:").grid(row=10, column=0, padx=5, pady=5, sticky="w")

        self.entry_data_final = tk.Entry(self.janela)
        self.entry_data_final.grid(row=11, column=1, padx=5, pady=5, sticky="ew")
        tk.Label(self.janela, text="Data Final:").grid(row=11, column=0, padx=5, pady=5, sticky="w")

        botao_ranking = tk.Button(self.janela, text="📊 Ver Ranking de Vendedores", command=self.ver_ranking_funcionarios)
        botao_ranking.grid(row=12, column=0, columnspan=2, padx=5, pady=5)  

        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_columnconfigure(3, weight=1)

    def atualizar_controller(self):
        using_orm = self.using_orm_flag.get()
        sql_injection_enabled = self.sql_injection_enabled_flag.get()

        if using_orm and sql_injection_enabled:
            self.mostrar_toast("Não é possível usar o SQLAlchemy e habilitar SQL Injection ao mesmo tempo.")
            self.order_controller = None
            self.using_orm_flag.set(False)
            self.sql_injection_enabled_flag.set(False)
            return

        self.order_controller = OrderController(using_orm=using_orm, sql_injection_enabled=sql_injection_enabled)

    def criar_campo(self, texto_label, linha):
        label = tk.Label(self.janela, text=texto_label)
        label.grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(self.janela)
        entry.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        setattr(self, f"entry_{texto_label.lower().replace(' ', '_').replace(':', '')}", entry)

    def criar_campo_texto(self, texto_label, linha):
        label = tk.Label(self.janela, text=texto_label)
        label.grid(row=linha, column=0, padx=5, pady=5, sticky="nw")
        text = tk.Text(self.janela, height=5, width=30)
        text.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        setattr(self, f"text_{texto_label.lower().replace(' ', '_').replace(':', '')}", text)

    def adicionar_item(self):
        indice = len(self.itens)
        frame_item = tk.Frame(self.frame_itens)
        frame_item.pack(pady=2)

        label_nome = tk.Label(frame_item, text=f"Nome Item {indice + 1}:")
        label_nome.pack(side="left", padx=5)
        entry_nome = tk.Entry(frame_item)
        entry_nome.pack(side="left", padx=5, fill="x", expand=True)

        label_quantidade = tk.Label(frame_item, text=f"Quantidade Item {indice + 1}:")
        label_quantidade.pack(side="left", padx=5)
        entry_quantidade = tk.Entry(frame_item, width=10)
        entry_quantidade.pack(side="left", padx=5)

        self.itens.append({
            "frame": frame_item,
            "nome": entry_nome,
            "quantidade": entry_quantidade
        })

    def remover_item(self):
        if len(self.itens) > 1:
            item_remover = self.itens.pop()
            item_remover["frame"].destroy()

    def mostrar_toast(self, mensagem):
        toast_window = tk.Toplevel(self.janela)
        toast_window.overrideredirect(True) 
        label = tk.Label(toast_window, text=mensagem, padx=20, pady=10)
        label.pack()

        janela_width = self.janela.winfo_width()
        janela_height = self.janela.winfo_height()
        toast_width = toast_window.winfo_reqwidth()
        toast_height = toast_window.winfo_reqheight()

        pos_x = int(self.janela.winfo_rootx() + janela_width/2 - toast_width/2)
        pos_y = int(self.janela.winfo_rooty() + janela_height - toast_height - 50) # Exibir na parte inferior

        toast_window.geometry(f"+{pos_x}+{pos_y}")

        toast_window.after(3000, toast_window.destroy)  # 3000 milissegundos = 3 segundos

    def enviar(self):
        self.atualizar_controller()

        if self.order_controller is None:
            return

        raw_date = self.text_dados_do_pedido.get("1.0", tk.END).strip()

        if raw_date:
            required_date = datetime.strptime(raw_date, "%Y-%m-%d")
        else:
            required_date = datetime.now()

        self.order_controller.InsertOrder(
            customer_name=self.entry_nome_do_cliente.get(),
            employee_name=self.entry_nome_do_vendedor.get(),
            ship_data={"required_date": required_date},
            items=[{
                "productname": item["nome"].get(),
                "quantity": item["quantidade"].get()
            } for item in self.itens]
        )
        self.mostrar_toast("✅ Pedido enviado com sucesso!")

    def ver_relatorio_pedido(self):
        self.atualizar_controller()

        if self.order_controller is None:
            self.mostrar_toast("⚠️ Modo inválido, corrija as opções no canto superior direito.")
            return

        order_id = self.entry_order_id.get().strip()

        if not order_id.isdigit():
            self.mostrar_toast("⚠️ Informe um número de pedido válido.")
            return

        try:
            dados = self.order_controller.GetOrderInformationById(int(order_id))

            if not dados:
                self.mostrar_toast("❌ Pedido não encontrado.")
                return

            print("\n--------------------------------")
            print("📋 DETALHES DO PEDIDO")
            cabecalho = dados[0]
            print(f"Pedido #{cabecalho[0]} - Data: {cabecalho[1]}")
            print(f"Cliente: {cabecalho[2]}")
            print(f"Vendedor: {cabecalho[3]}")
            print("Itens:")
            print("--------------------------------")
            for item in dados:
                print(f"- {item[4]} | Quantidade: {item[5]} | Preço: R$ {item[6]:.2f}")
            print("--------------------------------")

            self.mostrar_toast("✅ Detalhes do pedido exibidos no terminal.")

        except Exception as e:
            print(f"Erro no relatório: {e}")
            self.mostrar_toast(f"❌ Erro ao gerar relatório: {e}")

    def validar_datas(self, data_inicial, data_final):
        padrao = r'^\d{4}-\d{2}-\d{2}$'

        if not re.match(padrao, data_inicial) or not re.match(padrao, data_final):
            self.mostrar_toast("⚠️ Formato de data inválido. Use o formato YYYY-MM-DD.")
            return False

        if (datetime.strptime(data_inicial, "%Y-%m-%d") > datetime.strptime(data_final, "%Y-%m-%d")):
            self.mostrar_toast("⚠️ A data inicial não pode ser maior que a data final.")
            return False

        return True

    def ver_ranking_funcionarios(self):
        self.atualizar_controller()

        if self.order_controller is None:
            self.mostrar_toast("⚠️ Modo inválido, corrija as opções no canto superior direito.")
            return

        initial_date = self.entry_data_inicial.get()
        final_date = self.entry_data_final.get()

        if not initial_date or not final_date:
            self.mostrar_toast("⚠️ Informe as datas inicial e final.")
            return
        
        if not self.validar_datas(initial_date, final_date):
            return
        
        try:
            ranking = self.employee_controller.GetEmployeeRanking(initial_date, final_date)

            if not ranking:
                self.mostrar_toast("❌ Nenhum funcionário encontrado.")
                return
            
            print("\n--------------------------------")
            print("📋 RANKING DE VENDEDORES")
            print("--------------------------------")
            for funcionario in ranking:
                print(f"- {funcionario[0]} | Quantidade de vendas: {funcionario[1]} | Total de vendas: R$ {funcionario[2]:.2f}")
            print("--------------------------------")

            self.mostrar_toast("✅ Ranking de vendedores exibido no terminal.")

        except Exception as e:
            print(f"Erro no ranking: {e}")
            self.mostrar_toast(f"❌ Erro ao gerar ranking: {e}")
