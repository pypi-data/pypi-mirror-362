import os

from bluer_options.help.functions import get_help
from bluer_objects import file, README

from bluer_algo import NAME, VERSION, ICON, REPO_NAME
from bluer_algo.help.functions import help_functions


items = README.Items(
    [
        {
            "name": "tracker",
            "marquee": "https://github.com/kamangir/assets/raw/main/tracker-camshift-2025-07-16-11-07-52-4u3nu4/tracker.gif?raw=true",
            "description": "a visual tracker.",
            "url": "./bluer_algo/docs/tracker",
        },
        {
            "name": "image classifier",
            "marquee": "https://github.com/kamangir/assets/raw/main/swallow-model-2025-07-11-15-04-03-2glcch/evaluation.png?raw=true",
            "description": "an image classifier.",
            "url": "./bluer_algo/docs/image_classifier",
        },
    ]
)


def build():
    return all(
        README.build(
            items=readme.get("items", []),
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
            help_function=lambda tokens: get_help(
                tokens,
                help_functions,
                mono=True,
            ),
        )
        for readme in [
            {"path": "docs"},
            #
            {"items": items, "path": ".."},
            {"path": "docs/image_classifier"},
            {"path": "docs/image_classifier/dataset"},
            {"path": "docs/image_classifier/dataset/ingest.md"},
            {"path": "docs/image_classifier/dataset/review.md"},
            {"path": "docs/image_classifier/dataset/sequence.md"},
            {"path": "docs/image_classifier/model"},
            {"path": "docs/image_classifier/model/train"},
            {"path": "docs/image_classifier/model/train/small.md"},
            {"path": "docs/image_classifier/model/train/large.md"},
            {"path": "docs/image_classifier/model/prediction"},
            {"path": "docs/image_classifier/model/prediction/dev.md"},
            {"path": "docs/image_classifier/model/prediction/rpi.md"},
            #
            {"path": "docs/tracker"},
            {"path": "docs/tracker/camshift.md"},
            {"path": "docs/tracker/meanshift.md"},
            # aliases
            {"path": "docs/aliases"},
            {"path": "docs/aliases/image_classifier.md"},
            {"path": "docs/aliases/tracker.md"},
            {"path": "docs/aliases/socket.md"},
            #
            {"path": "docs/socket.md"},
        ]
    )
