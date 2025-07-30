from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import TextIO, Union
from urllib.request import urlretrieve

from Bio import Entrez

from pycirclizely import config


def load_prokaryote_example_file(
    filename: str,
    cache_dir: str | Path | None = None,
    overwrite_cache: bool = False,
) -> Path:
    """Load pycirclize example Genbank or GFF file.

    Load example file from <https://github.com/moshi4/pycirclize-data/>
    and cache file in local directory (Default: `~/.cache/pycirclize/`).

    List of example Genbank or GFF filename:

    - `enterobacteria_phage.[gbk|gff]`
    - `mycoplasma_alvi.[gbk|gff]`
    - `escherichia_coli.[gbk|gff].gz`

    Args:
        filename: Genbank or GFF filename (e.g. `enterobacteria_phage.gff`).
        cache_dir: Output cache directory (Default: `~/.cache/pycirclize/`).
        overwrite_cache: If True, overwrite cache file.
            Assumed to be used when cache file is corrupt.
    """
    # Check specified filename exists or not
    if filename not in config.PROKARYOTE_FILES:
        err_msg = f"{filename=} not found."
        raise ValueError(err_msg)

    # Cache local directory
    if cache_dir is None:
        package_name = __name__.split(".")[0]
        cache_base_dir = Path.home() / ".cache" / package_name
        cache_dir = cache_base_dir / "prokaryote"
        os.makedirs(cache_dir, exist_ok=True)
    else:
        cache_dir = Path(cache_dir)
        if not cache_dir.exists():
            raise ValueError(f"{cache_dir=} not exists.")

    # Download file
    file_url = config.GITHUB_DATA_URL + f"prokaryote/{filename}"
    file_path = cache_dir / filename
    if overwrite_cache or not file_path.exists():
        urlretrieve(file_url, file_path)

    return file_path


def load_eukaryote_example_dataset(
    name: str = "hg38",
    cache_dir: str | Path | None = None,
    overwrite_cache: bool = False,
) -> tuple[Path, Path, list[ChrLink]]:
    """Load pycirclize eukaryote example dataset.

    Load example file from <https://github.com/moshi4/pycirclize-data/>
    and cache file in local directory (Default: `~/.cache/pycirclize/`).

    List of dataset contents (download from UCSC):

    1. Chromosome BED file (e.g. `chr1 0 248956422`)
    2. Cytoband file (e.g. `chr1 0 2300000 p36.33 gneg`)
    3. Chromosome links (e.g. `chr1 1000 4321 chr3 8000 5600`)

    Args:
        name: Dataset name (`hg38`|`hs1`|`mm10`|`mm39`).
        cache_dir: Output cache directory (Default: `~/.cache/pycirclize/`).
        overwrite_cache: If True, overwrite cache dataset.
            Assumed to be used when cache dataset is corrupt.
    """
    # Check specified name dataset exists or not
    if name not in config.EUKARYOTE_DATASET:
        available_dataset = list(config.EUKARYOTE_DATASET.keys())
        raise ValueError(f"{name=} dataset not found.\n{available_dataset=}")

    # Dataset cache local directory
    if cache_dir is None:
        package_name = __name__.split(".")[0]
        cache_base_dir = Path.home() / ".cache" / package_name
        cache_dir = cache_base_dir / "eukaryote" / name
        os.makedirs(cache_dir, exist_ok=True)
    else:
        cache_dir = Path(cache_dir)
        if not cache_dir.exists():
            raise ValueError(f"{cache_dir=} not exists.")

    # Download & cache dataset
    eukaryote_files: list[Path] = []
    chr_links: list[ChrLink] = []
    for filename in config.EUKARYOTE_DATASET[name]:
        file_url = config.GITHUB_DATA_URL + f"eukaryote/{name}/{filename}"
        file_path = cache_dir / filename
        if overwrite_cache or not file_path.exists():
            urlretrieve(file_url, file_path)
        if str(file_path).endswith("link.tsv"):
            chr_links = ChrLink.load(file_path)
        else:
            eukaryote_files.append(file_path)

    return eukaryote_files[0], eukaryote_files[1], chr_links


def load_example_tree_file(filename: str) -> Path:
    """Load example phylogenetic tree file.

    List of example tree filename:

    - `small_example.nwk` (7 species)
    - `medium_example.nwk` (21 species)
    - `large_example.nwk` (190 species)
    - `alphabet.nwk` (26 species)

    Args:
        filename: Target filename.
    """
    example_data_dir = Path(__file__).parent / "example_data" / "trees"
    example_files = example_data_dir.glob("*.nwk")
    available_filenames = [f.name for f in example_files]
    if filename not in available_filenames:
        raise FileNotFoundError(f"{filename=} is invalid.\n{available_filenames=}")
    target_file = example_data_dir / filename
    return target_file


def fetch_genbank_by_accid(
    accid: str,
    gbk_outfile: Union[str, Path, None] = None,
    email: Union[str, None] = None,
) -> TextIO:
    """Fetch genbank text by `Accession ID`.

    Args:
        accid: Accession ID.
        gbk_outfile: If file path is set, write fetch data to file.
        email: Email address to notify download limitation (Required for bulk download).
    """
    # Handle email assignment
    setattr(Entrez, "email", email if email is not None else "")

    # Fetch data from NCBI - use TextIO as the variable type
    gbk_fetch_data: TextIO = Entrez.efetch(
        db="nucleotide",
        id=accid,
        rettype="gbwithparts",
        retmode="text",
    )

    # Handle file output if requested
    if gbk_outfile is not None:
        gbk_text = gbk_fetch_data.read()
        with open(gbk_outfile, "w", encoding="utf-8") as f:
            f.write(gbk_text)
        # Create new StringIO object to return
        gbk_fetch_data = StringIO(gbk_text)
        gbk_fetch_data.seek(0)  # Rewind to start of stream

    return gbk_fetch_data


@dataclass
class ChrLink:
    """Chromosome Link DataClass."""

    query_chr: str
    query_start: int
    query_end: int
    ref_chr: str
    ref_start: int
    ref_end: int

    @staticmethod
    def load(chr_link_file: str | Path) -> list[ChrLink]:
        """
        Args:
            chr_link_file: Chromosome link file.
        """
        chr_link_list = []
        with open(chr_link_file, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                qchr, qstart, qend = row[0], int(row[1]), int(row[2])
                rchr, rstart, rend = row[3], int(row[4]), int(row[5])
                chr_link_list.append(ChrLink(qchr, qstart, qend, rchr, rstart, rend))
        return chr_link_list
