#StuddyPlanner Projectcode
import os
import json
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import webbrowser
from tkinter import messagebox, simpledialog
import tkinter.font as tkfont
from datetime import datetime, timedelta
import calendar


class LoginWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Study Planner Login")
        self.root.geometry("320x220")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.users_file = "users.json"

        self.users = self.load_users()
        self.create_login_widgets()

    def create_login_widgets(self):
        frame = ctk.CTkFrame(self.root, corner_radius=8, border_width=1)
        frame.pack(expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="w")
        self.username = ctk.CTkEntry(frame)
        self.username.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="w")
        self.password = ctk.CTkEntry(frame, show="*")
        self.password.grid(row=1, column=1, pady=5)

        login_btn = ctk.CTkButton(frame, text="Login", command=self.login, fg_color="#4a90e2", text_color="white")
        login_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        register_btn = ctk.CTkButton(frame, text="Register", command=self.show_register, fg_color="#4a90e2", text_color="white")
        register_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

        phinmaed_btn = ctk.CTkButton(frame, text="Login with PHINMAED",
                command=self.login_with_phinmaed, fg_color="#4caf50", text_color="white")
        phinmaed_btn.grid(row=4, column=0, columnspan=2, pady=(8,0), sticky="ew")

        self.root.bind('<Return>', lambda e: self.login())

    def login_with_phinmaed(self):
        url = "https://sis-up.phinma.edu.ph/iitmsv4eGq0RuNHb0G5WbhLmTKLmTO7YBcJ4RHuXxCNPvuIw=?enc=Bayw8k7hhOLdOM1G6glNb1Zbw0siHGF946zcQ9ljtPs="
        try:
            webbrowser.open(url)
        except Exception:
            messagebox.showerror("Error", "Unable to open PHINMAED link in your browser.")

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_users(self):
        try:
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save users: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username.get().strip()
        password_hash = self.hash_password(self.password.get())

        if not username:
            messagebox.showwarning("Login", "Please enter a username.")
            return

        if username in self.users and self.users[username] == password_hash:
            messagebox.showinfo("Login", f"Welcome, {username}!")
            self.root.withdraw()
            app_root = tk.Toplevel(self.root)
            self.planner_window = StudyPlanner(app_root, username, self.root)
        else:
            messagebox.showerror("Login", "Invalid username or password.")
    def show_register(self):
        register_window = ctk.CTkToplevel(self.root)
        register_window.title("Register")
        register_window.geometry("320x200")

        frame = ctk.CTkFrame(register_window, corner_radius=8, border_width=1)
        frame.pack(expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="w")
        new_username = ctk.CTkEntry(frame)
        new_username.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="w")
        new_password = ctk.CTkEntry(frame, show="*")
        new_password.grid(row=1, column=1, pady=5)

        def register():
            u = new_username.get().strip()
            p = new_password.get()
            if not u or not p:
                messagebox.showwarning("Register", "Please enter username and password.")
                return
            if len(p) < 6:
                messagebox.showwarning("Register", "Password must be at least 6 characters long.")
                return
            if len(p) > 16:
                messagebox.showwarning("Register", "Password must not exceed 16 characters!")
                return
            if u in self.users:
                messagebox.showerror("Register", "Username already exists.")
                return
            self.users[u] = self.hash_password(p)
            self.save_users()
            messagebox.showinfo("Register", "Registration successful!")
            register_window.destroy()

        register_btn = ctk.CTkButton(frame, text="Register", command=register, fg_color="#4a90e2", text_color="white")
        register_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        phinmaed_reg_btn = ctk.CTkButton(frame, text="Register with PHINMAED",
                command=self.login_with_phinmaed, fg_color="#4caf50", text_color="white")
        phinmaed_reg_btn.grid(row=3, column=0, columnspan=2, sticky="ew")

        register_window.bind('<Return>', lambda e: register())








class StudyPlanner:
    def __init__(self, root, username, login_root):
        self.root = root
        self.username = username
        self.login_root = login_root
        self.root.title(f"Study Planner - {self.username}")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")




        # Data storage
        self.tasks = []
        self.filtered_task_indices = []
        self.search_var = tk.StringVar()
        # use a list so manage_subjects can append/remove
        self.subjects = ["GEN 001", "GEN 002", "MAT 152", "ITE 260", "ITE 366"]
        self.themes ={
            # Default background changed to white to remove distracting gray
            "Default": {"bg": "#ffffff", "accent": "#4a90e2", "text": "#333333"},
            "Red": {"bg": "#f37676", "accent": "#aa1212", "text": "#830e18"},
            "Green": {"bg": "#e8f5e8", "accent": "#4caf50", "text": "#2e7d32"},
            "Yellow": {"bg": "#faf2d0", "accent": "#f7e973", "text": "#838b07"},
            "Blue": {"bg": "#cedfff", "accent": "#2ba2e7", "text": "#1361a1"},
            "Purple": {"bg": "#f3e5f5", "accent": "#9c27b0", "text": "#4a148c"},
            "Pink": {"bg": "#ffc4f0", "accent": "#ff75c3", "text": "#8c146c"},








        }
        self.current_theme = "Default"
        # Card design settings: choose visual style for cards
        # 'A' = subtle rounded corner, thin border (default), 'B' = stronger accent border
        self.card_variant = 'A'
        # Enable borders with 2px width and rounded corners
        self.card_shadow = True
        # Compute the border width based on our chosen variant but allow disabling it via card_shadow
        computed_border = 2
        self.card_style = {
            'corner_radius': 8,
            'border_width': 2,
            'use_accent_border': True if self.card_variant == 'B' else False,
        }
        self.sticky_notes = []
        # remember left column view: 'tasks' or 'notes'
        self.left_view = 'tasks'
        self.data_file = f"data_{self.username}.json"
