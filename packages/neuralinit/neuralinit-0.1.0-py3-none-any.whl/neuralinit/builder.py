# neuralinit/builder.py

import os
import tkinter as tk
from tkinter import simpledialog, filedialog

def create_project_structure(base_dir, project_name):
    project_path = os.path.join(base_dir, project_name)
    os.makedirs(project_path, exist_ok=True)

    folders = [
        "data/raw", "data/processed", "data/external", "data/interim",
        "models/checkpoints",
        "results/figures", "results/metrics", "results/papers",
        "scripts/utils",
        "config",
        "exploratory"
    ]

    files = [
        "01_data_preprocessing.ipynb",
        "02_feature_engineering.ipynb",
        "03_model_training.ipynb",
        "04_evaluation_visuals.ipynb",
        "config/config.yaml",
        "config/params.json",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]

    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)

    for file in files:
        open(os.path.join(project_path, file), 'a').close()

    print(f"✅ Project '{project_name}' created at: {project_path}")

def main():
    root = tk.Tk()
    root.withdraw()

    project_name = simpledialog.askstring("Project Name", "Enter project folder name:")
    if not project_name:
        print("Cancelled.")
        return

    base_dir = filedialog.askdirectory(title="Select Base Directory for Project")
    if not base_dir:
        print("Cancelled.")
        return

    create_project_structure(base_dir, project_name)

if __name__ == "__main__":
    main()