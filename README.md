# Gitea Hash Extractor & Converter

This script extracts user hashes from a Gitea SQLite database and converts them into a Hashcat-compatible format.

## Usage

Run the script from the command line, providing the path to the Gitea SQLite database:
```
python3 gitea2hashcat.py gitea.db
```

### Options

| Flag | Description |
| --- | --- |
| `--hashcat` | Output machine-readable lines (`user:sha256:iter:salt:hash`), one per line, ready to pipe straight into hashcat. |

## Example Output

Default (human-readable):
```
Converted Hashes for Hashcat:
User: admin (admin@example.com) -> sha256:50000:YmFzZTY0U2FsdA==:YmFzZTY0SGFzaA==
User: user1 (user1@example.com) -> sha256:50000:YW5vdGhlclNhbHQ=:YW5vdGhlckhhc2g=
```

With `--hashcat`:
```
python3 gitea2hashcat.py gitea.db --hashcat
```
```
admin:sha256:50000:YmFzZTY0U2FsdA==:YmFzZTY0SGFzaA==
user1:sha256:50000:YW5vdGhlclNhbHQ=:YW5vdGhlckhhc2g=
```

## Crack it with Hashcat

Gitea uses PBKDF2-HMAC-SHA256, which is hashcat mode **10900**.

Write the hashes to a file and crack them. The leading `user:` field is handled by hashcat's `--username`:
```
python3 gitea2hashcat.py gitea.db --hashcat > hashes.txt
hashcat -m 10900 --username hashes.txt wordlist.txt
```