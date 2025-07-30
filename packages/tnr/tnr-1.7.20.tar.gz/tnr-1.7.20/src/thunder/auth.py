import click
import os
from thunder import utils

OAUTH_URL = "https://console.thundercompute.com/settings/tokens"
CONSOLE_URL = "https://console.thundercompute.com/settings/billing"


def get_token_from_user():
    try:
        return click.prompt("Token", type=str, hide_input=False)
    except (KeyboardInterrupt, EOFError):
        click.echo("\nLogin cancelled")
        exit(1)

def delete_data():
    credentials_file_path = get_credentials_file_path()
    try:
        os.remove(credentials_file_path)
    except OSError:
        pass

def get_credentials_file_path():
    home_dir = os.path.expanduser("~")
    credentials_dir = os.path.join(home_dir, ".thunder")
    if not os.path.exists(credentials_dir):
        os.makedirs(credentials_dir, mode=0o700, exist_ok=True)
    credentials_file_path = os.path.join(credentials_dir, "token")
    return credentials_file_path

def login():
    credentials_file_path = get_credentials_file_path()

    # Check if a saved token exists
    if os.path.exists(credentials_file_path):
        with open(credentials_file_path, "r", encoding="utf-8") as f:
            token = f.read().strip()

        if token:
            click.echo(
                "Already logged in. You can log out using `tnr logout` and try again."
            )
            return token  # Return the valid token, skip the login process
            
    click.echo(
        f"Please click the following link and generate an API token in the Thunder Compute console: {OAUTH_URL}"
    )
    # Wait for user to input the token
    success = False
    num_attempts = 0
    while not success and num_attempts < 5:
        token = get_token_from_user()
        
        success, error_message = utils.validate_token(token)
        
        if not success:
            click.echo(
                click.style(
                    error_message,
                    fg="red",
                    bold=True,
                )
            )
            if error_message.startswith("Failed to authenticate"):
                exit(1)
            num_attempts += 1

    if not success and num_attempts == 5:
        click.echo(
            click.style(
                f"Failed to log in to thunder compute. Please double check your API token and try again.",
                fg="red",
                bold=True,
            )
        )
        exit(1)

    credentials_file_path = get_credentials_file_path()
    with open(credentials_file_path, "w", encoding="utf-8") as f:
        f.write(token)
    click.echo(
        click.style(
            f"Success! Return to the console and add a payment method: {CONSOLE_URL}",
            fg="green",
        )
    )


def logout():
    delete_data()
    click.echo(
        click.style(
            "Logged out successfully",
            fg="green",
        )
    )


if __name__ == "__main__":
    login()