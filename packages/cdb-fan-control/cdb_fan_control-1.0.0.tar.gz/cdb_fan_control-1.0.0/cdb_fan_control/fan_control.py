"""
Coral Dev Board fan control module

Simple functions to enable/disable the fan directly on CDB.
"""

import argparse
import subprocess
import sys


def enable_cdb_fan():
    """Enable the Coral Dev Board fan."""
    try:
        subprocess.check_output(
            "echo 'enabled' > /sys/devices/virtual/thermal/thermal_zone0/mode",
            shell=True,
        )
        subprocess.check_output(
            "echo 8600 > /sys/devices/platform/gpio_fan/hwmon/hwmon0/fan1_target",
            shell=True,
        )
        return True
    except Exception:
        return False


def disable_cdb_fan():
    """Disable the Coral Dev Board fan."""
    try:
        subprocess.check_output(
            "echo 'disabled' > /sys/devices/virtual/thermal/thermal_zone0/mode",
            shell=True,
        )
        subprocess.check_output(
            "echo 0 > /sys/devices/platform/gpio_fan/hwmon/hwmon0/fan1_target",
            shell=True,
        )
        return True
    except Exception:
        return False


def main():
    """Main function for CDB fan control."""
    parser = argparse.ArgumentParser(description="Control Coral Dev Board fan")
    parser.add_argument(
        "action",
        choices=["enable", "disable"],
        help="Action to perform: enable or disable fan",
    )

    args = parser.parse_args()

    if args.action == "enable":
        if enable_cdb_fan():
            print("Fan enabled")
            sys.exit(0)
        else:
            print("Failed to enable fan")
            sys.exit(1)
    elif args.action == "disable":
        if disable_cdb_fan():
            print("Fan disabled")
            sys.exit(0)
        else:
            print("Failed to disable fan")
            sys.exit(1)


if __name__ == "__main__":
    main()
