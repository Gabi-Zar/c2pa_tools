import argparse
from pathlib import Path
import struct

CRITICAL_CHUNKS = {b'IHDR', b'PLTE', b'IDAT', b'IEND'}

def read_chunk(f):
    length_bytes = f.read(4)
    if len(length_bytes) < 4:
        return None
    length = struct.unpack(">I", length_bytes)[0]
    chunk_type = f.read(4)
    data = f.read(length)
    crc = f.read(4)
    return length_bytes, chunk_type, data, crc

def write_chunk(f, length_bytes, chunk_type, data, crc):
    f.write(length_bytes)
    f.write(chunk_type)
    f.write(data)
    f.write(crc)

def find_c2pa_chunks(input_file: Path):
    with open(input_file, 'rb') as f:
        sig = f.read(8)
        if sig != b'\x89PNG\r\n\x1a\n':
            print("❌ This file is not a valid PNG.")
            return []

        found = []
        offset = 8
        while True:
            chunk = read_chunk(f)
            if chunk is None:
                break
            length_bytes, chunk_type, data, crc = chunk
            chunk_len = struct.unpack(">I", length_bytes)[0]
            if b'c2pa' in chunk_type or b'c2pa' in data:
                found.append((offset, chunk_type, chunk_len))
            offset += 12 + chunk_len  # 4 (length) + 4 (type) + len + 4 (crc)
    return found

def remove_c2pa_chunks(input_file: Path, output_file: Path):
    with open(input_file, 'rb') as f:
        sig = f.read(8)
        if sig != b'\x89PNG\r\n\x1a\n':
            print("❌ This file is not a valid PNG.")
            return
        chunks = []
        while True:
            chunk = read_chunk(f)
            if chunk is None:
                break
            chunks.append(chunk)

    removed = 0
    input_file_size = input_file.stat().st_size
    with open(output_file, 'wb') as f:
        f.write(sig)
        for length_bytes, chunk_type, data, crc in chunks:
            if b'c2pa' in chunk_type or b'c2pa' in data:
                print(f"[INFO] Chunk supprimé : {chunk_type.decode(errors='ignore')}")
                removed += 1
                continue
            write_chunk(f, length_bytes, chunk_type, data, crc)

    output_file_size = output_file.stat().st_size

    print(f"✅ Cleaned file written in : {output_file}")
    print(f"🧹 {removed} chunk(s) containing 'c2pa' have been deleted.")
    print(f"↘️  Image size reduced by {input_file_size / 1000} ko to {output_file_size / 1000} ko.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lire ou supprimer les chunks C2PA d’un fichier PNG")
    parser.add_argument("input", type=Path, help="Fichier PNG source")
    parser.add_argument("--output", type=Path, help="Fichier PNG nettoyé (requis avec --remove)")
    parser.add_argument("--read", action="store_true", help="Afficher les chunks contenant 'c2pa'")
    parser.add_argument("--remove", action="store_true", help="Supprimer les chunks contenant 'c2pa'")
    parser.add_argument("--replace", action="store_true", help="remplacer le fichier d'entrée par le fichier de sortie")
    parser.add_argument("--extract", type=Path, help="extrait le contenu C2PA dans un fichier séparé")
    args = parser.parse_args()

    if args.read:
        found = find_c2pa_chunks(args.input)
        if found:
            print(f"🔍 {len(found)} chunk(s) C2PA trouvé(s) dans le fichier :")
            for offset, chunk_type, size in found:
                print(f" - Offset {offset} | Type: {chunk_type.decode(errors='ignore')} | Taille: {size} octets")
        else:
            print("❌ No C2PA chunk detected.")

    elif args.remove:
        if not args.output and not args.replace:
            print("❌ The --output or --replace option is required with --remove.")
        elif args.output:
            remove_c2pa_chunks(args.input, args.output)
        elif args.replace:
            remove_c2pa_chunks(args.input, args.input)

    elif args.extract:
        found = find_c2pa_chunks(args.input)
        if found:
            with open(args.extract, 'wb') as extract_file:
                for offset, chunk_type, size in found:
                    with open(args.input, 'rb') as input_file:
                        input_file.seek(offset + 8)  # Skip length and type
                        data = input_file.read(size)
                        extract_file.write(f"Chunk Type: {chunk_type.decode(errors='ignore')}\n".encode())
                        extract_file.write(data)
                        extract_file.write(b"\n\n")
            print(f"✅ C2PA content extracted in : {args.extract}")
        else:
            print("❌ No C2PA chunk detected.")

    else:
        print("❌ Specifies at least --read or --remove or --extract.")
