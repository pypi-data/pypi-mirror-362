# instascraper/setup_env.py
import getpass
import os

def main():
    print("Instagram credentials.")

    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password (input hidden): ")

    env_content = f"INSTAGRAM_USERNAME={username}\nINSTAGRAM_PASSWORD={password}\n"

    env_path = os.path.join(os.getcwd(), ".env")
    with open(env_path, "w") as f:
        f.write(env_content)

    print(f"\n .env file created at: {env_path}")

if __name__ == "__main__":
    main()

