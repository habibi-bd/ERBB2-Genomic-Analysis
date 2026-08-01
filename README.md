# ERBB2 Genomic Analysis

Hey there! This is the codebase for my research project looking into genomic datasets, molecular modeling, and classification pipelines. 

### What's in here?
* **`data_collection/`**: Scripts and utilities for pulling and prepping raw genomic and chemical data.
* **`linux/`**: Shell scripts and environment configuration tools for running workflows.
* **`paper_draft/`**: Working notes, drafts, and documentation for the research paper.
* **`silico/`**: In silico analysis pipeline components and modeling scripts.
* **`workspace/`**: Jupyter notebooks and experimental scripts used during development.

### Project Workflow
1. **Data Gathering & Prep:** Pulls compound data from ChEMBL and PubChem, then cleans and standardizes everything.
2. **Feature Modeling & Screening:** Converts molecular structures into formats for machine learning models, which are then used to virtually screen large compound libraries.
3. **Docking & Toxicity:** Prepares the HER2 (ERBB2) protein target, performs molecular docking on top candidate compounds, and checks their potential human organ toxicity profiles.

### Getting Started
If you want to spin this up locally:
1. Clone the repository.
2. Set up and activate a local Python virtual environment.
3. Install the required dependencies and you're good to go!

<img width="940" height="446" alt="Workflow_ERBB2" src="https://github.com/user-attachments/assets/799cdb84-1042-4c9a-8930-00d392a44f06" />
