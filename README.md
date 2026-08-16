# Cyber Wordlist Generator V4

A Python-based **wordlist generation tool** designed for authorized cybersecurity testing, password-auditing labs, CTF environments, and security research.

V4 improves the original generator by replacing large amounts of repetitive combination logic with a structured **pattern engine**. It generates candidates dynamically, removes exact duplicates, applies length limits, and gives the user control over how extensive the generated wordlist should be.

> **Important:** This project is a local wordlist generator only. It does not connect to targets, perform login attempts, brute-force accounts, scan networks, or bypass authentication.

## Features

* Username wordlist generation
* Password wordlist generation
* Generate both username and password lists
* First name support
* Last name support
* Nickname support
* Birth-date processing
* Custom numbers
* Custom symbols
* Case variations
* First + Last combinations
* Last + First combinations
* Name + Number
* Number + Name
* Multi-component combinations
* Symbol prefix/suffix patterns
* Symbol-between-name patterns
* Configurable maximum word length
* Automatic exact duplicate removal
* Three generation profiles
* Deterministic output sorting
* No external Python dependencies

## Generation Profiles

V4 provides three levels of generation.

### Focused

Generates the most basic and common structural patterns.

Use this when you want a smaller wordlist.

### Balanced

Adds additional combinations while keeping the generated list reasonably focused.

**Recommended default profile.**

### Extended

Generates additional combinations and number arrangements.

This can produce significantly more candidates.

## Case Variations

The generator supports:

```text
Lowercase
Uppercase
Capitalized
All
```

For example, a base word such as:

```text
Example
```

can produce case variants such as:

```text
example
EXAMPLE
Example
```

depending on the selected mode.

## Input Components

### Personal Information

The password generator can accept:

```text
First name
Last name
Nickname
```

### Numbers

Multiple numbers can be supplied:

```text
123,2026,01
```

### Birth Date

The generator accepts numeric date formats such as:

```text
12051999
121999
1999
```

It can derive useful numeric components from the supplied date.

### Symbols

Symbols can be supplied directly, for example:

```text
$@!
```

V4 removes duplicate symbols automatically.

## Pattern Engine

Instead of manually maintaining hundreds of password entries, V4 builds candidates from structural rules.

Conceptually:

```text
Personal Data
      │
      ▼
Case Engine
      │
      ▼
Core Pattern Engine
      │
      ├── First + Last
      ├── Last + First
      ├── Name + Number
      ├── Number + Name
      └── Extended combinations
      │
      ▼
Symbol Engine
      │
      ▼
Deduplication
      │
      ▼
Length Filter
      │
      ▼
Sorted Wordlist
```

This makes the generator easier to maintain and extend than a large hard-coded wordlist.

## Duplicate Reduction

V4 uses set-based deduplication throughout the generation process.

If different rules produce the same exact candidate, the final output contains it only once.

This is especially useful when multiple combinations overlap.

## Maximum Length

The default maximum word length is:

```text
32
```

You can change this when the program asks:

```text
Maximum word length [32]:
```

Only candidates within the selected limit are written to the output file.

## Installation

### Requirements

* Python 3.9+
* No third-party packages required

### Linux / Kali

Clone your repository:

```bash
git clone <YOUR-REPOSITORY-URL>
cd <YOUR-REPOSITORY-DIRECTORY>
```

Run:

```bash
python3 wordlist_generator_v4.py
```

You can also make it executable:

```bash
chmod +x wordlist_generator_v4.py
./wordlist_generator_v4.py
```

### Windows

Run:

```powershell
python wordlist_generator_v4.py
```

## Usage

Start the program:

```bash
python3 wordlist_generator_v4.py
```

You will see:

```text
[1] Username Wordlist
[2] Password Wordlist
[3] Both
[4] Exit
```

Choose the generation mode you need.

The program then asks for the relevant information and generation options.

## Output

Username lists are saved by default as:

```text
usernames_v4.txt
```

Password lists are saved by default as:

```text
passwords_v4.txt
```

You can provide a custom filename when prompted.

## Project Structure

```text
cyber-wordlist-generator/
│
├── wordlist_generator_v4.py
├── README.md
│
└── generated/
    ├── usernames_v4.txt
    └── passwords_v4.txt
```

The `generated` directory is optional; the program can save the output wherever you specify.

## Improvements Over Earlier Versions

### Earlier approach

The original approach generated many overlapping combinations and repeatedly applied transformations.

This could make the final wordlist much larger than necessary.

### V4 approach

V4 separates generation into dedicated stages:

```text
1. Input
2. Core patterns
3. Symbol patterns
4. Case expansion
5. Deduplication
6. Length filtering
7. Sorting
8. Output
```

This makes the code easier to understand, modify, and maintain.

## Security and Responsible Use

Use this tool only for systems, accounts, applications, or datasets where you have explicit authorization to perform security testing.

This project intentionally does **not** implement:

* Automated login attempts
* Credential stuffing
* Brute-force attacks
* Target authentication
* Network scanning
* Authentication bypass
* Remote target connections

It is a **wordlist generation component**, not an attack framework.

## Troubleshooting

### Python command not found

Check your Python installation:

```bash
python3 --version
```

On Windows:

```powershell
python --version
```

### Permission denied on Linux

Run:

```bash
chmod +x wordlist_generator_v4.py
```

Then:

```bash
./wordlist_generator_v4.py
```

### Wordlist is too large

Use:

```text
Focused
```

instead of:

```text
Extended
```

You can also reduce the number of supplied numbers and symbols or lower the maximum word length.

### Wordlist is too small

Use:

```text
Balanced
```

or:

```text
Extended
```

and enable word combinations.

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions of the MIT License.