# Daily motivational quotes
        self.quotes = [
            ("The secret of getting ahead is getting started.", "Mark Twain"),
            ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
            ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
            ("It always seems impossible until it's done.", "Nelson Mandela"),
            ("Start where you are. Use what you have. Do what you can.", "Arthur Ashe"),
            ("The future depends on what you do today.", "Mahatma Gandhi"),
            ("Do something today that your future self will thank you for.", "Unknown"),
            ("Small progress is still progress.", "Unknown"),
            ("One step at a time is good walking.", "Chinese Proverb"),
            ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar")
        ]
        self.quote_index = None

        # Initialize quote variables early so update_daily_quote can use them
        self.quote_text_var = tk.StringVar(value="")
        self.quote_author_var = tk.StringVar(value="")

        # Load data
        self.load_data()

        # Store widget references for theme updates
        self.themed_widgets = []




        # Create main interface
        self.create_widgets()
        #populate quick notes view now that widgets
        try:
            self.update_notes_display()
        except Exception:
            pass  
        self.update_calendar()
        self.check_reminders()




        # Apply theme after widgets are created
        self.apply_theme()




        # Save data on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.add_task())
        self.root.bind('<Control-s>', lambda e: self.save_data())

        # Auto-save every 5 minutes
        self.root.after(300000, self.auto_save)




    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=8, border_width=0)
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.themed_widgets.append(self.main_frame)




        self.title_label = ctk.CTkLabel(self.main_frame, text=f"Study Planner: {self.username}",
                        font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(0, 20))
        self.themed_widgets.append(self.title_label)




        # Header card containing the top controls (theme dropdown, buttons)
        self.top_card = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_card.pack(fill=ctk.X, pady=(0, 10), padx=4)
        self.themed_widgets.append(self.top_card)

        # Inner frame inside the card keeps the previous arrangement and spacing
        top_frame = ctk.CTkFrame(self.top_card, fg_color="transparent")
        top_frame.pack(fill=ctk.X, padx=8, pady=8)
        self.themed_widgets.append(top_frame)

        # Initialize theme variable before creating dropdown
        self.theme_var = tk.StringVar(value=self.current_theme)

        # Use a non-editable dropdown so the user can't type an arbitrary theme name
        try:
            # CTkOptionMenu is a simpler dropdown without an editable entry
            theme_dropdown = ctk.CTkOptionMenu(top_frame, values=list(self.themes.keys()), variable=self.theme_var,
                                            width=120, command=self.change_theme)
            theme_dropdown.pack(side=tk.LEFT, padx=(0, 20))
            theme_dropdown.set(self.current_theme)
            # ensure dropdown is included in theme updates
            self.themed_widgets.append(theme_dropdown)
        except Exception:
            # Fallback to readonly CTkComboBox if OptionMenu isn't available
            theme_combo = ctk.CTkComboBox(top_frame, values=list(self.themes.keys()), variable=self.theme_var,
                                        width=120, state="readonly")
            theme_combo.pack(side=tk.LEFT, padx=(0, 20))
            # ensure dropdown is included in theme updates
            self.themed_widgets.append(theme_combo)
            try:
                theme_combo.set(self.current_theme)
            except Exception:
                pass




        self.subjects_btn = ctk.CTkButton(top_frame, text="Manage Subjects", command=self.manage_subjects)
        self.subjects_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.subjects_btn)




        self.reminders_btn = ctk.CTkButton(top_frame, text="View Reminders", command=self.view_reminders)
        self.reminders_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.reminders_btn)

        self.export_btn = ctk.CTkButton(top_frame, text="Export Data", command=self.export_data)
        self.export_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        # ensure export button is included in theme updates
        self.themed_widgets.append(self.export_btn)

        # Container for the two main columns
        self.main_cols = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.main_cols.pack(fill=ctk.BOTH, expand=True)
        self.main_cols.grid_rowconfigure(0, weight=1)
        self.main_cols.grid_columnconfigure(0, weight=1)
        self.main_cols.grid_columnconfigure(1, weight=1)

        self.left_col = ctk.CTkFrame(self.main_cols, fg_color="transparent")
        self.right_col = ctk.CTkFrame(self.main_cols, fg_color="transparent")

        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0,6), pady=4)
        self.right_col.grid(row=0, column=1, sticky="nsew", padx=(6,0), pady=4)

        self.themed_widgets.append(self.left_col)
        self.themed_widgets.append(self.right_col)

        # Create a stacked container inside the left column for Tasks and Notes
        self.left_stack = ctk.CTkFrame(self.left_col, fg_color="transparent")
        self.left_stack.pack(fill=ctk.BOTH, expand=True)
        self.themed_widgets.append(self.left_stack)

        self.create_task_panel(self.left_stack)

        self.create_calendar_panel(self.right_col)

    def create_task_panel(self, parent):
        # Task panel shown as a card to separate it from surrounding UI
        self.task_frame = ctk.CTkFrame(parent, corner_radius=self.card_style['corner_radius'], border_width=self.card_style['border_width'])
        self.task_frame.pack(fill=ctk.BOTH, expand=True, padx=6, pady=(0, 10))
        self.themed_widgets.append(self.task_frame)




        form_frame = ctk.CTkFrame(self.task_frame, fg_color="transparent")
        form_frame.pack(fill=ctk.X, padx=10, pady=10)
        self.themed_widgets.append(form_frame)




        labels_data = [
            ("Type:", 0), ("Subject:", 1), ("Title:", 2),
            ("Date (YYYY-MM-DD):", 3), ("Time (HH:MM):", 4), ("Priority:", 5)
        ]




        self.form_labels = []
        for text, row in labels_data:
            lbl = ctk.CTkLabel(form_frame, text=text)
            lbl.grid(row=row, column=0, sticky="w", pady=2)
            self.form_labels.append(lbl)
            self.themed_widgets.append(lbl)
#task type
        self.task_type_var = tk.StringVar(value="Assignment")
        task_type_combo = ctk.CTkComboBox(form_frame, values=["Assignment", "Exam", "Class", "Study Session"], variable=self.task_type_var, width=150, state="readonly")
        task_type_combo.grid(row=0, column=1, pady=2, sticky="ew")
        task_type_combo.set("Assignment")
#subject
        self.subject_var = tk.StringVar()
        self.subject_combo = ctk.CTkComboBox(form_frame, values=self.subjects, variable=self.subject_var, width=150, state="readonly")
        self.subject_combo.grid(row=1, column=1, pady=2, sticky="ew")
        self.themed_widgets.append(self.subject_combo)
        # track the task type combobox for theming too
        self.themed_widgets.append(task_type_combo)
#title
        self.title_entry = ctk.CTkEntry(form_frame, width=180)
        self.title_entry.grid(row=2, column=1, pady=2, sticky="ew")
        # include form entries in themed widgets so apply_theme can adjust their colors
        self.themed_widgets.append(self.title_entry)
#time
        self.date_entry = ctk.CTkEntry(form_frame, width=180)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1, pady=2, sticky="ew")
        self.themed_widgets.append(self.date_entry)




        self.time_entry = ctk.CTkEntry(form_frame, width=180)
        self.time_entry.insert(0, "09:00")
        self.time_entry.grid(row=4, column=1, pady=2, sticky="ew")
        self.themed_widgets.append(self.time_entry)
        # AM / PM selector (ante meridiem / post meridiem)
        self.am_pm_var = tk.StringVar(value="AM")
        ampm_combo = ctk.CTkComboBox(form_frame, values=["AM", "PM"], variable=self.am_pm_var, width=60, state="readonly")
        ampm_combo.grid(row=4, column=2, padx=(5,0), pady=2)
        ampm_combo.set("AM")
#priority
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ctk.CTkComboBox(form_frame, values=["Low", "Medium", "High"], variable=self.priority_var, width=150, state="readonly")
        priority_combo.grid(row=5, column=1, pady=2, sticky="ew")
        priority_combo.set("Medium")
        self.themed_widgets.append(priority_combo)




        form_frame.columnconfigure(1, weight=1)




        btn_frame = ctk.CTkFrame(self.task_frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, padx=10, pady=5)
        self.themed_widgets.append(btn_frame)




        self.add_btn = ctk.CTkButton(btn_frame, text="Add Task", command=self.add_task)
        self.add_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.add_btn)
        self.edit_btn = ctk.CTkButton(btn_frame, text="Edit Selected", command=self.edit_task)
        self.edit_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        # include edit button in themed widgets
        self.themed_widgets.append(self.edit_btn)




        self.delete_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_task)
        self.delete_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.delete_btn)

        self.mark_done_btn = ctk.CTkButton(btn_frame, text="Mark Done", command=self.mark_task_done)
        self.mark_done_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.mark_done_btn)




