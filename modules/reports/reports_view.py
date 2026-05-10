import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from . import reports_queries

class ReportsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Admin Reports Panel", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20)
        
        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.report_buttons = [
            ("Top Craft Workshop", reports_queries.get_top_craft_workshop),
            ("Studios with No Bookings", reports_queries.get_studios_no_bookings),
            ("Most Active Artist", reports_queries.get_most_active_artist),
            ("Inactive Members", reports_queries.get_inactive_members),
            ("Materials Consumed", reports_queries.get_materials_consumed),
            ("Tool Rental Count", reports_queries.get_tool_rental_count)
        ]
        
        for i, (name, func) in enumerate(self.report_buttons):
            btn = ctk.CTkButton(self.buttons_frame, text=name, command=lambda f=func: self.display_report(f))
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            
        # Results Frame
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.grid_columnconfigure(1, weight=3)
        
        self.table_label = ctk.CTkLabel(self.results_frame, text="Report Results", font=ctk.CTkFont(size=16, weight="bold"))
        self.table_label.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self.results_frame, width=400, height=200)
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.chart_frame = ctk.CTkFrame(self.results_frame)
        self.chart_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def display_report(self, query_func):
        rows, columns = reports_queries.run_query(query_func)
        
        # Display Table (simplified as text for now)
        self.textbox.delete("1.0", ctk.END)
        header_str = " | ".join(columns)
        self.textbox.insert(ctk.END, header_str + "\n" + "-"*len(header_str) + "\n")
        for row in rows:
            self.textbox.insert(ctk.END, " | ".join(map(str, row)) + "\n")
            
        # Display Chart for Q1
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        if query_func == reports_queries.get_top_craft_workshop:
            self.show_chart(rows)

    def show_chart(self, data):
        if not data:
            return
            
        titles = [row[1] for row in data]
        participants = [row[2] for row in data]
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(titles, participants, color='skyblue')
        ax.set_title('Participants per Workshop')
        ax.set_ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
