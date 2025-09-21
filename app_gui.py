import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import threading


def start_analysis(self):
    """Iniciar análisis en un hilo separado"""
    topic = self.topic_var.get().strip()
    domain = self.domain_var.get().strip()
    
    if not topic or not domain:
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "❌ Error: Debes llenar Topic y Domain\n")
        return
    
    # ... resto del código ...

class SERPAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SERP Analysis Tool")
        self.root.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame de entrada
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Topic
        ttk.Label(input_frame, text="Keyword Principal:").grid(row=0, column=0, sticky=tk.W)
        self.topic_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.topic_var, width=40).grid(row=0, column=1, padx=5)
        
        # Domain
        ttk.Label(input_frame, text="Dominio:").grid(row=1, column=0, sticky=tk.W)
        self.domain_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.domain_var, width=40).grid(row=1, column=1, padx=5)
        
        self.topic_var.set("zapatos running mujer")
        self.domain_var.set("decathlon.es")
        
        # Max Keywords
        ttk.Label(input_frame, text="Nº Keywords:").grid(row=2, column=0, sticky=tk.W)
        self.max_kw_var = tk.StringVar(value="10")
        ttk.Entry(input_frame, textvariable=self.max_kw_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Botón de análisis
        self.analyze_btn = ttk.Button(input_frame, text="Analizar", command=self.start_analysis)
        self.analyze_btn.grid(row=3, column=1, pady=10, sticky=tk.E)
        
        # Progress bar
        self.progress = ttk.Progressbar(input_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Resultados
        result_frame = ttk.Frame(self.root, padding="10")
        result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=70, height=20)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
    
    def start_analysis(self):
        """Iniciar análisis en un hilo separado"""
        self.analyze_btn.config(state='disabled')
        self.progress.start()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Analizando...\n")
        
        # Ejecutar en hilo separado para no bloquear la UI
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()
    
    def run_analysis(self):
        """Ejecutar análisis y actualizar UI"""
        try:
            data = {
                "topic": self.topic_var.get(),
                "domain": self.domain_var.get(),
                "max_keywords": int(self.max_kw_var.get())
            }
            
            response = requests.post(
                "http://localhost:5001/api/analyze",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.show_results(result)
            else:
                self.result_text.insert(tk.END, f"Error: {response.text}\n")
                
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            self.progress.stop()
            self.analyze_btn.config(state='normal')
    
    def show_results(self, result):
        """Mostrar resultados formateados"""
        self.result_text.delete(1.0, tk.END)
        
        # Información básica
        self.result_text.insert(tk.END, f"🔍 ANÁLISIS SERP COMPLETO\n")
        self.result_text.insert(tk.END, f"═" * 50 + "\n\n")
        self.result_text.insert(tk.END, f"📊 Topic: {result['topic']}\n")
        self.result_text.insert(tk.END, f"🌐 Domain: {result['domain']}\n")
        self.result_text.insert(tk.END, f"⏱️ Tiempo: {result['processing_time']}s\n\n")
        
        # Keywords analizadas
        self.result_text.insert(tk.END, f"🔑 Keywords analizadas ({len(result['keywords_analyzed'])}):\n")
        for kw in result['keywords_analyzed']:
            self.result_text.insert(tk.END, f"   • {kw}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Clusters
        self.result_text.insert(tk.END, f"🎯 Intenciones de búsqueda ({len(result['clusters'])}):\n")
        for cluster in result['clusters']:
            self.result_text.insert(tk.END, f"   📦 Cluster {cluster['id']} ({cluster['size']} keywords):\n")
            for kw in cluster['keywords']:
                self.result_text.insert(tk.END, f"      • {kw}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Presencia del dominio
        present = len(result['domain_analysis']['present'])
        missing = len(result['domain_analysis']['missing'])
        self.result_text.insert(tk.END, f"📈 Presencia del dominio:\n")
        self.result_text.insert(tk.END, f"   ✅ Presente en {present} intenciones\n")
        self.result_text.insert(tk.END, f"   ❌ Ausente en {missing} intenciones\n\n")
        
        # Competidores
        if result['top_competitors']:
            self.result_text.insert(tk.END, f"🏆 Top Competidores:\n")
            for comp in result['top_competitors']:
                self.result_text.insert(tk.END, f"   • {comp['domain']} ({comp['count']} apariciones)\n")

def main():
    root = tk.Tk()
    app = SERPAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()