#search bar
        # Add a priority-toggle button and search entry side-by-side on the right
        # Priority button cycles through: All, High, Medium, Low (default: Medium)
        self.priority_levels = ["All", "High", "Medium", "Low"]
        # default to Medium so the UI shows that option at startup
        self.priority_index = self.priority_levels.index("All")


        def _toggle_priority_sort():
            # Advance to the next priority label and refresh list
            self.priority_index = (self.priority_index + 1) % len(self.priority_levels)
            self._update_priority_button_text()
            # also refresh color to reflect the new priority selection
            try:
                self._update_priority_button_color()
            except Exception:
                pass
            self.update_task_list()


        self.priority_btn = ctk.CTkButton(btn_frame, text=f"{self.priority_levels[self.priority_index]}",
                command=_toggle_priority_sort, width=100)
        # make sure priority button is styled by apply_theme
        self.themed_widgets.append(self.priority_btn)
        # pack the priority button so it's visible in the controls row
        try:
            self.priority_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        except Exception:
            pass
        # keep a helper to update the label when toggled
        def _update_priority_button_text():
            cur = self.priority_levels[self.priority_index]
            # show which priority is selected and keep label consistent
            self.priority_btn.configure(text=f"{cur}")


        def _update_priority_button_color():
            # Pick a color for each priority state. Keep good contrast for text.
            cur = self.priority_levels[self.priority_index]
            # Use theme accent for "All" so it looks neutral/primary
            theme = self.themes.get(getattr(self, 'current_theme', 'Default'), {
                'accent': '#4a90e2'
            })
            color_map = {
                'All': theme.get('accent', "#4a90e2"),
                'High': "#f44336",  # Red for high priority
                'Medium': "#ff9800",  # Orange for medium
                'Low': "#4caf50"  # Green for low
            }
            fg_color = color_map.get(cur, theme.get('accent', '#4a90e2'))
            # Decide foreground color based on brightness (use white for colored backgrounds)
            text_color = 'white'
            try:
                self.priority_btn.configure(fg_color=fg_color, text_color=text_color)
            except Exception:
                pass


        # Attach helpers as method-like attributes so other methods can call
        self._update_priority_button_text = _update_priority_button_text
        self._update_priority_button_color = _update_priority_button_color

