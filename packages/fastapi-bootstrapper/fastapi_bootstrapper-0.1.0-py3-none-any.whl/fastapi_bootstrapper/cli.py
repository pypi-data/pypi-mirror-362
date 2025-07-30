import os
import subprocess
import sys
from pathlib import Path

PROJECT_TYPES = {
    "1": "normal fastapi",
    "2": "llm fastapi",
    "3": "simple fastapi",
}

LLM_FUNCTIONS = {
    "openai.py": '''
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key =os.getenv("OPEN_AI_KEY", "")
def openai_llm(prompt, model="gpt-3.5-turbo", temperature=0, max_tokens=800):
    """
    Calls OpenAI ChatCompletion API with a prompt.
    Returns model response as string.
    """
    chat_response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return chat_response.choices[0].message["content"]
''',

    "claude.py": '''
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY", "")
def claude_llm(user_prompt, sys_prompt=None, model="claude-3-haiku-20240307", max_tokens=1024):
    """
    Calls the Claude LLM API with user and optional system prompt.
    Returns response as string.
    """
    client = anthropic.Anthropic(api_key=api_key)
    messages = []
    system = sys_prompt if sys_prompt else None
    messages.append({"role": "user", "content": user_prompt})

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages
    )
    if not response.content:
        raise ValueError("No content returned from Claude API")
    return "".join(block.text for block in response.content if block.type == "text")
''',

    "mistral.py": '''
import os
from mistralai import Mistral
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("MISTRAL_API",'')

model = "mistral-large-2411"
client = Mistral(api_key=api_key)
def mistral_llm(user_prompt, sys_prompt=None, model="mistral-large-2402", temperature=0, max_tokens=800):
    """
    Calls the Mistral LLM API with user and optional system prompt.
    Returns model response as string.
    """
    messages = []
    if sys_prompt:
        messages.append({"role": "system", "content": sys_prompt})
    messages.append({"role": "user", "content": user_prompt})
    chat_response = client.chat.complete(
        temperature=temperature,
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    if not chat_response.choices:
        raise ValueError("No choices returned from Mistral API")
    return chat_response.choices[0].message.content
''',

    "gemini.py": '''
from google import genai

def gemini_llm(prompt, model="gemini-2.5-flash"):
    """
    Calls the Gemini API with a prompt.
    Returns model response as string.
    """
    client = genai.Client(api_key="YOUR_API_KEY")
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text if hasattr(response, "text") else str(response)
'''
}


LOGGER_PY = '''
import logging
from pathlib import Path
from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
import os
from app.core.config import APP_STOARAGE_LOCATION

LOG_DIR = str(Path(APP_STOARAGE_LOCATION) / "logs")
LOG_FILE = "app.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)
MAX_LOG_SIZE = 50 * 1024 * 1024  # 50 MB
BACKUP_COUNT = 5

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"
        )
        file_handler = RotatingFileHandler(
            filename=LOG_PATH,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger
'''

SETTINGS_PY = '''
APP_STOARAGE_LOCATION = "."
DATABASE_URL = "sqlite:///./test.db"
'''

README_MD = '''# {project_name}

Project scaffolded with Python Project Bootstrapper.
'''

ROUTES_PY = '''from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {{"message": "API Root"}}
'''

MAIN_PY = '''from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

MODEL_PY = '''from pydantic import BaseModel

class ExampleModel(BaseModel):
    name: str
    age: int
