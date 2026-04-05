import argparse
import json
import sys
import math
from pymavlink import mavutil

# Parse arguements from CLI
def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert ArduPilot .BIN log to JSON/NDJSON" \
        "If message has binary data, it is expressed in hex format" \
        "If message has \"NaN\" value, it is expressed as \"\""
    )

    parser.add_argument("input", help="Path to .BIN file")
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--types",
        help="Comma-separated message types (e.g. GPS,ATT,IMU)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty JSON (slow, large)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of messages"
    )
    parser.add_argument(
        "--ndjson",
        action="store_true",
        help="NDJSON format instead of classic JSON"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Set up allowed types if any
    allowed_types = None
    if args.types:
        allowed_types = set(t.strip().upper() for t in args.types.split(","))

    # Open out file in write mode if specified
    out = open(args.output, "w") if args.output else sys.stdout

    # Open binary input file
    log = mavutil.mavlink_connection(args.input)

    # Set up counter if user specified --limit
    count = 0

    # If user doesn't set --ndjson parameter, add some roquired syntax for correct JSON
    if not args.ndjson:
        out.write("[\n")

    # Set up variable for identifying the first message
    first = True

    # Parse data from file
    try:
        while True:
            # Receive next block from input file
            msg = log.recv_match(blocking=False)

            # If The whole file is parsed, break the loop
            if msg is None:
                break

            # Get message type
            msg_type = msg.get_type()
            # Apply filters if any
            if allowed_types and msg_type not in allowed_types:
                continue

            # If it is not first entry in the loop, add comma
            if not first:
                out.write(",\n")
            first = False
            
            # Get dict type from message
            data = msg.to_dict()

            # If message has binary data, convert it to hex format
            data = {
                k: v.hex() if isinstance(v, bytes) else v
                for k, v in data.items()
            }

            # If message has "NaN" value, express it as ""
            data = {
                k: "" if isinstance(v, float) and math.isnan(v) else v
                for k, v in data.items()
            }

            # If user specifies --pretty, add indents
            if args.pretty:
                json.dump(data, out, indent=2)
            else:
                json.dump(data, out)

            # Update counter for --limit
            count += 1

            # If user sepcifies --limit, check counter
            if args.limit and count >= args.limit:
                break
            
    finally:
        # If user doesn't specify --ndjson, add some roquired syntax for correct JSON
        if not args.ndjson:
            out.write("\n]\n")
        else:
            out.write("\n")

        # If user specifies, --output, close the file
        if args.output:
            out.close()


if __name__ == "__main__":
    main()