# calendar
        # Ensure task_tree exists (create minimal Treeview if it was moved during refactor)
        try:
            if not hasattr(self, 'task_tree') or self.task_tree is None:
                list_frame = ctk.CTkFrame(self.task_frame, fg_color="transparent")
                list_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(5,10))
                self.task_tree = ttk.Treeview(list_frame, columns=("Priority", "Date", "Time", "Type", "Subject", "Title"), show="headings")
                for col, width, anchor in [("Priority", 80, "center"), ("Date", 100, "center"), ("Time", 90, "center"), ("Type", 100, "w"), ("Subject", 120, "w"), ("Title", 300, "w")]:
                    self.task_tree.heading(col, text=col)
                    self.task_tree.column(col, width=width, anchor=anchor)
                scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
                self.task_tree.configure(yscrollcommand=scrollbar.set)
                self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                try:
                    self.themed_widgets.append(self.task_tree)
                except Exception:
                    pass
        except Exception:
            self.task_tree = None
        try:
            if getattr(self, 'task_tree', None) is not None:
                self.task_tree.bind("<Double-1>", lambda e: self.edit_task())
        except Exception:
            pass




        self.update_task_list()


    def create_notes_panel(self, parent):
        """Create the Notes panel. Keeps widget names used elsewhere."""
        self.notes_frame = ctk.CTkFrame(parent, corner_radius=self.card_style['corner_radius'], border_width=self.card_style['border_width'])
        self.notes_frame.pack(fill=ctk.BOTH, expand=True, padx=0, pady=(10,0))
        self.themed_widgets.append(self.notes_frame)

        # Title for notes section
        notes_title = ctk.CTkLabel(self.notes_frame, text="Quick Notes", 
                                    font=("Arial", 14, "bold"))
        notes_title.pack(pady=(10, 5), padx=10)
        self.themed_widgets.append(notes_title)

        # Input row for new note
        self.note_input_frame = ctk.CTkFrame(self.notes_frame, fg_color="transparent")
        self.note_input_frame.pack(fill=ctk.X, padx=10, pady=(8, 6))
        self.themed_widgets.append(self.note_input_frame)

        self.note_entry = ctk.CTkEntry(self.note_input_frame)
        self.note_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        self.note_entry.bind('<Return>', lambda e: self.add_note())
        self.themed_widgets.append(self.note_entry)

        self.add_note_btn = ctk.CTkButton(self.note_input_frame, text="Add", command=self.add_note)
        self.add_note_btn.pack(side=ctk.RIGHT, padx=6, pady=4)
        self.themed_widgets.append(self.add_note_btn)

        # Buttons row (delete / clear)
        note_btn_frame = ctk.CTkFrame(self.notes_frame, fg_color="transparent")
        note_btn_frame.pack(fill=ctk.X, padx=10, pady=(0, 6))
        self.themed_widgets.append(note_btn_frame)

        self.edit_note_btn = ctk.CTkButton(note_btn_frame, text="Edit Selected", command=self.edit_note)
        self.edit_note_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.edit_note_btn)

        self.delete_note_btn = ctk.CTkButton(note_btn_frame, text="Delete Selected", command=self.delete_note)
        self.delete_note_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.delete_note_btn)

        self.clear_notes_btn = ctk.CTkButton(note_btn_frame, text="Clear All", command=self.clear_all_notes)
        self.clear_notes_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.clear_notes_btn)

        # Notes display
        notes_display_frame = ctk.CTkFrame(self.notes_frame, fg_color="transparent")
        notes_display_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.themed_widgets.append(notes_display_frame)

        self.notes_tree = ttk.Treeview(notes_display_frame, columns=("Date", "Time", "Note"), show="headings", height=8)
        self.notes_tree.heading("Date", text="Date")
        self.notes_tree.heading("Time", text="Time")
        self.notes_tree.heading("Note", text="Note")
        self.notes_tree.column("Date", width=100, anchor="center")
        self.notes_tree.column("Time", width=80, anchor="center")
        self.notes_tree.column("Note", width=320, anchor="w")

        notes_scrollbar = tk.Scrollbar(notes_display_frame, orient=tk.VERTICAL, command=self.notes_tree.yview)
        self.notes_tree.configure(yscrollcommand=notes_scrollbar.set)
        self.notes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.themed_widgets.append(self.notes_tree)
        
        # Bind double-click to edit note
        self.notes_tree.bind("<Double-1>", lambda e: self.edit_note())

        # Populate notes if any
        try:
            self.update_notes_display()
        except Exception:
            pass




    def create_calendar_panel(self, parent):
        # Top container to hold calendar (left) and daily quote (right)
        top_container = ctk.CTkFrame(parent, fg_color="transparent")
        top_container.pack(fill=ctk.X, pady=(0, 10))
        self.themed_widgets.append(top_container)




        # Calendar card (left) — visually grouped with subtle border and padding
        # Layout: calendar occupies most of the space; quotes (inspiration) is given a fixed width
        self.cal_frame = ctk.CTkFrame(top_container, corner_radius=self.card_style['corner_radius'], border_width=self.card_style['border_width'])
        self.cal_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0,6), pady=6)
        self.themed_widgets.append(self.cal_frame)




        nav_frame = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav_frame.pack(fill=ctk.X, padx=10, pady=5)
        self.themed_widgets.append(nav_frame)




        self.current_date = datetime.now()




        # Smaller prev/next buttons for a compact calendar control
        self.prev_btn = ctk.CTkButton(nav_frame, text="<<", command=self.prev_month, width=36, height=28)
        self.prev_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.prev_btn)




        self.month_label = ctk.CTkLabel(nav_frame, text="", font=("Arial", 12, "bold"))
        self.month_label.pack(side=ctk.LEFT, expand=True)
        self.themed_widgets.append(self.month_label)




        self.next_btn = ctk.CTkButton(nav_frame, text=">>", command=self.next_month, width=36, height=28)
        self.next_btn.pack(side=ctk.RIGHT, padx=6, pady=4)
        self.themed_widgets.append(self.next_btn)




        self.calendar_frame = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        # Make the calendar grid expand to fill the available space and ensure cells align
        self.calendar_frame.pack(fill=ctk.BOTH, padx=10, pady=5, expand=True)
        # We'll ensure the grid inside calendar_frame expands later in update_calendar via column/row configure
        self.themed_widgets.append(self.calendar_frame)




        # Quotes card (right) - shows a daily motivational quote (narrow fixed width so calendar gets more space)
        self.quote_card = ctk.CTkFrame(top_container, corner_radius=self.card_style['corner_radius'], 
                                       border_width=self.card_style['border_width'], width=280)
        self.quote_card.pack(side=ctk.RIGHT, fill=ctk.Y, padx=(6,0), pady=6)
        self.quote_card.pack_propagate(False)  # Maintain fixed width
        self.themed_widgets.append(self.quote_card)

        # Quote title
        quote_title = ctk.CTkLabel(self.quote_card, text="Daily Inspiration", 
                                    font=("Arial", 14, "bold"))
        quote_title.pack(pady=(10, 5), padx=10)
        self.themed_widgets.append(quote_title)

        # Quote text display
        self.quote_text_label = ctk.CTkLabel(self.quote_card, textvariable=self.quote_text_var,
                                             font=("Arial", 11, "italic"), wraplength=240, 
                                             justify="center")
        self.quote_text_label.pack(pady=(10, 5), padx=10, fill=ctk.X, expand=True)
        self.themed_widgets.append(self.quote_text_label)

        # Quote author display
        self.quote_author_label = ctk.CTkLabel(self.quote_card, textvariable=self.quote_author_var,
                                               font=("Arial", 10), wraplength=240, justify="center")
        self.quote_author_label.pack(pady=(0, 10), padx=10)
        self.themed_widgets.append(self.quote_author_label)

        # Button to cycle through quotes
        self.another_quote_btn = ctk.CTkButton(self.quote_card, text="Another Quote", 
                                               command=self._cycle_quote, width=120, height=28)
        self.another_quote_btn.pack(pady=(5, 10))
        self.themed_widgets.append(self.another_quote_btn)


        # notes input moved to create_notes_panel




        # add_note button moved to create_notes_panel




        # notes button frame moved to create_notes_panel




        # delete_note button moved to create_notes_panel




        # clear_notes button moved to create_notes_panel




        # notes display frame moved to create_notes_panel




        # notes treeview moved to create_notes_panel




        # notes scrollbar and packing moved to create_notes_panel




        # set initial quote
        self.update_daily_quote()
        
        # Create notes panel below calendar and quotes
        self.create_notes_panel(parent)




    def _show_left_view(self, value_or_view=None):
        """Toggle left column between Tasks and Notes views.
        Accepts either the segmented-button label ('Tasks'/'Notes') or the view name ('tasks'/'notes').
        """
        # Normalize input
        if isinstance(value_or_view, str):
            v = value_or_view.strip().lower()
            if v in ('tasks', 'notes'):
                view = v
            else:
                view = value_or_view.strip().lower()
        elif hasattr(self, 'left_view'):
            view = self.left_view
        else:
            view = 'tasks'

        # Hide/show frames — keep them alive so state persists
        try:
            if view == 'notes':
                if hasattr(self, 'task_frame'):
                    try:
                        self.task_frame.pack_forget()
                    except Exception:
                        pass
                if hasattr(self, 'notes_frame'):
                    try:
                        self.notes_frame.pack(fill=ctk.BOTH, expand=True, padx=6, pady=(6,0))
                    except Exception:
                        pass
                self.left_view = 'notes'
            else:
                # default to tasks
                if hasattr(self, 'notes_frame'):
                    try:
                        self.notes_frame.pack_forget()
                    except Exception:
                        pass
                if hasattr(self, 'task_frame'):
                    try:
                        self.task_frame.pack(fill=ctk.BOTH, expand=True, padx=6, pady=(0,10))
                    except Exception:
                        pass
                self.left_view = 'tasks'
        except Exception:
            pass

        # Keep segmented/btn UI consistent
        try:
            if hasattr(self, 'left_view_var'):
                self.left_view_var.set('Tasks' if self.left_view == 'tasks' else 'Notes')
        except Exception:
            pass


    def update_calendar(self):
        # Update month label
        self.month_label.configure(text=self.current_date.strftime("%B %Y"))




        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()




        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)




        # Day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        theme = self.themes[self.current_theme]




        for col, day in enumerate(days):
            lbl = ctk.CTkLabel(self.calendar_frame, text=day, font=("Arial", 10, "bold"))
            lbl.grid(row=0, column=col, padx=2, pady=2)

        # Make each calendar column (Mon..Sun) expand evenly
        try:
            for c in range(len(days)):
                self.calendar_frame.grid_columnconfigure(c, weight=1, uniform='day')
        except Exception:
            pass




        # Calendar dates
        today = datetime.now()
        for row_num, week in enumerate(cal, start=1):
            for col_num, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                else:
                    # Check if this is today
                    is_today = (day == today.day and
                            self.current_date.month == today.month and
                            self.current_date.year == today.year)




                    # Check if there are tasks on this day
                    date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                    has_task = any(t.get("datetime", "").startswith(date_str) for t in self.tasks)




                    bg_color = theme["accent"] if is_today else theme["bg"]
                    fg_color = "white" if is_today else theme["text"]




                    font_weight = "bold" if (is_today or has_task) else "normal"




                    lbl = ctk.CTkLabel(self.calendar_frame, text=str(day), font=("Arial", 9, font_weight))
                    lbl.bind("<Button-1>", lambda e, d=day: self.show_tasks_for_date(d))




                lbl.grid(row=row_num, column=col_num, padx=1, pady=1, sticky="nsew")
            # ensure the row expands so cells align evenly when the frame is stretched
            try:
                self.calendar_frame.grid_rowconfigure(row_num, weight=1)
            except Exception:
                pass




    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Add Task", "Please enter a title.")
            return
        try:
            date_text = self.date_entry.get().strip()
            time_text = self.time_entry.get().strip()
            # Expect time_text as HH:MM in 12-hour format plus AM/PM selector
            parts = time_text.split(":")
            if len(parts) != 2:
                raise ValueError("Invalid time")
            hour = int(parts[0])
            minute = int(parts[1])
            ampm = (self.am_pm_var.get() or "AM").upper()
            # Convert 12-hour -> 24-hour
            if ampm == "AM" and hour == 12:
                hour = 0
            elif ampm == "PM" and hour < 12:
                hour += 12
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                messagebox.showwarning("Add Task", "Invalid time: Hours 0-23, minutes 0-59.")
                return
            dt = datetime.strptime(f"{date_text} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M")
        except Exception:
            messagebox.showwarning("Add Task", "Invalid date/time format.")
            return
        task = {
            "type": self.task_type_var.get(),
            "subject": self.subject_var.get(),
            "title": title,
            "datetime": dt.isoformat(),
            "priority": self.priority_var.get()
        }
        self.tasks.append(task)
        self.save_data()
        self.update_task_list()
        self.update_calendar()
        self.clear_task_form()




    def edit_task(self):
        sel = self.task_tree.selection()
        if not sel:
            messagebox.showwarning("Edit Task", "Select a task to edit.")
            return
        # Reject separator rows (non-numeric iid) so user cannot edit them
        iid = sel[0]
        if not iid.isdigit():
            messagebox.showwarning("Edit Task", "Please select a real task, not the Finished separator.")
            return
        # iid is set to the actual tasks index in update_task_list
        actual_idx = int(iid)
        task = self.tasks[actual_idx]
        
        # Create professional edit dialog
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("450x500")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Center the window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (500 // 2)
        edit_window.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(edit_window, corner_radius=8, border_width=1)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(frame, text="Edit Task", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 20))
        
        # Form frame
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Task Type
        ctk.CTkLabel(form_frame, text="Type:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        type_var = tk.StringVar(value=task.get("type", "Assignment"))
        type_combo = ctk.CTkComboBox(form_frame, values=["Assignment", "Exam", "Class", "Study Session"], 
                                     variable=type_var, width=250, state="readonly")
        type_combo.grid(row=0, column=1, pady=8, sticky="ew")
        type_combo.set(task.get("type", "Assignment"))
        
        # Subject
        ctk.CTkLabel(form_frame, text="Subject:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
        subject_var = tk.StringVar(value=task.get("subject", ""))
        subject_combo = ctk.CTkComboBox(form_frame, values=self.subjects, variable=subject_var, 
                                        width=250, state="readonly")
        subject_combo.grid(row=1, column=1, pady=8, sticky="ew")
        subject_combo.set(task.get("subject", ""))
        
        # Title
        ctk.CTkLabel(form_frame, text="Title:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
        title_entry = ctk.CTkEntry(form_frame, width=250)
        title_entry.insert(0, task.get("title", ""))
        title_entry.grid(row=2, column=1, pady=8, sticky="ew")
        
        # Date
        ctk.CTkLabel(form_frame, text="Date:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=8, padx=(0, 10))
        date_entry = ctk.CTkEntry(form_frame, width=250)
        try:
            dt_obj = datetime.fromisoformat(task.get("datetime", ""))
            date_entry.insert(0, dt_obj.strftime("%Y-%m-%d"))
        except:
            date_entry.insert(0, task.get("datetime", "").split("T")[0] if "T" in task.get("datetime", "") else "")
        date_entry.grid(row=3, column=1, pady=8, sticky="ew")
        
        # Time
        ctk.CTkLabel(form_frame, text="Time:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=8, padx=(0, 10))
        time_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        time_frame.grid(row=4, column=1, pady=8, sticky="ew")
        
        time_entry = ctk.CTkEntry(time_frame, width=140)
        try:
            dt_obj = datetime.fromisoformat(task.get("datetime", ""))
            time_entry.insert(0, dt_obj.strftime("%I:%M"))
            ampm_value = dt_obj.strftime("%p")
        except:
            time_entry.insert(0, "09:00")
            ampm_value = "AM"
        time_entry.pack(side=ctk.LEFT)
        
        ampm_var = tk.StringVar(value=ampm_value)
        ampm_combo = ctk.CTkComboBox(time_frame, values=["AM", "PM"], variable=ampm_var, 
                                     width=80, state="readonly")
        ampm_combo.pack(side=ctk.LEFT, padx=(10, 0))
        ampm_combo.set(ampm_value)
        
        # Priority
        ctk.CTkLabel(form_frame, text="Priority:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=8, padx=(0, 10))
        priority_var = tk.StringVar(value=task.get("priority", "Medium"))
        priority_combo = ctk.CTkComboBox(form_frame, values=["Low", "Medium", "High"], 
                                         variable=priority_var, width=250, state="readonly")
        priority_combo.grid(row=5, column=1, pady=8, sticky="ew")
        priority_combo.set(task.get("priority", "Medium"))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Button frame
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=(15, 10))
        
        def save_changes():
            new_title = title_entry.get().strip()
            if not new_title:
                messagebox.showwarning("Edit Task", "Please enter a title.", parent=edit_window)
                return
            
            try:
                date_text = date_entry.get().strip()
                time_text = time_entry.get().strip()
                parts = time_text.split(":")
                if len(parts) != 2:
                    raise ValueError("Invalid time")
                hour = int(parts[0])
                minute = int(parts[1])
                ampm = ampm_var.get().upper()
                
                # Convert 12-hour to 24-hour
                if ampm == "AM" and hour == 12:
                    hour = 0
                elif ampm == "PM" and hour < 12:
                    hour += 12
                
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    messagebox.showwarning("Edit Task", "Invalid time: Hours 0-23, minutes 0-59.", parent=edit_window)
                    return
                
                dt = datetime.strptime(f"{date_text} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M")
            except Exception:
                messagebox.showwarning("Edit Task", "Invalid date/time format.", parent=edit_window)
                return
            
            # Update task
            task["type"] = type_var.get()
            task["subject"] = subject_var.get()
            task["title"] = new_title
            task["datetime"] = dt.isoformat()
            task["priority"] = priority_var.get()
            
            self.save_data()
            self.update_task_list()
            self.update_calendar()
            edit_window.destroy()
        
        def cancel():
            edit_window.destroy()
        
        # Save button
        save_btn = ctk.CTkButton(btn_frame, text="Save Changes", command=save_changes, 
                                 fg_color="#4a90e2", text_color="white", width=140)
        save_btn.pack(side=ctk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=cancel, 
                                   fg_color="#666666", text_color="white", width=140)
        cancel_btn.pack(side=ctk.LEFT, padx=5)
        
        # Bind Enter key to save and Escape to cancel
        edit_window.bind('<Return>', lambda e: save_changes())
        edit_window.bind('<Escape>', lambda e: cancel())
        
        # Focus on title entry
        title_entry.focus_set()




    def delete_task(self):
        sel = self.task_tree.selection()
        if not sel:
            messagebox.showwarning("Delete Task", "Select a task to delete.")
            return
        # Prevent deleting the separator row
        iid = sel[0]
        if not iid.isdigit():
            messagebox.showwarning("Delete Task", "Cannot delete the Finished separator. Please select a task.")
            return
        try:
            actual_idx = int(iid)
        except Exception:
            messagebox.showerror("Delete Task", "Could not determine selected task.")
            return
        if messagebox.askyesno("Delete Task", "Delete selected task?"):
            try:
                self.tasks.pop(actual_idx)
            except Exception:
                messagebox.showerror("Delete Task", "Failed to delete the selected task.")
                return
            self.save_data()
            self.update_task_list()
            self.update_calendar()




    def mark_task_done(self):
        sel = self.task_tree.selection()
        if not sel:
            messagebox.showwarning("Mark Done", "Select a task to mark as done.")
            return
        iid = sel[0]
        if not iid.isdigit():
            messagebox.showwarning("Mark Done", "Cannot mark the Finished separator. Please select a task.")
            return
        try:
            idx = int(iid)
        except Exception:
            messagebox.showerror("Mark Done", "Could not determine selected task.")
            return
        self.tasks[idx]["done"] = not self.tasks[idx].get("done", False)
        self.save_data()
        self.update_task_list()
        self.update_calendar()




    def clear_task_form(self):
        self.title_entry.delete(0, tk.END)
        self.subject_var.set("")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "09:00")
        self.priority_var.set("Medium")
        if hasattr(self, "am_pm_var"):
            self.am_pm_var.set("AM")




    def _format_time_entry(self, event=None):
        """Format time entry to auto-insert ':' after two digits (HH:MM)."""
        try:
            s = self.time_entry.get()
        except Exception:
            return
        # Keep only digits
        digits = ''.join(ch for ch in s if ch.isdigit())
        if not digits:
            new = ""
        elif len(digits) <= 2:
            new = digits
        else:
            new = digits[:2] + ":" + digits[2:4]
        # limit to 5 characters (HH:MM)
        new = new[:5]
        if new != s:
            # update entry without triggering recursion (we're on KeyRelease/FocusOut)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, new)
            # place cursor at end for simplicity
            try:
                self.time_entry.icursor(len(new))
            except Exception:
                pass




    def update_task_list(self):
        # prefer StringVar but fall back to entry content (handles placeholder)
        try:
            q = (self.search_var.get() or "").strip().lower()
        except Exception:
            q = ""
        # fallback to entry text if var is empty (entry may contain user text)
        if (not q or q == "") and hasattr(self, "search_entry"):
            try:
                q_e = (self.search_entry.get() or "").strip().lower()
                if q_e:
                    q = q_e
            except Exception:
                pass
        # ignore placeholder text
        if q == "search...":
            q = ""




        # Prepare sorted indices by datetime so tasks are shown in chronological order
        def _parse_dt(dt_str):
            if not dt_str:
                return datetime.max
            try:
                return datetime.fromisoformat(dt_str)
            except Exception:
                try:
                    return datetime.strptime(dt_str[:16].replace("T", " "), "%Y-%m-%d %H:%M")
                except Exception:
                    return datetime.max


        # sort by priority (High -> Medium -> Low), then by datetime
        priority_rank = {"High": 0, "Medium": 1, "Low": 2}
        # Determine current selection of the priority button (All/High/Medium/Low)
        try:
            selected_priority = self.priority_levels[self.priority_index]
        except Exception:
            selected_priority = "All"
        def _sort_key(i):
            t = self.tasks[i]
            pr = t.get("priority", "") or ""
            rank = priority_rank.get(pr, 3)  # unknown priorities go last
            return (rank, _parse_dt(t.get("datetime", "")))


        sorted_indices = sorted(range(len(self.tasks)), key=_sort_key)




        # Clear treeview and reset filtered indices
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        self.filtered_task_indices = []


        now = datetime.now()


        upcoming = []
        finished = []


        for i in sorted_indices:
            t = self.tasks[i]
            title = t.get("title", "")
            subject = t.get("subject", "")
            ttype = t.get("type", "")
            priority = t.get("priority", "")
            dt = t.get("datetime", "")




            # Format date/time for display
            date_only = ""
            time_only = ""
            dt_str = ""
            if dt:
                try:
                    # Prefer strict ISO parsing so we can format time nicely
                    dt_obj = datetime.fromisoformat(dt)
                except Exception:
                    try:
                        # Fallback to older stored format patterns
                        dt_obj = datetime.strptime(dt[:16].replace("T", " "), "%Y-%m-%d %H:%M")
                    except Exception:
                        dt_obj = None


                if dt_obj:
                    date_only = dt_obj.date().isoformat()
                    # show time in 12-hour format with AM/PM
                    time_only = dt_obj.strftime("%I:%M %p")
                    dt_str = f"{date_only} {time_only}".strip()
                else:
                    # best-effort fallback (keep original behavior)
                    try:
                        if "T" in dt:
                            date_only, time_part = dt.split("T", 1)
                        else:
                            parts = dt.split()
                            date_only = parts[0] if parts else ""
                            time_part = parts[1] if len(parts) > 1 else ""
                        time_only = time_part[:5]
                        dt_str = f"{date_only} {time_only}".strip()
                    except Exception:
                        dt_str = dt[:16].replace("T", " ")




            hay = f"{title} {subject} {ttype} {priority} {date_only} {dt_str}".lower()




            # Apply priority filter when selected (All shows everything)
            if selected_priority != "All" and priority != selected_priority:
                # skip items that don't match filter
                continue


            if not q or q in hay:
                # Determine if task datetime is in the past or manually marked done
                is_done = self.tasks[i].get("done", False)
                dt_obj = None
                if dt:
                    try:
                        dt_obj = datetime.fromisoformat(dt)
                    except Exception:
                        try:
                            dt_obj = datetime.strptime(dt[:16].replace("T", " "), "%Y-%m-%d %H:%M")
                        except Exception:
                            dt_obj = None
                if dt_obj and dt_obj < now:
                    is_done = True


                entry = (i, (priority, date_only, time_only, ttype, subject, title), is_done)
                if is_done:
                    finished.append(entry)
                else:
                    upcoming.append(entry)


        # Insert upcoming tasks first, then a separator, then finished tasks
        for (i, values, _done) in upcoming:
            iid = str(i)
            try:
                self.task_tree.insert("", tk.END, iid=iid, values=values)
            except Exception:
                self.task_tree.insert("", tk.END, iid=iid, values=values)
            self.filtered_task_indices.append(i)


        for (i, values, _done) in finished:
            iid = str(i)
            try:
                self.task_tree.insert("", tk.END, iid=iid, values=values, tags=("done",))
            except Exception:
                self.task_tree.insert("", tk.END, iid=iid, values=values, tags=("done",))
            self.filtered_task_indices.append(i)


        if finished:
            # Add a non-selectable separator row at the bottom indicating completion
            try:
                sep_values = ("", "", "", "", "", "— Finished —")
                self.task_tree.insert("", tk.END, iid="sep_finished", values=sep_values, tags=("sep",))
            except Exception:
                pass




    def show_tasks_for_date(self, day):
        date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
        tasks_on_date = [t for t in self.tasks if t.get("datetime", "").startswith(date_str)]
        if tasks_on_date:
            msg = "\n".join([f"{t['title']} ({t['type']})" for t in tasks_on_date])
        else:
            msg = "No tasks on this date."
        messagebox.showinfo("Tasks", msg)




    def prev_month(self):
        first = self.current_date.replace(day=1)
        prev_month = first - timedelta(days=1)
        self.current_date = prev_month.replace(day=1)
        self.update_calendar()




    def next_month(self):
        year = self.current_date.year + (1 if self.current_date.month == 12 else 0)
        month = (self.current_date.month % 12) + 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.update_calendar()




    def add_note(self):
        text = self.note_entry.get().strip()
        if not text:
            return
        # Use 12-hour clock with AM/PM for clarity in the notes view
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        self.sticky_notes.append({"text": text, "time": timestamp})
        self.note_entry.delete(0, tk.END)
        self.save_data()
        self.update_notes_display()  # Ensure the display updates after adding a note




    def delete_note(self):
        sel = self.notes_tree.selection()
        if not sel:
            messagebox.showwarning("Delete Note", "Please select a note to delete.")
            return
        # We store the sticky_notes index as the iid when populating
        try:
            actual_idx = int(sel[0])
        except Exception:
            messagebox.showwarning("Delete Note", "Could not determine selected note.")
            return
        if messagebox.askyesno("Delete Note", "Delete selected note?"):
            try:
                self.sticky_notes.pop(actual_idx)
            except Exception:
                messagebox.showerror("Delete Note", "Failed to delete the selected note.")
                return
            self.save_data()
            self.update_notes_display()




    def edit_note(self):
        sel = self.notes_tree.selection()
        if not sel:
            messagebox.showwarning("Edit Note", "Please select a note to edit.")
            return
        try:
            actual_idx = int(sel[0])
        except Exception:
            messagebox.showwarning("Edit Note", "Could not determine selected note.")
            return
        
        note = self.sticky_notes[actual_idx]
        
        # Create professional edit dialog
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Note")
        edit_window.geometry("400x300")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Center the window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (300 // 2)
        edit_window.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(edit_window, corner_radius=8, border_width=1)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(frame, text="Edit Note", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 15))
        
        # Note text input
        ctk.CTkLabel(frame, text="Note Text:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(5, 2))
        note_text = ctk.CTkTextbox(frame, height=80, width=340)
        note_text.pack(padx=20, pady=(0, 10))
        note_text.insert("1.0", note.get("text", ""))
        
        # Button frame
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 10))
        
        def save_changes():
            new_text = note_text.get("1.0", "end-1c").strip()
            if new_text:
                # Update the note text and timestamp
                self.sticky_notes[actual_idx]["text"] = new_text
                self.sticky_notes[actual_idx]["time"] = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                self.save_data()
                self.update_notes_display()
                edit_window.destroy()
            else:
                messagebox.showwarning("Edit Note", "Note text cannot be empty.", parent=edit_window)
        
        def cancel():
            edit_window.destroy()
        
        # Save button
        save_btn = ctk.CTkButton(btn_frame, text="Save", command=save_changes, 
                                 fg_color="#4a90e2", text_color="white", width=120)
        save_btn.pack(side=ctk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=cancel, 
                                   fg_color="#666666", text_color="white", width=120)
        cancel_btn.pack(side=ctk.LEFT, padx=5)
        
        # Bind Enter key to save
        edit_window.bind('<Return>', lambda e: save_changes())
        edit_window.bind('<Escape>', lambda e: cancel())
        
        # Focus on text input
        note_text.focus_set()

    def  clear_all_notes(self):
        if not self.sticky_notes:
            messagebox.showinfo("Clear Notes", "No notes to clear.")
            return
        if messagebox.askyesno("Clear All Notes", "Are you sure you want to delete all notes?"):
            self.sticky_notes.clear()
            self.save_data()
            self.update_notes_display()




    def update_notes_display(self):
        # Repopulate the notes tree. Use the sticky_notes index as iid so selection maps to data.
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        for idx, n in enumerate(self.sticky_notes):
            ts = n.get('time', '')
            date_part = ''
            time_part = ''
            if ts:
                # Support both old 24-hour format ("YYYY-MM-DD HH:MM") and new
                # 12-hour format ("YYYY-MM-DD HH:MM AM/PM").
                parts = ts.split(' ')
                date_part = parts[0] if len(parts) > 0 else ''
                if len(parts) >= 3:
                    # e.g. ['2025-11-20', '09:15', 'AM'] -> join time and AM/PM
                    time_part = parts[1] + ' ' + parts[2]
                elif len(parts) == 2:
                    # e.g. ['2025-11-20', '09:15']
                    time_part = parts[1]
                else:
                    time_part = ''
            note_text = n.get('text', '')
            # Insert with iid == index so we can map selection back to sticky_notes
            try:
                self.notes_tree.insert('', tk.END, iid=str(idx), values=(date_part, time_part, note_text))
            except Exception:
                # Fallback without iid
                self.notes_tree.insert('', tk.END, values=(date_part, time_part, note_text))




    def manage_subjects(self):
        manage_window = ctk.CTkToplevel(self.root)
        manage_window.title("Manage Subjects")
        manage_window.geometry("300x300")

        frame = ctk.CTkFrame(manage_window, corner_radius=8, border_width=1)
        frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Subjects:").pack(pady=5)

        subjects_list = tk.Listbox(frame, height=10)
        subjects_list.pack(fill=ctk.BOTH, expand=True, pady=5)
        for subj in self.subjects:
            subjects_list.insert(tk.END, subj)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, pady=5)

        def add_subject():
            new = simpledialog.askstring("Add Subject", "Subject name:", parent=manage_window)
            if new and new not in self.subjects:
                self.subjects.append(new)
                subjects_list.insert(tk.END, new)
                self.subject_combo.configure(values=self.subjects)
                self.save_data()

        def delete_subject():
            sel = subjects_list.curselection()
            if sel:
                subj = subjects_list.get(sel)
                if messagebox.askyesno("Delete", f"Delete '{subj}'?", parent=manage_window):
                    self.subjects.remove(subj)
                    subjects_list.delete(sel)
                    self.subject_combo.configure(values=self.subjects)
                    self.save_data()

        # Style subject management buttons with theme accent and consistent padding
        accent = self.themes.get(self.current_theme, {}).get('accent', '#4a90e2')
        ctk.CTkButton(btn_frame, text="Add", command=add_subject, fg_color=accent, text_color="white").pack(side=ctk.LEFT, padx=6, pady=4)
        ctk.CTkButton(btn_frame, text="Delete", command=delete_subject, fg_color="#f44336", text_color="white").pack(side=ctk.RIGHT, padx=6, pady=4)




    def export_data(self):
        import csv
        try:
            with open("export.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "Title", "Date", "Subject", "Priority"])
                for t in self.tasks:
                    dt = t.get("datetime", "")
                    date_only = dt.split("T")[0] if "T" in dt else dt
                    writer.writerow([t.get("type", ""), t.get("title", ""), date_only, t.get("subject", ""), t.get("priority", "")])
            messagebox.showinfo("Export", "Data exported to export.csv")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export: {e}")




    def view_reminders(self):
        upcoming = []
        now = datetime.now()
        for t in self.tasks:
            try:
                dt = datetime.fromisoformat(t["datetime"])
                if dt >= now:
                    # Show reminders using 12-hour format with AM/PM for readability
                    upcoming.append(f"{dt.strftime('%Y-%m-%d %I:%M %p')} - {t['title']}")
            except Exception:
                continue
        msg = "\n".join(upcoming[:20]) if upcoming else "No upcoming reminders."
        messagebox.showinfo("Reminders", msg)




    def get_daily_quote(self, seed_date=None):
        """Return (quote, author). Deterministic by date so user sees a 'daily' quote."""
        if seed_date is None:
            seed_date = datetime.now().date()
        idx = seed_date.toordinal() % len(self.quotes)
        return self.quotes[idx]




    def update_daily_quote(self, force_new=False):
        """Set displayed quote. If force_new True, cycle to next quote."""
        today = datetime.now().date()
        if force_new:
            # cycle index or initialize
            if self.quote_index is None:
                self.quote_index = today.toordinal() % len(self.quotes)
            self.quote_index = (self.quote_index + 1) % len(self.quotes)
            q, a = self.quotes[self.quote_index]
        else:
            q, a = self.get_daily_quote(today)
            self.quote_index = today.toordinal() % len(self.quotes)
        # Fallback if quotes list is empty or contains empty values
        if not q:
            q = "No quote available."
        # Update author only if available
        if a:
            self.quote_author_var.set(f"— {a}")
        else:
            self.quote_author_var.set("")
        # Use standard double quotes for wide compatibility
        self.quote_text_var.set(f'"{q}"')




    def _cycle_quote(self):
        """Handler for 'Another Quote' button to show a different quote."""
        self.update_daily_quote(force_new=True)




    def check_reminders(self):
        now = datetime.now()
        for t in self.tasks:
            try:
                dt = datetime.fromisoformat(t["datetime"])
                if 0 <= (dt - now).total_seconds() <= 600:
                    messagebox.showinfo("Reminder", f"Upcoming: {t['title']} at {dt.strftime('%Y-%m-%d %I:%M %p')}")
            except Exception:
                continue
        self.root.after(60000, self.check_reminders)




    def change_theme(self, event_or_value=None):
        # Support both event callbacks (option menu passes string) and variable-driven calls
        if isinstance(event_or_value, str):
            chosen = event_or_value
        else:
            chosen = self.theme_var.get()
        if chosen in self.themes:
            self.current_theme = chosen
            self.apply_theme()
            self.save_data()




    def apply_theme(self):
        theme = self.themes[self.current_theme]
        bg = theme["bg"]
        accent = theme["accent"]
        text = theme["text"]

        # helper color functions
        def hex_to_rgb(h):
            h = h.lstrip('#')
            if len(h) == 3:
                h = ''.join(ch*2 for ch in h)
            try:
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            except Exception:
                return (240, 240, 240)

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % tuple(max(0, min(255, int(v))) for v in rgb)

        def adjust_brightness(hex_color, factor):
            r, g, b = hex_to_rgb(hex_color)
            return rgb_to_hex((r * factor, g * factor, b * factor))

        # Decide subtle contrasting button background vs window background.
        # If background is light we slightly darken it; if dark we lighten it.
        try:
            r, g, b = hex_to_rgb(bg)
            luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        except Exception:
            luminance = 0.6
        if luminance > 0.6:
            button_bg = adjust_brightness(bg, 0.92)  # slightly darker on light bg
            combo_bg = adjust_brightness(bg, 0.96)
            entry_bg = adjust_brightness(bg, 0.97)
        else:
            button_bg = adjust_brightness(bg, 1.12)  # slightly lighter on dark bg
            combo_bg = adjust_brightness(bg, 1.06)
            entry_bg = adjust_brightness(bg, 1.06)




        # Update root and all themed widgets
        try:
            self.root.configure(fg_color=bg)
        except:
            self.root.configure(bg=bg)




        # Create or update a ttk style for treeviews so colors are applied there too.
        try:
            style = ttk.Style()
            # Use a custom style name to avoid interfering with global styles
            style.configure("Custom.Treeview", background=bg, fieldbackground=bg, foreground=text)
            style.configure("Custom.Treeview.Heading", background=accent, foreground="white")
            style.map("Custom.Treeview", background=[('selected', accent)], foreground=[('selected', 'white')])
        except Exception:
            style = None

        for widget in self.themed_widgets:
            try:
                # Try CTk-specific configuration first
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(fg_color=bg)
                    if widget == self.title_label or widget == self.month_label:
                        widget.configure(text_color=accent)
                    else:
                        widget.configure(text_color=text)
                elif isinstance(widget, ctk.CTkButton):
                    # Give CTkButtons a visible background color (not identical to window bg)
                    widget.configure(fg_color=button_bg, text_color=text)
                    # Make important action buttons use the accent color so they're visible.
                    primaries = [getattr(self, "subjects_btn", None), getattr(self, "reminders_btn", None),
                                getattr(self, "add_btn", None), getattr(self, "prev_btn", None),
                                getattr(self, "next_btn", None), getattr(self, "add_note_btn", None),
                                getattr(self, "edit_note_btn", None), getattr(self, "delete_note_btn", None), 
                                getattr(self, "new_quote_btn", None), getattr(self, "export_btn", None)]
                    if widget in primaries:
                        widget.configure(fg_color=accent, text_color="white")
                    # Task-specific special buttons
                    if widget == getattr(self, 'delete_btn', None):
                        # task deletion is destructive -> red
                        widget.configure(fg_color="#f44336", text_color="white")
                    if widget == getattr(self, 'mark_done_btn', None):
                        # mark-as-done should look positive
                        widget.configure(fg_color="#4caf50", text_color="white")
                elif isinstance(widget, ctk.CTkFrame):
                    # If a CTkFrame is being used as a card (has border_width > 0), give it a subtle border color
                    try:
                        bw = widget.cget('border_width')
                    except Exception:
                        bw = 0
                    try:
                        if bw and int(bw) > 0:
                            # Card frames get a border color — use theme accent for stronger variant
                            if getattr(self, 'card_style', {}).get('use_accent_border'):
                                border_color = accent
                            else:
                                # Slightly darker than the background for a subtle outline
                                border_color = adjust_brightness(bg, 0.92)
                            widget.configure(fg_color=bg, border_color=border_color)
                        else:
                            widget.configure(fg_color=bg)
                    except Exception:
                        try:
                            widget.configure(fg_color=bg)
                        except Exception:
                            pass
                elif isinstance(widget, (ctk.CTkComboBox, getattr(ctk, 'CTkOptionMenu', object))):
                    # combobox/option menus use different option names for colors
                    try:
                        # set a slightly contrasted background for dropdowns and keep text readable
                        widget.configure(fg_color=combo_bg, text_color=text)
                        # some CTk implementations support button_color to style the glyph
                        try:
                            widget.configure(button_color=accent)
                        except Exception:
                            pass
                    except Exception:
                        try:
                            widget.configure(bg=bg, fg=text)
                        except Exception:
                            pass
                elif isinstance(widget, ctk.CTkEntry):
                    # CTkEntry uses fg_color for background and text_color for text
                    widget.configure(fg_color=entry_bg, text_color=text)
                else:
                    # Handle plain tkinter / ttk widgets
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=bg, fg=text)
                    elif isinstance(widget, tk.Listbox):
                        widget.configure(bg=bg, fg=text, selectbackground=accent, selectforeground="white")
                    elif isinstance(widget, tk.Scrollbar):
                        try:
                            widget.configure(bg=bg)
                        except Exception:
                            pass
                    elif isinstance(widget, ttk.Treeview):
                        try:
                            if style:
                                widget.configure(style="Custom.Treeview")
                            # Force update for tag-based colors
                            widget.tag_configure('done', foreground='gray')
                            widget.tag_configure('sep', foreground='gray35')
                        except Exception:
                            pass
                    else:
                        # Generic fallback: try to set basic background/foreground properties
                        try:
                            widget.configure(background=bg)
                        except Exception:
                            pass
            except Exception:
                # Ignore failing updates for unsupported widget types
                pass
        # Ensure the "Clear All" button uses a specific orange and remains visible.
        try:
            if hasattr(self, "clear_notes_btn") and self.clear_notes_btn:
                self.clear_notes_btn.configure(fg_color="#ff9800", text_color="white")
        except:
            pass




        # Update calendar to reflect theme
        self.update_calendar()




    def save_data(self):
        data = {
            "tasks": self.tasks,
            "subjects": self.subjects,
            "sticky_notes": self.sticky_notes,
            "theme": self.current_theme,
            "left_view": getattr(self, 'left_view', 'tasks')
        }
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print("Failed to save data:", e)




    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.subjects = data.get("subjects", self.subjects)
                    self.sticky_notes = data.get("sticky_notes", [])
                    self.current_theme = data.get("theme", self.current_theme)
                    # restore which left view was active (tasks or notes)
                    try:
                        self.left_view = data.get('left_view', self.left_view)
                    except Exception:
                        pass
            except Exception:
                pass




    def on_closing(self):
        self.save_data()
        self.root.destroy()
        if self.login_root:
            self.login_root.deiconify()




    def auto_save(self):
        self.save_data()
        self.root.after(300000, self.auto_save)




if __name__ == "__main__":
    # login = LoginWindow()
    # login.root.mainloop()

    root = ctk.CTk()
    app = StudyPlanner(root, username="Guest", login_root=None)
    root.mainloop()
