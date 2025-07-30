# fastapi-bootstrapper

A modern **CLI tool** for instantly scaffolding production-ready FastAPI backend projects—with support for LLM (Large Language Model) integrations like OpenAI, Claude, Mistral, and Gemini.

---

## 🚀 Features

- **Interactive CLI wizard**: Walks you through naming, location, project type, logging, and requirements.
- **LLM-ready**: Instantly add stub integrations for OpenAI, Claude, Mistral, Gemini (auto-includes sample code and dependencies).
- **Custom structure**: Sets up all best-practice folders and main files—no `backend/` nesting, everything is organized at the top level.
- **Virtual environment**: Creates a fresh virtualenv for you.
- **Requirements**: Installs your dependencies; warns gracefully if any fail.
- **Logging**: Add (or skip) ready-to-use concurrent logging support.
- **Clean code**: Files are filled with high-quality Python boilerplate so you can get started right away.

---

## 📦 Installation

### From PyPI

```bash
pip install fastapi-bootstrapper
```

---

## 🛠️ Usage

Run the following in your terminal:

```bash
fastapi-bootstrap
```

The CLI wizard will ask you:

* **Project name** (e.g. `awesome-backend`)
* **Project location** (any path; leave blank for current directory)
* **Project type**:

  * Normal FastAPI
  * LLM FastAPI
  * Simple FastAPI
* **Enable logging?**
* **Extra requirements?** (comma separated, e.g. `sqlalchemy, asyncpg`)
* You’ll see a summary. Hit Enter to confirm.

After it finishes, your new project will look like this:

```
myproject/
  app/
    api/
    core/
      config/
      logs/         # only if you selected logging
      services/
        llm/        # only for LLM projects
      integrations/
      db/
    models/
  main.py
  requirements.txt
  README.md
  .gitignore
  venv/
```

---

## 🧑‍💻 Example: Quickstart

```bash
fastapi-bootstrap
```

```
Enter project name: my-awesome-api
Enter full path where you want to create the project (leave blank for current directory):
Select project type:
1. normal fastapi
2. llm fastapi
3. simple fastapi
Enter option: 2
Enable logging? [y/n]: y
List extra requirements (comma separated, blank for none): sqlalchemy, python-dotenv
--- Summary ---
project_name: my-awesome-api
project_location: /your/path
project_type: llm fastapi
logging: True
requirements: ['sqlalchemy', 'python-dotenv']
Path: /your/path/my-awesome-api
--------------------
Press Enter to confirm and create the project...
```

---

## 🦾 What’s Included

* Full FastAPI project tree (modular and ready for production)
* `.gitignore`, `README.md`, `requirements.txt` generated
* Virtualenv set up at `venv/`
* For **LLM FastAPI**:

  * All code stubs for OpenAI, Claude, Mistral, Gemini in `app/core/services/llm/`
* Logging support with rotating file handler (if enabled)
* Auto-installed dependencies (with failure notice if any package fails)

---


## ✍️ Author

Chaithanya K
[cchaithanya83@gmail.com](mailto:cchaithanya83@gmail.com)

---

## 🧩 Contributing

PRs and feature requests welcome!

---

## 💡 Tips

* Edit `requirements.txt` and run `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows) to enter your environment.
* Run `python main.py` or `uvicorn main:app --reload` to start your FastAPI server.
* For LLM features, add your API keys in an `.env` file as required.

---

**Happy coding! 🚀**


