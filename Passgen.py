#!/usr/bin/env python3

import os
import sys
import secrets
import string
from pathlib import Path


# ============================================================
# TERMINAL COLORS
# ============================================================

GREEN = "\033[92m"
RESET = "\033[0m"


# ============================================================
# ENABLE ANSI COLORS ON WINDOWS
# ============================================================

def enable_windows_ansi():
    """
    Enable ANSI escape sequences on Windows terminals.
    """

    if os.name == "nt":

        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32

            # Enable Virtual Terminal Processing
            handle = kernel32.GetStdHandle(-11)

            mode = ctypes.c_ulong()

            kernel32.GetConsoleMode(
                handle,
                ctypes.byref(mode)
            )

            kernel32.SetConsoleMode(
                handle,
                mode.value | 0x0004
            )

        except Exception:
            pass


# ============================================================
# GREEN PRINT
# ============================================================

def gprint(text="", end="\n"):

    print(
        GREEN + text + RESET,
        end=end
    )


# ============================================================
# CLEAR SCREEN
# ============================================================

def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")


# ============================================================
# BANNER
# ============================================================

def show_banner():

    clear_screen()

    banner = r"""
╭──────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│      ██████╗  █████╗ ███████╗███████╗ ███████╗███████╗███╗   ██╗           │
│     ██╔═══██╗██╔══██╗██╔════╝██╔════╝ ██╔════╝██╔════╝████╗  ██║           │
│     ██║   ██║███████║███████╗███████╗ █████╗  █████╗  ██╔██╗ ██║           │
│     ██║   ██║██╔══██║╚════██║╚════██║ ██╔══╝  ██╔══╝  ██║╚██╗██║           │
│     ╚██████╔╝██║  ██║███████║███████║ ███████╗███████╗██║ ╚████║           │
│      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝           │
│                                                                              │
│              Created by https://github.com/darklegionn                     │
│                                                                              │
│                    E D U C A T I O N A L   P A S S W O R D                 │
│                              G E N E R A T O R                               │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
"""

    # The screenshot uses a custom ASCII PASSGEN.
    # We keep the surrounding design and green terminal style.

    for line in banner.splitlines():

        gprint(line)

    gprint("")


# ============================================================
# INFORMATION PANEL
# ============================================================

def show_information_panel():

    left = [
        "[+] Tool      : Passgen",
        "[+] Version   : 1.0",
        "[+] Author    : https://github.com/darklegionn",
        "[+] Purpose   : Educational / Personal Use",
        "[+] Platform  : Linux / Windows (Python 3)",
    ]

    right = [
        "│  Generate Stronger Passwords  │",
        "│  Learn Security Concepts      │",
        "│  Practice Responsibly         │",
        "│  Make a Safer Digital World   │",
    ]

    width = 72

    gprint("─" * width)

    # Print left panel
    for line in left:
        gprint(line)

    gprint("")

    # Right-side message
    for line in right:
        gprint(line)

    gprint("─" * width)

    gprint("")


# ============================================================
# DESCRIPTION
# ============================================================

def show_description():

    gprint(
        "This tool creates password variations from a user-provided "
        "reference password."
    )

    gprint(
        "All passwords are generated locally. Nothing is sent to the Internet."
    )

    gprint(
        "Use this tool for educational and personal purposes only."
    )

    gprint("")

    gprint(
        "┌──────────────────────────────────────────────────────────────────────────┐"
    )

    gprint(
        "│ [!] IMPORTANT: Keep generated password lists private. An encrypted      │"
    )

    gprint(
        "│     physical drive is recommended.                                      │"
    )

    gprint(
        "└──────────────────────────────────────────────────────────────────────────┘"
    )

    gprint("")

    gprint(
        "──────────────  Keep Learning  •  Keep Practicing  •  "
        "Make a Safer Digital World  ──────────────"
    )

    gprint("")


# ============================================================
# SECTION HEADER
# ============================================================

def section(title):

    gprint("─" * 48)

    gprint(title)

    gprint("─" * 48)


# ============================================================
# INPUT
# ============================================================

def ask_reference_password():

    section("REFERENCE PASSWORD")

    while True:

        gprint(
            "Enter your reference password: ",
            end=""
        )

        reference = input()

        if reference:

            return reference

        gprint(
            "[!] Reference password cannot be empty."
        )


