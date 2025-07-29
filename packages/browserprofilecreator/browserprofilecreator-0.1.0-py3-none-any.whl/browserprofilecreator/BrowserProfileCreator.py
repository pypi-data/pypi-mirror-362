#!/usr/bin/env python3
"""
Browser Profile Creator

Detect installed browsers, create isolated user data directories,
and generate .desktop files for launching profiles.
"""

import os
import re
import subprocess
import configparser

from .Helper import Helper


class BrowserProfileCreator:
    """
    Manages creation of isolated browser profiles and corresponding .desktop files.
    """
    DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/browserProfileCreator/config.ini")

    BROWSER_CHROME = "chrome"
    BROWSER_FIREFOX = "firefox"

    def __init__(self, config_path=None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = configparser.ConfigParser()

        self.applications_dir = ""
        self.profiles_dir = ""
        self.icons_dir = ""
        self.desktop_template = ""

        self.load_or_create_config()

    def load_or_create_config(self):
        """
        Load existing configuration or create a default one.
        """
        if not os.path.exists(self.config_path):
            self.create_default_config()

        self.config.read(self.config_path)
        self.applications_dir = os.path.expanduser(self.config["Paths"]["applications_dir"])
        self.profiles_dir = os.path.expanduser(self.config["Paths"]["profiles_dir"])
        self.icons_dir = os.path.expanduser(self.config["Paths"]["icons_dir"])
        self.desktop_template = self.config["Templates"]["desktop"]

    def create_default_config(self):
        """
        Generate a default config file with typical paths and a template.
        """
        default_cfg = configparser.ConfigParser()
        default_cfg["Paths"] = {
            "applications_dir": Helper.prompt_user_setting(
                "Enter the default-directory for your .desktop files:",
                "~/.local/share/applications"
            ),
            "profiles_dir": Helper.prompt_user_setting(
                "Enter the default-directory for your browser-folders:",
                "~/browsers"
            ),
            "icons_dir": Helper.prompt_user_setting(
                "Enter the default-directory for your icons:",
                "~/Bilder/icons"
            )
        }
        default_cfg["Templates"] = {
            "desktop": (
                "[Desktop Entry]\n"
                "Name={name}\n"
                "Comment={comment}\n"
                "Exec={exec_cmd}\n"
                "Terminal=false\n"
                "Type=Application\n"
                "Icon={icon_path}\n"
                "Categories=Network;WebBrowser;\n"
                "StartupWMClass={startup_wm_class}\n"
                "MimeType=x-scheme-handler/http;x-scheme-handler/https;text/html;"
            )
        }

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        with open(self.config_path, "w") as cfg_file:
            default_cfg.write(cfg_file)

    def create_profile(self, browser_type=None, purpose=None, dry_run=False):
        """
        Main routine to create a new browser profile and its .desktop entry.
        """
        if dry_run:
            print("######### dry run #########")
        browsers = Helper.detect_browsers()
        if not browsers:
            print("No supported browsers found.")
            return

        if not browser_type:
            browser_type = Helper.prompt_user_option_list(
                list(browsers.keys()), "Select browser type: "
            )
        if not purpose:
            purpose = input("Enter purpose name for the new profile: ").strip()

        # Create profile directory
        purpose_nospaces = re.sub(r"\W+", "_", purpose)
        profile_dir = os.path.join(self.profiles_dir, purpose_nospaces)
        os.makedirs(profile_dir, exist_ok=True)

        exe_path = browsers[browser_type]
        exec_cmd = exe_path

        # TODO: proper escaping for spaces
        if browser_type == BrowserProfileCreator.BROWSER_CHROME:
            exec_cmd += f" --user-data-dir={profile_dir}"
            if Helper.is_wayland():
                exec_cmd += " --ozone-platform=wayland"  # needed for drag & drop
        elif browser_type == BrowserProfileCreator.BROWSER_FIREFOX:
            exec_cmd += f" -profile={profile_dir}"

        name = f"{browser_type.capitalize()} {purpose_nospaces}"
        comment = f"{browser_type.capitalize()} with isolated profile for {purpose}"
        icon_filename = f"{browser_type}_{purpose_nospaces}_icon.png"
        icon_path = os.path.join(self.icons_dir, icon_filename)
        startup_wm_class = f"{browser_type}-{purpose_nospaces}"

        # Generate .desktop content
        desktop_content = self.desktop_template.format(
            name=name,
            comment=comment,
            exec_cmd=exec_cmd,
            icon_path=icon_path,
            startup_wm_class=startup_wm_class
        )

        # Write .desktop file
        desktop_filename = f"{browser_type}-{purpose_nospaces}.desktop"
        desktop_filepath = os.path.join(self.applications_dir, desktop_filename)
        os.makedirs(self.applications_dir, exist_ok=True)
        if dry_run:
            print(f"would write file `{desktop_filepath}` with contents:")
            for line in desktop_content.split("\n"):
                print("  ", line)
        else:
            with open(desktop_filepath, "w") as desktop_file:
                desktop_file.write(desktop_content)

        print(f"you may put a custom icon in this location: {icon_path}")

        # Update desktop database
        if not dry_run:
            subprocess.run(
                ["update-desktop-database", self.applications_dir],
                check=True
            )

        if dry_run:
            print(f"dry run: did not create profile at: {desktop_filepath}")
        else:
            print(f"Profile created: {desktop_filepath}")
