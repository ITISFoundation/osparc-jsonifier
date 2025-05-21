import json
import logging

import osparc_filecomms.tools as osfct
import pydantic as pyda
import pydantic_settings


logging.basicConfig(
    level=logging.INFO, format="[%(filename)s:%(lineno)d] %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main"""

    print("Started")
