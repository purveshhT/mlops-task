import argparse
import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import sys


def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        required = ["seed", "window", "version"]
        for key in required:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        return config
    except Exception as e:
        raise ValueError(f"Config error: {str(e)}")


def load_data(input_path):
    try:
        df = pd.read_csv(input_path)

        if df.empty:
            raise ValueError("CSV file is empty")

        if "close" not in df.columns:
            raise ValueError("Missing 'close' column")

        return df
    except FileNotFoundError:
        raise ValueError("Input file not found")
    except Exception as e:
        raise ValueError(f"CSV error: {str(e)}")


def main(args):
    start_time = time.time()

    try:
        setup_logger(args.log_file)
        logging.info("Job started")

        # Load config
        config = load_config(args.config)
        logging.info(f"Config loaded: {config}")

        np.random.seed(config["seed"])

        # Load data
        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        # Rolling mean
        window = config["window"]
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # Drop NaN rows
        df = df.dropna()

        # Signal
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        # Metrics
        rows_processed = len(df)
        signal_rate = df["signal"].mean()
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": config["version"],
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        logging.info(f"Metrics: {metrics}")

        # Write metrics
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        print(json.dumps(metrics, indent=4))
        logging.info("Job completed successfully")

    except Exception as e:
        error_metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_metrics, f, indent=4)

        logging.error(str(e))
        print(json.dumps(error_metrics, indent=4))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()
    main(args)