import itertools
import random

def to_leetspeak(word):
    leet_map = str.maketrans({
        'a': '4', 'A': '4',
        'e': '3', 'E': '3',
        'i': '1', 'I': '1',
        'o': '0', 'O': '0',
        's': '$', 'S': '$',
        't': '7', 'T': '7'
    })
    return word.translate(leet_map)

def generate_passwords(firstname, middlename, lastname, birthdate, phone, email, extras=None):
    birth_year = birthdate[-4:] if len(birthdate) >= 4 else ""
    birth_month = birthdate[:2] if len(birthdate) >= 2 else ""
    birth_day = birthdate[2:4] if len(birthdate) >= 4 else ""

    name_variations = [
        firstname, middlename, lastname,
        firstname + lastname, lastname + firstname,
        firstname[:3] + lastname[:3], firstname + birth_year,
        lastname + birth_year, firstname + birth_month + birth_day
    ]

    if birth_year:
        name_variations.extend([
            birth_year, birth_year[-2:],
            birth_month + birth_year[-2:], birth_day + birth_month,
            birth_month + birth_day + birth_year[-2:]
        ])

    phone_variations = []
    if phone:
        phone_variations.extend([
            phone,
            phone[-4:], phone[:6], phone[-6:],
            phone[:3] + phone[-3:], firstname + phone[-4:], lastname + phone[-4:],
            firstname + phone[:3], lastname + phone[:3],
            phone[:2] + firstname, phone[-2:] + lastname,
            firstname + phone[:2] + phone[-2:], lastname + phone[:2] + phone[-2:],
            f"{firstname}#{phone[3:5]}", f"{firstname.capitalize()}#{phone[3:5]}",
            f"#{firstname.capitalize()}{phone[3:5]}", f"{firstname}@{phone[-4:]}",
            f"{firstname.capitalize()}@{phone[-4:]}", f"{lastname}#{phone[:4]}",
            f"{lastname.capitalize()}#{phone[:4]}"
        ])

    email_prefix = email.split("@")[0] if email else ""
    email_variations = [email_prefix] if email_prefix else []

    extras = extras if extras else []
    common_suffixes = ["123", "!", "@", "#", "*"]
    special_separators = ["@", "#", "$", "_", "-"]

    base_words = list(set(name_variations + phone_variations + email_variations + extras))

    passwords = set()
    for word in base_words:
        if word:
            variations = [
                word,
                word.capitalize(),
                word.lower(),
                word[::-1],
                to_leetspeak(word),
                to_leetspeak(word.capitalize())
            ]
            for var in variations:
                passwords.add(var)
                for suffix in common_suffixes:
                    passwords.add(var + suffix)
                    passwords.add(suffix + var)

    if firstname and birth_month and birth_day:
        firstname_cap = firstname.capitalize()
        firstname_short = firstname_cap[:5] if len(firstname_cap) > 5 else firstname_cap

        custom_patterns = {
            f"#{firstname_cap}{birth_day}{birth_month}",
            f"@{firstname_cap}{birth_month}{birth_day}",
            f"#{firstname}{birth_day}{birth_month}",
            f"@{firstname}{birth_month}{birth_day}",
            f"#{firstname_short}{birth_day}{birth_month}",
            f"@{firstname_short}{birth_month}{birth_day}",
            f"{firstname}@{birth_month}{birth_day}",
            f"{firstname_cap}@{birth_month}{birth_day}",
            f"{firstname}@{birth_day}{birth_month}",
            f"{firstname_cap}@{birth_day}{birth_month}",
            f"{firstname.lower()}@{birth_day}{birth_month}",
            f"{firstname.lower()}@{birth_month}{birth_day}",
            f"{firstname.capitalize()}@{birth_day}{birth_month}",
            f"{firstname.capitalize()}@{birth_month}{birth_day}"
        }

        for sep in special_separators:
            custom_patterns.update({
                f"{firstname_cap}{sep}{birth_day}{birth_month}",
                f"{firstname_cap}{sep}{birth_month}{birth_day}",
                f"{firstname}{sep}{birth_day}{birth_month}",
                f"{firstname}{sep}{birth_month}{birth_day}",
                f"{firstname_cap[:3]}{sep}{birth_day}{birth_month}",
                f"{firstname.lower()}{sep}{birth_month}{birth_day}",
                f"{sep}{firstname_cap}{sep}{birth_month}{birth_day}"
            })

        if phone and len(phone) >= 6:
            phone_mid = phone[3:5]
            custom_patterns.update({
                f"#{firstname_cap}{phone_mid}",
                f"#{firstname.lower()}{phone_mid}",
                f"@{firstname_cap}{phone_mid}",
                f"{firstname_cap}@{phone_mid}",
                f"{firstname.lower()}#{phone_mid}",
                f"{firstname_cap}_{phone_mid}",
                f"{firstname_cap}-{phone_mid}",
                f"{firstname_cap}{phone_mid}#"
            })

        passwords.update(custom_patterns)

    for combo in itertools.permutations(base_words, 2):
        joined = "".join(combo)
        passwords.add(joined)
        passwords.add(to_leetspeak(joined))
        for sep in special_separators:
            separated = sep.join(combo)
            passwords.add(separated)
            passwords.add(to_leetspeak(separated))

    # Add variants with mixed upper/lowercase
    complex_variants = set()
    for pw in list(passwords):
        if pw.isalpha() and len(pw) >= 6:
            complex_variants.add(pw[0].upper() + pw[1:-1] + pw[-1].lower())
            complex_variants.add(pw.capitalize())
            complex_variants.add(pw.lower())
            complex_variants.add(pw.upper())
        elif any(c.isdigit() for c in pw) and any(c.isalpha() for c in pw):
            complex_variants.add(pw.lower().capitalize())
            if len(pw) > 2:
                complex_variants.add(pw[:2].upper() + pw[2:].lower())

    passwords.update(complex_variants)

    tier1 = sorted([p for p in passwords if len(p) <= 10])
    tier2 = sorted([p for p in passwords if 10 < len(p) <= 14])
    tier3 = sorted([p for p in passwords if len(p) > 14])

    return tier1 + tier2 + tier3

if __name__ == "__main__":
    firstname = input("Enter first name: ")
    middlename = input("Enter middle name (or press Enter to skip): ")
    lastname = input("Enter last name: ")
    birthdate = input("Enter birthdate (MMDDYYYY): ")
    phone = input("Enter phone number (or press Enter to skip): ")
    email = input("Enter email address (or press Enter to skip): ")

    extras = []
    extra_input = input("Enter any extra words (e.g., pet name, hobby, favorite color), comma-separated: ")
    if extra_input:
        extras = [word.strip() for word in extra_input.split(",") if word.strip()]

    output_file = input("Enter output filename (default: password_list.txt): ").strip() or "password_list.txt"
    sample_limit_input = input("Enter max number of passwords to save (press Enter to save all): ").strip()
    sample_limit = int(sample_limit_input) if sample_limit_input.isdigit() else None

    passwords = generate_passwords(firstname, middlename, lastname, birthdate, phone, email, extras)

    if sample_limit:
        passwords = random.sample(passwords, min(sample_limit, len(passwords)))

    with open(output_file, "w") as f:
        for password in passwords:
            f.write(password + "\n")

    print(f"Generated {len(passwords)} prioritized passwords in {output_file}")
