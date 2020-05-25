import configparser
import json
import os
import subprocess
import sys

import click
import pkg_resources.py2_warn

creds = configparser.ConfigParser()
file_path = os.path.expanduser("~/.aws/credentials")
creds.read(file_path)


@click.command()
@click.option("--profile", "-p", help="Name of AWS profile as listed in ~/.aws/config")
def main(profile):

    if not profile:
        return

    sso_start_url, sso_region, sso_account_id, sso_role_name = get_sso_params(profile)
    access_token = get_access_token(sso_start_url, sso_region, profile)
    profile_access_key, profile_secret_key, profile_token = get_role_credentials(
        access_token, sso_account_id, sso_role_name, sso_region, profile
    )

    if profile in creds:
        creds.remove_section(profile)
        add_profile(profile, profile_access_key, profile_secret_key, profile_token)
        save_file()
        click.echo(f"Credentials for {profile} updated.")
    else:
        add_profile(profile, profile_access_key, profile_secret_key, profile_token)
        save_file()
        click.echo(f"Credentials for {profile} added to credentials file.")


def get_sso_params(profile):
    section = f"profile {profile}"
    config_path = os.path.expanduser("~/.aws/config")
    config = configparser.ConfigParser()
    config.read(config_path)
    sso_start_url = config[section]["sso_start_url"]
    sso_region = config[section]["sso_region"]
    sso_account_id = config[section]["sso_account_id"]
    sso_role_name = config[section]["sso_role_name"]
    return sso_start_url, sso_region, sso_account_id, sso_role_name


def get_access_token(sso_start_url, sso_region, profile):
    sso_path = os.path.expanduser("~/.aws/sso/cache")
    files = os.listdir(sso_path)
    for f in files:
        if (
            f.endswith(".json")
            and len(f.split(".")[0]) == 40
            and int(f.split(".")[0], 16)
        ):
            ff = open(f"{sso_path}/{f}", "r")
            contents = ff.readline()
            ff.close()
            if (
                json.loads(contents)["startUrl"] == sso_start_url
                and json.loads(contents)["region"] == sso_region
            ):
                return json.loads(contents)["accessToken"]

    login(profile)
    return get_access_token(sso_start_url, sso_region, profile)


def login(profile):
    subprocess.run(
        ["aws", "sso", "login", "--profile", profile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def get_role_credentials(access_token, account_id, role_name, region, profile):
    process = subprocess.run(
        [
            "aws",
            "sso",
            "get-role-credentials",
            "--access-token",
            access_token,
            "--account-id",
            account_id,
            "--role-name",
            role_name,
            "--region",
            region,
            "--profile",
            profile,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if "UnauthorizedException" in process.stderr.decode(encoding="utf-8"):
        login(profile)
        process = subprocess.run(
            [
                "aws",
                "sso",
                "get-role-credentials",
                "--access-token",
                access_token,
                "--account-id",
                account_id,
                "--role-name",
                role_name,
                "--region",
                region,
                "--profile",
                profile,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    elif len(process.stderr.decode(encoding="utf-8")) > 1:
        sys.tracebacklimit = 0
        raise Exception(process.stderr.decode(encoding="utf-8"))
    else:
        output = process.stdout.decode(encoding="utf-8")
        creds = json.loads(output)
        access_key = creds["roleCredentials"]["accessKeyId"]
        secret_key = creds["roleCredentials"]["secretAccessKey"]
        session_token = creds["roleCredentials"]["sessionToken"]
        return access_key, secret_key, session_token


def save_file():
    with open(file_path, "w") as credsfile:
        creds.write(credsfile)


def add_profile(profile, access_key, secret_key, session_token):
    creds.add_section(profile)
    creds[profile]["aws_access_key_id"] = access_key
    creds[profile]["aws_secret_access_key"] = secret_key
    creds[profile]["aws_session_token"] = session_token


if __name__ == "__main__":
    main()
