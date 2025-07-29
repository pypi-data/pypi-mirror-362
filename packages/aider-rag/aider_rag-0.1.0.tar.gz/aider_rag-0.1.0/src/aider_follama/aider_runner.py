import subprocess
import os

def run_aider(file_path, prompt, model="codeqwen", https_url="https://localhost:443"):
    os.environ["AIDER_MODEL"] = model
    os.environ["AIDER_OLLAMA_BASE_URL"] = https_url
    os.environ["AIDER_ALLOW_UNVERIFIED_SSL"] = "true"

    cmd = [
        "aider",
        file_path,
        "--yes",
        "--message", prompt
    ]
    subprocess.run(cmd, check=True)