# ============================================================
# INTEGER INPUT
# ============================================================

def ask_count():

    section("GENERATION COUNT")

    while True:

        gprint(
            "How many passwords? (1000-10000): ",
            end=""
        )

        value = input().strip()

        try:

            count = int(value)

            if 1000 <= count <= 10000:

                return count

            gprint(
                "[!] Enter a number between 1000 and 10000."
            )

        except ValueError:

            gprint(
                "[!] Please enter a valid number."
            )


# ============================================================
# SAVE OPTION
# ============================================================

def ask_save_option():

    section("SAVE OPTIONS")

    gprint(
        "1. Create a new TXT file"
    )

    gprint(
        "2. Append to an existing TXT file"
    )

    gprint("")

    while True:

        gprint(
            "Choose an option (1 or 2): ",
            end=""
        )

        choice = input().strip()

        if choice in ("1", "2"):

            return choice

        gprint(
            "[!] Please enter 1 or 2."
        )


# ============================================================
# CHARACTER TYPE
# ============================================================

def get_type(character):

    if character.isdigit():
        return "D"

    if character.islower():
        return "L"

    if character.isupper():
        return "U"

    return "S"


# ============================================================
# REFERENCE PATTERN
# ============================================================

def get_pattern(reference):

    return "".join(
        get_type(character)
        for character in reference
    )


# ============================================================
# DISPLAY SUMMARY
# ============================================================

def show_summary(
    reference,
    count,
    pattern,
    save_option
):

    section("GENERATION SUMMARY")

    gprint(
        f"Reference password : {reference}"
    )

    gprint(
        f"Password length    : {len(reference)}"
    )

    gprint(
        f"Pattern            : {pattern}"
    )

    gprint(
        f"Requested passwords: {count}"
    )

    if save_option == "1":

        gprint(
            "Save mode          : New TXT file"
        )

    else:

        gprint(
            "Save mode          : Append to existing TXT"
        )

    gprint("")

    gprint(
        "Generation method  :"
    )

    gprint(
        "  1. Same-character combinations"
    )

    gprint(
        "  2. Reference-based mutations"
    )

    gprint(
        "  3. Additional combinations"
    )

    gprint("")


# ============================================================
# EXACT CHARACTER SHUFFLE
# ============================================================

def exact_shuffle(reference):

    characters = list(reference)

    secrets.SystemRandom().shuffle(
        characters
    )

    return "".join(characters)


# ============================================================
# MOVE CHARACTERS
# ============================================================

def move_character(reference):

    length = len(reference)

    if length < 2:

        return reference

    source = secrets.randbelow(length)

    character = reference[source]

    remaining = (
        reference[:source]
        +
        reference[source + 1:]
    )

    destination = secrets.randbelow(
        len(remaining) + 1
    )

    result = (
        remaining[:destination]
        +
        character
        +
        remaining[destination:]
    )

    return result


# ============================================================
# REVERSE
# ============================================================

def reverse_password(reference):

    return reference[::-1]


# ============================================================
# ROTATE
# ============================================================

def rotate_password(reference):

    length = len(reference)

    if length < 2:

        return reference

    position = secrets.randbelow(
        length - 1
    ) + 1

    return (
        reference[position:]
        +
        reference[:position]
    )


# ============================================================
# RANDOM CHARACTER FOR TYPE
# ============================================================

def random_character(char_type):

    if char_type == "D":

        return secrets.choice(
            string.digits
        )

    if char_type == "L":

        return secrets.choice(
            string.ascii_lowercase
        )

    if char_type == "U":

        return secrets.choice(
            string.ascii_uppercase
        )

    symbols = "!@#$%^&*()-_=+[]{}?"

    return secrets.choice(
        symbols
    )


# ============================================================
# REFERENCE-BASED MUTATION
# ============================================================

def mutate_reference(reference, pattern):

    result = []

    for index, char_type in enumerate(pattern):

        # Characters in reference having the same type
        same_type = [
            c
            for c in reference
            if get_type(c) == char_type
        ]

        if same_type:

            # Mostly use reference characters
            # to keep generated passwords memorable.
            if secrets.randbelow(100) < 70:

                result.append(
                    secrets.choice(same_type)
                )

            else:

                result.append(
                    random_character(char_type)
                )

        else:

            result.append(
                random_character(char_type)
            )

    return "".join(result)


