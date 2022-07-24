#!/usr/bin/python3

import argparse
import json
import os
import subprocess

APP_DESCRIPTION = \
    """
A basic utility to extract all chapters from any media format supported by ffmpeg
"""

CWD = os.path.abspath(os.path.curdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser.add_argument("-i", "--input-file", required=True, metavar="FILE",
                        help="Input file to be split")
    parser.add_argument("-o", "--output-dir", metavar="DIR", default=CWD,
                        help="Output directory. Defaults to current directory")
    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    if os.path.isfile(args.output_dir):
        raise Exception("Output path cannot be a file")
    if not os.path.exists(args.input_file):
        raise Exception("Input path does not exist")
    if not os.path.isfile(args.input_file):
        raise Exception("Input path is not a file")
    inputFileExtension = os.path.basename(args.input_file.split(".")[-1])
    res = subprocess.run(["ffprobe", "-i", args.input_file,
                         "-print_format", "json", "-show_chapters"],
                         capture_output=True, text=True, check=True)
    chapters = json.loads(res.stdout)["chapters"]
    for chapter in chapters:
        subprocess.run(
            [
                "ffmpeg", "-i", args.input_file,
                "-ss", chapter["start_time"],
                "-to", chapter["end_time"],
                "-c", "copy",
                os.path.join(args.output_dir,
                             chapter["tags"]["title"] + "." + inputFileExtension)
            ],
            check=True)
