#!/usr/bin/env python3

"""
============================================================
              NAWAZ PASSWORD GENERATOR
============================================================

Educational / Personal Password Generator

This program creates password variations from a user-provided
reference password.

Generation happens in stages:

STAGE 1
-------
Uses the exact characters from the reference password and
creates different arrangements.

STAGE 2
-------
Creates structured mutations using characters from the
reference password.

STAGE 3
-------
Creates additional combinations using the character types
detected in the reference password.

All generated passwords keep the SAME LENGTH as the
reference password.

Features:
    - 1,000 to 10,000 passwords
    - Duplicate prevention
    - Reference-based generation
    - Same password length
    - Local generation
    - TXT export
    - Append to existing TXT file
    - Create a new TXT file

============================================================
"""

import secrets
import string
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

SYMBOLS = "!@#$%^&*()-_=+[]{}?"

MIN_PASSWORDS = 1000
MAX_PASSWORDS = 10000


# ============================================================
# BANNER
# ============================================================

def show_banner():

    print("\n" + "=" * 68)
    print("              WELCOME TO NAWAZ PASSWORD GENERATOR")
    print("=" * 68)

    print()
    print("  Educational Personal Password Generator")
    print()
    print("  Generate password variations from your own")
    print("  reference password pattern.")
    print()
    print("  Passwords are generated locally.")
    print("  Nothing is sent to the Internet.")
    print()
    print("  IMPORTANT:")
    print("  Keep generated password lists private.")
    print("  An encrypted physical drive is recommended.")
    print()
    print("=" * 68)
    print()


# ============================================================
# INTEGER INPUT
# ============================================================

def get_integer(prompt, minimum, maximum):

    while True:

        value = input(prompt).strip()

        try:

            number = int(value)

            if minimum <= number <= maximum:

                return number

            print(
                f"[!] Enter a number between "
                f"{minimum} and {maximum}."
            )

        except ValueError:

            print("[!] Please enter a valid number.")


# ============================================================
# CHARACTER TYPE
# ============================================================

def character_type(character):

    if character.isdigit():
        return "D"

    if character.islower():
        return "L"

    if character.isupper():
        return "U"

    return "S"


# ============================================================
# CREATE PATTERN
# ============================================================

def create_pattern(reference):

    return "".join(
        character_type(character)
        for character in reference
    )


# ============================================================
# DISPLAY REFERENCE INFORMATION
# ============================================================

def show_reference_information(reference):

    pattern = create_pattern(reference)

    print("\n" + "-" * 68)
    print("REFERENCE PASSWORD ANALYSIS")
    print("-" * 68)

    print(
        f"\nReference password : {reference}"
    )

    print(
        f"Password length    : {len(reference)}"
    )

    print(
        f"Pattern            : {pattern}"
    )

    print("\nPattern legend:")
    print("D = Digit")
    print("L = Lowercase")
    print("U = Uppercase")
    print("S = Symbol")

    print("-" * 68)

    return pattern


# ============================================================
# RANDOM CHARACTER FROM TYPE
# ============================================================

def random_character_from_type(char_type):

    if char_type == "D":

        return secrets.choice(
            string.digits
        )

    elif char_type == "L":

        return secrets.choice(
            string.ascii_lowercase
        )

    elif char_type == "U":

        return secrets.choice(
            string.ascii_uppercase
        )

    elif char_type == "S":

        return secrets.choice(
            SYMBOLS
        )

    return ""


# ============================================================
# STAGE 1
# EXACT REFERENCE CHARACTERS
# ============================================================

def stage_one_variations(reference, password_set, target):

    """
    Stage 1 tries to rearrange the exact characters
    from the reference password.

    Example:

        98765123@#@

    can produce:

        @#@98765123
        9876@#@5123
        98@#@765123
        #@98765123@
        etc.

    The exact characters are preserved.
    """

    length = len(reference)

    # --------------------------------------------------------
    # Add the original password
    # --------------------------------------------------------

    password_set.add(reference)

    # --------------------------------------------------------
    # Reverse
    # --------------------------------------------------------

    password_set.add(
        reference[::-1]
    )

    # --------------------------------------------------------
    # Rotations
    # --------------------------------------------------------

    for shift in range(1, length):

        rotated = (
            reference[shift:] +
            reference[:shift]
        )

        password_set.add(rotated)

    # --------------------------------------------------------
    # Move individual characters
    # --------------------------------------------------------

    for source in range(length):

        character = reference[source]

        remaining = (
            reference[:source] +
            reference[source + 1:]
        )

        for destination in range(
            len(remaining) + 1
        ):

            candidate = (
                remaining[:destination]
                + character
                + remaining[destination:]
            )

            if len(candidate) == length:

                password_set.add(candidate)

            if len(password_set) >= target:

                return

    # --------------------------------------------------------
    # Random exact-character shuffling
    # --------------------------------------------------------

    characters = list(reference)

    attempts = 0

    while len(password_set) < target:

        secrets.SystemRandom().shuffle(
            characters
        )

        candidate = "".join(characters)

        password_set.add(candidate)

        attempts += 1

        if attempts >= target * 20:

            break


