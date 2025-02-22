# Gitea Hash Extractor & Converter

This script extracts user hashes from a Gitea SQLite database and converts them into a Hashcat-compatible format.

## Usage

Run the script from the command line, providing the path to the Gitea SQLite database:
```
python3 script.py gitea.db
```
## Example Output
```
Converted Hashes for Hashcat:
User: admin (admin@example.com) -> sha256:50000:YmFzZTY0U2FsdA==:YmFzZTY0SGFzaA==
User: user1 (user1@example.com) -> sha256:50000:YW5vdGhlclNhbHQ=:YW5vdGhlckhhc2g=
```

## Crack it with Hashcat
```
hashcat -m 10900 hashes.txt wordlist.txt
```