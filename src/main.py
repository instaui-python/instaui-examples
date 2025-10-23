from pathlib import Path
import subprocess
from shared.cmd import parse_offline_flag

SRC_ROOT = Path(__file__).parent

if __name__ == "__main__":
    offline = parse_offline_flag()
    print(f"Offline mode: {offline}")

    startup_moudles = ["index", "echarts", "shiki"]

    for module_name in startup_moudles:
        module_root = SRC_ROOT / module_name
        module_main = module_root / "main.py"

        print(f"▶️ Running {module_main} ...")

        # uv run main.py
        subprocess.run(
            ["uv", "run", "main.py", "--offline" if offline else ""],
            cwd=module_root,
            check=True,
        )
