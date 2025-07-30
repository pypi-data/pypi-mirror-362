import logging

logger = logging.getLogger("switch_hub")
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(message)s'))
    logger.addHandler(handler)

logger.setLevel(logging.INFO)
