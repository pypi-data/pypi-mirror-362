"""
CLI Encoding Interface
"""

import argparse
from .chain_layer import encode_pipeline, decode_pipeline

def run_cli():
    parser = argparse.ArgumentParser(description="hanifx CLI Encoder/Decoder")
    parser.add_argument("text", help="Text or file path to encode/decode")
    parser.add_argument("--layers", nargs='+', default=["base64"], help="Encoding layers")
    parser.add_argument("--decode", action="store_true", help="Decode instead of encode")
    args = parser.parse_args()

    from .smart import smart_input
    text = smart_input(args.text)

    if args.decode:
        result = decode_pipeline(text, args.layers)
        print("Decoded:", result)
    else:
        result = encode_pipeline(text, args.layers)
        print("Encoded:", result)
