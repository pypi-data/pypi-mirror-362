import os
import shutil


class Helper:

    @staticmethod
    def is_wayland():
        """
        Returns True if the system appears to be using Wayland, False otherwise.
        """
        # Common Wayland-related environment variables
        return (
            os.environ.get("WAYLAND_DISPLAY") is not None
            or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        )

    @staticmethod
    def prompt_user_setting(question, default=""):
        user_input = ""

        while True:
            default_text = ""
            if default:
                default_text = " (default: {})".format(default)

            user_input = input(question + default_text).strip()
            if user_input:
                return user_input
            elif default:
                return default

            print("Invalid Input, please try again.")

    @staticmethod
    def prompt_user_option_list(options, prompt_message):
        """
        Prompt the user to select from a list of options.
        """

        for index, key in enumerate(options, start=1):
            print(f"{index}. {key}")

        while True:
            choice = input(prompt_message)
            try:
                index = int(choice)
                if 1 <= index <= len(options):
                    return options[index - 1]

            except ValueError:
                pass

            print("Invalid selection, please choose a number from the list.")

    @staticmethod
    def detect_browsers():
        """
        Detect installed Chrome- or Firefox-based browsers.

        Returns:
            dict: Mapping of browser type to executable path.
        """
        candidates = {
            "chrome": ["google-chrome", "chromium", "chromium-browser"],
            "firefox": ["firefox"]
        }

        found = {}
        for browser_type, executables in candidates.items():
            for exe in executables:
                path = shutil.which(exe)
                if path:
                    found[browser_type] = path
                    break

        return found


if __name__ == "__main__":
    print(Helper.is_wayland())
