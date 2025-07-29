"""Module that implements SOIL's Command LIne Interface"""

import argparse
import getpass
import json
import os
import shutil
import subprocess  # nosec
import sys
from json import JSONDecodeError
from typing import Dict, Optional, Tuple

import requests
import yaml

parser = argparse.ArgumentParser(prog="soil")
subparsers = parser.add_subparsers(dest="command")

login_cmd = subparsers.add_parser("login", help="Login to configured soil instance")
login_cmd.add_argument("--user", type=str, help="User name or email of the user")
login_cmd.add_argument("--password", type=str, help="Password")
login_cmd.add_argument("--trust", type=str, required=False, help="2FA trust cookie")

run_cmd = subparsers.add_parser(
    "run", help="Runs the provided module in the current soil project"
)
run_cmd.add_argument(
    "chapter",
    metavar="chapter",
    help="Chapter in soil.yml (setup, data, migration, ...)",
)
run_cmd.add_argument("module", metavar="module", help="Module of chapter in soil.yml")
run_cmd.add_argument(
    "module_args", nargs=argparse.REMAINDER, help="Arguments to be passed to the module"
)


def _save_environment(config: Dict, env: Dict) -> None:
    """Saves the environment keys to a file.
    The file is located in ~/.soil/soil.env and ~/.soil/:app_id/soil.env
    Where app_id is the app_id in the config.
    Notice that ~/.soil/soil.env will store the last login only.
    """
    try:
        os.makedirs(os.path.expanduser("~/.soil/" + config["auth_app_id"]))
    except FileExistsError:
        # directory already exists
        pass

    with open(
        os.path.expanduser("~/.soil/soil.env"), "w", encoding="utf-8"
    ) as env_file:
        env_file.write(json.dumps(env, indent=4, sort_keys=True))

    shutil.copyfile(
        os.path.expanduser("~/.soil/soil.env"),
        os.path.expanduser("~/.soil/" + config["auth_app_id"] + "/soil.env"),
    )


def _get_soil_root(relpath: str):  # type: ignore
    """Checks if the current dir is under a soil environment
    and returns its root. Returns None otherwise.
    """
    path = os.path.abspath(relpath) + "/"

    while path != "/":
        path, _ = os.path.split(path)
        if "soil.yml" in os.listdir(path):
            return path

    return None


def _soil_init() -> Tuple[Dict, Optional[Dict]]:
    """Loads configuration and environment."""
    project_root = _get_soil_root(".")
    try:
        if project_root is None:
            raise FileNotFoundError("Project root not found.")
        with open(project_root + "/soil.conf", encoding="utf-8") as config_file:
            config = json.loads(config_file.read())
    except FileNotFoundError:
        try:
            with open(
                os.path.expanduser("~/.soil/soil.conf"), "r", encoding="utf-8"
            ) as config_file:
                config = json.loads(config_file.read())
        except (IOError, JSONDecodeError):
            if sys.argv[1] != "configure":
                try:
                    os.rename(
                        os.path.expanduser("~/.soil/soil.conf.bak"),
                        os.path.expanduser("~/.soil/soil.conf"),
                    )
                except IOError:
                    print(
                        "Can not load soil configuration. Plase run soil configure to configure it."
                    )
                    sys.exit(1)
            else:
                config = None
    try:
        with open(
            os.path.expanduser("~/.soil/soil.env"), "r", encoding="utf-8"
        ) as env_file:
            env = json.loads(env_file.read())
        return config, env
    except (IOError, JSONDecodeError):
        if sys.argv[1] != "configure" and sys.argv[1] != "login":
            try:
                os.rename(
                    os.path.expanduser("~/.soil/soil.conf.bak"),
                    os.path.expanduser("~/.soil/soil.conf"),
                )
            except IOError:
                print(
                    "Can not load soil environment. Plase run soil configure to initialize it."
                )
                sys.exit(1)
        return config, None


def _login(args: argparse.Namespace, config: Dict, env: Optional[Dict]) -> None:
    """Authenticates to the authentication backend and stores the credentials (JWT) in the environment"""
    print(f"Authenticating to {config['auth_url']} for app {config['auth_app_id']}...")

    if env is None:
        env = {}

    if args.user is not None and args.password is not None:
        username = args.user
        password = args.password
    else:
        if "auth" in env:
            username = input(
                "Username: ["
                + env["auth"]["user"].get(
                    "username", env["auth"]["user"].get("email", "")
                )
                + "]"
            )  # nosec - Input is safe in python3
            if username == "":
                username = env["auth"]["user"].get(
                    "username", env["auth"]["user"].get("email", "")
                )
        else:
            username = input("Username: ")  # nosec - Input is safe in python3
        password = getpass.getpass()

    request_json = {
        "loginId": username,
        "password": password,
        "applicationId": config["auth_app_id"],
    }

    resp = requests.post(
        config["auth_url"] + "/api/login",
        headers={"Authorization": config["auth_api_key"]},
        json=request_json,
        timeout=10,
        cookies={"fusionauth.trust": args.trust} if args.trust is not None else None,
    )

    if resp.status_code in {200, 202}:
        env["auth"] = json.loads(resp.content)
        _save_environment(config, env)
        print(
            "Successfully logged in as "
            + env["auth"]["user"].get("username", env["auth"]["user"].get("email", ""))
            + "!"
        )
    elif resp.status_code == 404:
        print("The user was not found or the password was incorrect.")
        sys.exit(1)
    elif resp.status_code == 400:
        print(
            f"Invalid parameters. Perhaps the api key {config['auth_api_key']} or \
                 the app id {config['auth_app_id']} are not correct."
        )
        sys.exit(1)
    else:
        print("Login failed with status code", resp.status_code)
        sys.exit(1)


def _run(args: argparse.Namespace) -> None:
    """Runs the script provided as argument using the python in the virtual environment"""
    soil_root = _get_soil_root(".")
    if not soil_root:
        print(
            "This folder is not initalized as a soil project. "
            "Please run soil init to initialize it."
        )
        sys.exit(1)

    chapter = vars(args)["chapter"]
    module = vars(args)["module"]
    module_args = vars(args)["module_args"]

    os.chdir(soil_root)
    with open("soil.yml", encoding="utf-8") as f:
        conf = yaml.safe_load(f)
    try:
        script = next(
            script for script in conf[chapter] if script.get(module) is not None
        )[module]
    except (IndexError, KeyError):
        print("Script", module, "not found.")
        sys.exit(1)
    params = script.get("params", {})
    params = [["--" + k, str(v)] for (k, v) in params.items()]
    params = [item for sublist in params for item in sublist]
    try:
        shell = [".venv/bin/python", "-m", script["path"], *params, *module_args]
        print("Running:", " ".join(shell), flush=True)
        subprocess.run(shell, check=True)  # nosec
        print("Finished:", " ".join(shell), flush=True)
    except subprocess.CalledProcessError:
        print("Failed executing:", " ".join(shell), flush=True)
        sys.exit(1)


def main() -> None:
    """Main function"""
    args = parser.parse_args()

    config, env = _soil_init()

    try:
        if args.command == "login":
            _login(args, config, env)
        elif args.command == "run":
            _run(args)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt - Exit...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)  # pylint: disable=protected-access


if __name__ == "__main__":
    main()
