from pathlib import Path
import subprocess


SRC_ROOT = Path(__file__).parent

if __name__ == "__main__":
    startup_moudles = [
        "index",
        "echarts",
    ]

    for module_name in startup_moudles:
        module_root = SRC_ROOT / module_name
        module_main = module_root / "main.py"

        print(f"▶️ Running {module_main} ...")

        # uv run main.py
        subprocess.run(["uv", "run", "main.py"], cwd=module_root, check=True)
