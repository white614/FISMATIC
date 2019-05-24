import glob
import os.path
import sys
from .docx_parser import DocxParser
from . import similarity


def report(outfile, control_set):
    implementations_by_id = control_set.get_implementations_by_id()

    num_controls = control_set.num_controls()
    num_implementations = control_set.num_implementations()
    print("Parsed {} controls".format(num_controls))
    print("{} total words in the controls.".format(control_set.num_words()))
    print(
        "Comparing {} narratives from {} controls".format(
            num_implementations, num_controls
        )
    )
    print(
        "{} identical narratives found".format(
            control_set.num_identical_implementations()
        )
    )

    diffs = similarity.generate_diffs_with_labels(implementations_by_id)
    similarity.write_matrix(diffs, filename=outfile)

    very_similar = similarity.similar_controls(diffs)
    similarity.print_similarity(very_similar)


def run(input_path):
    files = glob.glob(input_path)
    if not files:
        print("No files found matching the input path.", file=sys.stderr)

    os.makedirs("out", exist_ok=True)
    for input_file in files:
        print("---------------\nParsing {} ...".format(input_file))
        parser = DocxParser(input_file)
        control_set = parser.get_control_set()
        outfile = os.path.join("out", input_file.replace(".docx", ".csv"))
        report(outfile, control_set)
