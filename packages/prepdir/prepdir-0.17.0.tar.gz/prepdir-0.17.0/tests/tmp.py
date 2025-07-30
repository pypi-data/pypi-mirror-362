import os
import logging

logger = logging.getLogger(__name__)

path_components = ["a", "b", "c"]
for i in range(len(path_components)):
    path_to_check = os.sep.join(path_components[: i + 1])
    logger.warning(f"checking {path_to_check}")
