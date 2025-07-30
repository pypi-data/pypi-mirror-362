import pathlib


def load_metadata(metadata_path):

    if pathlib.Path(metadata_path).exists():
        metadata = {}
        with open(metadata_path, 'r') as file:
            for line_number, line in enumerate(file, 1):
                assert len(line.split("=")) == 2
                k = line.split("=")[0]
                v = line.split("=")[-1]
                metadata.setdefault(k, v)
        return metadata

