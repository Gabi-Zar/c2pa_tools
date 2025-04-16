# C2PA Tools

This repository contains a Python script designed to assist with read and removing C2PA data from png images (more extension coming soon). C2PA (Coalition for Content Provenance and Authenticity) metadata is used to provide information about the origin and authenticity of digital content.

> [!CAUTION]
> Use this script responsibly. Ensure you have the right to modify the files you process.

## Features

- **c2pas_tools**: Removes and read C2PA metadata from png images.

## Requirements

- Python 3 or higher

## Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/c2pa-remover.git
    cd c2pa-remover
    ```

2. Run the script:
    - read
        ```bash
        python c2pa_tools.py input.png 
        ```
    - remove
        ```bash
        python c2pa_tools.py input.png --remove --output output.png
        ```
    - remove and replace
        ```bash
        python c2pa_tools.py input.png --remove --replace
        ```
    - extract
        ```bash
        python c2pa_tools.py input.png --extract
        ```

## How does it work

1. the script searches for all occurrences of "c2pa" in the image's hexadecimal code
2. the script deletes all chunks containing "c2pa" unless they are critical chunks that could corrupt the image

## FAQ

- Why not use [C2PA command line tool](https://github.com/contentauth/c2pa-rs/tree/main/cli)
    - The script does not use this library, which means that non-standard c2pa chunks can be deleted as long as they contain the word c2pa.
    <br>
- Comment supprimer la signature c2pa d'autre format de fichier que .png
    - wait for me to update
    - use [C2PA command line tool](https://github.com/contentauth/c2pa-rs/tree/main/cli) for standard c2pa signatures
    - Manually edit the file with a hexadecimal editor

## License

This project is licensed under the [MIT License](LICENSE).