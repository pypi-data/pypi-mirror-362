# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

"""Entry point for running esp-metrics-cli as a module."""

from app.cli import click_cli

if __name__ == '__main__':
    click_cli()
