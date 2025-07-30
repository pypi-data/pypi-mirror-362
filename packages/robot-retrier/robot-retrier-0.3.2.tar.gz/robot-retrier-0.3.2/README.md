# 🤖 Robot Framework GUI Debugger & Retry Tool

A live **GUI-based debugger** for Robot Framework that intercepts test failures, displays call stacks, and allows users to **retry failed keywords** with edited arguments — all without restarting the test run.

---

## 🥉 Features

- ✅ Opens a GUI at the start of test execution
- ✅ Intercepts keyword failures and allows retry or skip
- ✅ Editable argument fields with validation
- ✅ Live variable viewer / Editor
- ✅ Call stack view with live updates
- ✅ Retry logging with result tagging (`debugger-retried`, `debugger-skipped`)
- ✅ Works in  **listener**  mode
- ✅ Handles `Run Keyword And Ignore Error`, and others
- ✅ Light, standalone — no server or browser needed



## 🚀 Installation

```bash
pip install robot-retrier
```


## 🥪 Usage Options

### ✅ As a Listener

```bash
robot --listener RobotRetrier tests/
```

This hooks directly into Robot's execution and shows the GUI on failure.

Good for manual triggering or environments where listeners aren’t usable.

---

## 🖥️ How It Works

1. At test start, the GUI opens
2. Every keyword is logged to a live stack tree
3. On failure:
   - GUI highlights the failed keyword
   - User can retry with modified arguments or skip it
4. Execution resumes based on user choice
5. Logs and stack remain visible throughout the suite

---


## 🧠 Design Notes

- ✅ Built for **Robot Framework 6.1+**
- ✅ Uses **Listener API v3**
- ✅ Tkinter-based for full offline GUI support
- ❌ Does not depend on Selenium, Appium, or browser-based UIs
- ✅ Supports long-running tests and deep stacks with auto-trimmed logs

---

## ⚙️ Advanced Features

- `Muted Keywords`: Automatically skips retry for wrapped keywords like:
  - `Run Keyword And Ignore Error`
  - `Run Keyword And Return Status`
- `Retry Signature`: Auto-loads expected arguments for any keyword
- `Live Logs`: Auto-scroll and trim old lines to keep UI fast



## 📄 License

MIT License. Use freely with attribution.

---

## 👨‍💻 Author

Made with ❤️ by [Suriya]\
Contributions and feedback welcome!

