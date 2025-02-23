import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import ipaddress
import threading
from queue import Queue
import requests
import json
import csv
import os

# Default settings
DEFAULT_SETTINGS = {
    "ports": [80, 443, 8080],
    "credentials": [{"username": "admin", "password": "admin"}],
    "timeout": 2,
    "max_threads": 50,
    "dark_theme": False
}

class MasterEyeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Master Eye")
        self.root.geometry("1000x700")
        
        self.current_theme = "default"
        self.scan_active = False
        self.stop_event = threading.Event()
        self.results = []
        self.queue = Queue()
        self.current_range = ""
        
        # Setup styles
        self.setup_theme()
        
        # Create UI
        self.create_widgets()
        self.create_menu()
        self.load_settings()

    def setup_theme(self, dark=False):
        style = ttk.Style()
        if dark:
            self.root.configure(bg='#2e2e2e')
            style.theme_use('alt')
            style.configure('TLabel', background='#2e2e2e', foreground='white')
            style.configure('TFrame', background='#2e2e2e')
            style.configure('Treeview', background='#404040', fieldbackground='#404040', foreground='white')
            style.map('Treeview', background=[('selected', '#0066cc')])
            self.current_theme = "dark"
        else:
            style.theme_use('clam')
            self.root.configure(bg='')  # Fixed for Linux compatibility
            self.current_theme = "light"

    def create_widgets(self):
        # Control Frame
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="IP Range:").grid(row=0, column=0, padx=5)
        self.range_entry = ttk.Entry(control_frame, width=40)
        self.range_entry.grid(row=0, column=1, padx=5)
        
        self.start_btn = ttk.Button(control_frame, text="Start Scan", command=self.start_scan)
        self.start_btn.grid(row=0, column=2, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_scan, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=3, padx=5)

        # Results Treeview
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=('IP', 'Status', 'Ports', 'Login'), show='headings')
        self.tree.heading('IP', text='IP Address', command=lambda: self.sort_column('IP', False))
        self.tree.heading('Status', text='Status', command=lambda: self.sort_column('Status', False))
        self.tree.heading('Ports', text='Open Ports', command=lambda: self.sort_column('Ports', False))
        self.tree.heading('Login', text='Login Success', command=lambda: self.sort_column('Login', False))
        
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Export CSV", command=lambda: self.export_results('csv'))
        file_menu.add_command(label="Export JSON", command=lambda: self.export_results('json'))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings Menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Configure Ports/Credentials", command=self.open_settings)
        settings_menu.add_checkbutton(label="Dark Theme", command=self.toggle_theme)
        
        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)

    def show_about(self):
        messagebox.showinfo("About Master Eye", "Created by UsamaHacker0\nVersion 1.0")

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        
        # Ports Configuration
        ttk.Label(settings_win, text="Ports (comma-separated):").grid(row=0, column=0, padx=5, pady=2)
        self.ports_entry = ttk.Entry(settings_win, width=30)
        self.ports_entry.insert(0, ','.join(map(str, self.settings['ports'])))
        self.ports_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Credentials Configuration
        cred_frame = ttk.LabelFrame(settings_win, text="Credentials")
        cred_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.cred_entries = []
        for i, cred in enumerate(self.settings['credentials']):
            user_entry = ttk.Entry(cred_frame, width=15)
            user_entry.insert(0, cred['username'])
            user_entry.grid(row=i, column=0, padx=2)
            
            pass_entry = ttk.Entry(cred_frame, width=15)
            pass_entry.insert(0, cred['password'])
            pass_entry.grid(row=i, column=1, padx=2)
            self.cred_entries.append((user_entry, pass_entry))
        
        ttk.Button(settings_win, text="Save", command=self.save_settings).grid(row=2, column=1, pady=5)

    def save_settings(self):
        try:
            self.settings['ports'] = [int(p.strip()) for p in self.ports_entry.get().split(',')]
            self.settings['credentials'] = [
                {'username': u.get(), 'password': p.get()}
                for u, p in self.cred_entries
            ]
            messagebox.showinfo("Settings Saved", "Settings updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid settings: {str(e)}")

    def toggle_theme(self):
        self.setup_theme(not self.settings.get('dark_theme', False))
        self.settings['dark_theme'] = not self.settings.get('dark_theme', False)

    def start_scan(self):
        if self.scan_active:
            return
        
        ip_range = self.range_entry.get().strip()
        if not ip_range:
            messagebox.showerror("Error", "Please enter a valid IP range")
            return
        
        try:
            start_ip, end_ip = ip_range.split('-')
            self.start_ip = ipaddress.IPv4Address(start_ip.strip())
            self.end_ip = ipaddress.IPv4Address(end_ip.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Invalid IP range: {str(e)}")
            return
        
        self.scan_active = True
        self.current_range = ip_range.replace(' ', '')
        self.stop_event.clear()
        self.start_btn.config(state=tk.DISABLED)
        self.range_entry.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress['value'] = 0
        self.tree.delete(*self.tree.get_children())
        self.results = []
        
        self.total_ips = int(self.end_ip) - int(self.start_ip) + 1
        self.progress['maximum'] = self.total_ips
        
        threading.Thread(target=self.scan_controller, daemon=True).start()
        self.root.after(100, self.process_queue)

    def scan_controller(self):
        thread_pool = []
        semaphore = threading.Semaphore(self.settings['max_threads'])
        
        for ip_int in range(int(self.start_ip), int(self.end_ip) + 1):
            if self.stop_event.is_set():
                break
            
            semaphore.acquire()
            ip = str(ipaddress.IPv4Address(ip_int))
            thread = threading.Thread(target=self.scan_ip, args=(ip, semaphore))
            thread.start()
            thread_pool.append(thread)
        
        for thread in thread_pool:
            thread.join()
        
        self.root.after(0, self.on_scan_complete)

    def on_scan_complete(self):
        self.scan_active = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.range_entry.config(state=tk.NORMAL)
        self.auto_save_results()
        self.update_stats()

    def scan_ip(self, ip, semaphore):
        if self.stop_event.is_set():
            semaphore.release()
            return
        
        result = {'ip': ip, 'status': 'Dead', 'ports': [], 'login': 'No'}
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.settings['timeout'])
            if sock.connect_ex((ip, 80)) == 0:
                result['status'] = 'Alive'
                
                # Port scanning
                for port in self.settings['ports']:
                    if self.stop_event.is_set():
                        break
                    try:
                        s = socket.socket()
                        s.settimeout(1)
                        s.connect((ip, port))
                        s.close()
                        result['ports'].append(port)
                    except:
                        pass
                
                # Credential check
                for cred in self.settings['credentials']:
                    try:
                        response = requests.post(
                            f"http://{ip}",
                            data=cred,
                            timeout=self.settings['timeout']
                        )
                        if response.status_code == 200 and "login" not in response.text.lower():
                            result['login'] = 'Yes'
                            break
                    except:
                        pass
        except:
            pass
        
        self.queue.put(result)
        semaphore.release()

    def process_queue(self):
        while not self.queue.empty():
            result = self.queue.get()
            self.results.append(result)
            self.tree.insert('', 'end', values=(
                result['ip'],
                result['status'],
                ', '.join(map(str, result['ports'])) if result['ports'] else 'None',
                result['login']
            ))
            self.progress['value'] += 1
            self.status_bar.config(text=f"Scanned {self.progress['value']} of {self.total_ips} IPs")
        
        if self.scan_active:
            self.root.after(100, self.process_queue)

    def stop_scan(self):
        self.stop_event.set()
        self.scan_active = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.range_entry.config(state=tk.NORMAL)
        self.status_bar.config(text="Scan stopped by user")

    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def export_results(self, format):
        if not self.results:
            messagebox.showwarning("No Data", "No scan results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format}",
            filetypes=[(f"{format.upper()} Files", f"*.{format}")]
        )
        if not file_path:
            return
        
        try:
            if format == 'csv':
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['IP Address', 'Status', 'Open Ports', 'Login Success'])
                    for res in self.results:
                        writer.writerow([res['ip'], res['status'], ','.join(map(str, res['ports'])), res['login']])
            elif format == 'json':
                with open(file_path, 'w') as f:
                    json.dump(self.results, f, indent=2)
            
            messagebox.showinfo("Export Successful", f"Results exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def auto_save_results(self):
        if not self.results:
            return
        
        base_name = self.current_range.replace(' ', '').replace('/', '_').replace(':', '_')
        csv_path = f"{base_name}_scan_results.csv"
        json_path = f"{base_name}_scan_results.json"
        
        try:
            # Save CSV
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['IP Address', 'Status', 'Open Ports', 'Login Success'])
                for res in self.results:
                    writer.writerow([res['ip'], res['status'], ', '.join(map(str, res['ports'])) if res['ports'] else 'None', res['login']])
            
            # Save JSON
            with open(json_path, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            self.status_bar.config(text=f"Results auto-saved to {csv_path} and {json_path}")
        except Exception as e:
            messagebox.showerror("Auto-Save Error", str(e))

    def update_stats(self):
        alive = sum(1 for res in self.results if res['status'] == 'Alive')
        logins = sum(1 for res in self.results if res['login'] == 'Yes')
        self.status_bar.config(text=f"Scan complete. Alive hosts: {alive}, Successful logins: {logins}")

    def load_settings(self):
        self.settings = DEFAULT_SETTINGS.copy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterEyeApp(root)
    root.mainloop()