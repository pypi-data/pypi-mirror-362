import os
import time
import webbrowser

import bugsnag
import typer
from yaspin import yaspin
from yaspin.spinners import Spinners

from cerebrium.api import cerebrium_request
from cerebrium.context import get_config_value, set_config_value, get_default_region
from cerebrium.utils.check_cli_version import print_update_cli_message
from cerebrium.utils.logging import cerebrium_log, console

CEREBRIUM_ENV = os.getenv("CEREBRIUM_ENV", "prod")

auth_cli = typer.Typer(no_args_is_help=True)


@auth_cli.command("login")
def login():
    """
    Authenticate user via oAuth and store token in the configuration
    """

    print_update_cli_message()

    auth_response = cerebrium_request("POST", "device-authorization", {}, False, v1=True)
    if auth_response is None:
        cerebrium_log(
            level="ERROR",
            message="There was an error getting your device code. Please try again.\nIf the problem persists, please contact support.",
        )
        bugsnag.notify(Exception("There was an error getting your device code."))
        raise typer.Exit(1)
    auth_response = auth_response.json()["deviceAuthResponsePayload"]
    verification_uri = auth_response["verification_uri_complete"]

    console.print("You will be redirected to the following URL to authenticate:")
    console.print(verification_uri)
    webbrowser.open(verification_uri, new=2)

    start_time = time.time()
    with yaspin(Spinners.arc, text="Waiting for authentication...", color="magenta"):
        response = cerebrium_request(
            "POST",
            "token",
            {"device_code": auth_response["device_code"]},
            False,
            v1=True,
        )
        while time.time() - start_time < 60 and response.status_code == 400:  # 1 minutes
            time.sleep(0.5)
            response = cerebrium_request(
                "POST",
                "token",
                {"device_code": auth_response["device_code"]},
                False,
                v1=True,
            )
    if response.status_code == 200:
        # Get the response data
        response_data = response.json()
        access_token = response_data["accessToken"]
        refresh_token = response_data["refreshToken"]

        # Print environment-specific messages
        if CEREBRIUM_ENV == "dev":
            console.print("Logging in with dev API key")
        elif CEREBRIUM_ENV == "local":
            console.print("Logging in with local API key")

        # Save tokens using context functions
        set_config_value("accessToken", access_token)
        set_config_value("refreshToken", refresh_token)

        # Set default region if not already set
        if not get_config_value("defaultRegion"):
            set_config_value("defaultRegion", "us-east-1")

        console.print("Logged in successfully.")

        projects_response = cerebrium_request("GET", "v2/projects", {}, True)
        assert projects_response is not None
        if projects_response.status_code != 200:
            return  # Early return to simplify the flow

        projects = projects_response.json()
        current_project_id = get_config_value("project")

        if current_project_id and any(p["id"] == current_project_id for p in projects):
            console.print(f"Using existing project context ID: {current_project_id}")
        else:
            current_project = projects[0]["id"]
            set_config_value("project", current_project)
            if current_project_id:
                console.print(
                    f"Updated project context to ID: {current_project} (previous project not found)"
                )
            else:
                console.print(f"Current project context set to ID: {current_project}")
    else:
        try:
            console.print(auth_response.json()["message"])
            bugsnag.notify(Exception("Error logging in."))
        except Exception as e:
            console.print(auth_response.text)
            console.print("There was an error logging in. Please try again.")
            bugsnag.notify(e)


@auth_cli.command("save-auth-config")
def save_auth_config(access_token: str, refresh_token: str, project_id: str):
    """
    Saves the access token, refresh token, and project ID to the config file. Run `cerebrium save-auth-config --help` for more information.

    This function is a helper method to allow users to store credentials\n
    directly for the framework. Mostly used for CI/CD
    """
    # Check for missing values
    if not access_token:
        console.print("Access token is missing.")
        raise typer.Exit(1)
    if not refresh_token:
        console.print("Refresh token is missing.")
        raise typer.Exit(1)
    if not project_id:
        console.print("Project ID is missing.")
        raise typer.Exit(1)

    # Print environment-specific messages
    if CEREBRIUM_ENV == "dev":
        console.print("Logging in with dev API key")
    elif CEREBRIUM_ENV == "local":
        console.print("Logging in with local API key")

    # Save credentials using context functions
    set_config_value("accessToken", access_token)
    set_config_value("refreshToken", refresh_token)
    set_config_value("project", project_id)

    console.print("Configuration saved successfully.")
