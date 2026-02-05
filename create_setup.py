import os

# Base project structure
FOLDERS = [
    "data/raw",
    "data/processed",
    "data/samples",
    "notebooks",
    "src/config",
    "src/ingestion",
    "src/preprocessing",
    "src/features",
    "src/models",
    "src/evaluation",
    "src/services",
    "src/utils",
    "tests",
    "docs"
]

FILES = [
    "src/__init__.py",
    "src/config/settings.py",
    "src/ingestion/load_data.py",
    "src/preprocessing/text_cleaner.py",
    "src/features/feature_builder.py",
    "src/models/category_classifier.py",
    "src/models/sentiment_model.py",
    "src/models/escalation_model.py",
    "src/models/sla_predictor.py",
    "src/evaluation/metrics.py",
    "src/services/inference_service.py",
    "src/utils/logger.py",
    "docs/r_and_d_notes.md",
    "docs/architecture.md",
    "docs/api_design.md",
    "main.py",
    "README.md"
]


def create_folders():
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)
        print(f" Created folder: {folder}")


def create_files():
    for file in FILES:
        if not os.path.exists(file):
            with open(file, "w") as f:
                pass
            print(f" Created file: {file}")
        else:
            print(f" File already exists: {file}")


def main():
    print(" Setting up AI-Driven Customer Support Ticketing System structure...\n")
    create_folders()
    create_files()
    print("\n Project structure setup completed successfully!")


if __name__ == "__main__":
    main()
