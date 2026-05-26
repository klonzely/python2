from app import WeaponApp
from cli import CLI

def main():
    app = WeaponApp("weapons.json")
    cli = CLI(app)
    cli.run()

if __name__ == "__main__":
    main()