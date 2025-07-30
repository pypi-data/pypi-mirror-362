import cv2

from blueness import module

from bluer_algo import NAME
from bluer_algo.tracker.classes.target import Target
from bluer_algo.tracker.classes.camshift import CamShiftTracker
from bluer_algo.tracker.classes.meanshift import MeanShiftTracker
from bluer_algo.logger import logger


NAME = module.name(__file__, NAME)


def track(
    source: str,
    algo: str = "camshift",
    frame_count: int = -1,
    verbose: bool = True,
    show_gui: bool = True,
    title: str = "tracker",
) -> bool:
    logger.info(
        "{}.track({}){}{} on {}".format(
            NAME,
            algo,
            "" if frame_count == -1 else " {} frame(s)".format(frame_count),
            " with gui" if show_gui else "",
            source,
        )
    )

    cap = cv2.VideoCapture(0 if source == "camera" else source)

    # take first frame of the video
    ret, frame = cap.read()
    if source == "camera" and not ret:
        logger.error("failed to grab initial frame from camera.")
        cap.release()
        return False

    # setup initial location of window
    if source == "camera":
        ret, frame = cap.read()
        success, roi = Target.select(frame)
        if not success:
            logger.error("target not found.")
            cap.release()
            cv2.destroyAllWindows()
            return False

        x, y, w, h = roi
    else:
        x, y, w, h = 300, 200, 100, 50  # simply hardcoded the values
    track_window = (x, y, w, h)

    tracker_class = (
        CamShiftTracker
        if algo == "camshift"
        else MeanShiftTracker if algo == "meanshift" else None
    )
    if tracker_class is None:
        logger.error(f"algo: {algo} not found.")
        return False

    tracker = tracker_class(with_gui=show_gui)
    tracker.start(
        frame=frame,
        track_window=track_window,
    )

    frame_index: int = 0
    while 1:
        success, frame = cap.read()
        if not success:
            break

        frame_index += 1
        if frame_count != -1 and frame_index > frame_count:
            logger.info(f"frame_count={frame_count} reached.")
            break

        ret, track_window, output_image = tracker.track(
            frame=frame,
            track_window=track_window,
        )

        if verbose:
            logger.info(f"frame #{frame_index}: ret={ret}, track_window={track_window}")

        if show_gui:
            cv2.imshow(title, output_image)

            k = cv2.waitKey(30) & 0xFF
            if k == 27:
                break

    if source == "camera":
        cap.release()

    if show_gui:
        cv2.destroyAllWindows()

    return True
