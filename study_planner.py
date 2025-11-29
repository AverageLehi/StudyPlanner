#StuddyPlanner Projectcode
import os
import json
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import webbrowser
from tkinter import messagebox, simpledialog
from tkinter import filedialog
from datetime import datetime, timedelta
import calendar

class LoginWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Study Planner Login")
        self.root.geometry("500x280")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.users_file = "users.json"

        self.users = self.load_users()
        self.create_login_widgets()
        
        # Set focus after all widgets are created and window is ready
        self.root.after(100, lambda: self.username.focus_force())

    def create_login_widgets(self):
        # Outer card/container for a professional look
        container = ctk.CTkFrame(self.root, corner_radius=10, border_width=2)
        container.pack(expand=True, fill=ctk.BOTH, padx=16, pady=16)

        title = ctk.CTkLabel(container, text="Welcome to Study Planner", font=("Arial", 16, "bold"))
        title.pack(pady=(12, 4))
        subtitle = ctk.CTkLabel(container, text="Plan. Focus. Achieve.", font=("Arial", 12, "italic"))
        subtitle.pack(pady=(0, 12))

        form = ctk.CTkFrame(container, fg_color="transparent")
        form.pack(fill=ctk.X, padx=16, pady=(0, 10))

        # Username
        user_row = ctk.CTkFrame(form, fg_color="transparent")
        user_row.pack(fill=ctk.X, pady=(4, 6))
        ctk.CTkLabel(user_row, text="Username", width=120).pack(side=ctk.LEFT)
        self.username = ctk.CTkEntry(user_row, width=220, border_color="#4a90e2")
        self.username.pack(side=ctk.LEFT, fill=ctk.X, expand=True)

        # Password with show/hide toggle
        pass_row = ctk.CTkFrame(form, fg_color="transparent")
        pass_row.pack(fill=ctk.X, pady=(4, 6))
        ctk.CTkLabel(pass_row, text="Password", width=120).pack(side=ctk.LEFT)
        self.password = ctk.CTkEntry(pass_row, show="*", width=220, border_color="#4a90e2")
        self.password.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        show_var = tk.BooleanVar(value=False)
        def _toggle_login_password():
            try:
                self.password.configure(show="" if show_var.get() else "*")
            except Exception:
                pass
        show_btn = ctk.CTkCheckBox(pass_row, text="Show", variable=show_var, command=_toggle_login_password,
                                  border_width=1, corner_radius=4, checkbox_height=18)
        show_btn.pack(side=ctk.LEFT, padx=8)

        # Action buttons
        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(fill=ctk.X, padx=16, pady=(6, 6))
        login_btn = ctk.CTkButton(actions, text="Login", command=self.login, width=120)
        register_btn = ctk.CTkButton(actions, text="Register", command=self.show_register, width=120)
        login_btn.pack(side=ctk.LEFT)
        register_btn.pack(side=ctk.LEFT, padx=8)

        # Secondary actions
        secondary = ctk.CTkFrame(container, fg_color="transparent")
        secondary.pack(fill=ctk.X, padx=16, pady=(0, 8))
        phinmaed_btn = ctk.CTkButton(secondary, text="Login with PHINMAED",
                                     command=self.login_with_phinmaed, width=160)
        phinmaed_btn.pack(side=ctk.LEFT)
        
        # Admin quick login button (right side)
        admin_btn = ctk.CTkButton(secondary, text="🔑 Admin", command=self.admin_login, 
                                 width=80, fg_color="#9c27b0", hover_color="#7b1fa2")
        admin_btn.pack(side=ctk.RIGHT)

        # Theming tweak: set border color aligned with text color
        try:
            # Use same theme logic as app default
            theme = {"bg": "#ffffff", "text": "#333333"}
            container.configure(border_color=theme["text"])
        except Exception:
            pass

        # Keyboard shortcut
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

    def admin_login(self):
        """Quick admin login with master password - CustomTkinter window."""
        admin_window = ctk.CTkToplevel(self.root)
        admin_window.title("Admin Access")
        admin_window.geometry("440x220")
        admin_window.transient(self.root)
        admin_window.grab_set()
        admin_window.resizable(False, False)
        
        # Center window
        admin_window.update_idletasks()
        x = (admin_window.winfo_screenwidth() // 2) - (440 // 2)
        y = (admin_window.winfo_screenheight() // 2) - (220 // 2)
        admin_window.geometry(f"440x220+{x}+{y}")
        
        # Container
        container = ctk.CTkFrame(admin_window, corner_radius=10, border_width=1)
        container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with key emoji
        title = ctk.CTkLabel(container, text="🔑 Admin Access", 
                            font=("Arial", 18, "bold"))
        title.pack(pady=(15, 5))
        
        subtitle = ctk.CTkLabel(container, text="Enter master password", 
                               font=("Arial", 11))
        subtitle.pack(pady=(0, 15))
        
        # Password entry with show toggle
        pass_frame = ctk.CTkFrame(container, fg_color="transparent")
        pass_frame.pack(fill=ctk.X, padx=20, pady=(0, 10))
        
        admin_pw_var = tk.StringVar()
        pw_entry = ctk.CTkEntry(pass_frame, textvariable=admin_pw_var, 
                                show="*", width=220, height=35,
                                placeholder_text="Admin password", border_color="#9c27b0")
        pw_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        pw_entry.focus_set()
        # Reassert focus shortly after to handle OS focus quirks
        try:
            admin_window.after(120, lambda: pw_entry.focus_force())
        except Exception:
            pass
        
        # Show password toggle
        show_var = tk.BooleanVar(value=False)
        def toggle_show():
            pw_entry.configure(show="" if show_var.get() else "*")
        
        show_check = ctk.CTkCheckBox(pass_frame, text="Show", variable=show_var, 
                                     command=toggle_show, width=60,
                                     border_width=1, corner_radius=4, checkbox_height=18)
        show_check.pack(side=ctk.LEFT, padx=(8, 0))
        
        # Login function
        def attempt_login():
            admin_pw = admin_pw_var.get()
            if admin_pw == "admin123":
                admin_window.destroy()
                messagebox.showinfo("Admin Access", "Welcome, Admin! Logged in as Guest.")
                self.root.withdraw()
                app_root = tk.Toplevel(self.root)
                StudyPlanner(app_root, "Guest", self.root)
            elif admin_pw:
                messagebox.showerror("Admin Login", "Invalid admin password.")
                pw_entry.delete(0, tk.END)
                pw_entry.focus_set()
            else:
                messagebox.showwarning("Admin Login", "Please enter a password.")
        
        # Buttons
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, padx=20, pady=(5, 10))
        
        login_btn = ctk.CTkButton(btn_frame, text="Login", command=attempt_login,
                                  fg_color="#9c27b0", hover_color="#7b1fa2",
                                  height=35, width=140)
        login_btn.pack(side=ctk.LEFT, padx=(0, 8))
        
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", 
                                   command=admin_window.destroy,
                                   fg_color="gray50", hover_color="gray40",
                                   height=35, width=140)
        cancel_btn.pack(side=ctk.LEFT)
        
        # Keyboard shortcuts
        admin_window.bind('<Return>', lambda e: attempt_login())
        admin_window.bind('<Escape>', lambda e: admin_window.destroy())

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
        register_window.title("Register an Account")
        register_window.geometry("480x260")
        # Keep register window above login and modal-like
        try:
            register_window.transient(self.root)
            register_window.grab_set()
            register_window.lift()
            register_window.focus_force()
        except Exception:
            pass

        card = ctk.CTkFrame(register_window, corner_radius=10, border_width=1)
        card.pack(expand=True, fill=ctk.BOTH, padx=16, pady=16)
        ctk.CTkLabel(card, text="Create Account", font=("Arial", 15, "bold")).pack(pady=(12,6))

        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill=ctk.X, padx=16, pady=(0,10))

        # Username
        urow = ctk.CTkFrame(form, fg_color="transparent")
        urow.pack(fill=ctk.X, pady=(4,6))
        ctk.CTkLabel(urow, text="Username", width=120).pack(side=ctk.LEFT)
        new_username = ctk.CTkEntry(urow, width=220, border_color="#4a90e2")
        new_username.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        new_username.focus_set()
        # Reassert focus shortly after to handle OS focus quirks
        try:
            register_window.after(120, lambda: new_username.focus_force())
        except Exception:
            pass

        # Password with show toggle
        prow = ctk.CTkFrame(form, fg_color="transparent")
        prow.pack(fill=ctk.X, pady=(4,6))
        ctk.CTkLabel(prow, text="Password", width=120).pack(side=ctk.LEFT)
        new_password = ctk.CTkEntry(prow, show="*", width=220, border_color="#4a90e2")
        new_password.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        reg_show_var = tk.BooleanVar(value=False)
        def _toggle_reg_password():
            try:
                new_password.configure(show="" if reg_show_var.get() else "*")
            except Exception:
                pass
        ctk.CTkCheckBox(prow, text="Show", variable=reg_show_var, command=_toggle_reg_password,
                       border_width=1, corner_radius=4, checkbox_height=18).pack(side=ctk.LEFT, padx=8)

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

        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill=ctk.X, padx=16)
        register_btn = ctk.CTkButton(actions, text="Register", command=register, width=120)
        register_btn.pack(side=ctk.LEFT)
        phinmaed_reg_btn = ctk.CTkButton(actions, text="Register with PHINMAED",
            command=self.login_with_phinmaed, width=180)
        phinmaed_reg_btn.pack(side=ctk.LEFT, padx=8)
        register_window.bind('<Return>', lambda e: register())