'''

SCHEMA_PY = '''# SQLAlchemy or Pydantic schemas go here
'''

GITIGNORE = '''
env/
venv
__pycache__/
*.pyc
*.pyo
*.pyd
*.sqlite3
*.db
.DS_Store
*.env
'''

def prompt_choice(prompt, options):
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")
    while True:
        choice = input("Enter option: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid option, try again.")

def yes_no(prompt):
    while True:
        ans = input(f"{prompt} [y/n]: ").lower().strip()
        if ans in ["y", "yes"]: return True
        if ans in ["n", "no"]: return False
        print("Please type 'y' or 'n'.")

def print_summary(info):
    print("\n--- Summary ---")
    for k, v in info.items():
        print(f"{k}: {v}")
    print(f"Path: {info['project_location']}/{info['project_name']}")
    print("-" * 20)

def create_file(filepath, content=""):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def create_project(info):
    BASE = Path(info["project_location"]).expanduser().absolute() / info["project_name"]
    errors = []
    # Directory structure (no backend)
    app = BASE / "app"
    api = app / "api"
    core = app / "core"
    config = core / "config"
    logs = core / "logs"
    services = core / "services"
    integrations = core / "integrations"
    db = core / "db"
    models = app / "models"

    # Create directories
    for d in [api, config, logs, services, integrations, models, db]:
        d.mkdir(parents=True, exist_ok=True)

    # API and main FastAPI files
    create_file(api / "__init__.py")
    create_file(api / "routes.py", ROUTES_PY)
    create_file(BASE / "main.py", MAIN_PY)
    create_file(BASE / "README.md", README_MD.format(project_name=info["project_name"]))
    create_file(BASE / ".gitignore", GITIGNORE)
    create_file(BASE / "requirements.txt", "\n".join(["fastapi", "uvicorn"] + info["requirements"]) + "\n")
    create_file(models / "__init__.py")
    create_file(models / "model.py", MODEL_PY)
    create_file(core / "__init__.py")
    create_file(config / "__init__.py")
    create_file(config / "settings.py", SETTINGS_PY)
    create_file(db / "__init__.py")
    create_file(db / "schema.py", SCHEMA_PY)
    create_file(services / "__init__.py")
    create_file(integrations / "__init__.py")

    # Logging
    if info["logging"]:
        create_file(logs / "__init__.py")
        create_file(logs / "logger.py", LOGGER_PY)
    else:
        logs.rmdir()  # Remove logs dir if no logging

    # LLM fastapi project only
    if info["project_type"] == "llm fastapi":
        llm_dir = services / "llm"
        llm_dir.mkdir(parents=True, exist_ok=True)
        for fname, fcontent in LLM_FUNCTIONS.items():
            create_file(llm_dir / fname, fcontent)
    # Virtualenv
    env_dir = BASE / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(env_dir)])

    # Install requirements
    pip_exe = env_dir / "Scripts" / "pip" if os.name == "nt" else env_dir / "bin" / "pip"
    reqs = ["fastapi", "uvicorn"] + info["requirements"]
    if info["logging"]:
        reqs.append("concurrent-log-handler")
    if info["project_type"] == "llm fastapi":
        reqs += ["openai", "anthropic", "google-generativeai", "mistralai"]
    failed_pkgs = []
    for pkg in set(reqs):
        try:
            subprocess.run([str(pip_exe), "install", pkg], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            failed_pkgs.append(pkg)
    return BASE, failed_pkgs

def main():
    print("Python Project Bootstrapper\n")
    project_name = input("Enter project name: ").strip()
    project_location = input("Enter full path where you want to create the project (leave blank for current directory): ").strip()
    if not project_location:
        project_location = str(Path.cwd())
    project_type = prompt_choice("Select project type:", PROJECT_TYPES)
    logging = yes_no("Enable logging?")
    requirements = input("List extra requirements (comma separated, blank for none): ").strip()
    requirements = [r.strip() for r in requirements.split(",") if r.strip()]
    info = {
        "project_name": project_name,
        "project_location": project_location,
        "project_type": project_type,
        "logging": logging,
        "requirements": requirements,
    }
    print_summary(info)
    input("Press Enter to confirm and create the project...")

    base_path, failed = create_project(info)
    print(f"\n✅ Project created at {base_path}")
    if failed:
        print("\nWARNING: Some packages failed to install:")
        for pkg in failed:
            print(" -", pkg)
        print("You may need to install them manually inside your virtualenv.")
    else:
        print("\nAll dependencies installed successfully!")


if __name__ == "__main__":
    main()
