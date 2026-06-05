import os
import subprocess
import sys
import time

CREATE_NEW_CONSOLE = 0x00000010


def main():
    print("==========================================")
    print("       CHABU AI - LAUNCHER")
    print("==========================================")
    print("Starting Voice window + Web dashboard...\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = os.path.join(base_dir, "venv312", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = sys.executable

    main_py = os.path.join(base_dir, "cli_assistant", "main.py")
    app_py = os.path.join(base_dir, "web_assistant", "app.py")

    # Voice must run in a visible console on Windows
    if os.name == "nt":
        subprocess.Popen(
            [python_exe, main_py],
            creationflags=CREATE_NEW_CONSOLE,
            cwd=base_dir,
        )
    else:
        subprocess.Popen([python_exe, main_py], cwd=base_dir)

    time.sleep(2)

    web_process = subprocess.Popen(
        [python_exe, "-m", "streamlit", "run", app_py],
        cwd=base_dir,
    )
    
    # Force open the browser since Streamlit sometimes fails to auto-open when run as a subprocess
    import webbrowser
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

    try:
        web_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        web_process.terminate()


if __name__ == "__main__":
    main()
