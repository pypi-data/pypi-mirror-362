import argparse
import logging
import sys

from loguru import logger

from . import viewer


def main():
    parser = argparse.ArgumentParser(
        prog="lv",
        description="LatentViewer, a 3D interactive image embedding inspector",
    )
    parser.add_argument(
        "-e",
        "--embeddings",
        help="Embeddings file, a CSV file that contains the embbeddings",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--image-archive",
        help="Trajectory image archive (hdf5)",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--filecolumn",
        help="Filename column in the embeddings file",
        default="filename",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Run in debug mode",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-p",
        "--embedding-column-prefix",
        help="Prefix for embedding column names",
        type=str,
        default="emb_dim",
    )
    parser.add_argument(
        "-c",
        "--class-column",
        help="Name of class column",
        type=str,
        default="class",
    )

    args = parser.parse_args()
    viewer.embeddings_file = args.embeddings
    viewer.arrays_file = args.image_archive
    viewer.filecolumn = args.filecolumn
    viewer.emb_dim_prefix = args.embedding_column_prefix
    viewer.classcolumn = args.class_column
    debug = args.debug

    log_level = "INFO"
    if debug is True:
        log_level = "DEBUG"
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    viewer.app.run(debug=debug)


if __name__ == "__main__":
    main()
