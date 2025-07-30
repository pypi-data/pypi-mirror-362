# *************************************************************************** #
# This file is subject to the terms and conditions defined in the             #
# file 'LICENSE.txt', which is part of this source code package.              #
#                                                                             #
# No part of the package, including this file, may be copied, modified,       #
# propagated, or distributed except according to the terms contained in       #
# the file 'LICENSE.txt'.                                                     #
#                                                                             #
# (C) Copyright European Space Agency, 2025                                   #
# *************************************************************************** #
import argparse
import json
import logging
from pathlib import Path
from importlib import resources
from juice_simphony.juice_simphony import main as main_runner

logger = logging.getLogger(__name__)

# Define default config path
base_package = (__package__ or "").split(".")[0]
config_file_path = resources.files(base_package) / "data"
default_config_path = config_file_path / "config_scenario.json"

def dump_template():
    template = default_config_path
    logger.info(template.read_text())

def run():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(description="Standalone Simphony Scenario Generator")
    parser.add_argument('--config', type=str, default=default_config_path, help="Path to JSON config file")
    parser.add_argument('--template', action='store_true', help='Optional flag to dump template and exit')
    parser.add_argument('--mapps', action='store_true', help='Enable MAPPS-specific behaviour')
    parser.add_argument('--zip', action='store_true', help='Save the output as a ZIP file')
    args = parser.parse_args()

    if args.template:
        dump_template()
        return

    with open(args.config, 'r') as f:
        config = json.load(f)

    main_runner(config, mapps=args.mapps, zip=args.zip)
