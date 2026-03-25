# MLOps Task 0

This project is a simple batch pipeline built using Python.  
The goal was to simulate a small MLOps workflow with config-based execution, logging, and Docker support.

---

## What this project does

- Reads configuration from a YAML file
- Loads a CSV dataset (OHLCV data)
- Calculates rolling mean on the `close` column
- Generates a signal:
  - 1 → if close > rolling mean
  - 0 → otherwise
- Outputs metrics in JSON format
- Logs the entire run

---

## Files in the project

- `run.py` → main script  
- `config.yaml` → configuration (seed, window, version)  
- `data.csv` → input dataset  
- `requirements.txt` → dependencies  
- `Dockerfile` → for container execution  
- `metrics.json` → output file  
- `run.log` → logs  

---

## How to run locally

First install dependencies:

```bash
pip install -r requirements.txt