# aws-profile-switch

`aws-profile-switch` is a Python-based command-line tool designed to drastically simplify AWS CLI profile switching for AWS administrators managing numerous accounts and roles. It aims to eliminate the tedium of navigating a large number of profiles in environments utilizing AWS IAM Identity Center (formerly AWS SSO).

-----

## Key Features and Implementation Tasks

This tool provides the following core functionalities. Each feature includes a brief overview of the tasks an LLM should focus on for implementation.

### 1\. Profile Information Loading and Parsing

  * **Functionality**: Reads and parses AWS CLI profile information from the `~/.aws/config` file into an internal, easy-to-manage data structure. It specifically identifies AWS IAM Identity Center (SSO)-related profiles (those possessing `sso_start_url`, `sso_account_name`, `sso_account_id`, `sso_role_name`, etc.).
  * **Implementation Tasks**:
      * Implement a parser to read the `~/.aws/config` file (Python's `configparser` module is suitable).
      * Define a data structure to store extracted relevant information (`sso_account_name`, `sso_account_id`, `sso_role_name`, etc.) from each `[profile <profile_name>]` section.
      * Implement logic to identify SSO-related profiles, for example, by checking for `sso_auto_populated = true` or the presence of SSO-specific keys.

### 2\. Interactive Profile Selection UI

  * **Functionality**: Provides a rich, interactive user interface (UI) in the terminal for users to select profiles. This UI will be built using the `prompt_toolkit` library, ensuring no reliance on external tools like `fzf` or `peco`.
  * **Implementation Tasks**:
      * **UI Framework Integration**: Incorporate `prompt_toolkit` into the project and set up basic input prompting and candidate list display functionalities.
      * **Keyboard Input Handling**: Implement keybindings for navigating candidates (up/down arrows), confirming selection (Enter key), and canceling (Esc key).

### 3\. Multi-Stage Profile Search and Refinement

  * **Functionality**: Guides the user through a progressive filtering workflow to narrow down profile selections based on their input.

    1.  **Initial Display & Recent Profiles**: Upon tool launch, the most recently used five profiles will be displayed as initial candidates.
    2.  **Account Name Search**: As the user types, a real-time fuzzy search will be performed on `sso_account_name` fields, dynamically updating the displayed account name candidates.
    3.  **Role Name Refinement**: After an account is selected, only the `sso_role_name` values associated with that specific account will be displayed as candidates for the user to choose from.

  * **Implementation Tasks**:

      * **History Management**: Implement logic to save and load recently used profile names (e.g., in a JSON file within the user's home directory).
      * **Fuzzy Search Logic**: Implement an efficient fuzzy search algorithm targeting both `sso_account_name` and `sso_role_name`.
      * **Dynamic Candidate Updates**: Implement logic to dynamically update the `prompt_toolkit` candidate list based on user input and selections.
      * **Multi-Stage Transition**: Implement state management logic to transition automatically from account name selection to role name selection.
      * **Display Formatting**: Format the candidate list to display relevant information (e.g., `sso_account_name`, `sso_role_name`) alongside the profile name, adapting the displayed details to the current selection stage.

### 4\. `AWS_PROFILE` Environment Variable Setting

  * **Functionality**: Once a profile is selected, its name will be automatically set as the `AWS_PROFILE` environment variable in the current shell session.
  * **Implementation Tasks**:
      * **Shell Environment Detection**: Implement logic to detect whether the current shell is Bash/Zsh (Linux/WSL) or PowerShell (Windows).
      * **Command Output**: Output the appropriate shell command string (e.g., `export AWS_PROFILE="<profile_name>"` for Bash/Zsh or `$env:AWS_PROFILE = "<profile_name>"` for PowerShell) to standard output. This output will be `eval`-ed or `Invoke-Expression`-ed by the shell to set the variable.

### 5\. Cross-Platform Compatibility and Installation

  * **Functionality**: The tool will operate seamlessly across Linux (including WSL) and Windows (PowerShell) environments, and be easily installable via `pipx`.
  * **Implementation Tasks**:
      * **Python Packaging**: Create `setup.py` or `pyproject.toml` to configure `aws-profile-switch` as a `pipx`-installable Python package.
      * **Dependency Definition**: Define necessary library dependencies (like `prompt_toolkit`) in `requirements.txt` or `pyproject.toml`.

### 6\. Error Handling and Robustness

  * **Functionality**: Provides robust error handling for common issues such as missing `~/.aws/config` files, failed profile parsing, or incomplete SSO-related information.
  * **Implementation Tasks**:
      * Implement exception handling for file reading errors, data parsing errors, invalid profile formats, and other critical failure points.
      * Ensure user-friendly error messages are displayed.

-----

## Installation

`aws-profile-switch` is best installed using `pipx`, a tool for installing and running Python applications in isolated environments.

### Prerequisites

  * Python 3.8 or newer
  * `pipx` installed (If not, run: `python3 -m pip install --user pipx && python3 -m pipx ensurepath`)
  * `aws-sso-util` or a similar tool has been used to generate profiles in your `~/.aws/config`.

### Installation Command

You can install this tool directly from the GitHub repository.

```bash
pipx install git+https://github.com/takedai0313/aws-profile-switch.git
```

-----

## Usage

### Recommended Setup (Alias)

For the most convenient usage, set up an alias or function in your shell configuration. This ensures that the selected profile's environment variable is applied to your current shell session.

**For Bash / Zsh:**

Add the following line to your `~/.bashrc` or `~/.zshrc` file:

```bash
alias aps='eval "$(aws-profile-switch)"'
```

**For Fish:**

Add the following line to your `~/.config/fish/config.fish` file:

```fish
alias aps='eval (aws-profile-switch)'
```

**For PowerShell:**

Add the following function to your PowerShell profile file (typically located at `$PROFILE`):

```powershell
function aps {
    $command = aws-profile-switch
    if ($command -and $command.Trim() -ne '' -and -not $command.StartsWith('#')) {
        Invoke-Expression $command
    }
}
```

After applying the configuration (by restarting your shell or sourcing the profile file), simply run the `aps` command to launch the interactive profile selection UI.

### Other Options

The tool also provides a few command-line flags for different behaviors.

*   **Show Usage Information (`--info`)**: Displays help and usage instructions.
    ```bash
    aws-profile-switch --info
    ```

*   **Test Profile (`--test`)**: After selecting a profile, it runs `aws sts get-caller-identity` to verify that the profile is working correctly.
    ```bash
    aws-profile-switch --test
    ```

*   **Generate a Script (`--exec`)**: Instead of outputting a command for `eval`, this generates a temporary shell script that you can `source`. This is useful in environments where `eval` might not be preferred.
    ```bash
    aws-profile-switch --exec
    # To apply, run the suggested 'source /path/to/temp_script.sh'
    ```

-----

## Development and Contribution

This project is open-source. Contributions, including feature enhancements and bug fixes, are welcome.

-----

## License

This project is released under the [MIT](LICENSE) license.