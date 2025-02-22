import sqlite3
import sys
import base64
import argparse

def convert(salt, hash):
    """ Convert salt and hash from hex to base64 """
    if not salt or not hash:
        return None
    try:
        decoded_salt=bytes.fromhex(salt)
        decoded_hash=bytes.fromhex(hash)
    
        resulted_salt= base64.b64encode(decoded_salt).decode()
        resulted_hash= base64.b64encode(decoded_hash).decode()
        return resulted_salt, resulted_hash
    except ValueError as e:
        print(f"Error encoding values: {e}")
        return None



def fetch_gitea_user_data(database_name):
    """ Fetching user data from gitea database """
    try:
        conn=sqlite3.connect(database_name)
        cursor=conn.cursor()
        query='''SELECT name,email,passwd,salt from user'''
        cursor.execute(query)
        
        users = cursor.fetchall() 
        return users
    except sqlite3.Error as e:
        print(f"Error fetching database: {e}")
        return None
    finally:
        if conn:
            conn.close()

def gitea2hashcat(gitea_salt,gitea_hash):
    result= convert(gitea_salt,gitea_hash)
    if result is None:
        return None
    [salt,hash]=result
    return f"sha256:50000:{salt}:{hash}" 

def main():
    
    parser = argparse.ArgumentParser(
        description="Extract user hashes from a Gitea SQLite database and convert them into Hashcat-compatible format."
    )
    parser.add_argument(
        "database", 
        help="Path to the Gitea SQLite database file."
    )

    args = parser.parse_args()
    
    users = fetch_gitea_user_data(args.database)
    if not users:
        print("No user found.")
        return

    print("Converted Hashes for Hashcat:")
    for name, email, passwd, salt in users:
        converted_hash = gitea2hashcat(salt, passwd)
        if converted_hash:
            print(f"User: {name} ({email}) -> {converted_hash}")
        else:
            print(f"Failed to convert hash for user: {name}")

if __name__ == "__main__":
    main()