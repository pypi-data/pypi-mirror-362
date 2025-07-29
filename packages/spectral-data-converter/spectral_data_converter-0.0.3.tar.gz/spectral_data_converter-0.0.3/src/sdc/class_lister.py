from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "sdc.reader",
        ],
        "seppl.io.DirectReader": [
            "sdc.reader",
        ],
        "seppl.io.Filter": [
            "sdc.filter",
        ],
        "seppl.io.Writer": [
            "sdc.writer",
        ],
        "seppl.io.DirectWriter": [
            "sdc.writer",
        ],
        "sdc.api.Generator": [
            "sdc.generator",
        ],
        "sdc.api.Cleaner": [
            "sdc.cleaner",
        ],
    }
