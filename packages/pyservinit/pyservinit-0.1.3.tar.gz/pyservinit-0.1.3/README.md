# 🚀 PyServInit - Project Bootstrapper

`pyservinit` is a Python-based utility script for initializing a backend project with a standardized structure. It creates directories, touches empty boilerplate files, and copies template files into a new project folder.

## 📦 Features

* Creates a structured directory tree for a new project.
* Populates essential files (`Dockerfile`, `docker-compose.yaml`, `main.py`, etc.).
* Loads content from `.template` files bundled in `pyservinit.templates`.
* Automatically sets executable permissions for shell scripts.
* Easy to use via command line.

---

## 📁 Project Structure Created

```
<project-name>/
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── push.sh
├── data/
│   ├── request_data/
│   └── sample_data/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── api.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── constants.py
│   ├── core/
│   │   └── __init__.py
│   ├── main.py
│   ├── mapper_classes/
│   │   ├── __init__.py
│   │   ├── input_classes.py
│   │   └── output_classes.py
│   ├── misc/
│   ├── tests/
│   │   └── __init__.py
│   └── utils/
│       ├── __init__.py
│       └── utils.py
```

---

## 🛠 Usage

```bash
python path/to/pyservinit.py <project-name>
```

### Example:

```bash
python pyservinit.py my-backend-service
```

If `my-backend-service` already exists, the script will abort to prevent overwriting.

---

## 📄 Templates

The script relies on templates stored in `pyservinit.templates` (an importable Python package resource).

Files like these are included:

* `Dockerfile.template`
* `main.py.template`
* `push.sh.template`
* etc.

You can add more `.template` files to the `pyservinit/templates/` directory and either:

* Map them explicitly in `DESTINATION_MAP`
* Or have them default to `src/misc/<template-name>` after removing `.template`

## 🧩 Dependencies

Ensure `pyservinit.templates` is installed or accessible as a Python package.

## 📌 Notes

* It is suitable for backend services in microservice-style architectures or for setting up ML inference services.
* Shell script files (e.g., `push.sh`) are made executable automatically by the script.