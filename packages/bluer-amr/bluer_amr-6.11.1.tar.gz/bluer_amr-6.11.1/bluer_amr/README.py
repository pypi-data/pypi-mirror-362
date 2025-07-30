import os

from bluer_objects import file, README

from bluer_amr import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "meta-analysis",
            "marquee": "https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true",
            "description": "meta analysis of anti-biotics for cholera.",
            "url": "./bluer_amr/docs/meta-analysis.md",
        }
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
        )
        for readme in [
            {"items": items, "path": ".."},
            {"path": "docs/meta-analysis.md"},
        ]
    )
