import functools
import time
from io import BytesIO
from pathlib import Path
from typing import List, Tuple
from xml.dom import minidom

import requests
from tqdm.auto import tqdm


def extract_details_from_product_id(product_id: str) -> Tuple[str, str, str]:
    """
    Extracts the grid square, latitude band, and path number from a given product ID.

    Args:
        product_id (str): The Sentinel-2 product ID.

    Returns:
        Tuple[str, str, str]: The grid square, latitude band, and path number.

    Raises:
        ValueError: If the product ID format is not valid.
    """
    try:
        details = product_id.split("_")[-2]
        return details[1:3], details[3], details[4:6]
    except ValueError:
        raise ValueError("Invalid product ID format")


def build_download_url(
    base_url: str,
    product_id: str,
    grid_square: str,
    latitude_band: str,
    path_number: str,
) -> str:
    """
    Constructs a Sentinel-2 download URL using the provided parameters.

    Args:
        base_url (str): The base URL for Sentinel-2 data.
        product_id (str): The Sentinel-2 product ID.
        grid_square (str): The grid square.
        latitude_band (str): The latitude band.
        path_number (str): The path number.

    Returns:
        str: The constructed download URL.
    """
    return f"{base_url}/{grid_square}/{latitude_band}/{path_number}/{product_id}.SAFE/"


@functools.lru_cache(maxsize=None)
def create_request_session():
    """
    Creates and caches a request session for downloading Sentinel-2 data.

    Returns:
        requests.Session: The created and cached request session.
    """
    return requests.Session()


def fetch_data_from_url(session: requests.Session, url: str) -> bytes:
    """
    Fetches data from a URL using the provided request session.

    Args:
        session (requests.Session): The request session.
        url (str): The URL from which to fetch data.

    Returns:
        bytes: The fetched data.
    """
    with session.get(url, allow_redirects=True) as response:
        return response.content


def save_file_from_url(session: requests.Session, url: str, target_file_path: Path):
    """
    Downloads a file from a URL and saves it to a specified location.

    Args:
        session (requests.Session): The request session. url (str): The URL from
        which to download the file. target_file_path (Path): The location where
        the downloaded file should be saved.

    Raises:
        ValueError: If the download attempts all failed or the Content-Type is
        unexpected.
    """
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    max_attempts = 5
    for i in range(max_attempts):
        with session.get(url, allow_redirects=True) as response:
            content_type = response.headers.get("Content-Type")
            if content_type == "text/html; charset=UTF-8":
                time.sleep(i + 2)
            elif content_type == "application/octet-stream":
                with target_file_path.open("wb") as output_file:
                    output_file.write(response.content)
                break
            else:
                raise ValueError(f"Unexpected Content-Type: {content_type}")
    else:
        raise ValueError("All attempts to download the file failed")


def get_xml(session: requests.Session, xml_url: str):
    """
    Fetches and parses XML data from a URL using a request session.

    Args:
        session (requests.Session): The request session.
        xml_url (str): The URL from which to fetch XML data.

    Returns:
        xml.dom.minidom.Document: The parsed XML document.

    Raises:
        Exception: If it failed to fetch XML data from the URL.
    """
    max_attempts = 5
    for i in range(max_attempts):
        try:
            xml_data = fetch_data_from_url(session, xml_url)
            xml_dom_tree = minidom.parse(BytesIO(xml_data))
            return xml_dom_tree
        except Exception:
            time.sleep(i + 2)
    raise Exception(f"Sorry, we failed to fetch XML data from {xml_url}")


def fetch_product_data(
    session: requests.Session,
    base_url: str,
    product_id: str,
    grid_square: str,
    latitude_band: str,
    path_number: str,
    target_directory: Path,
):
    """
    Downloads Sentinel-2 product data from a given URL and saves it to a target
    directory.

    Args:
        session (requests.Session): The request session. base_url (str): The
        base URL for Sentinel-2 data. product_id (str): The Sentinel-2 product
        ID. grid_square (str): The grid square. latitude_band (str): The
        latitude band. path_number (str): The path number. target_directory
        (Path): The directory where the downloaded data should be saved.

    Returns:
        Path: The directory path where the scene data is saved.
    """
    download_url = build_download_url(
        base_url, product_id, grid_square, latitude_band, path_number
    )
    target_directory.mkdir(parents=True, exist_ok=True)

    xml_url = f"{download_url}MTD_MSIL1C.xml"
    xml_dom_tree = get_xml(session, xml_url)

    image_file_nodes = xml_dom_tree.getElementsByTagName("IMAGE_FILE")

    image_files_urls = [
        f"{download_url}{node.firstChild.data}.jp2" for node in image_file_nodes  # type: ignore  # noqa: E501
    ]
    if len(image_files_urls) == 0:
        raise ValueError(f"Sorry we failed to find product {product_id}")

    scene_dir = target_directory / f"{product_id}.SAFE"
    for url, file_path in tqdm(
        zip(
            image_files_urls,
            [scene_dir / f"{node.firstChild.data}.jp2" for node in image_file_nodes],  # type: ignore  # noqa: E501
        ),
        desc="Downloading scene data",
        leave=False,
        total=len(image_files_urls),
        unit="Scene file",
    ):
        save_file_from_url(session, url, file_path)

    return scene_dir


def fetch_single_sentinel_product(
    base_url: str, product_id: str, target_directory: Path
) -> Path:
    """
    Fetches and saves a single Sentinel-2 product's data.

    Args:
        base_url (str): The base URL for Sentinel-2 data. product_id (str): The
        Sentinel-2 product ID. target_directory (Path): The directory where the
        downloaded data should be saved.

    Returns:
        Path: The directory path where the scene data is saved.
    """
    session = create_request_session()
    grid_square, latitude_band, path_number = extract_details_from_product_id(
        product_id
    )

    scene_dir = fetch_product_data(
        session,
        base_url,
        product_id,
        grid_square,
        latitude_band,
        path_number,
        target_directory,
    )

    return scene_dir


def fetch_multiple_sentinel_products(
    product_ids: List[str],
    target_directory: Path,
    base_url: str = "https://storage.googleapis.com/gcp-public-data-sentinel-2/tiles",
) -> List[Path]:
    """
    Fetches and saves multiple Sentinel-2 products' data.

    Args:
        product_ids (List[str]): A list of Sentinel-2 product IDs.
        target_directory (Path): The directory where the downloaded data should
        be saved. base_url (str, optional): The base URL for Sentinel-2 data.
        Defaults to
        "https://storage.googleapis.com/gcp-public-data-sentinel-2/tiles".

    Returns:
        List[Path]: A list of directory paths where each scene's data is saved.
    """
    scene_dirs = []
    for product_id in tqdm(
        product_ids, leave=False, desc="Downloading multiple scenes", unit="Scene"
    ):
        scene_dirs.append(
            fetch_single_sentinel_product(
                base_url=base_url,
                product_id=product_id,
                target_directory=target_directory,
            )
        )
    return scene_dirs
