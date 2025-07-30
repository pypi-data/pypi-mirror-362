import subprocess
import tempfile
import os
from pyngrok import ngrok
import getpass
import time
import shutil

def clone_repo(repo_url, dest):
    print("Cloning repo...")
    subprocess.run(["git", "--version"])
    subprocess.run(["git", "clone", repo_url, dest], check=True)

def create_virtualenv(venv_dir):
    print("Creating virtual environment...")
    subprocess.run(["python", "-m", "venv", venv_dir], check=True)

def get_venv_executables(venv_dir):
    pip_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    python_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")
    return pip_executable, python_executable

def install_requirements(pip_executable):
    print("Installing requirements...")
    if os.path.exists("requirements.txt"):
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"], check=True)
    subprocess.run([pip_executable, "install", "grpcio", "grpcio-tools", "pyngrok"], check=True)

def setup_repo(repo_url, dest):
    clone_repo(repo_url, dest)
    os.chdir(dest)
    venv_dir = os.path.join(os.getcwd(), ".venv")
    create_virtualenv(venv_dir)
    pip_executable, python_executable = get_venv_executables(venv_dir)
    install_requirements(pip_executable)
    return python_executable

def launch_server(repo_url, entry, port):
    temp_dir = tempfile.mkdtemp()
    try:
        python = setup_repo(repo_url, temp_dir)

        auth_token = getpass.getpass("ngrok Auth Token: ")
        ngrok.set_auth_token(auth_token)
        
        tunnel = ngrok.connect(str(port), "tcp")
        public_url = tunnel.public_url
        assert public_url
        print(f"Server running on {public_url}")

        proc = subprocess.Popen([python, entry])
        try:
            proc.wait()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            ngrok.disconnect(public_url)
            proc.terminate()
            proc.wait()
    finally:
        # Wait a bit to ensure all handles are released
        for _ in range(5):
            try:
                shutil.rmtree(temp_dir)
                break
            except PermissionError:
                time.sleep(1)