# ============================================================
# REARRANGE MUTATION
# ============================================================

def rearrange_mutation(reference):

    characters = list(reference)

    # Choose between several transformations

    method = secrets.randbelow(4)

    if method == 0:

        return exact_shuffle(reference)

    elif method == 1:

        return move_character(reference)

    elif method == 2:

        return rotate_password(reference)

    else:

        return reverse_password(reference)


# ============================================================
# GENERATE PASSWORD LIST
# ============================================================

def generate_passwords(
    reference,
    count
):

    password_set = set()

    pattern = get_pattern(reference)

    # --------------------------------------------------------
    # STAGE 1
    # --------------------------------------------------------

    gprint("")
    gprint(
        "[+] Stage 1: Generating combinations from the "
        "exact reference characters..."
    )

    # Original
    password_set.add(reference)

    # Reverse
    password_set.add(
        reverse_password(reference)
    )

    # Rotations
    for _ in range(100):

        if len(password_set) >= count:
            break

        password_set.add(
            rotate_password(reference)
        )

    # Character movement
    for _ in range(300):

        if len(password_set) >= count:
            break

        password_set.add(
            move_character(reference)
        )

    # Exact shuffles
    attempts = 0

    while (
        len(password_set) < count
        and attempts < count * 20
    ):

        password_set.add(
            exact_shuffle(reference)
        )

        attempts += 1

    gprint(
        f"[+] Stage 1 complete: "
        f"{len(password_set)} unique passwords"
    )

    # --------------------------------------------------------
    # STAGE 2
    # --------------------------------------------------------

    if len(password_set) < count:

        gprint("")
        gprint(
            "[+] Stage 2: Generating reference-based "
            "mutations..."
        )

        attempts = 0

        while (
            len(password_set) < count
            and attempts < count * 50
        ):

            password_set.add(
                mutate_reference(
                    reference,
                    pattern
                )
            )

            attempts += 1

        gprint(
            f"[+] Stage 2 complete: "
            f"{len(password_set)} unique passwords"
        )

    # --------------------------------------------------------
    # STAGE 3
    # --------------------------------------------------------

    if len(password_set) < count:

        gprint("")
        gprint(
            "[+] Stage 3: Generating additional "
            "combinations..."
        )

        attempts = 0

        while (
            len(password_set) < count
            and attempts < count * 100
        ):

            # Combine reference-based mutation
            # with a structural rearrangement.
            candidate = mutate_reference(
                reference,
                pattern
            )

            characters = list(candidate)

            secrets.SystemRandom().shuffle(
                characters
            )

            candidate = "".join(
                characters
            )

            if len(candidate) == len(reference):

                password_set.add(
                    candidate
                )

            attempts += 1

        gprint(
            f"[+] Stage 3 complete: "
            f"{len(password_set)} unique passwords"
        )

    # --------------------------------------------------------
    # FINAL LENGTH CHECK
    # --------------------------------------------------------

    password_set = {
        password
        for password in password_set
        if len(password) == len(reference)
    }

    return password_set


# ============================================================
# PREVIEW
# ============================================================

def show_preview(passwords):

    section("PASSWORD PREVIEW")

    password_list = list(passwords)

    # Don't show too many passwords in terminal.
    preview = password_list[:20]

    for index, password in enumerate(
        preview,
        start=1
    ):

        gprint(
            f"{index:04d}. {password}"
        )

    if len(passwords) > 20:

        gprint("")

        gprint(
            f"... Showing first 20 of "
            f"{len(passwords)} passwords"
        )


# ============================================================
# FILE PATH INPUT
# ============================================================

def ask_file_path(
    mode
):

    while True:

        if mode == "new":

            gprint(
                "Enter new TXT file name/path: ",
                end=""
            )

        else:

            gprint(
                "Enter existing TXT file name/path: ",
                end=""
            )

        file_name = input().strip()

        if not file_name:

            gprint(
                "[!] File name cannot be empty."
            )

            continue

        if not file_name.lower().endswith(
            ".txt"
        ):

            gprint(
                "[!] File must have a .txt extension."
            )

            continue

        path = Path(
            file_name
        ).expanduser()

        return path


# ============================================================
# SAVE PASSWORDS
# ============================================================

