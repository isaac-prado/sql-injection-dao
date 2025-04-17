import tkinter as tk
from view.formulario_pedido import FormularioPedidoDinamico

def main():
    janela = tk.Tk()
    app = FormularioPedidoDinamico(janela)
    janela.mainloop()

if __name__ == "__main__":
    main()