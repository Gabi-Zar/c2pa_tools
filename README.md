<h1 align="center">C2PA Tools in python</h1>
<p align="center">
    <img alt="Version" src="https://img.shields.io/badge/Version-0.1.0-blue?style=for-the-badge&color=blue">
    <img alt="Stars" src="https://img.shields.io/github/stars/Gabi-Zar/c2pa_tools?style=for-the-badge&color=magenta">
    <img alt="Forks" src="https://img.shields.io/github/forks/Gabi-Zar/c2pa_tools?color=cyan&style=for-the-badge&color=purple">
    <img alt="License" src="https://img.shields.io/github/license/Gabi-Zar/c2pa_tools?style=for-the-badge&color=blue">
    <br>
    <a href="https://github.com/Gabi-Zar"><img title="Developer" src="https://img.shields.io/badge/Developer-GabiZar-red?style=flat-square"></a>
    <img alt="Maintained" src="https://img.shields.io/badge/Maintained-Yes-blue?style=flat-square">
    <img alt="Written In" src="https://img.shields.io/badge/Written%20In-Python-yellow?style=flat-square">
</p>


This repository contains a Python script designed to assist with read and removing C2PA data from png images (more extension coming soon). C2PA (Coalition for Content Provenance and Authenticity) metadata is used to provide information about the origin and authenticity of digital content.

> [!CAUTION]
> Use this script responsibly. Ensure you have the right to modify the files you process.

## 🌟 Highlights

- Works with any .png file
- check if a file contains a c2pa signature
- Delete the chunk(s) containing the signature
- Extract the c2pa signature in a BIN file

## 🔗 Requirements

- [Python 3](https://www.python.org/) or higher

## 🚀 Usage

1. Clone this repository or download it manually:
    ```bash
    git clone https://github.com/Gabi-Zar/c2pa_tools.git
    cd c2pa_tools
    ```

2. Run the script:
    - Read c2pa signature
        ```bash
        python c2pa_tools.py input.png 
        ```
    - Remove c2pa signature
        ```bash
        python c2pa_tools.py input.png --remove --output output.png
        ```
    - Remove c2pa signature and replace original file
        ```bash
        python c2pa_tools.py input.png --remove --replace
        ```
    - Extract c2pa signature in a BIN file
        ```bash
        python c2pa_tools.py input.png --extract
        ```

## ⚙️ How does it work

1. the script searches for all occurrences of "c2pa" in the image's hexadecimal code
2. the script deletes all chunks containing "c2pa" unless they are critical chunks that could corrupt the image

## ❓ FAQ

- Why not use [C2PA command line tool](https://github.com/contentauth/c2pa-rs/tree/main/cli)
    - The script does not use this library, which means that non-standard c2pa chunks can be deleted as long as they contain the word c2pa.
    <br>
- How to remove the c2pa signature from a file format other than .png
    - wait for me to update
    - use [C2PA command line tool](https://github.com/contentauth/c2pa-rs/tree/main/cli) for standard c2pa signatures
    - Manually edit the file with a hexadecimal editor

## 📜 License

This project is licensed under the [MIT License](LICENSE).
