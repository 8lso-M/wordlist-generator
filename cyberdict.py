#!/usr/bin/env python3

import os
import re
from itertools import permutations


BANNER = r"""
╔════════════════════════════════════════╗
║        CYBER WORDLIST GENERATOR        ║
║              Version 4.0               ║
╚════════════════════════════════════════╝
"""


# ============================================================
# GENERAL HELPERS
# ============================================================

def ask_yes_no(question, default=True):
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{question} {suffix}: ").strip().lower()

    if not answer:
        return default

    return answer in ("y", "yes")


def clean_word(word):
    return word.strip()


def unique(items):
    """
    Remove exact duplicates while preserving generation order.
    """
    return list(dict.fromkeys(
        item for item in items
        if item
    ))


def normalize_symbols(raw):
    """
    Treat each character as a symbol and remove duplicates.
    """
    return unique(list(raw.strip()))


# ============================================================
# CASE ENGINE
# ============================================================

def transform_case(word, mode):
    """
    Generate case variants for ONE base component.

    This is deliberately done before structural combinations.
    That avoids repeatedly transforming the same generated
    candidate later.
    """

    if not word:
        return []

    if mode == "lower":
        return [word.lower()]

    if mode == "upper":
        return [word.upper()]

    if mode == "capitalized":
        return [word.capitalize()]

    if mode == "all":
        return unique([
            word,
            word.lower(),
            word.upper(),
            word.capitalize()
        ])

    return [word]


def choose_case_variations():
    print("\n========== CASE VARIATIONS ==========")
    print("[1] Lowercase")
    print("[2] Uppercase")
    print("[3] Capitalized")
    print("[4] All")

    while True:
        choice = input("\nSelect: ").strip()

        if choice == "1":
            return "lower"

        if choice == "2":
            return "upper"

        if choice == "3":
            return "capitalized"

        if choice == "4":
            return "all"

        print("[-] Invalid choice.")


# ============================================================
# GENERATION PROFILE
# ============================================================

def choose_profile():
    print("\n========== GENERATION PROFILE ==========")
    print("[1] Focused")
    print("[2] Balanced")
    print("[3] Extended")

    while True:
        choice = input("\nSelect [2]: ").strip()

        if not choice:
            return "balanced"

        if choice == "1":
            return "focused"

        if choice == "2":
            return "balanced"

        if choice == "3":
            return "extended"

        print("[-] Invalid choice.")


# ============================================================
# PERSONAL DATA
# ============================================================

def get_personal_data():
    data = {}

    print("\n========== PERSONAL INFORMATION ==========")

    if ask_yes_no("Add first name?", True):
        value = input("First name: ").strip()

        if value:
            data["first"] = value

    if ask_yes_no("Add last name?", False):
        value = input("Last name: ").strip()

        if value:
            data["last"] = value

    if ask_yes_no("Add nickname?", False):
        value = input("Nickname: ").strip()

        if value:
            data["nickname"] = value

    return data


# ============================================================
# DATE / NUMBER INPUT
# ============================================================

def get_birth_date():
    if not ask_yes_no("\nAdd birth date?", False):
        return []

    print("\nSupported examples:")
    print("  12051999")
    print("  121999")
    print("  1999")

    birth_date = input("Birth date: ").strip()

    if not birth_date:
        return []

    birth_date = re.sub(r"\D", "", birth_date)

    results = [birth_date]

    if len(birth_date) == 8:

        day = birth_date[:2]
        month = birth_date[2:4]
        year = birth_date[4:]

        results.extend([
            day,
            month,
            year,
            day + month,
            month + day,
            day + year,
            year + day,
            month + year,
            year + month
        ])

    elif len(birth_date) == 6:

        month = birth_date[:2]
        year = birth_date[2:]

        results.extend([
            month,
            year,
            month + year,
            year + month
        ])

    elif len(birth_date) == 4:
        results.append(birth_date)

    return unique(results)


def get_numbers():

    if not ask_yes_no("\nAdd numbers?", True):
        return []

    print("\nEnter numbers separated by commas.")
    print("Example: 123,2026,01")

    raw = input("Numbers: ").strip()

    if not raw:
        return []

    numbers = []

    for item in raw.split(","):

        item = item.strip()

        if item:
            numbers.append(item)

    return unique(numbers)


def get_symbols():

    if not ask_yes_no("\nAdd symbols?", True):
        return []

    print("\nEnter symbols.")
    print("Example: $@!")

    raw = input("Symbols: ").strip()

    if not raw:
        return []

    return normalize_symbols(raw)


# ============================================================
# COMPONENT ENGINE
# ============================================================

