from configparser import ConfigParser
import json, os, time
def getconfig(action, account: str | None = None):
    if action == "account":
        account_maker()
    if action == "config":
        if account is not None:
            config_maker_barons(account)
        else:
            print("Error: account name must be provided for config action.")

def account_maker():
    # Create ./configs directory if it doesn't exist
    config_dir = os.path.join('.', 'configs')
    os.makedirs(config_dir, exist_ok=True)
    accountlist_path = os.path.join(config_dir, 'accountlist.ini')
    config = ConfigParser()
    if os.path.exists(accountlist_path):
        config.read(accountlist_path)
    account_name = input("Enter account name: ").strip()
    if not account_name:
        print("Account name cannot be empty.")
        return
    if config.has_section(account_name):
        overwrite = input(f"Account '{account_name}' already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Aborted.")
            return
        config.remove_section(account_name)
    username = input("Enter nickname: ").strip()
    password = input("Enter password: ").strip()
    server = input("Enter server: ").strip()
    config.add_section(account_name)
    config.set(account_name, 'username', username)
    config.set(account_name, 'password', password)
    config.set(account_name, 'server', server)
    with open(accountlist_path, 'w') as f:
        config.write(f)
    print(f"Account '{account_name}' saved to {accountlist_path}. Exiting...")
    time.sleep(1)
    exit()

def config_maker_barons(filename: str):
    # Ensure ./configs directory exists
    config_dir = os.path.join('.', 'configs')
    os.makedirs(config_dir, exist_ok=True)
    # Create the config file path
    config_path = os.path.join(config_dir, f"{filename}_config.ini")
    config = ConfigParser()
    # === Instructions for config_maker_barons ===
    print("""
================ Baronix Config Maker Instructions ================
This utility will help you create a config file for the Baronix bot.
You will be prompted for each setting, with options and explanations.

INSTRUCTIONS:
1. You will be asked to enter a config name (e.g. pluto_ice). If the name exists, you can overwrite it.
2. For each setting, follow the prompt. Enter values as described (e.g. integers, comma-separated lists).
3. For unit/tool selections, type the number of your choice from the displayed list.
4. If you are unsure, you can exit at any prompt by pressing Ctrl+C.
5. All configs are saved in ./configs/ as {yourname}_config.ini.
==================================================================
""")

    unit_options = {
        "1": ("Distance Veteran Demon", '10'),
        "2": ("Distance Mead lvl 10", '216'),
        "3": ("Meelee   Mead lvl 10", '215'),
    }

    flank_tool_options = {
        "1": ("5%   ladders", '614'),
        "2": ("5%   wooden shields", '651'),
        "3": ("--   None", '-1')
    }

    front_tool_options_1 = {
        "1": ("5%   ladders", '614'),
        "2": ("5%   wooden walls (anti distance)", '651'),
        "3": ("--   None", '-1')
    }

    front_tool_options_2 = {
        "1": ("20%  ram", '648'),
        "2": ("5%   ram", '611'),
        "3": ("--   None", '-1')
    }

    # Read existing config if it exists
    if os.path.exists(config_path):
        config.read(config_path)
    print(f'Saves: {config.sections()}')
    save_name = input("Enter the desired config name(e.g. pluto_ice): ").strip()
    while True:
        if not save_name:
            print("...")
            exit()
        elif config.has_section(save_name):
            if_overwrite = input("Save with this name already exists. Do you want to overwrite it?\n(y/n): ")
            if if_overwrite == 'y': 
                config.remove_section(save_name)
            else:
                print("Exitting.")
                exit()
        else:
            break
    config.add_section(save_name)

    def input_int_list(prompt):
        while True:
            raw = input(prompt).strip()
            if raw:
                try:
                    values = [int(item.strip()) for item in raw.split(",") if item.strip()]
                    return ",".join(str(val) for val in values)
                except ValueError:
                    print("Please enter valid comma separated integers (e.g. 2,29,30,31).")
            else:
                print("Input cannot be empty.")

    def input_int(prompt):
        while True:
            raw = input(prompt).strip()
            if raw:
                try:
                    return str(int(raw))
                except ValueError:
                    print("Please enter a valid integer.")
            else:
                print("Input cannot be empty.")

    kid = input("Kingdom Green = Green, Kingdom Fire = Fire, Kingdom Sand = Sands, Kingdom Ice = Ice\nKingdom -> <-\b\b\b")
    config.set(save_name, "kid", kid)

    excluded_commanders = input_int_list("Enter excluded commanders (comma separated integers, e.g. 2,3,17. -1 if none): ")
    config.set(save_name, "excluded_commanders", excluded_commanders)


    distance = input_int("Distance for attacks (not preicse): ")
    config.set(save_name, "distance", distance)
    horse = input_int("Type of horse, Coin / Feather")
    config.set(save_name, "horse", horse)
    print("The script will use 4 waves. Always. Each wave will have the same setup. If you exceed the max ammount of units on given side, attack will fail.")
    max_flank = input_int("Enter ammount of units on a flank (0 if none)  : ")
    config.set(save_name, "max_flank", max_flank)

    max_front = input_int("Enter ammount of units on the front (0 if none): ")
    config.set(save_name, "max_front", max_front)

    print("\nPick units to send in the attack\n")
    for key, value in unit_options.items():
        print(f"{key}   - {value[0]}\n")
    unit_choice = (input("Selection: "))
    print(f'Selected option "{unit_options[unit_choice][0]}"')
    config.set(save_name, "unit_id", str(unit_options[unit_choice][1]))

    print("\nPick wich tool do you want to use on the flanks\n")
    for key, value in flank_tool_options.items():
        print(f"{key}   - {value[0]}\n")
    flank_choice = input("Selection: ")
    print(f'Selected option "{flank_tool_options[flank_choice][0]}"')
    config.set(save_name, "flank_id", str(flank_tool_options[flank_choice][1]))

    if flank_tool_options[flank_choice][0] != "--   None":
        flank_tool_ammount = input_int("Enter ammount of those tools per flank: ")
        config.set(save_name, "flank_tool_ammount", flank_tool_ammount)
    else:
        config.set(save_name, "flank_tool_ammount", "0")

    print("\nPick the first tool you want to use on the front\n")
    for key, value in front_tool_options_1.items():
        print(f"{key}   - {value[0]}\n")
    front_choice1 = input("Selection: ")
    print(f'Selected option "{front_tool_options_1[front_choice1][0]}"')
    config.set(save_name, "front_id_1", str(front_tool_options_1[front_choice1][1]))

    if front_tool_options_1[front_choice1][0] != "--   None":
        front_tool_ammount1 = input_int("Enter ammount of those tools per front: ")
        config.set(save_name, "front_tool_ammount1", front_tool_ammount1)
    else:
        config.set(save_name, "front_tool_ammount1", "0")

    print("\nPick the second tool you want to use on the front\n")
    for key, value in front_tool_options_2.items():
        print(f"{key}   - {value[0]}\n")
    front_choice2 = input("Selection: ")
    print(f'Selected option "{front_tool_options_2[front_choice2][0]}"')
    config.set(save_name, "front_id_2", str(front_tool_options_2[front_choice2][1]))

    if front_tool_options_2[front_choice2][0] != "--   None":
        front_tool_ammount2 = input_int("Enter ammount of those tools per front: ")
        config.set(save_name, "front_tool_ammount2", front_tool_ammount2)
    else:
        config.set(save_name, "front_tool_ammount2", "0")
    
    with open(config_path, "w") as f:
        config.write(f)
    print(f"\nConfiguration saved to {config_path}.")
    exit()
