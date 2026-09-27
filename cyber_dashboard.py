import socket
import time
import requests
from colorama import Fore, Style, init

init(autoreset=True)


def line():
    print(Fore.CYAN + "=" * 65)


def section(title):
    print()
    print(Fore.CYAN + "┌" + "─" * 63 + "┐")
    print(Fore.CYAN + "│ " + Fore.WHITE + title.center(61) + Fore.CYAN + " │")
    print(Fore.CYAN + "└" + "─" * 63 + "┘")


def clean_domain(domain):
    domain = domain.strip().lower()

    if domain.startswith("https://"):
        domain = domain[8:]

    elif domain.startswith("http://"):
        domain = domain[7:]

    domain = domain.split("/")[0]

    return domain


def cyber_scan(domain):

    line()
    print(
        Fore.CYAN + Style.BRIGHT +
        "              CYBER INTELLIGENCE DASHBOARD"
    )
    line()

    print(Fore.YELLOW + f"\nTarget Domain : {domain}")

    # ---------------- DNS VERIFICATION ----------------

    section("DOMAIN VERIFICATION")

    try:
        ip = socket.gethostbyname(domain)

        print(Fore.GREEN + "✓ Domain is reachable through DNS")
        print(Fore.WHITE + f"  Resolved IP : {ip}")

    except socket.gaierror:

        print(Fore.RED + "✗ Domain could not be resolved.")
        print(
            Fore.WHITE +
            "  No live DNS record was found for this domain."
        )
        print(
            Fore.YELLOW +
            "  Scan stopped because the domain could not be verified."
        )
        return

    # ---------------- WEBSITE REQUEST ----------------

    section("LIVE WEBSITE INFORMATION")

    try:

        start = time.time()

        response = requests.get(
            "https://" + domain,
            timeout=10,
            allow_redirects=True
        )

        end = time.time()

        response_time = round(
            (end - start) * 1000, 2
        )

        print(Fore.GREEN + "✓ Website responded")
        print(Fore.WHITE + f"  Status Code  : {response.status_code}")
        print(Fore.WHITE + f"  Response Time : {response_time} ms")
        print(Fore.WHITE + f"  Final URL    : {response.url}")

    except requests.RequestException as error:

        print(Fore.RED + "✗ Website could not be reached using HTTPS.")
        print(Fore.WHITE + f"  Reason : {error}")
        return

    # ---------------- HTTPS ----------------

    section("HTTPS INFORMATION")

    if response.url.startswith("https://"):
        print(Fore.GREEN + "✓ HTTPS is being used")
    else:
        print(Fore.YELLOW + "⚠ HTTPS was not detected")

    # ---------------- SERVER ----------------

    section("SERVER INFORMATION")

    server = response.headers.get("Server")

    if server:
        print(Fore.WHITE + f"Server : {server}")
    else:
        print(
            Fore.YELLOW +
            "Server : Not publicly disclosed"
        )

    # ---------------- REDIRECTS ----------------

    section("REDIRECT INFORMATION")

    if response.history:

        print(
            Fore.WHITE +
            f"Redirects : {len(response.history)}"
        )

        for i, redirect in enumerate(response.history, 1):

            print(
                Fore.WHITE +
                f"  {i}. {redirect.status_code} → "
                f"{redirect.url}"
            )

    else:

        print(Fore.GREEN + "No redirects detected")

    # ---------------- SECURITY HEADERS ----------------

    section("PUBLIC SECURITY HEADERS")

    security_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy",
        "Permissions-Policy"
    ]

    for header in security_headers:

        value = response.headers.get(header)

        if value:

            print(Fore.GREEN + f"✓ {header}")
            print(Fore.WHITE + f"  Value: {value}")

        else:

            print(
                Fore.YELLOW +
                f"• {header} : Not returned"
            )

    # ---------------- ALL PUBLIC HEADERS ----------------

    section("PUBLIC RESPONSE DATA")

    for key, value in response.headers.items():

        print(
            Fore.WHITE +
            f"{key} : {value}"
        )

    # ---------------- COMPLETE ----------------

    print()
    line()

    print(
        Fore.GREEN +
        Style.BRIGHT +
        "                  SCAN COMPLETED ✓"
    )

    line()


# ================= PROGRAM START =================

print(
    Fore.CYAN +
    Style.BRIGHT +
    "\nCYBER INTELLIGENCE TOOL"
)

domain = input(
    Fore.WHITE +
    "\nEnter any domain: "
)

domain = clean_domain(domain)

if not domain:

    print(Fore.RED + "\n✗ No domain entered.")

else:

    cyber_scan(domain)
