from tkinter import scrolledtext, messagebox
from datetime import datetime
import threading
from functools import wraps
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
        DEBUGGER_VERSION = "0.3.1"
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

        footer_frame = ttk.Frame(self.root)
        footer_frame.grid(row=99, column=0, columnspan=10, sticky="ew", pady=(10, 0))  # bottom row, full width

        version_label = ttk.Label(
            footer_frame,
            text=f"Version: {DEBUGGER_VERSION}",
            font=("Segoe UI", 8),  # subtle small font
            foreground="#666666"  # gray text for subtle look
        )
        version_label.pack(side="right", padx=10, pady=2)
        # Color tags for styled log output
        # self.failure_text.tag_config("fail", foreground="red")
        # self.failure_text.tag_config("pass", foreground="green")
        # self.failure_text.tag_config("pending", foreground="gray")

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
        self.sub_tabs.add(self.retry_tab, text="Retry Failed Keyword")
        self.var_tab = tk.Frame(self.sub_tabs)
        self.sub_tabs.add(self.var_tab, text="Variable Inspector")
        self.sub_tabs.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self._setup_variable_tab()
        self._setup_retry_tab()



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



    @_thread_safe
    def show_failure(self, suite, test, keyword, message, args, call_stack=None):
        timestamp = datetime.now().strftime("%H:%M:%S")

        # 🧱 Build call stack display
        if call_stack:
            stack_lines = ["  Call Stack:"]
            for depth, kw in enumerate(call_stack):
                indent = "    " * depth
                kw_name = getattr(kw, "name", "UNKNOWN")
                kw_args = getattr(kw, "args", [])
                args_preview = ", ".join(str(a) for a in kw_args) if kw_args else ""
                stack_lines.append(f"{indent}↳ {kw_name}({args_preview})")
                # args_preview = ", ".join(str(a) for a in kw.get("args", [])) if kw.get("args") else ""
                # stack_lines.append(f"{indent}↳ {kw.get('name')}({args_preview})")
            stack_text = "\n".join(stack_lines)
        else:
            stack_text = "  Call Stack: [not captured]"

        # 📝 Full message with stack
        full_text = (
            f"[{timestamp}] ❗ TEST FAILURE\n"
            f"  Test Name : {test}\n"
            f"  Keyword   : {keyword}\n"
            f"  Message   : {message.strip()}\n"
            f"{stack_text}\n"
            f"{'-' * 60}\n"
        )

        # Insert into text area
        self.failure_text.config(state=tk.NORMAL)
        self.failure_text.insert(tk.END, full_text)
        self.failure_text.see(tk.END)
        self.failure_text.config(state=tk.DISABLED)

        self.kw_name_var.set(keyword)

        # ✅ Resolve variables like ${locator}
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