# ============================================================
# STAGE 2
# REFERENCE CHARACTER MUTATIONS
# ============================================================

def stage_two_variations(
    reference,
    pattern,
    password_set,
    target
):

    """
    Stage 2 keeps the same character-type structure,
    but allows characters to be replaced/repeated.

    Example pattern:

        DDDDDDDDSS

    Possible results:

        12345678@#
        98765432#@
        11112222@#
        99887766##
        etc.
    """

    while len(password_set) < target:

        result = []

        for index, char_type in enumerate(pattern):

            # ------------------------------------------------
            # Sometimes reuse a character from the same
            # category in the reference password.
            # ------------------------------------------------

            matching_characters = [
                character
                for character in reference
                if character_type(character) == char_type
            ]

            if matching_characters:

                # 60% chance to use a reference character
                if secrets.randbelow(100) < 60:

                    character = secrets.choice(
                        matching_characters
                    )

                else:

                    character = random_character_from_type(
                        char_type
                    )

            else:

                character = random_character_from_type(
                    char_type
                )

            result.append(character)

        candidate = "".join(result)

        password_set.add(candidate)


# ============================================================
# STAGE 3
# EXTRA COMBINATIONS
# ============================================================

def stage_three_variations(
    reference,
    pattern,
    password_set,
    target
):

    """
    Stage 3 introduces more variation while preserving
    the reference password length and character-type
    structure.

    This creates additional combinations after the
    more reference-focused stages.
    """

    reference_characters = list(reference)

    while len(password_set) < target:

        result = []

        for char_type in pattern:

            # Characters of this type in reference
            matching = [
                character
                for character in reference_characters
                if character_type(character) == char_type
            ]

            # ------------------------------------------------
            # Prefer reference characters, but occasionally
            # introduce a new character of the same type.
            # ------------------------------------------------

            if matching and secrets.randbelow(100) < 40:

                result.append(
                    secrets.choice(matching)
                )

            else:

                result.append(
                    random_character_from_type(
                        char_type
                    )
                )

        # ----------------------------------------------------
        # Randomly rearrange the resulting characters
        # ----------------------------------------------------

        secrets.SystemRandom().shuffle(
            result
        )

        candidate = "".join(result)

        # Because shuffling can change the type-position
        # structure, it is still the same length.

        if len(candidate) == len(reference):

            password_set.add(candidate)


# ============================================================
# GENERATE PASSWORD LIST
# ============================================================

def generate_passwords(
    reference,
    count
):

    pattern = create_pattern(reference)

    passwords = set()

    # ========================================================
    # STAGE 1
    # ========================================================

    print()
    print("[+] Stage 1: Exact reference-character combinations...")
    print()

    stage_one_variations(
        reference,
        passwords,
        count
    )

    print(
        f"[+] Stage 1 generated: {len(passwords)} unique passwords"
    )

    # ========================================================
    # STAGE 2
    # ========================================================

    if len(passwords) < count:

        print()
        print(
            "[+] Stage 2: Reference-based character mutations..."
        )
        print()

        stage_two_variations(
            reference,
            pattern,
            passwords,
            count
        )

        print(
            f"[+] Stage 2 total: {len(passwords)} unique passwords"
        )

    # ========================================================
    # STAGE 3
    # ========================================================

    if len(passwords) < count:

        print()
        print(
            "[+] Stage 3: Additional combinations..."
        )
        print()

        stage_three_variations(
            reference,
            pattern,
            passwords,
            count
        )

        print(
            f"[+] Stage 3 total: {len(passwords)} unique passwords"
        )

    return passwords


# ============================================================
# PREVIEW
# ============================================================

def show_preview(passwords):

    print("\n" + "-" * 68)
    print("PASSWORD PREVIEW")
    print("-" * 68)

    password_list = list(passwords)

    preview_count = min(
        20,
        len(password_list)
    )

    for index in range(preview_count):

        print(
            f"{index + 1:04d}. "
            f"{password_list[index]}"
        )

    if len(passwords) > preview_count:

        print()
        print(
            f"... showing {preview_count} "
            f"of {len(passwords)} passwords"
        )

    print("-" * 68)


# ============================================================
# SAVE / APPEND
# ============================================================

