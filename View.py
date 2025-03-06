import tkinter as tk
from tkinter import ttk
from FiFo import FIFO
from SJF import SJF
from Prioridad import Prioridad
from Controller import Gestor, Metrics

class PlanificadorView:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de Procesos")
        self.root.geometry("800x400")  # Aumentar ancho de ventana
        self.root.resizable(False, False)  # Deshabilitar redimensionamiento
        
        # Inicializar el gestor con FIFO como algoritmo inicial
        self.gestor = Gestor(FIFO(), debug=False)
        self.gestor.set_output_callback(self.update_output)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Selector de algoritmo
        ttk.Label(main_frame, text="Algoritmo:").grid(row=0, column=0, sticky=tk.W)
        self.algorithm_var = tk.StringVar(value="FIFO")
        algorithm_combo = ttk.Combobox(main_frame, 
                                     textvariable=self.algorithm_var,
                                     values=["FIFO", "SJF", "Prioridad"],
                                     state="readonly")
        algorithm_combo.grid(row=0, column=1, sticky=tk.W)
        algorithm_combo.bind('<<ComboboxSelected>>', self.change_algorithm)
        
        # Métricas
        metrics_frame = ttk.LabelFrame(main_frame, text="Métricas", padding="5")
        metrics_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.te_var = tk.StringVar(value="Te promedio: --")
        self.ts_var = tk.StringVar(value="Ts promedio: --")
        
        ttk.Label(metrics_frame, textvariable=self.te_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(metrics_frame, textvariable=self.ts_var).grid(row=1, column=0, sticky=tk.W)
        
        # Botones de control
        ttk.Button(main_frame, text="Iniciar", command=self.start_simulation).grid(row=2, column=0)
        ttk.Button(main_frame, text="Detener", command=self.stop_simulation).grid(row=2, column=1)
        
        # Área de log con título
        ttk.Label(main_frame, text="Log de ejecución:").grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.log_text = tk.Text(main_frame, height=15, width=90)  # Aumentar width de 70 a 90
        self.log_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Scrollbar para el log
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar pesos de las filas y columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def change_algorithm(self, event=None):
        algorithm_name = self.algorithm_var.get()
        if algorithm_name == "FIFO":
            self.gestor.set_algorithm(FIFO())
        elif algorithm_name == "SJF":
            self.gestor.set_algorithm(SJF())
        elif algorithm_name == "Prioridad":
            self.gestor.set_algorithm(Prioridad())
        
    def update_process_display(self):
        # Limpiar el área de texto
        self.process_text.delete(1.0, tk.END)
        
        # Mostrar procesos actuales
        if self.gestor.time and self.gestor.time.algorithm.queue:
            for process in self.gestor.time.algorithm.queue:
                self.process_text.insert(tk.END, 
                    f"Proceso: {process.name}\n"
                    f"Tiempo de llegada: {process.getArrivalTime()}\n"
                    f"Tiempo de ejecución restante: {process.execution_time}\n"
                    f"{'Prioridad: ' + str(process.priority) if hasattr(process, 'priority') else ''}\n\n")
    
    def update_metrics(self):
        if self.gestor.time and self.gestor.time.completed_processes:
            metrics = Metrics()
            for process in self.gestor.time.completed_processes:
                metrics.add_process(process)
            self.te_var.set(f"Te promedio: {metrics.calculate_average_te():.2f}")
            self.ts_var.set(f"Ts promedio: {metrics.calculate_average_ts():.2f}")
    
    def start_simulation(self):
        self.log_text.delete(1.0, tk.END)  # Clear log
        self.gestor.run()
        self.update_metrics()
        self.update_process_display()
    
    def stop_simulation(self):
        pass  # Implementar la lógica para detener la simulación

    def update_output(self, message, end="\n"):
        self.log_text.insert(tk.END, message + end)
        self.log_text.see(tk.END)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanificadorView(root)
    root.mainloop()
