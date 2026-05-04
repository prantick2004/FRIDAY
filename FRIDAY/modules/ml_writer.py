import sys
import os
sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")

from ai_chat import write_code
from file_manager import create_file, open_file

def write_ml_program(task):
    prompt = f"""
Write complete working Python machine learning code for: {task}
Use scikit-learn or tensorflow.
Include: imports, sample data, preprocessing, train, evaluate, print results.
Return ONLY Python code. No explanation. No markdown.
    """
    code = write_code(prompt)
    filename = task.replace(" ", "_")[:25] + "_ml.py"
    path = create_file(filename, code)
    open_file(path)
    return path