def build_components(personal_data, numbers, case_mode):

    components = {}

    for key, value in personal_data.items():

        value = clean_word(value)

        if not value:
            continue

        components[key] = transform_case(
            value,
            case_mode
        )

    components["number"] = unique(numbers)

    return components


# ============================================================
# CORE PATTERN ENGINE
# ============================================================

def generate_core_patterns(
    personal_data,
    numbers,
    profile,
    combine_words
):

    generated = []

    first = personal_data.get("first")
    last = personal_data.get("last")
    nickname = personal_data.get("nickname")

    names = [
        value
        for value in [first, last, nickname]
        if value
    ]

    # --------------------------------------------------------
    # FOCUSED
    # --------------------------------------------------------

    # Basic individual components
    generated.extend(names)
    generated.extend(numbers)

    # Name + number
    for name in names:

        for number in numbers:

            generated.append(name + number)
            generated.append(number + name)

    # First + Last
    if first and last:

        generated.append(first + last)
        generated.append(last + first)

    # --------------------------------------------------------
    # BALANCED
    # --------------------------------------------------------

    if profile in ("balanced", "extended"):

        if first and last:

            for number in numbers:

                generated.extend([
                    first + last + number,
                    last + first + number,
                    number + first + last,
                    number + last + first
                ])

        # Individual name + number + number
        if len(numbers) >= 2:

            for name in names:

                for a, b in permutations(numbers, 2):

                    generated.append(
                        name + a + b
                    )

                    generated.append(
                        a + name + b
                    )

        # Name combinations
        if combine_words and len(names) >= 2:

            for length in range(
                2,
                min(len(names), 3) + 1
            ):

                for combo in permutations(names, length):

                    generated.append(
                        "".join(combo)
                    )

    # --------------------------------------------------------
    # EXTENDED
    # --------------------------------------------------------

    if profile == "extended":

        if combine_words and len(names) >= 2:

            for length in range(
                2,
                min(len(names), 4) + 1
            ):

                for combo in permutations(names, length):

                    combined = "".join(combo)

                    for number in numbers:

                        generated.extend([
                            combined + number,
                            number + combined
                        ])

        # Number combinations
        if numbers:

            for name in names:

                for number_a in numbers:

                    for number_b in numbers:

                        generated.extend([
                            name + number_a + number_b,
                            number_a + name + number_b,
                            number_a + number_b + name
                        ])

    return unique(generated)


# ============================================================
# SYMBOL ENGINE
# ============================================================

def apply_symbols(
    words,
    symbols,
    profile,
    personal_data,
    numbers
):

    if not symbols:
        return words

    generated = list(words)

    # --------------------------------------------------------
    # Focused:
    # prefix / suffix
    # --------------------------------------------------------

    for word in words:

        for symbol in symbols:

            generated.append(symbol + word)
            generated.append(word + symbol)

    # --------------------------------------------------------
    # Balanced:
    # symbol between components
    # --------------------------------------------------------

    if profile in ("balanced", "extended"):

        first = personal_data.get("first")
        last = personal_data.get("last")

        if first and last:

            for symbol in symbols:

                generated.extend([
                    first + symbol + last,
                    last + symbol + first
                ])

                for number in numbers:

                    generated.extend([
                        first + symbol + last + number,
                        first + last + symbol + number,
                        last + symbol + first + number,
                        last + first + symbol + number
                    ])

    # --------------------------------------------------------
    # Extended:
    # symbols around numbers
    # --------------------------------------------------------

    if profile == "extended":

        for word in words:

            for number in numbers:

                for symbol in symbols:

                    generated.extend([
                        word + symbol + number,
                        word + number + symbol,
                        symbol + word + number,
                        number + symbol + word
                    ])

    return unique(generated)


# ============================================================
# CASE EXPANSION
# ============================================================

def apply_case_to_generated(words, case_mode):
    """
    Apply case transformation once to the final structural
    candidates.

    Exact duplicates are removed immediately.
    """

    result = []

    for word in words:

        result.extend(
            transform_case(
                word,
                case_mode
            )
        )

    return unique(result)


# ============================================================
# FINAL GENERATOR
# ============================================================

def generate_wordlist(
    personal_data,
    numbers,
    symbols,
    case_mode,
    profile,
    combine_words,
    max_length
):

    # 1. Generate structural patterns
    core = generate_core_patterns(
        personal_data=personal_data,
        numbers=numbers,
        profile=profile,
        combine_words=combine_words
    )

    # 2. Apply symbols
    symbolized = apply_symbols(
        words=core,
        symbols=symbols,
        profile=profile,
        personal_data=personal_data,
        numbers=numbers
    )

    # 3. Apply case ONCE
    final_words = apply_case_to_generated(
        symbolized,
        case_mode
    )

    # 4. Length filter
    final_words = [
        word
        for word in final_words
        if word and len(word) <= max_length
    ]

    # 5. Final exact deduplication
    final_words = unique(final_words)

    # 6. Stable readable ordering
    final_words.sort(
        key=lambda x: (
            len(x),
            x.lower(),
            x
        )
    )

    return final_words


