from pathlib import Path
import runpy


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "models" / "classifier" / "train_classifier.py"

runpy.run_path(SCRIPT_PATH, run_name="__main__")