def save_passwords(
    passwords,
    option
):

    section("SAVE PASSWORD LIST")

    if option == "1":

        path = ask_file_path(
            "new"
        )

        # Existing file
        if path.exists():

            gprint(
                "[!] File already exists."
            )

            while True:

                gprint(
                    "Overwrite existing file? (y/n): ",
                    end=""
                )

                answer = input().strip().lower()

                if answer == "y":
                    break

                if answer == "n":

                    path = ask_file_path(
                        "new"
                    )

                    if not path.exists():
                        break

        try:

            # Create parent directory if necessary
            if path.parent:

                path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                for password in sorted(
                    passwords
                ):

                    file.write(
                        password + "\n"
                    )

            gprint("")
            gprint(
                "[+] New TXT file created successfully."
            )

            gprint(
                f"[+] Location: {path.resolve()}"
            )

        except PermissionError:

            gprint(
                "[!] Permission denied."
            )

        except OSError as error:

            gprint(
                f"[!] Error: {error}"
            )

    # --------------------------------------------------------
    # APPEND
    # --------------------------------------------------------

    else:

        path = ask_file_path(
            "existing"
        )

        if not path.exists():

            gprint(
                "[!] File does not exist."
            )

            while True:

                gprint(
                    "Create this file instead? (y/n): ",
                    end=""
                )

                answer = input().strip().lower()

                if answer == "y":

                    try:

                        with open(
                            path,
                            "w",
                            encoding="utf-8"
                        ) as file:

                            for password in sorted(
                                passwords
                            ):

                                file.write(
                                    password + "\n"
                                )

                        gprint(
                            "[+] File created and passwords saved."
                        )

                        return

                    except OSError as error:

                        gprint(
                            f"[!] Error: {error}"
                        )

                        return

                if answer == "n":

                    path = ask_file_path(
                        "existing"
                    )

                    if path.exists():

                        break

        try:

            with open(
                path,
                "a",
                encoding="utf-8"
            ) as file:

                for password in sorted(
                    passwords
                ):

                    file.write(
                        password + "\n"
                    )

            gprint("")
            gprint(
                "[+] Passwords appended successfully."
            )

            gprint(
                f"[+] Location: {path.resolve()}"
            )

        except PermissionError:

            gprint(
                "[!] Permission denied."
            )

        except OSError as error:

            gprint(
                f"[!] Error: {error}"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    enable_windows_ansi()

    show_banner()

    # --------------------------------------------------------
    # Reference
    # --------------------------------------------------------

    reference = ask_reference_password()

    pattern = get_pattern(
        reference
    )

    # --------------------------------------------------------
    # Count
    # --------------------------------------------------------

    count = ask_count()

    # --------------------------------------------------------
    # Save option
    # --------------------------------------------------------

    save_option = ask_save_option()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    show_summary(
        reference,
        count,
        pattern,
        save_option
    )

    # --------------------------------------------------------
    # Confirmation
    # --------------------------------------------------------

    gprint(
        "Start generation? (y/n): ",
        end=""
    )

    confirmation = input().strip().lower()

    if confirmation != "y":

        gprint("")
        gprint(
            "[!] Generation cancelled."
        )

        return

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    gprint("")
    gprint(
        "[+] Starting password generation..."
    )

    passwords = generate_passwords(
        reference,
        count
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    gprint("")
    gprint(
        "=" * 68
    )

    gprint(
        "GENERATION COMPLETE"
    )

    gprint(
        "=" * 68
    )

    gprint(
        f"Requested : {count}"
    )

    gprint(
        f"Generated : {len(passwords)}"
    )

    gprint(
        f"Unique    : {len(passwords)}"
    )

    # --------------------------------------------------------
    # Not enough combinations
    # --------------------------------------------------------

    if len(passwords) < count:

        gprint("")
        gprint(
            "[!] The reference pattern did not produce "
            "enough unique combinations."
        )

        gprint(
            "[!] Try a longer/more varied reference password."
        )

    # --------------------------------------------------------
    # Preview
    # --------------------------------------------------------

    show_preview(
        passwords
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_passwords(
        passwords,
        save_option
    )

    # --------------------------------------------------------
    # Finish
    # --------------------------------------------------------

    gprint("")
    gprint(
        "=" * 68
    )

    gprint(
        "THANK YOU FOR USING PASSGEN"
    )

    gprint(
        "=" * 68
    )

    gprint("")
    gprint(
        "Keep your generated password list private."
    )

    gprint("")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
