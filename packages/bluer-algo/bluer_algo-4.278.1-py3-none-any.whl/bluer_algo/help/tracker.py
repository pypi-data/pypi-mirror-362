from typing import List

from bluer_options.terminal import show_usage, xtra


def help_tracker(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "algo=camshift|meanshift,camera",
            xtra(",~download,dryrun,sandbox", mono=mono),
        ]
    )

    args = [
        "[--frame_count <-1>]",
        "[--log <0 | 1>]",
        "[--show_gui <0 | 1>]",
    ]

    return show_usage(
        [
            "@algo",
            "tracker",
            f"[{options}]",
        ]
        + args,
        "run sandbox/algo.",
        mono=mono,
    )
