"""Library for extracting domains."""

import gzip
import pathlib
import urllib.parse

_RESOURCE_DIR = pathlib.Path(__file__).parent / "resources"
_PUBLIC_SUFFIXES_FILE = _RESOURCE_DIR.joinpath("public_suffix_list.dat.gz")
_PUBLIC_SUFFIXES = (
    gzip.decompress(_PUBLIC_SUFFIXES_FILE.read_bytes()).decode("utf-8").splitlines()
)
_PUBLIC_SUFFIXES = [
    tld for tld in _PUBLIC_SUFFIXES if not tld.startswith("//") and tld.strip()
]


_PUBLIC_SUFFIXES += ["wordpress.com"]


def get_domain(value: str) -> str:
    """Extract a standardized domain from a url."""
    if value.startswith("https://") or value.startswith("http://"):
        base_domain = urllib.parse.urlparse(value).netloc
    else:
        base_domain = value.split("/")[0]
    base_domain = base_domain.split(":")[0]
    matched = [tld for tld in _PUBLIC_SUFFIXES if base_domain.endswith(f".{tld}")]
    use_count = 2
    if matched:
        selected = sorted(matched, key=lambda x: len(x))[-1]
        use_count = len(selected.split(".")) + 1
    return ".".join(base_domain.split(".")[-use_count:]).lower()
