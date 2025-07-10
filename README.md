# 🐚 Mini Shell in Python

This project is a simple and functional implementation of a **mini command-line interpreter (shell)** developed in pure Python. It supports multiple built-in commands, parallel execution, output redirection, and more!

---

## ✨ Features

- 📁 **`cd` command**: change directories.
- 📍 **`pwd` command**: print current directory.
- 📂 **`ls` command**: list files and directories.
- 📄 **`cat` command**: print file contents.
- 📢 **`echo` command**: display messages.
- 💻 **External command execution** (e.g., `python`, `ping`, `gcc`, etc.).
- 🧲 **Output redirection** with `>` to write results to files.
- ⛓️ **Sequential execution** with `;` and **parallel execution** with `&`.

---

## ⚙️ How it works

This shell simulates the behavior of Unix/Linux terminals using:

- `os.fork()` (on Unix systems) and `multiprocessing.Process()` (on Windows) to create **child processes**.
- `subprocess.run()` and `os.execvp()` to execute external commands.
- Direct file manipulation using `os.open()` and `os.dup2()` for output redirection.
- `;` and `&` as separators for sequential and parallel execution.

### 🔀 Example usage:

```bash
pwd
cd folder ; ls
echo "Log message" > log.txt
cat log.txt
ls & echo "Running in parallel"
```

---

## ▶️ How to use

### 🔧 Requirements

- Python 3.8+
- Compatible with **Windows**

### 🚀 Running the Shell

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mini-shell-python.git
   cd mini-shell-python
   ```

2. Run the shell:
   ```bash
   python "Mini Shell.py"
   ```

3. Start typing commands! For example:
   ```bash
   pwd
   ls
   cd subfolder ; ls
   echo "Created file" > output.txt
   ```