class StudyPlanner:
    def __init__(self, root, username, login_root):
        self.root = root
        self.username = username
        self.login_root = login_root
        self.root.title(f"Study Planner - {self.username}")
        self.root.geometry("1600x800")
        self.root.minsize(1600, 800)
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
            "Default": {
                "bg": "#ffffff", 
                "accent": "#4a90e2", 
                "text": "#333333"},

            "Red": {
                "bg": "#ffe5e5", 
                "accent": "#c73939", 
                "text": "#8b1a1a"},

            "Green": {
                "bg": "#e8f5e8", 
                "accent": "#4caf50", 
                "text": "#2e7d32"},

            "Yellow": {
                "bg": "#faf2d0", 
                "accent": "#d4a50a", 
                "text": "#6b5d03"},

            "Blue": {
                "bg": "#cedfff", 
                "accent": "#2ba2e7", 
                "text": "#1361a1"},

            "Purple": {
                "bg": "#f3e5f5", 
                "accent": "#9c27b0", 
                "text": "#4a148c"},

            "Pink": {
                "bg": "#ffc4f0", 
                "accent": "#ff75c3", 
                "text": "#8c146c"},

        }
        self.current_theme = "Default"
        # Card design settings: rounded corners and borders
        self.card_style = {
            'corner_radius': 8,
            'border_width': 2,
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
            ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
            ("Education is the most powerful weapon which you can use to change the world.", "Nelson Mandela"),
            ("The expert in anything was once a beginner.", "Helen Hayes"),
            ("Study while others are sleeping; work while others are loafing; prepare while others are playing.", "William Arthur Ward"),
            ("The only way to learn mathematics is to do mathematics.", "Paul Halmos"),
            ("Don't let what you cannot do interfere with what you can do.", "John Wooden"),
            ("Success doesn't come from what you do occasionally, it comes from what you do consistently.", "Unknown"),
            ("Your attitude, not your aptitude, will determine your altitude.", "Zig Ziglar"),
            ("The difference between ordinary and extraordinary is that little extra.", "Jimmy Johnson"),
            ("Learning is not attained by chance, it must be sought for with ardor and attended to with diligence.", "Abigail Adams"),
            ("I never dreamed about success, I worked for it.", "Estée Lauder"),
            ("Strive for progress, not perfection.", "Unknown"),
            ("The more that you read, the more things you will know. The more that you learn, the more places you'll go.", "Dr. Seuss"),
            ("Push yourself, because no one else is going to do it for you.", "Unknown"),
            ("Great things never come from comfort zones.", "Unknown"),
            ("Dream big, work hard, stay focused, and surround yourself with good people.", "Unknown")
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





        # Header title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Study Planner", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(0, 2))
        self.themed_widgets.append(self.title_label)

        # Slogan/subtitle
        self.slogan_label = ctk.CTkLabel(self.main_frame, text="Plan. Focus. Achieve.", font=("Arial", 14, "italic"))
        self.slogan_label.pack(pady=(0, 18))
        self.themed_widgets.append(self.slogan_label)

        # Username label (top-right)
        self.username_label = ctk.CTkLabel(self.main_frame, text=f"Logged in as: {self.username}", font=("Arial", 11))
        self.username_label.place(relx=1.0, y=8, anchor="ne")
        self.themed_widgets.append(self.username_label)




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

        # Account Settings (align to the right side)
        self.account_settings_btn = ctk.CTkButton(top_frame, text="Account Settings", command=self.open_account_settings)
        self.account_settings_btn.pack(side=ctk.RIGHT, padx=6, pady=4)
        self.themed_widgets.append(self.account_settings_btn)


        # Notes export lives in the Quick Notes panel as CSV/TXT buttons

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

        # Task Management title
        task_title = ctk.CTkLabel(self.task_frame, text="Task Management", font=("Arial", 16, "bold"))
        task_title.pack(pady=(12, 8))
        self.themed_widgets.append(task_title)

        # Bordered container for inputs and Add button
        input_container = ctk.CTkFrame(self.task_frame, corner_radius=8, border_width=2)
        input_container.pack(fill=ctk.X, padx=10, pady=(0, 10))
        self.themed_widgets.append(input_container)

        form_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        form_frame.pack(fill=ctk.X, padx=10, pady=10)
        self.themed_widgets.append(form_frame)

        # Configure grid layout: compact design
        # Row 0: Title (full width)
        # Row 1: Type | Subject | Priority | Date | Time
        
        self.form_labels = []
        
        # Title - full width
        self.title_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter task title")
        self.title_entry.grid(row=0, column=0, columnspan=5, pady=4, sticky="ew")
        self.themed_widgets.append(self.title_entry)
        
        # Row 1: All fields on same row
        # Type
        self.task_type_var = tk.StringVar(value="Type:")
        task_type_combo = ctk.CTkComboBox(form_frame, values=["Assignment", "Exam", "Class", "Study Session"], 
                          variable=self.task_type_var, width=140, state="readonly")
        task_type_combo.grid(row=1, column=0, pady=4, padx=(0, 6), sticky="ew")
        task_type_combo.set("Type:")
        self.themed_widgets.append(task_type_combo)
        
        # Subject
        self.subject_var = tk.StringVar(value="Subject:")
        self.subject_combo = ctk.CTkComboBox(form_frame, values=self.subjects, variable=self.subject_var, 
                             width=140, state="readonly")
        self.subject_combo.grid(row=1, column=1, pady=4, padx=(0, 6), sticky="ew")
        self.subject_combo.set("Subject:")
        self.themed_widgets.append(self.subject_combo)
        
        # Priority
        self.priority_var = tk.StringVar(value="Priority:")
        priority_combo = ctk.CTkComboBox(form_frame, values=["Low", "Medium", "High"], 
                         variable=self.priority_var, width=120, state="readonly")
        priority_combo.grid(row=1, column=2, pady=4, padx=(0, 6), sticky="ew")
        priority_combo.set("Priority:")
        self.themed_widgets.append(priority_combo)
        
        # Date
        self.selected_date = datetime.now()
        self.date_btn = ctk.CTkButton(form_frame, text="Date: " + self.selected_date.strftime("%b %d, %Y"), 
                                       command=self.open_date_picker, width=140, anchor="w")
        self.date_btn.grid(row=1, column=3, pady=4, padx=(0, 6), sticky="ew")
        self.themed_widgets.append(self.date_btn)
        
        # Time container with entry and AM/PM buttons
        time_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        time_container.grid(row=1, column=4, pady=4, sticky="ew")
        
        self.time_entry = ctk.CTkEntry(time_container, width=60, placeholder_text="Time:")
        self.time_entry.pack(side=ctk.LEFT, padx=(0, 4))
        self.themed_widgets.append(self.time_entry)
        
        # AM/PM toggle buttons with white text
        self.am_pm_var = tk.StringVar(value="AM")
        self.am_btn = ctk.CTkButton(time_container, text="AM", width=35, height=28,
                                    command=lambda: self.toggle_am_pm("AM"), text_color="white")
        self.am_btn.pack(side=ctk.LEFT, padx=1)
        self.themed_widgets.append(self.am_btn)
        
        self.pm_btn = ctk.CTkButton(time_container, text="PM", width=35, height=28,
                                    command=lambda: self.toggle_am_pm("PM"), text_color="white")
        self.pm_btn.pack(side=ctk.LEFT, padx=1)
        self.themed_widgets.append(self.pm_btn)
        
        # Set initial button states
        self.update_am_pm_buttons()
        
        # Configure column weights for responsive layout
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=1)
        form_frame.columnconfigure(3, weight=1)
        form_frame.columnconfigure(4, weight=1)

        # Add Task button inside the bordered input container
        add_btn_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        add_btn_frame.pack(fill=ctk.X, padx=10, pady=(0, 10))
        self.themed_widgets.append(add_btn_frame)

        self.add_btn = ctk.CTkButton(add_btn_frame, text="Add Task", command=self.add_task, width=120)
        self.add_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.add_btn)




        btn_frame = ctk.CTkFrame(self.task_frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, padx=10, pady=5)
        self.themed_widgets.append(btn_frame)




        self.edit_btn = ctk.CTkButton(btn_frame, text="Edit Selected", command=self.edit_task, width=90)
        self.edit_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.edit_btn)




        self.delete_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_task, width=90)
        self.delete_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.delete_btn)

        self.mark_done_btn = ctk.CTkButton(btn_frame, text="Mark Done", command=self.mark_task_done, width=90)
        self.mark_done_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.mark_done_btn)

        # Export buttons for tasks (CSV and TXT)
        self.export_tasks_csv_btn = ctk.CTkButton(btn_frame, text="Export CSV", command=self.export_tasks_csv, width=90)
        self.export_tasks_csv_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.export_tasks_csv_btn)
        self.export_tasks_txt_btn = ctk.CTkButton(btn_frame, text="Export TXT", command=self.export_tasks_txt, width=90)
        self.export_tasks_txt_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.export_tasks_txt_btn)

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


        self.priority_btn = ctk.CTkButton(btn_frame, text=f"Priority: {self.priority_levels[self.priority_index]}",
            command=_toggle_priority_sort, width=110)
        # make sure priority button is styled by apply_theme
        self.themed_widgets.append(self.priority_btn)
        # pack the priority button so it's visible in the controls row
        try:
            self.priority_btn.pack(side=ctk.RIGHT, padx=6, pady=4)
        except Exception:
            pass
        
        # Live filter entry for tasks
        self.search_entry = ctk.CTkEntry(btn_frame, placeholder_text="🔍 Filter tasks", width=160)
        self.search_entry.pack(side=ctk.RIGHT, padx=6, pady=4)
        self.search_entry.bind('<KeyRelease>', lambda e: self.update_task_list())
        self.themed_widgets.append(self.search_entry)
        # keep a helper to update the label when toggled
        def _update_priority_button_text():
            cur = self.priority_levels[self.priority_index]
            self.priority_btn.configure(text=f"Priority: {cur}")

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
                self.task_tree = ttk.Treeview(list_frame, columns=("Priority", "Date", "Time", "Type", "Subject", "Title"), show="headings", style="Custom.Treeview")
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
                                    font=("Arial", 16, "bold"))
        notes_title.pack(pady=(10, 5), padx=10)
        self.themed_widgets.append(notes_title)

        # Input row for new note
        self.note_input_frame = ctk.CTkFrame(self.notes_frame, fg_color="transparent")
        self.note_input_frame.pack(fill=ctk.X, padx=10, pady=(8, 6))
        self.themed_widgets.append(self.note_input_frame)

        self.note_entry = ctk.CTkEntry(self.note_input_frame, placeholder_text="Enter note description")
        self.note_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        self.note_entry.bind('<Return>', lambda e: self.add_note())
        self.themed_widgets.append(self.note_entry)

        # Add button only in input row
        self.add_note_btn = ctk.CTkButton(self.note_input_frame, text="Add", command=self.add_note, width=60)
        self.add_note_btn.pack(side=ctk.RIGHT, padx=6, pady=4)
        self.themed_widgets.append(self.add_note_btn)

        # Buttons row (edit / delete / clear / export)
        note_btn_frame = ctk.CTkFrame(self.notes_frame, fg_color="transparent")
        note_btn_frame.pack(fill=ctk.X, padx=10, pady=(0, 6))
        self.themed_widgets.append(note_btn_frame)

        self.edit_note_btn = ctk.CTkButton(note_btn_frame, text="Edit Selected", command=self.edit_note, width=90)
        self.edit_note_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.edit_note_btn)

        self.delete_note_btn = ctk.CTkButton(note_btn_frame, text="Delete Selected", command=self.delete_note, width=90)
        self.delete_note_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.delete_note_btn)

        self.clear_notes_btn = ctk.CTkButton(note_btn_frame, text="Clear All", command=self.clear_all_notes, width=90)
        self.clear_notes_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.clear_notes_btn)

        # Export buttons placed after action buttons
        self.export_notes_csv_btn = ctk.CTkButton(note_btn_frame, text="Export CSV",
                              command=self.export_notes_csv, width=80)
        self.export_notes_csv_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.export_notes_csv_btn)
        self.export_notes_txt_btn = ctk.CTkButton(note_btn_frame, text="Export TXT",
                              command=self.export_notes_txt, width=80)
        self.export_notes_txt_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.export_notes_txt_btn)

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
        
        # Calendar View title
        cal_title = ctk.CTkLabel(self.cal_frame, text="Calendar View", font=("Arial", 16, "bold"))
        cal_title.pack(pady=(12, 2))
        self.themed_widgets.append(cal_title)
        
        # Calendar subtitle
        cal_subtitle = ctk.CTkLabel(self.cal_frame, text="Click highlighted ." \
        "dates to view scheduled tasks", 
                                     font=("Arial", 10, "italic"))
        cal_subtitle.pack(pady=(0, 8))
        self.themed_widgets.append(cal_subtitle)
        
        nav_frame = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav_frame.pack(fill=ctk.X, padx=10, pady=5)
        self.themed_widgets.append(nav_frame)
        self.current_date = datetime.now()

        # Smaller prev/next buttons for a compact calendar control
        self.prev_btn = ctk.CTkButton(nav_frame, text="<<", command=self.prev_month, width=32, height=28)
        self.prev_btn.pack(side=ctk.LEFT, padx=6, pady=4)
        self.themed_widgets.append(self.prev_btn)

        self.month_label = ctk.CTkLabel(nav_frame, text="", font=("Arial", 12, "bold"))
        self.month_label.pack(side=ctk.LEFT, expand=True)
        self.themed_widgets.append(self.month_label)

        self.next_btn = ctk.CTkButton(nav_frame, text=">>", command=self.next_month, width=32, height=28)
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
                                    font=("Arial", 16, "bold"))
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

                    # Determine colors: today gets primary accent, dates with tasks get lighter accent
                    if is_today:
                        bg_color = theme["accent"]
                        fg_color = "white"
                    elif has_task:
                        # Lighter accent for dates with tasks
                        bg_color = theme["accent"]
                        fg_color = "white"
                    else:
                        bg_color = theme["bg"]
                        fg_color = theme["text"]

                    font_weight = "bold" if (is_today or has_task) else "normal"

                    lbl = ctk.CTkLabel(self.calendar_frame, text=str(day), font=("Arial", 9, font_weight),
                                      fg_color=bg_color, text_color=fg_color, corner_radius=4)
                    lbl.bind("<Button-1>", lambda e, d=day: self.show_tasks_for_date(d))

                lbl.grid(row=row_num, column=col_num, padx=1, pady=1, sticky="nsew")
            # ensure the row expands so cells align evenly when the frame is stretched
            try:
                self.calendar_frame.grid_rowconfigure(row_num, weight=1)
            except Exception:
                pass

    def toggle_am_pm(self, period):
        """Toggle between AM and PM"""
        self.am_pm_var.set(period)
        self.update_am_pm_buttons()
    
    def update_am_pm_buttons(self):
        """Update AM/PM button appearances based on selection"""
        current = self.am_pm_var.get()
        # Get the theme colors
        theme = self.themes.get(self.current_theme, self.themes["Default"])
        accent = theme["accent"]
        text_col = theme["text"]
        
        # Use white text for all themes except Default
        button_text_color = text_col if self.current_theme == "Default" else "white"
        
        if current == "AM":
            self.am_btn.configure(fg_color=accent, hover_color=accent, text_color=button_text_color)
            self.pm_btn.configure(fg_color="gray40", hover_color="gray30", text_color=button_text_color)
        else:
            self.am_btn.configure(fg_color="gray40", hover_color="gray30", text_color=button_text_color)
            self.pm_btn.configure(fg_color=accent, hover_color=accent, text_color=button_text_color)
    
    def open_date_picker(self):
        """Open a custom date picker dialog"""
        picker = ctk.CTkToplevel(self.root)
        picker.title("Select Date")
        picker.geometry("380x450")
        picker.transient(self.root)
        picker.grab_set()
        picker.resizable(False, False)  # Fixed size
        
        # Get current theme colors
        theme = self.themes.get(self.current_theme, self.themes["Default"])
        accent = theme["accent"]
        
        # Center the window
        picker.update_idletasks()
        x = (picker.winfo_screenwidth() // 2) - (380 // 2)
        y = (picker.winfo_screenheight() // 2) - (450 // 2)
        picker.geometry(f"380x450+{x}+{y}")
        
        # Current date for navigation
        current_date = [self.selected_date.year, self.selected_date.month]
        
        # Month/Year navigation
        nav_frame = ctk.CTkFrame(picker)
        nav_frame.pack(pady=15, padx=15, fill="x")
        
        month_year_label = ctk.CTkLabel(nav_frame, text="", font=("Arial", 16, "bold"))
        month_year_label.pack()
        
        btn_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        btn_frame.pack(pady=8)
        
        def update_calendar():
            month_name = calendar.month_name[current_date[1]]
            month_year_label.configure(text=f"{month_name} {current_date[0]}")
            
            # Clear existing day buttons
            for widget in days_frame.winfo_children():
                widget.destroy()
            
            # Configure grid for centered layout
            for i in range(7):
                days_frame.grid_columnconfigure(i, weight=1, uniform="day")
            
            # Day headers with theme-aware colors
            for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
                lbl = ctk.CTkLabel(days_frame, text=day, font=("Arial", 11, "bold"), width=45)
                lbl.grid(row=0, column=i, padx=3, pady=(5, 8), sticky="ew")
            
            # Get calendar for current month
            cal = calendar.monthcalendar(current_date[0], current_date[1])
            
            # Create day buttons with theme colors
            today_date = datetime.now().date()
            for week_num, week in enumerate(cal, start=1):
                for day_num, day in enumerate(week):
                    if day == 0:
                        # Empty cell for days outside current month
                        continue
                    
                    day_date = datetime(current_date[0], current_date[1], day)
                    is_selected = (day_date.date() == self.selected_date.date())
                    is_past = day_date.date() < today_date
                    
                    # Disable past dates: gray and non-clickable
                    if is_past:
                        btn = ctk.CTkButton(
                            days_frame, 
                            text=str(day), 
                            width=45, 
                            height=40,
                            fg_color="gray20",
                            hover_color="gray20",
                            text_color="gray50",
                            font=("Arial", 12),
                            state="disabled"
                        )
                    else:
                        # Use theme accent color for selected date
                        btn = ctk.CTkButton(
                            days_frame, 
                            text=str(day), 
                            width=45, 
                            height=40,
                            fg_color=accent if is_selected else "gray30",
                            hover_color=accent if is_selected else "gray40",
                            font=("Arial", 12),
                            command=lambda d=day: select_date(d)
                        )
                    btn.grid(row=week_num, column=day_num, padx=3, pady=3, sticky="nsew")
            
            # Configure row weights for even spacing
            for i in range(len(cal) + 1):
                days_frame.grid_rowconfigure(i, weight=1)
        
        def prev_month():
            current_date[1] -= 1
            if current_date[1] < 1:
                current_date[1] = 12
                current_date[0] -= 1
            update_calendar()
        
        def next_month():
            current_date[1] += 1
            if current_date[1] > 12:
                current_date[1] = 1
                current_date[0] += 1
            update_calendar()
        
        def select_date(day):
            selected = datetime(current_date[0], current_date[1], day)
            # Prevent selecting past dates
            if selected.date() < datetime.now().date():
                messagebox.showwarning("Invalid Date", "Cannot select a date in the past.", parent=picker)
                return
            self.selected_date = selected
            self.date_btn.configure(text=self.selected_date.strftime("%B %d, %Y"))
            picker.destroy()
        
        # Navigation buttons with theme colors
        ctk.CTkButton(btn_frame, text="◀", width=50, command=prev_month, 
                     fg_color=accent).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Today", width=80, command=lambda: [
            current_date.__setitem__(0, datetime.now().year),
            current_date.__setitem__(1, datetime.now().month),
            update_calendar()
        ], fg_color=accent).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="▶", width=50, command=next_month,
                     fg_color=accent).pack(side=ctk.LEFT, padx=5)
        
        # Days grid - centered container
        days_frame = ctk.CTkFrame(picker, width=350, height=280)
        days_frame.pack(pady=10, padx=15)
        days_frame.pack_propagate(False)  # Maintain fixed size
        
        update_calendar()
        
        # Close button
        ctk.CTkButton(picker, text="Cancel", width=100, command=picker.destroy,
                     fg_color="gray50").pack(pady=15)

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Add Task", "Please enter a title.")
            return
        try:
            date_text = self.selected_date.strftime("%Y-%m-%d")
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
        
        # Title - first field
        ctk.CTkLabel(form_frame, text="Title:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        title_entry = ctk.CTkEntry(form_frame, width=250)
        title_entry.insert(0, task.get("title", ""))
        title_entry.grid(row=0, column=1, pady=8, sticky="ew")
        
        # Task Type
        ctk.CTkLabel(form_frame, text="Type:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
        type_var = tk.StringVar(value=task.get("type", "Assignment"))
        type_combo = ctk.CTkComboBox(form_frame, values=["Assignment", "Exam", "Class", "Study Session"], 
                                     variable=type_var, width=250, state="readonly")
        type_combo.grid(row=1, column=1, pady=8, sticky="ew")
        type_combo.set(task.get("type", "Assignment"))
        
        # Subject
        ctk.CTkLabel(form_frame, text="Subject:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
        subject_var = tk.StringVar(value=task.get("subject", ""))
        subject_combo = ctk.CTkComboBox(form_frame, values=self.subjects, variable=subject_var, 
                                        width=250, state="readonly")
        subject_combo.grid(row=2, column=1, pady=8, sticky="ew")
        subject_combo.set(task.get("subject", ""))
        
        # Date - with picker button
        ctk.CTkLabel(form_frame, text="Date:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=8, padx=(0, 10))
        
        try:
            edit_selected_date = datetime.fromisoformat(task.get("datetime", ""))
        except:
            edit_selected_date = datetime.now()
        
        date_btn_var = tk.StringVar(value=edit_selected_date.strftime("%B %d, %Y"))
        
        def open_edit_date_picker():
            picker = ctk.CTkToplevel(edit_window)
            picker.title("Select Date")
            picker.geometry("380x450")
            picker.transient(edit_window)
            picker.grab_set()
            picker.resizable(False, False)  # Fixed size
            
            # Get current theme colors
            theme = self.themes.get(self.current_theme, self.themes["Default"])
            accent = theme["accent"]
            
            # Center the picker
            picker.update_idletasks()
            px = (picker.winfo_screenwidth() // 2) - (380 // 2)
            py = (picker.winfo_screenheight() // 2) - (450 // 2)
            picker.geometry(f"380x450+{px}+{py}")
            
            current_date = [edit_selected_date.year, edit_selected_date.month]
            
            nav_frame = ctk.CTkFrame(picker)
            nav_frame.pack(pady=15, padx=15, fill="x")
            
            month_year_label = ctk.CTkLabel(nav_frame, text="", font=("Arial", 16, "bold"))
            month_year_label.pack()
            
            btn_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
            btn_frame.pack(pady=8)
            
            def update_calendar():
                month_name = calendar.month_name[current_date[1]]
                month_year_label.configure(text=f"{month_name} {current_date[0]}")
                
                for widget in days_frame.winfo_children():
                    widget.destroy()
                
                # Configure grid for centered layout
                for i in range(7):
                    days_frame.grid_columnconfigure(i, weight=1, uniform="day")
                
                # Day headers with theme-aware colors
                for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
                    lbl = ctk.CTkLabel(days_frame, text=day, font=("Arial", 11, "bold"), width=45)
                    lbl.grid(row=0, column=i, padx=3, pady=(5, 8), sticky="ew")
                
                cal = calendar.monthcalendar(current_date[0], current_date[1])
                
                # Create day buttons with theme colors
                today_date = datetime.now().date()
                for week_num, week in enumerate(cal, start=1):
                    for day_num, day in enumerate(week):
                        if day == 0:
                            continue
                        
                        day_date = datetime(current_date[0], current_date[1], day)
                        is_selected = (day_date.date() == edit_selected_date.date())
                        is_past = day_date.date() < today_date
                        
                        # Disable past dates: gray and non-clickable
                        if is_past:
                            btn = ctk.CTkButton(
                                days_frame, 
                                text=str(day), 
                                width=45, 
                                height=40,
                                fg_color="gray20",
                                hover_color="gray20",
                                text_color="gray50",
                                font=("Arial", 12),
                                state="disabled"
                            )
                        else:
                            # Use theme accent color for selected date
                            btn = ctk.CTkButton(
                                days_frame, 
                                text=str(day), 
                                width=45, 
                                height=40,
                                fg_color=accent if is_selected else "gray30",
                                hover_color=accent if is_selected else "gray40",
                                font=("Arial", 12),
                                command=lambda d=day: select_date(d)
                            )
                        btn.grid(row=week_num, column=day_num, padx=3, pady=3, sticky="nsew")
                
                # Configure row weights for even spacing
                for i in range(len(cal) + 1):
                    days_frame.grid_rowconfigure(i, weight=1)
            
            def prev_month():
                current_date[1] -= 1
                if current_date[1] < 1:
                    current_date[1] = 12
                    current_date[0] -= 1
                update_calendar()
            
            def next_month():
                current_date[1] += 1
                if current_date[1] > 12:
                    current_date[1] = 1
                    current_date[0] += 1
                update_calendar()
            
            def select_date(day):
                nonlocal edit_selected_date
                selected = datetime(current_date[0], current_date[1], day)
                # Prevent selecting past dates
                if selected.date() < datetime.now().date():
                    messagebox.showwarning("Invalid Date", "Cannot select a date in the past.", parent=picker)
                    return
                edit_selected_date = selected
                date_btn_var.set(edit_selected_date.strftime("%B %d, %Y"))
                edit_date_btn.configure(text=edit_selected_date.strftime("%B %d, %Y"))
                picker.destroy()
            
            # Navigation buttons with theme colors
            ctk.CTkButton(btn_frame, text="◀", width=50, command=prev_month,
                         fg_color=accent).pack(side=ctk.LEFT, padx=5)
            ctk.CTkButton(btn_frame, text="Today", width=80, command=lambda: [
                current_date.__setitem__(0, datetime.now().year),
                current_date.__setitem__(1, datetime.now().month),
                update_calendar()
            ], fg_color=accent).pack(side=ctk.LEFT, padx=5)
            ctk.CTkButton(btn_frame, text="▶", width=50, command=next_month,
                         fg_color=accent).pack(side=ctk.LEFT, padx=5)
            
            # Days grid - centered container
            days_frame = ctk.CTkFrame(picker, width=350, height=280)
            days_frame.pack(pady=10, padx=15)
            days_frame.pack_propagate(False)  # Maintain fixed size
            
            update_calendar()
            
            ctk.CTkButton(picker, text="Cancel", width=100, command=picker.destroy,
                         fg_color="gray50").pack(pady=15)
        
        edit_date_btn = ctk.CTkButton(form_frame, text=edit_selected_date.strftime("%B %d, %Y"), 
                                      command=open_edit_date_picker, width=250, anchor="w")
        edit_date_btn.grid(row=3, column=1, pady=8, sticky="ew")
        
        # Time - with AM/PM toggle buttons
        ctk.CTkLabel(form_frame, text="Time:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=8, padx=(0, 10))
        time_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        time_frame.grid(row=4, column=1, pady=8, sticky="ew")
        
        time_entry = ctk.CTkEntry(time_frame, width=100, placeholder_text="HH:MM")
        try:
            dt_obj = datetime.fromisoformat(task.get("datetime", ""))
            time_entry.insert(0, dt_obj.strftime("%I:%M"))
            ampm_value = dt_obj.strftime("%p")
        except:
            time_entry.insert(0, "09:00")
            ampm_value = "AM"
        time_entry.pack(side=ctk.LEFT)
        
        ampm_var = tk.StringVar(value=ampm_value)
        
        def toggle_edit_am_pm(period):
            ampm_var.set(period)
            if period == "AM":
                edit_am_btn.configure(fg_color="#1f538d", hover_color="#14375e")
                edit_pm_btn.configure(fg_color="gray40", hover_color="gray30")
            else:
                edit_am_btn.configure(fg_color="gray40", hover_color="gray30")
                edit_pm_btn.configure(fg_color="#1f538d", hover_color="#14375e")
        
        edit_am_btn = ctk.CTkButton(time_frame, text="AM", width=50, height=28,
                                    command=lambda: toggle_edit_am_pm("AM"))
        edit_am_btn.pack(side=ctk.LEFT, padx=(10, 2))
        
        edit_pm_btn = ctk.CTkButton(time_frame, text="PM", width=50, height=28,
                                    command=lambda: toggle_edit_am_pm("PM"))
        edit_pm_btn.pack(side=ctk.LEFT, padx=2)
        
        # Set initial button states
        toggle_edit_am_pm(ampm_value)
        
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
                date_text = edit_selected_date.strftime("%Y-%m-%d")
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
        self.selected_date = datetime.now()
        self.date_btn.configure(text=self.selected_date.strftime("%B %d, %Y"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "09:00")
        self.priority_var.set("Medium")
        if hasattr(self, "am_pm_var"):
            self.am_pm_var.set("AM")
            self.update_am_pm_buttons()

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
        
        # Create comprehensive dialog
        win = ctk.CTkToplevel(self.root)
        win.title(f"Tasks on {self.current_date.strftime('%B')} {day}, {self.current_date.year}")
        win.geometry("850x450")
        try:
            win.transient(self.root)
            win.grab_set()
            win.lift()
            win.focus_force()
            win.attributes("-topmost", True)
        except Exception:
            pass
        
        # Center window
        try:
            win.update_idletasks()
            x = (win.winfo_screenwidth() // 2) - (850 // 2)
            y = (win.winfo_screenheight() // 2) - (450 // 2)
            win.geometry(f"850x450+{x}+{y}")
        except Exception:
            pass
        
        # Container
        body = ctk.CTkFrame(win, corner_radius=8, border_width=1)
        body.pack(fill=ctk.BOTH, expand=True, padx=12, pady=12)
        
        if not tasks_on_date:
            ctk.CTkLabel(body, text="No tasks scheduled for this date.",
                        font=("Arial", 12)).pack(pady=20)
        else:
            # Task list
            list_frame = ctk.CTkFrame(body, fg_color="transparent")
            list_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
            
            task_tree = ttk.Treeview(list_frame, columns=("Time", "Title", "Type", "Subject", "Priority"),
                                     show="headings", height=12, style="Custom.Treeview")
            for col, w in [("Time", 100), ("Title", 320), ("Type", 120), ("Subject", 140), ("Priority", 90)]:
                task_tree.heading(col, text=col)
                task_tree.column(col, width=w, anchor="center" if col in ("Time", "Priority") else "w")
            
            scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=task_tree.yview)
            task_tree.configure(yscrollcommand=scroll.set)
            task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate tasks
            for t in sorted(tasks_on_date, key=lambda x: x.get("datetime", "")):
                dt_str = t.get("datetime", "")
                time_only = ""
                try:
                    dt_obj = datetime.fromisoformat(dt_str)
                    time_only = dt_obj.strftime("%I:%M %p")
                except Exception:
                    time_only = dt_str.split(" ")[1] if " " in dt_str else ""
                
                values = (time_only, t.get("title", ""), t.get("type", ""),
                         t.get("subject", ""), t.get("priority", ""))
                task_tree.insert("", tk.END, values=values)
        
        # Close button
        footer = ctk.CTkFrame(win, fg_color="transparent")
        footer.pack(fill=ctk.X, padx=12, pady=(0,12))
        close_btn = ctk.CTkButton(footer, text="Close", width=80, command=win.destroy)
        close_btn.pack(side=ctk.RIGHT)
        win.bind("<Escape>", lambda e: win.destroy())




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


    def open_account_settings(self):
        """Open a CustomTkinter window to change display name and password."""
        # Helpers for users persistence and hashing
        def _users_path():
            return os.path.join(os.getcwd(), "users.json")

        def _load_users():
            try:
                p = _users_path()
                if os.path.exists(p):
                    with open(p, "r", encoding="utf-8") as f:
                        return json.load(f)
            except Exception:
                pass
            return {}

        def _save_users(users):
            try:
                with open(_users_path(), "w", encoding="utf-8") as f:
                    json.dump(users, f, indent=2)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save users.json: {e}")
                return False

        def _hash_password(pw):
            try:
                return hashlib.sha256(pw.encode()).hexdigest()
            except Exception:
                return ""

        # Build window
        win = ctk.CTkToplevel(self.root)
        win.title("Account Settings")
        win.geometry("680x520")
        win.transient(self.root)
        win.grab_set()
        try:
            # center window
            win.update_idletasks()
            x = (win.winfo_screenwidth() // 2) - (520 // 2)
            y = (win.winfo_screenheight() // 2) - (420 // 2)
            win.geometry(f"+{x}+{y}")
        except Exception:
            pass

        theme = self.themes.get(self.current_theme, self.themes["Default"])

        container = ctk.CTkFrame(win, corner_radius=10, border_width=1)
        container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Section: Display Name
        name_section = ctk.CTkFrame(container, fg_color="transparent")
        name_section.pack(fill=ctk.X, padx=16, pady=(8, 8))
        ctk.CTkLabel(name_section, text="Display Name", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0,6))
        new_name_var = tk.StringVar(value=self.username)
        new_name_entry = ctk.CTkEntry(name_section, textvariable=new_name_var, width=400)
        new_name_entry.pack(fill=ctk.X, pady=(2, 8))
        # Ensure the name field is ready to type on open
        try:
            new_name_entry.focus_set()
            win.after(120, lambda: new_name_entry.focus_force())
        except Exception:
            pass

        def _apply_name_change():
            users = _load_users()
            old = self.username.strip()
            new = new_name_var.get().strip()
            if not new:
                messagebox.showwarning("Invalid Name", "Display name cannot be empty.")
                return
            if new == old:
                messagebox.showinfo("No Change", "Display name is unchanged.")
                return
            if new in users:
                messagebox.showerror("Name Taken", "Another account already uses that name.")
                return
            # Move user password hash to new key
            pw_hash = users.get(old, None)
            if pw_hash is None:
                messagebox.showerror("Error", "Current user not found in users.json.")
                return
            users[new] = pw_hash
            if old in users:
                del users[old]
            if not _save_users(users):
                return
            # Rename per-user data file if present
            old_file = self.data_file
            new_file = f"data_{new}.json"
            try:
                if os.path.exists(old_file):
                    os.replace(old_file, new_file)
            except Exception as e:
                messagebox.showwarning("Data Rename", f"Renamed account, but failed to move data file: {e}\nA new file will be used going forward.")
            # Update runtime state and UI
            self.username = new
            self.data_file = new_file
            try:
                self.root.title(f"Study Planner - {self.username}")
                if hasattr(self, "username_label"):
                    self.username_label.configure(text=f"Logged in as: {self.username}")
            except Exception:
                pass
            messagebox.showinfo("Success", "Display name updated.")

        save_name_btn = ctk.CTkButton(name_section, text="Save Name", command=_apply_name_change, width=140)
        save_name_btn.pack(anchor="w", pady=(0,4))
        # Bind Enter to save name while Account Settings is active
        try:
            win.bind('<Return>', lambda e: _apply_name_change())
        except Exception:
            pass

        # Divider
        ctk.CTkLabel(container, text="").pack(pady=6)

        # Section: Change Password
        pwd_section = ctk.CTkFrame(container, fg_color="transparent")
        pwd_section.pack(fill=ctk.X, padx=16, pady=(8, 8))
        ctk.CTkLabel(pwd_section, text="Change Password", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0,6))

        # Current password display (non-editable, shows masked by default)
        ctk.CTkLabel(pwd_section, text="Current Password").pack(anchor="w", pady=(2,2))
        current_pw_label = ctk.CTkLabel(pwd_section, text="••••••••", 
                                        anchor="w", height=35,
                                        fg_color=("gray85", "gray25"), 
                                        corner_radius=6, padx=10)
        current_pw_label.pack(fill=ctk.X, pady=(0,6))
        
        # Store current password (will be set when user verifies)
        current_password_text = {"value": None, "showing": False}

        new_var = tk.StringVar()
        confirm_var = tk.StringVar()

        ctk.CTkLabel(pwd_section, text="New Password").pack(anchor="w", pady=(2,2))
        new_entry = ctk.CTkEntry(pwd_section, textvariable=new_var, show="*", width=400)
        new_entry.pack(fill=ctk.X, pady=(0,6))

        ctk.CTkLabel(pwd_section, text="Confirm New Password").pack(anchor="w", pady=(2,2))
        confirm_entry = ctk.CTkEntry(pwd_section, textvariable=confirm_var, show="*", width=400)
        confirm_entry.pack(fill=ctk.X, pady=(0,6))

        # Show/Hide toggle (affects all password fields)
        show_var = tk.BooleanVar(value=False)
        def _toggle_visibility():
            # Toggle show state
            showing = show_var.get()
            current_password_text["showing"] = showing
            
            # New password fields
            if showing:
                new_entry.configure(show="")
                confirm_entry.configure(show="")
            else:
                new_entry.configure(show="*")
                confirm_entry.configure(show="*")
            
            # Current password - verify identity first time showing
            if showing and current_password_text["value"] is None:
                # Create CustomTkinter verification dialog
                verify_dialog = ctk.CTkToplevel(win)
                verify_dialog.title("Verify Identity")
                verify_dialog.geometry("400x200")
                verify_dialog.transient(win)
                verify_dialog.grab_set()
                verify_dialog.resizable(False, False)
                
                # Center dialog
                verify_dialog.update_idletasks()
                x = (verify_dialog.winfo_screenwidth() // 2) - 200
                y = (verify_dialog.winfo_screenheight() // 2) - 100
                verify_dialog.geometry(f"400x200+{x}+{y}")
                
                # Container
                verify_container = ctk.CTkFrame(verify_dialog, corner_radius=10, border_width=1)
                verify_container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
                
                # Title
                ctk.CTkLabel(verify_container, text="Verify Identity", 
                            font=("Arial", 16, "bold")).pack(pady=(10, 5))
                ctk.CTkLabel(verify_container, text="Enter your current password to view it:", 
                            font=("Arial", 11)).pack(pady=(0, 15))
                
                # Password entry
                verify_pw_var = tk.StringVar()
                verify_entry = ctk.CTkEntry(verify_container, textvariable=verify_pw_var,
                                           show="*", width=300, height=35,
                                           placeholder_text="Current password")
                verify_entry.pack(pady=(0, 15))
                verify_entry.focus_set()
                try:
                    verify_dialog.after(120, lambda: verify_entry.focus_force())
                except Exception:
                    pass
                
                # Result storage
                result = {"password": None, "confirmed": False}
                
                def verify_and_close():
                    pw = verify_pw_var.get()
                    if pw:
                        users = _load_users()
                        if _hash_password(pw) == users.get(self.username.strip()):
                            result["password"] = pw
                            result["confirmed"] = True
                            verify_dialog.destroy()
                        else:
                            messagebox.showerror("Error", "Incorrect password.", parent=verify_dialog)
                            verify_entry.delete(0, tk.END)
                            verify_entry.focus_set()
                            try:
                                verify_dialog.after(120, lambda: verify_entry.focus_force())
                            except Exception:
                                pass
                    else:
                        messagebox.showwarning("Error", "Please enter a password.", parent=verify_dialog)
                
                def cancel():
                    verify_dialog.destroy()
                
                # Buttons
                btn_frame = ctk.CTkFrame(verify_container, fg_color="transparent")
                btn_frame.pack(pady=(0, 10))
                
                ctk.CTkButton(btn_frame, text="Verify", command=verify_and_close,
                             fg_color="#4a90e2", hover_color="#357abd",
                             width=120, height=35).pack(side=ctk.LEFT, padx=5)
                ctk.CTkButton(btn_frame, text="Cancel", command=cancel,
                             fg_color="gray50", hover_color="gray40",
                             width=120, height=35).pack(side=ctk.LEFT, padx=5)
                
                # Keyboard shortcuts
                verify_dialog.bind('<Return>', lambda e: verify_and_close())
                verify_dialog.bind('<Escape>', lambda e: cancel())
                
                # Wait for dialog to close
                verify_dialog.wait_window()
                
                # Process result
                if result["confirmed"] and result["password"]:
                    current_password_text["value"] = result["password"]
                    current_pw_label.configure(text=result["password"])
                else:
                    show_var.set(False)
                    return
            
            # Update current password display
            if current_password_text["value"]:
                if showing:
                    current_pw_label.configure(text=current_password_text["value"])
                else:
                    current_pw_label.configure(text="••••••••")
                    
        show_toggle = ctk.CTkCheckBox(pwd_section, text="Show Passwords", variable=show_var, command=_toggle_visibility,
                                     border_width=1, corner_radius=4, checkbox_height=18)
        show_toggle.pack(anchor="w", pady=(6,2))

        def _apply_password_change():
            users = _load_users()
            name = self.username.strip()
            if name not in users:
                messagebox.showerror("Error", "Current user not found in users.json.")
                return
            
            # Prompt for current password verification
            verify_pw = simpledialog.askstring("Verify Identity", 
                                              "Enter your current password to continue:",
                                              parent=win, show='*')
            if not verify_pw:
                return
            
            if _hash_password(verify_pw) != users.get(name):
                messagebox.showerror("Invalid", "Current password is incorrect.")
                return
            
            newp = new_var.get()
            conf = confirm_var.get()
            
            if not newp or not conf:
                messagebox.showwarning("Missing Info", "Please enter new password in both fields.")
                return
            if len(newp) < 6 or len(newp) > 16:
                messagebox.showwarning("Weak Password", "New password must be 6–16 characters.")
                return
            if newp != conf:
                messagebox.showerror("Mismatch", "New password and confirm do not match.")
                return
            if _hash_password(newp) == users.get(name):
                messagebox.showwarning("No Change", "New password is same as current.")
                return
            users[name] = _hash_password(newp)
            if not _save_users(users):
                return
            messagebox.showinfo("Success", "Password updated.")
            try:
                new_var.set("")
                confirm_var.set("")
            except Exception:
                pass

        save_pwd_btn = ctk.CTkButton(pwd_section, text="Save Password", command=_apply_password_change, width=160)
        save_pwd_btn.pack(anchor="w", pady=(8,0))
        # Bind Enter to save password in this dialog
        try:
            win.bind('<Return>', lambda e: _apply_password_change())
        except Exception:
            pass

        # Footer
        footer = ctk.CTkFrame(container, fg_color="transparent")
        footer.pack(fill=ctk.X, pady=(12,0))
        ctk.CTkButton(footer, text="Close", width=110, command=win.destroy).pack(side=ctk.RIGHT)

        # Theme styling via existing method
        try:
            # Ensure border colors match theme
            if hasattr(container, 'configure'):
                container.configure(border_color=theme.get('text', '#333333'))
            self.themed_widgets.extend([win, container, name_section, pwd_section])
            self.apply_theme()
        except Exception:
            pass

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
        # Professional-grade subjects manager with search, add/edit/delete
        win = ctk.CTkToplevel(self.root)
        win.title("Manage Subjects")
        try:
            win.transient(self.root)
            win.grab_set()
            win.lift()
            win.focus_force()
            # Ensure it appears above on Windows
            win.attributes("-topmost", True)
        except Exception:
            pass
        win.geometry("480x380")
        try:
            win.resizable(True, True)
        except Exception:
            pass
        # Center on screen
        try:
            win.update_idletasks()
            x = (win.winfo_screenwidth() // 2) - (560 // 2)
            y = (win.winfo_screenheight() // 2) - (420 // 2)
            win.geometry(f"560x420+{x}+{y}")
        except Exception:
            pass

        body = ctk.CTkFrame(win, corner_radius=8, border_width=1)
        body.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(10,5))
        footer = ctk.CTkFrame(win, fg_color="transparent")
        footer.pack(fill=ctk.X, padx=10, pady=(5,10))

        # One-column: editor on top, list below
        editor = ctk.CTkFrame(body, fg_color="transparent")
        editor.pack(fill=ctk.X, padx=10, pady=(10,6))
        ctk.CTkLabel(editor, text="Subject Name").pack(anchor="w")
        name_var = tk.StringVar()
        name_entry = ctk.CTkEntry(editor, textvariable=name_var, placeholder_text="Subject name")
        name_entry.pack(fill=ctk.X, pady=(6,0))

        list_frame = ctk.CTkFrame(body, fg_color="transparent")
        list_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(6,10))
        ctk.CTkLabel(list_frame, text="Subjects").pack(anchor="w")
        subj_list = tk.Listbox(list_frame, height=12)
        subj_list.pack(fill=tk.BOTH, expand=True, pady=(6,0))

        # Footer buttons
        add_btn = ctk.CTkButton(footer, text="Add", width=80)
        edit_btn = ctk.CTkButton(footer, text="Save", width=80)
        del_btn = ctk.CTkButton(footer, text="Delete", width=80)
        close_btn = ctk.CTkButton(footer, text="Close", width=80, command=win.destroy)
        add_btn.pack(side=ctk.LEFT)
        edit_btn.pack(side=ctk.LEFT, padx=6)
        del_btn.pack(side=ctk.LEFT)
        close_btn.pack(side=ctk.RIGHT)

        def refresh_list():
            subj_list.delete(0, tk.END)
            for s in sorted(self.subjects):
                subj_list.insert(tk.END, s)

        def select_list_item(event=None):
            try:
                idxs = subj_list.curselection()
                if not idxs:
                    return
                val = subj_list.get(idxs[0])
                name_var.set(val)
                name_entry.focus_set()
            except Exception:
                pass

        def add_subject():
            name = (name_var.get() or "").strip()
            if not name:
                messagebox.showwarning("Validation", "Subject name is required.", parent=win)
                return
            if name in self.subjects:
                messagebox.showinfo("Duplicate", "Subject already exists.", parent=win)
                return
            self.subjects.append(name)
            self.subjects.sort()
            refresh_list()
            try:
                self.subject_combo.configure(values=self.subjects)
            except Exception:
                pass
            self.save_data()
            name_var.set("")

        def update_subject():
            idxs = subj_list.curselection()
            if not idxs:
                messagebox.showinfo("Select", "Select a subject to update.", parent=win)
                return
            old = subj_list.get(idxs[0])
            new = (name_var.get() or "").strip()
            if not new:
                messagebox.showwarning("Validation", "Subject name is required.", parent=win)
                return
            if new != old and new in self.subjects:
                messagebox.showinfo("Duplicate", "Another subject with this name exists.", parent=win)
                return
            try:
                pos = self.subjects.index(old)
                self.subjects[pos] = new
                self.subjects.sort()
            except ValueError:
                pass
            refresh_list()
            try:
                self.subject_combo.configure(values=self.subjects)
            except Exception:
                pass
            self.save_data()

        def delete_subject():
            idxs = subj_list.curselection()
            if not idxs:
                messagebox.showinfo("Select", "Select a subject to delete.", parent=win)
                return
            val = subj_list.get(idxs[0])
            if messagebox.askyesno("Confirm", f"Delete subject '{val}'?", parent=win):
                try:
                    self.subjects.remove(val)
                except ValueError:
                    pass
                refresh_list()
                try:
                    self.subject_combo.configure(values=self.subjects)
                except Exception:
                    pass
                self.save_data()
                name_var.set("")

        # Bindings
        subj_list.bind("<<ListboxSelect>>", select_list_item)
        add_btn.configure(command=add_subject)
        edit_btn.configure(command=update_subject)
        del_btn.configure(command=delete_subject)
        win.bind("<Escape>", lambda e: win.destroy())
        name_entry.bind("<Return>", lambda e: add_subject())

        # Theme-responsive button colors
        try:
            theme = self.themes.get(self.current_theme, self.themes["Default"])
            accent = theme.get("accent", "#4a90e2")
            add_btn.configure(fg_color=accent, text_color="white")
            edit_btn.configure(fg_color=accent, text_color="white")
            del_btn.configure(fg_color="#f44336", text_color="white")
            close_btn.configure(fg_color="gray50", text_color="white")
        except Exception:
            pass

        refresh_list()
        name_entry.focus_set()





    def export_tasks_csv(self):
        import csv
        dest_csv = filedialog.asksaveasfilename(parent=self.root, title="Save Tasks CSV",
                                                defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not dest_csv:
            return  # Cancelled, do nothing
        try:
            with open(dest_csv, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "Title", "Date", "Subject", "Priority"])
                for t in self.tasks:
                    dt = t.get("datetime", "")
                    date_only = dt.split("T")[0] if "T" in dt else dt
                    writer.writerow([t.get("type", ""), t.get("title", ""), date_only, t.get("subject", ""), t.get("priority", "")])
            messagebox.showinfo("Export", f"Tasks exported to {dest_csv}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export CSV: {e}")

    def export_tasks_txt(self):
        dest_txt = filedialog.asksaveasfilename(parent=self.root, title="Save Tasks TXT",
                                                defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not dest_txt:
            return  # Cancelled, do nothing
        try:
            lines = ["Type\tTitle\tDate\tSubject\tPriority"]
            for t in self.tasks:
                dt = t.get("datetime", "")
                date_only = dt.split("T")[0] if "T" in dt else dt
                vals = [t.get("type", ""), t.get("title", ""), date_only, t.get("subject", ""), t.get("priority", "")]
                lines.append("\t".join(vals))
            with open(dest_txt, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Export", f"Tasks exported to {dest_txt}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export TXT: {e}")

    def export_notes_csv(self):
        # Export Quick Notes to CSV with destination selection
        import csv
        dest_csv = filedialog.asksaveasfilename(parent=self.root, title="Save Notes CSV",
                                                defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not dest_csv:
            return
        try:
            with open(dest_csv, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Time", "Note"])
                for n in self.sticky_notes:
                    ts = n.get('time', '')
                    date_part = ''
                    time_part = ''
                    if ts:
                        parts = ts.split(' ')
                        date_part = parts[0] if len(parts) > 0 else ''
                        if len(parts) >= 3:
                            time_part = parts[1] + ' ' + parts[2]
                        elif len(parts) == 2:
                            time_part = parts[1]
                    writer.writerow([date_part, time_part, n.get('text', '')])
            messagebox.showinfo("Export", f"Notes exported to {dest_csv}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export Notes CSV: {e}")

    def export_notes_txt(self):
        # Export Quick Notes to TXT with destination selection
        dest_txt = filedialog.asksaveasfilename(parent=self.root, title="Save Notes TXT",
                                                defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not dest_txt:
            return
        try:
            lines = ["Date\tTime\tNote"]
            for n in self.sticky_notes:
                ts = n.get('time', '')
                date_part = ''
                time_part = ''
                if ts:
                    parts = ts.split(' ')
                    date_part = parts[0] if len(parts) > 0 else ''
                    if len(parts) >= 3:
                        time_part = parts[1] + ' ' + parts[2]
                    elif len(parts) == 2:
                        time_part = parts[1]
                lines.append("\t".join([date_part, time_part, n.get('text', '')]))
            with open(dest_txt, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Export", f"Notes exported to {dest_txt}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export Notes TXT: {e}")




    def view_reminders(self):
        # Comprehensive reminders manager window
        win = ctk.CTkToplevel(self.root)
        win.title("Reminders")
        win.geometry("950x560")
        try:
            win.transient(self.root)
            win.grab_set()
            win.lift()
            win.focus_force()
            win.attributes("-topmost", True)
        except Exception:
            pass

        # Theme
        theme = self.themes.get(self.current_theme, self.themes["Default"])
        accent = theme["accent"]
        text_color = theme["text"]
        bg_color = theme["bg"]

        # Layout containers
        header = ctk.CTkFrame(win, fg_color="transparent")
        header.pack(fill=ctk.X, padx=12, pady=(12,6))
        body = ctk.CTkFrame(win, corner_radius=8, border_width=1, border_color=text_color, fg_color=bg_color)
        body.pack(fill=ctk.BOTH, expand=True, padx=12, pady=6)
        footer = ctk.CTkFrame(win, fg_color="transparent")
        footer.pack(fill=ctk.X, padx=12, pady=(6,12))

        # Header filters
        timeframe_var = tk.StringVar(value="7 days")
        ctk.CTkLabel(header, text="Timeframe:").pack(side=ctk.LEFT)
        timeframe_menu = ctk.CTkOptionMenu(header, values=["Today", "3 days", "7 days", "30 days", "All"],
                           variable=timeframe_var)
        timeframe_menu.pack(side=ctk.LEFT, padx=(6,12))

        subject_var = tk.StringVar(value="All")
        ctk.CTkLabel(header, text="Subject:").pack(side=ctk.LEFT)
        subject_menu = ctk.CTkOptionMenu(header, values=["All"] + sorted(self.subjects), variable=subject_var)
        subject_menu.pack(side=ctk.LEFT, padx=(6,12))

        type_var = tk.StringVar(value="All")
        ctk.CTkLabel(header, text="Type:").pack(side=ctk.LEFT)
        type_menu = ctk.CTkOptionMenu(header, values=["All", "Assignment", "Exam", "Class", "Study Session"],
                           variable=type_var)
        type_menu.pack(side=ctk.LEFT, padx=(6,12))

        sort_var = tk.StringVar(value="Date")
        ctk.CTkLabel(header, text="Sort:").pack(side=ctk.LEFT)
        sort_menu = ctk.CTkOptionMenu(header, values=["Date", "Priority", "Subject"], variable=sort_var)
        sort_menu.pack(side=ctk.LEFT, padx=(6,0))

        # Body: Treeview
        body.pack_propagate(False)
        list_frame = ctk.CTkFrame(body, fg_color="transparent")
        list_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        reminders_tree = ttk.Treeview(list_frame, columns=("Date", "Time", "Title", "Type", "Subject", "Priority"), show="headings")
        for col, w in [("Date", 110), ("Time", 90), ("Title", 240), ("Type", 110), ("Subject", 140), ("Priority", 90)]:
            reminders_tree.heading(col, text=col)
            reminders_tree.column(col, width=w, anchor="center" if col in ("Date","Time","Priority") else "w")
        scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=reminders_tree.yview)
        reminders_tree.configure(yscrollcommand=scroll.set)
        reminders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Footer actions
        export_btn = ctk.CTkButton(footer, text="Export CSV", width=90)
        close_btn = ctk.CTkButton(footer, text="Close", width=80, command=win.destroy)
        export_btn.pack(side=ctk.LEFT)
        close_btn.pack(side=ctk.RIGHT)

        def _parse_dt(dt_str):
            try:
                return datetime.fromisoformat(dt_str)
            except Exception:
                try:
                    return datetime.strptime(dt_str[:16].replace("T"," "), "%Y-%m-%d %H:%M")
                except Exception:
                    return None

        def _filter_and_populate():
            for item in reminders_tree.get_children():
                reminders_tree.delete(item)

            now = datetime.now()
            tf = timeframe_var.get()
            if tf == "Today":
                end = now.replace(hour=23, minute=59, second=59)
            elif tf == "3 days":
                end = now + timedelta(days=3)
            elif tf == "7 days":
                end = now + timedelta(days=7)
            elif tf == "30 days":
                end = now + timedelta(days=30)
            else:
                end = None

            filtered = []
            for i, t in enumerate(self.tasks):
                dt = _parse_dt(t.get("datetime", ""))
                if not dt:
                    continue
                if dt < now:
                    # skip past events; this view focuses upcoming
                    continue
                if end and dt > end:
                    continue
                if subject_var.get() != "All" and t.get("subject") != subject_var.get():
                    continue
                if type_var.get() != "All" and t.get("type") != type_var.get():
                    continue
                filtered.append((i, t, dt))

            sv = sort_var.get()
            if sv == "Priority":
                pr_rank = {"High":0, "Medium":1, "Low":2}
                filtered.sort(key=lambda x: (pr_rank.get(x[1].get("priority"), 3), x[2]))
            elif sv == "Subject":
                filtered.sort(key=lambda x: (x[1].get("subject",""), x[2]))
            else:  # Date
                filtered.sort(key=lambda x: x[2])

            for i, t, dt in filtered:
                date_only = dt.strftime("%Y-%m-%d")
                time_only = dt.strftime("%I:%M %p")
                values = (date_only, time_only, t.get("title",""), t.get("type",""), t.get("subject",""), t.get("priority",""))
                try:
                    reminders_tree.insert("", tk.END, iid=str(i), values=values)
                except Exception:
                    reminders_tree.insert("", tk.END, values=values)

        def _export_csv():
            import csv
            dest = filedialog.asksaveasfilename(parent=win, title="Save Reminders CSV",
                                                defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if not dest:
                return
            try:
                with open(dest, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date","Time","Title","Type","Subject","Priority"])
                    for iid in reminders_tree.get_children():
                        writer.writerow(reminders_tree.item(iid, "values"))
                messagebox.showinfo("Export", f"Exported reminders to {dest}", parent=win)
            except Exception as e:
                messagebox.showerror("Export", f"Failed to export: {e}", parent=win)


        def _export_txt():
            dest = filedialog.asksaveasfilename(parent=win, title="Save Reminders TXT",
                                                defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if not dest:
                return
            try:
                lines = ["Date\tTime\tTitle\tType\tSubject\tPriority"]
                for iid in reminders_tree.get_children():
                    vals = reminders_tree.item(iid, "values")
                    lines.append("\t".join(vals))
                with open(dest, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                messagebox.showinfo("Export", f"Exported reminders to {dest}", parent=win)
            except Exception as e:
                messagebox.showerror("Export", f"Failed to export: {e}", parent=win)

        export_btn.configure(command=_export_csv, fg_color=accent, text_color="white")
        txt_btn = ctk.CTkButton(footer, text="Export TXT", width=90)
        txt_btn.pack(side=ctk.LEFT, padx=6)
        txt_btn.configure(command=_export_txt)
        try:
            txt_btn.configure(fg_color=accent, text_color="white")
            close_btn.configure(fg_color="gray50", text_color="white")
        except Exception:
            pass

        # Bind filters
        timeframe_menu.configure(command=lambda _=None: _filter_and_populate())
        subject_menu.configure(command=lambda _=None: _filter_and_populate())
        type_menu.configure(command=lambda _=None: _filter_and_populate())
        sort_menu.configure(command=lambda _=None: _filter_and_populate())
        win.bind("<Escape>", lambda e: win.destroy())

        _filter_and_populate()




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
        # Use a neutral off-white background that blends with all themes
        root_bg = "#f5f5f7"  # Soft off-white that works with all accents
        try:
            self.root.configure(fg_color=root_bg)
        except:
            self.root.configure(bg=root_bg)




        # Create or update a ttk style for treeviews so colors are applied there too.
        # Calculate off-white tree background (slightly whiter than frame bg)
        try:
            r, g, b = hex_to_rgb(bg)
            luminance_bg = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        except Exception:
            luminance_bg = 0.6
        
        # For light themes, make tree slightly lighter; for dark themes, slightly lighter too
        if luminance_bg > 0.6:
            # Light theme: make tree whiter than frame
            tree_bg = "#f9f9fc" if self.current_theme == "Default" else adjust_brightness(bg, 1.03)
        else:
            # Dark theme: make tree slightly lighter
            tree_bg = adjust_brightness(bg, 1.08)
        
        try:
            style = ttk.Style()
            # Use a custom style name to avoid interfering with global styles
            style.configure("Custom.Treeview", background=tree_bg, fieldbackground=tree_bg, foreground=text)
            # Heading text color: always use theme text (dark) for readability across themes
            style.configure("Custom.Treeview.Heading", background=accent, foreground=text)
            style.map("Custom.Treeview", background=[('selected', accent)], foreground=[('selected', 'white')])
        except Exception:
            style = None

        for widget in self.themed_widgets:
            try:
                # Try CTk-specific configuration first
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(fg_color="transparent")
                    if widget == self.title_label or widget == self.month_label:
                        widget.configure(text_color=accent)
                    else:
                        widget.configure(text_color=text)
                elif isinstance(widget, ctk.CTkButton):
                    # Give CTkButtons a visible background color (not identical to window bg)
                    widget.configure(fg_color=button_bg, text_color=text, border_width=1, border_color=accent)
                    # Make important action buttons use the accent color so they're visible.
                    primaries = [getattr(self, "subjects_btn", None), getattr(self, "reminders_btn", None),
                                getattr(self, "add_btn", None), getattr(self, "prev_btn", None),
                                getattr(self, "next_btn", None), getattr(self, "add_note_btn", None),
                                getattr(self, "edit_note_btn", None), getattr(self, "delete_note_btn", None), 
                                getattr(self, "new_quote_btn", None), getattr(self, "export_btn", None)]
                    if widget in primaries:
                        widget.configure(fg_color=accent, text_color="white", border_width=1, border_color=accent)
                    # Task-specific special buttons
                    if widget == getattr(self, 'delete_btn', None):
                        # task deletion is destructive -> red
                        widget.configure(fg_color="#f44336", text_color="white", border_width=1, border_color=accent)
                    if widget == getattr(self, 'mark_done_btn', None):
                        # mark-as-done should look positive
                        widget.configure(fg_color="#4caf50", text_color="white", border_width=1, border_color=accent)
                elif isinstance(widget, ctk.CTkFrame):
                    # Main frame and transparent frames use neutral bg, card frames use themed bg
                    if widget == self.main_frame:
                        widget.configure(fg_color=root_bg, border_color=accent)
                    else:
                        # Always set border_color to accent for theme responsiveness
                        try:
                            widget.configure(fg_color=bg, border_color=accent)
                        except Exception:
                            try:
                                widget.configure(fg_color=bg)
                            except Exception:
                                pass
                elif isinstance(widget, (ctk.CTkComboBox, getattr(ctk, 'CTkOptionMenu', object))):
                    # combobox/option menus use different option names for colors
                    try:
                        # set a slightly contrasted background for dropdowns and keep text readable
                        widget.configure(fg_color=combo_bg, text_color=text, border_width=1, border_color=accent)
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
                    # CTkEntry uses fg_color for background, text_color for text, and border_color for borders
                    widget.configure(fg_color=entry_bg, text_color=text, border_color=accent, border_width=1)
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
                            # Completed tasks should use theme text color with dimmed effect
                            # Instead of gray, use slightly dimmed theme text color
                            r, g, b = hex_to_rgb(text)
                            dimmed_text = rgb_to_hex((r * 0.6, g * 0.6, b * 0.6))
                            widget.tag_configure('done', foreground=dimmed_text)
                            widget.tag_configure('sep', foreground=accent)
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
    login = LoginWindow()
    login.root.mainloop()