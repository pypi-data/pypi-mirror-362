import sys
import argparse
import os
import json
import base64
import io

import requests
import pandas as pd

# ← baked-in Cloud Run endpoint:
ENDPOINT = "https://speak2py-service-602634266479.us-central1.run.app/run"

def run_remote(command: str):
    """Send the command to your Speak2Py HTTP service and return its JSON payload."""
    resp = requests.post(
        ENDPOINT,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"command": command}),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(
        prog="speak2py",
        description="Run an English‐style pandas command via the hosted Speak2Py service."
    )
    parser.add_argument(
        "command",
        help='The English‐style command in quotes, e.g. "read file \'data.csv\' and head 5"'
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="If the result is a DataFrame, print it; if it’s a plot, save to PNG (or --out)."
    )
    parser.add_argument(
        "--out",
        help="When used with --show, write DataFrame (as CSV) or figure (as PNG) to this file."
    )
    args = parser.parse_args()

    payload = run_remote(args.command)
    typ = payload.get("type")

    # 1) DataFrame result
    if typ == "dataframe":
        df = pd.DataFrame(payload["data"])
        if args.show:
            if args.out:
                # write CSV
                df.to_csv(args.out, index=False)
                print(f"Saved table to {args.out}")
            else:
                print(df.to_string(index=False))
        # else: silent
        return

    # 2) Plot result (base64-encoded PNG)
    if typ == "plot":
        img_data = base64.b64decode(payload["data"])
        if args.show:
            out_path = args.out or "plot.png"
            with open(out_path, "wb") as f:
                f.write(img_data)
            print(f"Saved plot to {out_path}")
        return

    # 3) Unknown
    print(f"Error: unexpected response type: {typ}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