# ============================================================
# MAX LENGTH
# ============================================================

def get_max_length():

    while True:

        value = input(
            "\nMaximum word length [32]: "
        ).strip()

        if not value:
            return 32

        try:

            value = int(value)

            if value > 0:
                return value

        except ValueError:
            pass

        print(
            "[-] Please enter a valid positive number."
        )


# ============================================================
# SAVE
# ============================================================

def save_wordlist(words, filename):

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            for word in words:
                file.write(word + "\n")

        return True

    except OSError as error:

        print(
            f"[-] Could not save {filename}: {error}"
        )

        return False


# ============================================================
# USERNAME GENERATOR
# ============================================================

def username_generator():

    print("\n========== USERNAME WORDLIST ==========")

    username = input(
        "Enter username: "
    ).strip()

    if not username:

        print(
            "[-] Username cannot be empty."
        )

        return

    words = {
        "username": username
    }

    if ask_yes_no("Add first name?", True):

        value = input(
            "First name: "
        ).strip()

        if value:
            words["first"] = value

    if ask_yes_no("Add last name?", False):

        value = input(
            "Last name: "
        ).strip()

        if value:
            words["last"] = value

    if ask_yes_no("Add nickname?", False):

        value = input(
            "Nickname: "
        ).strip()

        if value:
            words["nickname"] = value

    numbers = get_numbers()
    symbols = get_symbols()

    cases = choose_case_variations()

    profile = choose_profile()

    combine = ask_yes_no(
        "\nCombine words?",
        True
    )

    max_length = get_max_length()

    print(
        "\n[+] Generating username wordlist..."
    )

    result = generate_wordlist(
        personal_data=words,
        numbers=numbers,
        symbols=symbols,
        case_mode=cases,
        profile=profile,
        combine_words=combine,
        max_length=max_length
    )

    print(
        f"[+] Generated: {len(result):,} usernames"
    )

    filename = input(
        "\nSave username list as [usernames_v4.txt]: "
    ).strip()

    if not filename:
        filename = "usernames_v4.txt"

    if save_wordlist(result, filename):

        print(
            f"[✓] Saved to: "
            f"{os.path.abspath(filename)}"
        )


# ============================================================
# PASSWORD GENERATOR
# ============================================================

def password_generator():

    print("\n========== PASSWORD WORDLIST ==========")

    words = get_personal_data()

    if not words:

        print(
            "[-] You need to provide at least one word."
        )

        return

    birth_dates = get_birth_date()

    numbers = get_numbers()

    # Birth-date components become numeric components
    numbers = unique(
        numbers + birth_dates
    )

    symbols = get_symbols()

    cases = choose_case_variations()

    profile = choose_profile()

    combine = ask_yes_no(
        "\nCombine words?",
        True
    )

    max_length = get_max_length()

    print(
        "\n[+] Generating password wordlist..."
    )

    result = generate_wordlist(
        personal_data=words,
        numbers=numbers,
        symbols=symbols,
        case_mode=cases,
        profile=profile,
        combine_words=combine,
        max_length=max_length
    )

    print(
        f"[+] Generated: {len(result):,} passwords"
    )

    filename = input(
        "\nSave password list as [passwords_v4.txt]: "
    ).strip()

    if not filename:
        filename = "passwords_v4.txt"

    if save_wordlist(result, filename):

        print(
            f"[✓] Saved to: "
            f"{os.path.abspath(filename)}"
        )


# ============================================================
# BOTH
# ============================================================

def both_generator():

    print("\n========== BOTH WORDLISTS ==========")

    username_generator()

    print(
        "\n" + "=" * 45
    )

    password_generator()


# ============================================================
# MAIN
# ============================================================

def main():

    print(BANNER)

    while True:

        print("\n[1] Username Wordlist")
        print("[2] Password Wordlist")
        print("[3] Both")
        print("[4] Exit")

        choice = input(
            "\nSelect: "
        ).strip()

        if choice == "1":

            username_generator()

        elif choice == "2":

            password_generator()

        elif choice == "3":

            both_generator()

        elif choice == "4":

            print(
                "\n[+] Goodbye."
            )

            break

        else:

            print(
                "[-] Invalid choice. "
                "Select 1-4."
            )


if __name__ == "__main__":
    main()
