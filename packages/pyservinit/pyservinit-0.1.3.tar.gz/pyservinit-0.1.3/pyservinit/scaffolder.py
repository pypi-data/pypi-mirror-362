import sys
from pathlib import Path
import importlib.resources as pkg_resources
import pyservinit.templates

BASE_DIRS = [
    "data/request_data",
    "data/sample_data",
    "src/api",
    "src/config",
    "src/core",
    "src/mapper_classes",
    "src/misc",
    "src/tests",
    "src/utils",
]

EMPTY_FILES = [
    "docker-compose.yaml",
    "Dockerfile",
    "requirements.txt",
    "src/api/__init__.py",
    "src/api/api.py",
    "src/config/__init__.py",
    "src/core/__init__.py",
    "src/main.py",
    "src/mapper_classes/__init__.py",
    "src/mapper_classes/input_classes.py",
    "src/mapper_classes/output_classes.py",
    "src/misc/__init__.py",
    "src/tests/__init__.py",
    "src/utils/__init__.py",
    "src/utils/utils.py"
]

DESTINATION_MAP: dict[str, str] = {
    "push.sh.template": "push.sh",
    "constants.py.template": "src/config/constants.py",
    "api.py.template": "src/api/api.py",
    "input_classes.py.template": "src/mapper_classes/input_classes.py",
    "output_classes.py.template": "src/mapper_classes/output_classes.py",
    "main.py.template": "src/main.py",
    "docker-compose.yaml.template": "docker-compose.yaml",
    "Dockerfile.template": "Dockerfile",
    "requirements.txt.template": "requirements.txt",
    "utils.py.template": "src/utils/utils.py"
}

def create_dirs(base_path: Path) -> None:
    for dir_path in BASE_DIRS:
        (base_path / dir_path).mkdir(parents=True, exist_ok=True)


def create_empty_files(base_path: Path) -> None:
    for file_path in EMPTY_FILES:
        (base_path / file_path).touch()


def copy_template_files(base_path: Path) -> None:
    for resource in pkg_resources.contents(pyservinit.templates):
        if not resource.endswith(".template"):
            continue

        try:
            content = pkg_resources.read_text(pyservinit.templates, resource)
            print(resource)
        except FileNotFoundError:
            print(f"❌ Missing template: {resource}")
            continue

        if resource in DESTINATION_MAP:
            dest_path = base_path / DESTINATION_MAP[resource]
        else:
            # Guess destination: strip `.template` and place in `src/misc/`
            filename = resource.replace(".template", "")
            dest_path = base_path / f"src/misc/{filename}"

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(content)

        # Make shell scripts executable
        if dest_path.suffix == ".sh":
            dest_path.chmod(dest_path.stat().st_mode | 0o111)


def main() -> None:
    if len(sys.argv) < 2:
        print("❌ Project name not provided.\nUsage: pyservinit <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]
    base_path = Path.cwd() / project_name

    if base_path.exists():
        print(f"❌ Directory '{project_name}' already exists.")
        sys.exit(1)

    print(f"📁 Creating project: {project_name}")
    base_path.mkdir(parents=True)

    create_dirs(base_path)
    create_empty_files(base_path)
    copy_template_files(base_path)

    print("✅ Project structure created successfully.")


if __name__ == "__main__":
    main()
