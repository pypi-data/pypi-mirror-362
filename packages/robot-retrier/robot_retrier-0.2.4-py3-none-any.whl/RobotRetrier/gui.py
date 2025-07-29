import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import threading
from functools import wraps
from robot.libdocpkg import LibraryDocumentation
import logging
from robot.libraries.BuiltIn import BuiltIn
import tkinter as tk
from tkinter import ttk
from .event_logger import (
    log_suite_start,
    log_suite_end,
    log_test_start,
    log_test_end,
)




class SimpleRetryGUI:
    def __init__(self, core):
        self.core = core
        self.gui_ready = False

        core.gui_controller = self
        self._lock = threading.Lock()
        self.execution_in_progress = False

        self.root = tk.Tk()
        self.root.title("Robot Framework Debugger")
        self.root.geometry("900x700")
        self.root.minsize(850, 600)
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.max_log_lines = 1000
        # Color tags for styled log output
        # self.failure_text.tag_config("fail", foreground="red")
        # self.failure_text.tag_config("pass", foreground="green")
        # self.failure_text.tag_config("pending", foreground="gray")

        self.libraries = {}
        self.library_names = []
        self._setup_ui()
        # self.root.withdraw()
        self.gui_ready = True

    def _thread_safe(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self._lock:
                if self.root.winfo_exists():
                    self.root.after(0, lambda: func(self, *args, **kwargs))
        return wrapper

    def _setup_ui(self):
        header = tk.Label(
            self.root,
            text="🔧 Robot Framework Retry Debugger",
            font=("Segoe UI", 14, "bold"),
            fg="navy"
        )
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        # === Failure Info Panel ===
        # === Failure Info Panel ===
        self.failure_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            height=30,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Consolas", 10),
            borderwidth=1,
            relief=tk.FLAT
        )
        self.failure_text.tag_config("fail", foreground="red")
        self.failure_text.tag_config("pass", foreground="green")
        self.failure_text.tag_config("pending", foreground="gray")
        self.failure_text.tag_config("header", font=("Consolas", 10, "bold"))
        self.failure_text.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.failure_text.config(state=tk.DISABLED)

        # === Tag Styles for colored log lines ===
        self.failure_text.tag_config("fail")
        self.failure_text.tag_config("pass")
        self.failure_text.tag_config("pending")
        self.failure_text.tag_config("header", font=("Consolas", 10))

        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 10),
            bg="#e9f1ff",
            anchor='w',
            padx=10
        )
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))
        # Apply improved tab style
        style = ttk.Style()
        style.theme_use("clam")  # Better rendering than 'default'

        style.configure("TNotebook", background="#dcdcdc", borderwidth=1)
        style.configure("TNotebook.Tab", background="#f2f2f2", padding=(12, 6), font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")])
        exit_btn = tk.Button(
            self.root,
            text="❌ Close Debugger",
            command=self.safe_close,
            bg="#f44336",
            fg="white"
        )
        exit_btn.grid(row=99, column=0, pady=10)

        # === Sub-tabs for Retry and Custom Keyword ===
        self.sub_tabs = ttk.Notebook(self.root)
        self.sub_tabs.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.root.rowconfigure(2, weight=1)

        self.retry_tab = tk.Frame(self.sub_tabs)
        self.custom_tab = tk.Frame(self.sub_tabs)
        self.sub_tabs.add(self.retry_tab, text="Retry Failed Keyword")
        self.sub_tabs.add(self.custom_tab, text="Run Custom Keyword")
        self.var_tab = tk.Frame(self.sub_tabs)
        self.sub_tabs.add(self.var_tab, text="Variable Inspector")
        self.sub_tabs.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self._setup_variable_tab()
        self._setup_retry_tab()
        self._setup_custom_tab()


    def _on_tab_changed(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
        if selected_tab == "Variable Inspector":
            self._refresh_variable_view()

    # === RETRY TAB ===
    def _setup_retry_tab(self):
        self.kw_name_var = tk.StringVar()

        kw_frame = tk.Frame(self.retry_tab)
        kw_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(kw_frame, text="Keyword Name:").pack(side=tk.LEFT)
        self.kw_name_entry = tk.Entry(kw_frame, textvariable=self.kw_name_var, width=50)
        self.kw_name_entry.pack(side=tk.LEFT, padx=5)

        self.args_frame = tk.LabelFrame(self.retry_tab, text="Edit Keyword Arguments", padx=5, pady=5)
        self.args_frame.pack(fill=tk.X, padx=5, pady=5)

        buttons_frame = tk.Frame(self.retry_tab)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.retry_btn = tk.Button(buttons_frame, text="Retry and Continue", command=self._on_retry_and_continue)
        self.retry_btn.pack(side=tk.LEFT, padx=5)


        self.add_arg_btn = tk.Button(buttons_frame, text="+ Add Arg", command=self._on_add_argument)
        self.add_arg_btn.pack(side=tk.LEFT, padx=5)

        self.skip_kw_btn = tk.Button(buttons_frame, text="Skip and Continue", command=self._on_skip_keyword, bg="#DAA520")
        self.skip_kw_btn.pack(side=tk.LEFT, padx=5)

        self.skip_btn = tk.Button(buttons_frame, text="Skip Test", command=self._on_skip_test, bg="#FFA500")
        self.skip_btn.pack(side=tk.LEFT, padx=5)

        self.abort_btn = tk.Button(buttons_frame, text="Abort Suite", command=self._on_abort_suite, bg="#FF6347")
        self.abort_btn.pack(side=tk.RIGHT, padx=5)

    # === CUSTOM EXECUTOR TAB ===
    def _setup_custom_tab(self):
        self.library_var = tk.StringVar()
        self.keyword_var = tk.StringVar()
        self.command_var = tk.StringVar()
        # self.result_var = tk.StringVar()

        selector_frame = tk.Frame(self.custom_tab)
        selector_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(selector_frame, text="Library:").pack(side=tk.LEFT)
        self.library_dropdown = ttk.Combobox(selector_frame, textvariable=self.library_var, state="readonly")
        self.library_dropdown.pack(side=tk.LEFT, padx=5)

        tk.Label(selector_frame, text="Keyword:").pack(side=tk.LEFT)
        self.keyword_dropdown = ttk.Combobox(selector_frame,width=50, textvariable=self.keyword_var, state="readonly")
        self.keyword_dropdown.pack(side=tk.LEFT, padx=5)

        self.library_dropdown.bind("<<ComboboxSelected>>", self._on_library_selected)
        self.keyword_dropdown.bind("<<ComboboxSelected>>", self._on_keyword_selected)

        self.custom_args_frame = tk.LabelFrame(self.custom_tab, text="Keyword Arguments")
        self.custom_args_frame.pack(fill=tk.X, padx=10, pady=5)

        btn_frame = tk.Frame(self.custom_tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="Execute", command=self._execute_command).pack(side=tk.LEFT)
        # self.result_display = tk.Label(btn_frame, textvariable=self.result_var, fg='green')

        # self.result_display.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="+ Add Arg", command=self._add_custom_argument_field).pack(side=tk.LEFT, padx=5)

        doc_frame = tk.LabelFrame(self.custom_tab, text="Keyword Documentation", padx=5, pady=5)
        doc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.doc_display = scrolledtext.ScrolledText(doc_frame, wrap=tk.WORD)
        self.doc_display.pack(fill=tk.BOTH, expand=True)
        self.doc_display.config(state=tk.DISABLED)
        self.executor_ready = True
        self.load_libraries_and_keywords()
        self._refresh_library_dropdown()
        #
        # if self.libraries:
        #     # print("[DEBUG] refreshing dropdown after UI ready")
        #     self._refresh_library_dropdown()

    def _on_library_selected(self, event=None):
        lib = self.library_var.get()
        if lib not in self.libraries:
            return
        self.keyword_dropdown['values'] = [kw['name'] for kw in self.libraries[lib]]
        if self.keyword_dropdown['values']:
            self.keyword_var.set(self.keyword_dropdown['values'][0])
            self._on_keyword_selected()

    def _on_keyword_selected(self, event=None):
        lib = self.library_var.get()
        kw_name = self.keyword_var.get()

        if not lib or not kw_name:
            return

        if lib in self.libraries:
            for kw in self.libraries[lib]:
                if kw['name'] == kw_name:
                    self._populate_custom_args_editor(kw['args'])

                    # ✅ Show signature
                    args_text = ", ".join(
                        a.name if hasattr(a, "name") else str(a)
                        for a in kw['args']
                    )
                    signature = f"{kw_name}({args_text})"
                    self.command_var.set(signature)

                    # ✅ Show doc
                    self.doc_display.config(state=tk.NORMAL)
                    self.doc_display.delete("1.0", tk.END)
                    self.doc_display.insert(tk.END, f"{kw_name}\n\nSignature:\n{signature}\n\nDoc:\n{kw['doc']}")
                    self.doc_display.config(state=tk.DISABLED)
                    break

    def _populate_custom_args_editor(self, args):
        for widget in self.custom_args_frame.winfo_children():
            widget.destroy()
        self.custom_arg_vars = []

        for i, arg in enumerate(args or []):
            if hasattr(arg, "name"):
                name = arg.name
                default = getattr(arg, "default", None)
            else:
                name = str(arg)
                default = None

            label = f"{name}" if default is None else f"{name} (default={default})"
            var = tk.StringVar(value=str(default) if default is not None else "")

            frame = tk.Frame(self.custom_args_frame)
            frame.pack(anchor='w', pady=2, fill='x')

            tk.Label(frame, text=f"{label}:").pack(side='left')
            entry = tk.Entry(frame, textvariable=var, width=60)
            entry.pack(side='left', padx=5)
            tk.Button(frame, text="–", command=lambda f=frame: self._remove_custom_argument_field(f)).pack(side='left')

            # Optional tooltip for extra polish
            def create_tooltip(widget, text):
                tip = None

                def on_enter(event):
                    nonlocal tip
                    tip = tk.Toplevel(widget)
                    tip.wm_overrideredirect(True)
                    x = widget.winfo_rootx() + 20
                    y = widget.winfo_rooty() + 20
                    tip.geometry(f"+{x}+{y}")
                    tk.Label(tip, text=text, background="lightyellow", relief='solid', borderwidth=1).pack()

                def on_leave(event):
                    nonlocal tip
                    if tip:
                        tip.destroy()

                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

            create_tooltip(entry, label)
            self.custom_arg_vars.append(var)

        # self._add_custom_argument_field()  # start with one empty field

    def _add_custom_argument_field(self, value=""):
        var = tk.StringVar(value=str(value))
        frame = tk.Frame(self.custom_args_frame)
        frame.pack(anchor='w', pady=2, fill='x')
        tk.Label(frame, text=f"Arg {len(self.custom_arg_vars) + 1}:").pack(side='left')
        tk.Entry(frame, textvariable=var, width=60).pack(side='left', padx=2)
        tk.Button(frame, text="–", command=lambda f=frame: self._remove_custom_argument_field(f)).pack(side='left')
        self.custom_arg_vars.append(var)

    def _remove_custom_argument_field(self, frame):
        idx = list(self.custom_args_frame.children.values()).index(frame)
        frame.destroy()
        del self.custom_arg_vars[idx]

    def _execute_command(self):
        lib = self.library_var.get()
        kw = self.keyword_var.get()

        if not lib or not kw:
            self._update_failure_display("Cannot execute. Please select both library and keyword.",
                                         "[Custom] Execution Blocked", "fail")
            return

        args = [self.core.parse_arg(var.get()) for var in getattr(self, 'custom_arg_vars', [])]

        try:
            result = BuiltIn().run_keyword(f"{lib}.{kw}", *args)
            BuiltIn().set_test_variable("${RETURN_VALUE}", result)
            self._update_failure_display(
                f"Executed: {lib}.{kw}\nArgs: {args}\n\n${{RETURN_VALUE}} = {result}",
                f"[Custom] {lib}.{kw} ✅",
                "pass",
                keyword_name=kw,
                args=args
            )
        except Exception as e:
            self._update_failure_display(
                f"Executed: {lib}.{kw}\nArgs: {args}\n\nError: {e}",
                f"[Custom] {lib}.{kw} ❌",
                "fail",
                keyword_name=kw,
                args=args
            )

    def _update_keywords(self):
        lib = self.library_var.get()
        menu = self.keyword_dropdown["menu"]
        menu.delete(0, "end")

        if lib not in self.libraries:
            return

        keywords = self.libraries[lib]
        for kw in keywords:
            menu.add_command(label=kw['name'], command=lambda name=kw['name']: self.keyword_var.set(name))

    def _update_command_from_keyword(self):
        lib = self.library_var.get()
        kw_name = self.keyword_var.get()
        if lib in self.libraries:
            for kw in self.libraries[lib]:
                if kw['name'] == kw_name:
                    args = [arg for arg in kw['args'] if '=' not in arg]
                    self.command_var.set(f"{lib}.{kw_name}    {'    '.join(args)}")

                    self.doc_display.config(state=tk.NORMAL)
                    self.doc_display.delete("1.0", tk.END)
                    self.doc_display.insert(tk.END, f"{kw_name}\n\nArgs:\n{kw['args']}\n\nDoc:\n{kw['doc']}")
                    self.doc_display.config(state=tk.DISABLED)
                    break

    # def _execute_command(self):
    #     parts = [p.strip() for p in self.command_var.get().split("    ") if p.strip()]
    #     try:
    #         result = BuiltIn().run_keyword(*parts)
    #         BuiltIn().set_test_variable("${RETURN_VALUE}", result)
    #         self.result_var.set(f"✅ RETURN = {result}")
    #     except Exception as e:
    #         self.result_var.set(f"❌ {e}")
    def _execute_command(self):
        if self.execution_in_progress:
            self._update_failure_display("Execution in progress. Please wait.", "[Custom] Busy", "fail")
            return

        lib = self.library_var.get()
        kw = self.keyword_var.get()

        if not lib or not kw:
            self._update_failure_display("Cannot execute. Please select both library and keyword.",
                                         "[Custom] Execution Blocked", "fail")
            return

        args = [self.core.parse_arg(var.get()) for var in getattr(self, 'custom_arg_vars', [])]
        self.execution_in_progress = True

        def _run():
            try:
                result = BuiltIn().run_keyword(f"{lib}.{kw}", *args)
                BuiltIn().set_test_variable("${RETURN_VALUE}", result)
                self._update_failure_display(
                    f"Executed: {lib}.{kw}\nArgs: {args}\n\n${{RETURN_VALUE}} = {result}",
                    f"[Custom] {lib}.{kw} ✅",
                    "pass",
                    keyword_name=kw,
                    args=args
                )
            except Exception as e:
                self._update_failure_display(
                    f"Executed: {lib}.{kw}\nArgs: {args}\n\nError: {e}",
                    f"[Custom] {lib}.{kw} ❌",
                    "fail",
                    keyword_name=kw,
                    args=args
                )
            finally:
                self.execution_in_progress = False

        threading.Thread(target=_run, daemon=True).start()

    @_thread_safe
    def show_failure(self, suite, test, keyword, message, args):
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_text = (
            f"[{timestamp}] ❗ TEST FAILURE\n"
            f"  Test Name : {test}\n"
            f"  Keyword   : {keyword}\n"
            f"  Message   : {message.strip()}\n"
            f"{'-' * 60}\n"
        )

        self.failure_text.config(state=tk.NORMAL)
        self.failure_text.insert(tk.END, full_text)
        self.failure_text.see(tk.END)
        self.failure_text.config(state=tk.DISABLED)

        self.kw_name_var.set(keyword)

        # ✅ Resolve variables like ${locator} into actual values
        builtin = BuiltIn()
        resolved_args = []
        for a in args:
            if isinstance(a, str) and a.startswith("${") and a.endswith("}"):
                try:
                    resolved_args.append(builtin.get_variable_value(a))
                except:
                    resolved_args.append(a)
            else:
                resolved_args.append(a)

        self._build_args_editor(resolved_args)
        self._show_window()

    def _build_args_editor(self, args):
        for widget in self.args_frame.winfo_children():
            widget.destroy()
        self.arg_vars = []
        for val in args or []:
            self._add_argument_field(val)

    def _add_argument_field(self, value=""):
        index = len(self.arg_vars)
        var = tk.StringVar(value=str(value))
        frame = tk.Frame(self.args_frame)
        frame.pack(anchor='w', pady=2, fill='x')
        tk.Label(frame, text=f"Arg {index + 1}:").pack(side='left')
        tk.Entry(frame, textvariable=var, width=70).pack(side='left', padx=2)
        tk.Button(frame, text="–", command=lambda f=frame: self._remove_argument_field(f)).pack(side='left')
        self.arg_vars.append(var)

    def _remove_argument_field(self, frame):
        idx = list(self.args_frame.children.values()).index(frame)
        frame.destroy()
        del self.arg_vars[idx]

    def _on_add_argument(self):
        self._add_argument_field()

    def _on_retry_and_continue(self):
        if not self.core.failed_keyword:
            messagebox.showerror("Error", "No failed keyword to retry.")
            return
        # kw_name = self.core.failed_keyword.name
        kw_name = self.kw_name_var.get().strip()
        args = [self.core.parse_arg(var.get()) for var in self.arg_vars]
        if not kw_name:
            messagebox.showerror("Invalid Input", "Keyword name cannot be empty.")
            return
        self.update_status("Retrying...", "blue")
        status, message = self.core.retry_keyword(kw_name, args)
        if status == 'PASS':
            self._update_failure_display(
                f"Retry succeeded: {kw_name}\nArgs: {args}",
                f"[{self.core.current_test}] Retry Passed",
                "pass",
                keyword_name=kw_name,
                args=args
            )
            self.core.retry_success = True
            self.core.continue_event.set()

        else:
            self._update_failure_display(
                f"Retry failed: {kw_name}\nArgs: {args}\nError: {message}",
                f"[{self.core.current_test}] Retry failed",
                "fail",
                keyword_name=kw_name,
                args=args
            )

    def _update_failure_display(self, text, prefix, status, keyword_name=None, args=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {"pass": "✅", "fail": "❌", "pending": "🕓"}
        icon = icons.get(status, "🕓")

        test_name = self.core.current_test or "Unknown Test"
        if not keyword_name:
            keyword_name = self.core.failed_keyword.name if self.core.failed_keyword else "Unknown Keyword"
        if args is None:
            args = self.core.failed_keyword.args if self.core.failed_keyword else []

        # Format Robot Framework-style keyword syntax
        keyword_line = f"{keyword_name}    " + "    ".join(str(arg) for arg in args)

        # Extract error/reason
        reason = ""
        if "Error:" in text:
            reason = text.split("Error:", 1)[-1].strip()
        elif "Retry failed:" in text:
            reason = text.split("Retry failed:", 1)[-1].strip()

        # Build full formatted message
        full_text = (
            f"[{timestamp}] {icon} {'Keyword Passed' if status == 'pass' else 'Keyword Failed'}\n"
            f"  Test Name   : {test_name}\n"
            f"  Keyword     : {keyword_line}\n"
            f"  Status      : {status.upper()}\n"
        )

        # if reason:
        #     full_text += f"  Reason      : {reason}\n"
        if reason:
            full_text += f"  Reason      : {reason}\n"

            # ✅ NEW: Show return value if present in 'text'
        if "${RETURN_VALUE}" in text or "return value" in text.lower():
            lines = text.splitlines()
            for line in lines:
                if "${RETURN_VALUE}" in line or "return value" in line.lower():
                    full_text += f"  Return      : {line.split('=')[-1].strip()}\n"

        full_text += "-" * 60 + "\n"

        # Tag styling
        tag = {"pass": "pass", "fail": "fail", "pending": "pending"}.get(status)

        self.failure_text.config(state=tk.NORMAL)
        self.failure_text.insert(tk.END, full_text, tag)
        self.failure_text.see(tk.END)
        self.failure_text.config(state=tk.DISABLED)

        self._trim_failure_log()

    def _trim_failure_log(self, max_lines=500):
        lines = self.failure_text.get("1.0", tk.END).splitlines()
        if len(lines) > max_lines:
            trimmed = "\n".join(lines[-max_lines:])
            self.failure_text.config(state=tk.NORMAL)
            self.failure_text.delete("1.0", tk.END)
            self.failure_text.insert(tk.END, trimmed)
            self.failure_text.config(state=tk.DISABLED)

    # def update_status(self, text, color="black"):
    #     self.status_label.config(text=text, fg=color)
    def update_status(self, text, color="black"):
        self.status_label.config(text=text)
        bg = {
            "blue": "#e9f1ff",
            "red": "#ffe6e6",
            "green": "#e6ffe6",
            "gray": "#f0f0f0"
        }.get(color, "#f0f0f0")
        self.status_label.config(fg=color, bg=bg)

    def _on_skip_test(self):
        self.update_status("⚠️ Test skipped", "orange")
        self.core.skip_test = True
        self.core.continue_event.set()

    def _on_abort_suite(self):
        if messagebox.askyesno("Abort Suite", "Really abort entire test suite?"):
            self.update_status("❌ Suite aborted", "red")
            self.core.abort_suite = True
            self.core.continue_event.set()

    def _on_window_close(self):
        self.root.withdraw()

    def _show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def library_imported(self, name):
        # print(f"[DEBUG] library_imported called for: {name}")
        try:
            libdoc = LibraryDocumentation(name)
            keywords = [{'name': kw.name, 'args': kw.args, 'doc': kw.doc} for kw in libdoc.keywords]
            self.libraries[libdoc.name] = keywords
            # print(f"[DEBUG] Loaded library: {libdoc.name} with {len(keywords)} keywords")

            # ✅ Only refresh dropdown if custom tab is fully built
            if getattr(self, "executor_ready", False):
                self._refresh_library_dropdown()
        except Exception as e:
            print(f"[!] Failed to load library: {name} -> {e}")

    def _refresh_library_dropdown(self):
        """Refresh the library and keyword dropdowns in the Custom Keyword tab."""

        required = ["library_dropdown", "keyword_dropdown", "doc_display"]
        if not all(hasattr(self, attr) for attr in required):
            return  # GUI not ready yet

        lib_names = sorted(self.libraries.keys())
        self.library_dropdown["values"] = lib_names
        if not self.library_var.get() and lib_names:
            self.library_var.set(lib_names[0])
            self._on_library_selected()
        current = self.library_dropdown.get()
        if current not in lib_names:
            self.library_dropdown.set('')
            self.keyword_dropdown.set('')
            self.keyword_dropdown["values"] = []

            # Clear argument editor
            for widget in self.custom_args_frame.winfo_children():
                widget.destroy()
            self.custom_arg_vars = []

            # Clear doc
            self.doc_display.config(state=tk.NORMAL)
            self.doc_display.delete("1.0", tk.END)
            self.doc_display.config(state=tk.DISABLED)

    def start(self):
        self.root.mainloop()

    def _on_skip_keyword(self):
        self.update_status(" Keyword skipped", "goldenrod")
        self.core.skip_keyword = True
        self.core.continue_event.set()

        # ✅ Visual log entry
        if self.core.failed_keyword:
            self._update_failure_display(
                f"Keyword skipped by user.\nName: {self.core.failed_keyword.name}",
                f"[{self.core.current_test}] Skip Keyword",
                "pass"
            )

    def log_keyword_event(self, action, name, args=None, status="pending", message=""):
        if status.lower() == "pending":
            return
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {"start": "➡", "end": "⬅", "fail": "❌", "pass": "✅", "skip": "⏭️", "pending": "🕓"}

        tag = {"PASS": "pass", "FAIL": "fail", "SKIP": "pending"}.get(status.upper(), "pending")
        icon = icons.get(action, "📝")

        # Format args
        args_lines = ""
        if args:
            for i, arg in enumerate(args):
                args_lines += f"    Arg{i + 1}: {arg}\n"

        # Format message
        msg_block = f"      {message}\n" if message else ""

        # Compose final log block
        full_text = (
            f"[{timestamp}] {icon} {name}  [{status.upper()}]\n"
            f"{args_lines}"
            f"{msg_block}"
            f"{'-' * 60}\n"
        )

        self.failure_text.config(state=tk.NORMAL)
        self.failure_text.insert(tk.END, f"[{timestamp}] {icon} {name}  [{status.upper()}]\n", ("header", tag))
        self.failure_text.insert(tk.END, args_lines, tag)
        if msg_block:
            self.failure_text.insert(tk.END, msg_block, tag)
        self.failure_text.insert(tk.END, f"{'-' * 60}\n", tag)
        self.failure_text.see(tk.END)
        self.failure_text.config(state=tk.DISABLED)

    def _setup_variable_tab(self):
        from tkinter import StringVar

        # === Layout using grid instead of mix of pack/grid ===
        self.var_tab.columnconfigure(0, weight=1)
        self.var_tab.rowconfigure(1, weight=1)

        # --- Top Bar: Search + Refresh ---
        control_frame = tk.Frame(self.var_tab)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        control_frame.columnconfigure(1, weight=1)

        tk.Label(control_frame, text="Search:").grid(row=0, column=0, sticky="w")
        self.var_search_var = StringVar()
        search_entry = tk.Entry(control_frame, textvariable=self.var_search_var, width=30)
        search_entry.grid(row=0, column=1, sticky="ew", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self._refresh_variable_view())

        tk.Button(control_frame, text=" Refresh", command=self._refresh_variable_view).grid(row=0, column=2)

        # --- Treeview for Variables ---
        self.variable_tree = ttk.Treeview(self.var_tab)
        self.variable_tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.variable_tree["columns"] = ("value", "type")
        self.variable_tree.heading("#0", text="Variable")
        self.variable_tree.heading("value", text="Value")
        self.variable_tree.heading("type", text="Type")
        self.variable_tree.column("value", width=350)
        self.variable_tree.column("type", width=100)
        self.variable_tree.bind("<<TreeviewSelect>>", self._on_variable_select)

        # --- Editor Section ---
        editor = tk.LabelFrame(self.var_tab, text="Create or Update Variable")
        editor.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        editor.columnconfigure(1, weight=1)

        tk.Label(editor, text="Name:").grid(row=0, column=0, padx=5, sticky="e")
        self.var_name_var = StringVar()
        self.var_name_entry = tk.Entry(editor, textvariable=self.var_name_var, width=40)
        self.var_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(editor, text="Note: No need to include ${}, it will be added automatically.", fg="gray",
                 font=("Segoe UI", 9)).grid(row=1, column=1, sticky="w", padx=5, pady=(0, 5))

        tk.Label(editor, text="Value:").grid(row=2, column=0, padx=5, sticky="e")
        self.var_value_var = StringVar()
        self.var_value_entry = tk.Entry(editor, textvariable=self.var_value_var, width=60)
        self.var_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(editor, text="Set Variable", command=self._set_variable_from_editor).grid(
            row=2, column=2, padx=10)

    def _refresh_variable_view(self):
        from robot.libraries.BuiltIn import BuiltIn
        search = self.var_search_var.get().lower()
        self.variable_tree.delete(*self.variable_tree.get_children())

        try:
            all_vars = BuiltIn().get_variables()

            for name, value in sorted(all_vars.items()):
                name_str = str(name)
                value_str = str(value)
                vtype = type(value).__name__

                if search and (search not in name_str.lower() and search not in value_str.lower()):
                    continue

                display_value = value_str[:100] + "..." if len(value_str) > 100 else value_str
                self.variable_tree.insert("", "end", text=name_str, values=(display_value, vtype))

        except Exception as e:
            self._update_failure_display(f"Variable load failed: {e}", "[Variables]", "fail")

    def _on_variable_select(self, event):
        selected = self.variable_tree.selection()
        if not selected:
            return
        item = selected[0]
        name = self.variable_tree.item(item, "text")
        value = self.variable_tree.set(item, "value")

        self.var_name_var.set(name)
        self.var_value_var.set(value)

    def _set_variable_from_editor(self):
        from robot.libraries.BuiltIn import BuiltIn
        name = self.var_name_var.get().strip()
        value = self.var_value_var.get().strip()

        if not name.startswith("${"):
            name = "${" + name.strip("${}") + "}"  # auto-wrap

        try:
            BuiltIn().set_test_variable(name, value)

            # ✅ Correct logging format — avoid retry/keyword confusion
            self._update_failure_display(
                text=f"Set variable: {name} = {value}",
                prefix="[Variables]",
                status="pass",
                keyword_name="Set Variable",
                args=[name, value]
            )

            self._refresh_variable_view()
            self.var_name_var.set(name)
            self.var_value_var.set("")
        except Exception as e:
            self._update_failure_display(
                text=f" Failed to set variable {name}: {e}",
                prefix="[Variables]",
                status="fail",
                keyword_name="Set Variable",
                args=[name, value]
            )

    def log_suite_start(self, data):
        log_suite_start(self, data)

    def log_suite_end(self, data, result):
        log_suite_end(self, data, result)

    def log_test_start(self, data):
        log_test_start(self, data)

    def log_test_end(self, data, result):
        log_test_end(self, data, result)

    def safe_close(self):
        try:
            self.root.after(0, self.root.quit)
        except Exception as e:
             logging.warning(f"GUI close failed: {e}")

    def schedule_variable_refresh(self, delay_ms=300):
        if not hasattr(self, "_variable_refresh_scheduled") or not self._variable_refresh_scheduled:
            self._variable_refresh_scheduled = True
            self.root.after(delay_ms, self._perform_variable_refresh)

    def _perform_variable_refresh(self):
        self._variable_refresh_scheduled = False
        try:
            self._refresh_variable_view()
        except Exception as e:
            import logging
            logging.warning(f"Variable refresh failed: {e}")

    from robot.libraries.BuiltIn import BuiltIn

    def load_libraries_and_keywords(self):
        try:
            builtin = BuiltIn()
            lib_names = builtin.get_library_instance_names()
            self.loaded_libraries = {}

            for name in lib_names:
                try:
                    instance = builtin.get_library_instance(name)
                    if instance:
                        self.loaded_libraries[name] = instance
                except Exception as e:
                    print(f"[Debugger GUI] Could not load library '{name}': {e}")

            # Populate the library dropdown
            self.library_dropdown["values"] = list(self.loaded_libraries.keys())
            if self.loaded_libraries:
                self.library_dropdown.current(0)
                self.update_keyword_dropdown()

        except Exception as e:
            print(f"[Debugger GUI] Failed to fetch libraries: {e}")

    def update_keyword_dropdown(self, *_):
        selected_lib = self.library_dropdown.get()
        instance = self.loaded_libraries.get(selected_lib)

        if not instance:
            self.keyword_dropdown["values"] = []
            return

        keyword_names = []
        try:
            keyword_names = instance.get_keyword_names()
        except Exception as e:
            print(f"[Debugger GUI] Failed to get keywords for {selected_lib}: {e}")

        self.keyword_dropdown["values"] = keyword_names
        if keyword_names:
            self.keyword_dropdown.current(0)
