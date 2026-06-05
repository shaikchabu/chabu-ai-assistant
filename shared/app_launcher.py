import os


def normalize(text):
    """Normalize names for fuzzy matching."""
    return (
        text.lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def find_application(app_name):
    """
    Search for an installed application by name.
    Returns full path if found, otherwise None.
    """

    app_name_norm = normalize(app_name)

    search_dirs = [
        os.path.expanduser("~/Desktop"),

        os.path.join(
            os.environ.get("ProgramData", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs"
        ),

        os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs"
        ),

        os.environ.get("ProgramFiles", ""),

        os.environ.get("ProgramFiles(x86)", "")
    ]

    matches = []

    for directory in search_dirs:

        if not directory or not os.path.exists(directory):
            continue

        try:
            for root, dirs, files in os.walk(directory):

                for file in files:

                    if not file.lower().endswith((".exe", ".lnk")):
                        continue

                    file_norm = normalize(
                        os.path.splitext(file)[0]
                    )

                    # Exact match
                    if file_norm == app_name_norm:
                        return os.path.join(root, file)

                    # Partial match
                    if app_name_norm in file_norm:
                        matches.append(
                            os.path.join(root, file)
                        )

        except Exception:
            pass

    if matches:
        return matches[0]

    return None


def open_application(app_name):
    """
    Find and open application.
    """

    path = find_application(app_name)

    if not path:
        return None

    try:
        os.startfile(path)
        return f"Opening {os.path.basename(path)}"

    except Exception as e:
        return f"Failed to open application: {e}"