def save_passwords(passwords):

    print("\n" + "=" * 68)
    print("SAVE PASSWORD LIST")
    print("=" * 68)

    print()
    print(
        "Do you want to add the generated passwords "
        "to an existing TXT file?"
    )

    print()
    print("1. Yes - append to existing TXT file")
    print("2. No  - create a new TXT file")

    while True:

        choice = input(
            "\nChoose (1/2): "
        ).strip()

        if choice in ("1", "2"):

            break

        print("[!] Please choose 1 or 2.")

    # ========================================================
    # EXISTING FILE
    # ========================================================

    if choice == "1":

        while True:

            file_path = input(
                "\nEnter existing TXT file path/name: "
            ).strip()

            if not file_path:

                print(
                    "[!] File name cannot be empty."
                )

                continue

            if not file_path.lower().endswith(
                ".txt"
            ):

                print(
                    "[!] Please provide a .txt file."
                )

                continue

            path = Path(
                file_path
            ).expanduser()

            if not path.exists():

                print(
                    "[!] File does not exist."
                )

                create_anyway = input(
                    "Create this file? (y/n): "
                ).strip().lower()

                if create_anyway != "y":

                    continue

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

                print()
                print(
                    "[+] Passwords appended successfully."
                )

                print(
                    f"[+] File: {path.resolve()}"
                )

                return

            except PermissionError:

                print(
                    "[!] Permission denied."
                )

            except OSError as error:

                print(
                    f"[!] Error: {error}"
                )

    # ========================================================
    # NEW FILE
    # ========================================================

    else:

        while True:

            file_path = input(
                "\nEnter new TXT file path/name: "
            ).strip()

            if not file_path:

                print(
                    "[!] File name cannot be empty."
                )

                continue

            if not file_path.lower().endswith(
                ".txt"
            ):

                file_path += ".txt"

            path = Path(
                file_path
            ).expanduser()

            if path.exists():

                print()
                print(
                    "[!] This file already exists."
                )

                overwrite = input(
                    "Overwrite it? (y/n): "
                ).strip().lower()

                if overwrite != "y":

                    continue

            try:

                # Create parent folder if necessary
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

                print()
                print(
                    "[+] New password file created."
                )

                print(
                    f"[+] File: {path.resolve()}"
                )

                return

            except PermissionError:

                print(
                    "[!] Permission denied."
                )

            except OSError as error:

                print(
                    f"[!] Error: {error}"
                )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Banner
    # --------------------------------------------------------

    show_banner()

    # --------------------------------------------------------
    # Reference password
    # --------------------------------------------------------

    print("REFERENCE PASSWORD")
    print("-" * 68)

    while True:

        reference = input(
            "\nEnter your reference password: "
        )

        if reference:

            break

        print(
            "[!] Reference password cannot be empty."
        )

    # --------------------------------------------------------
    # Analyze reference
    # --------------------------------------------------------

    pattern = show_reference_information(
        reference
    )

    # --------------------------------------------------------
    # Number of passwords
    # --------------------------------------------------------

    print("\nGENERATION COUNT")
    print("-" * 68)

    count = get_integer(
        f"\nHow many passwords? "
        f"({MIN_PASSWORDS}-{MAX_PASSWORDS}): ",
        MIN_PASSWORDS,
        MAX_PASSWORDS
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n" + "=" * 68)
    print("GENERATION SUMMARY")
    print("=" * 68)

    print(
        f"Reference password : {reference}"
    )

    print(
        f"Password length    : {len(reference)}"
    )

    print(
        f"Detected pattern   : {pattern}"
    )

    print(
        f"Requested passwords: {count}"
    )

    print("=" * 68)

    confirmation = input(
        "\nStart generation? (y/n): "
    ).strip().lower()

    if confirmation != "y":

        print(
            "\n[!] Generation cancelled."
        )

        return

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    passwords = generate_passwords(
        reference,
        count
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    print("\n" + "=" * 68)
    print("GENERATION COMPLETE")
    print("=" * 68)

    print(
        f"\nRequested : {count}"
    )

    print(
        f"Generated : {len(passwords)}"
    )

    print(
        f"Unique    : {len(passwords)}"
    )

    # --------------------------------------------------------
    # Check length
    # --------------------------------------------------------

    incorrect_lengths = [
        password
        for password in passwords
        if len(password) != len(reference)
    ]

    if incorrect_lengths:

        print(
            "\n[!] ERROR:"
        )

        print(
            "Some generated passwords have an incorrect length."
        )

        print(
            "They will be removed before saving."
        )

        passwords = {
            password
            for password in passwords
            if len(password) == len(reference)
        }

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
        passwords
    )

    # --------------------------------------------------------
    # Finish
    # --------------------------------------------------------

    print("\n" + "=" * 68)
    print(
        "THANK YOU FOR USING NAWAZ PASSWORD GENERATOR"
    )
    print("=" * 68)

    print()
    print(
        "Keep your generated password list private."
    )
    print()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()
