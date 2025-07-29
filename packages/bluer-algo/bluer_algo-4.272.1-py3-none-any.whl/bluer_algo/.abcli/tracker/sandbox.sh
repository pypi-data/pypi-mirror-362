#! /usr/bin/env bash

export BLUER_ALGO_TRACKER_ALGO_VERSIONS="camshift=v3,meanshift=v3"

function bluer_algo_tracker_sandbox() {
    local options=$1
    local algo=$(bluer_ai_option "$options" algo camshift)

    local version=$(bluer_ai_option $BLUER_ALGO_TRACKER_ALGO_VERSIONS $algo)
    if [[ -z "$version" ]]; then
        bluer_ai_log_error "algo: $algo not found."
        return 1
    fi

    local use_camera=$(bluer_ai_option_int "$options" camera 0)

    local video_source="camera"
    if [[ "$use_camera" == 0 ]]; then
        local object_name="mean-cam-shift-data-v1"
        local url="https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4"
        local filename="$ABCLI_OBJECT_ROOT/$object_name/slow_traffic_small.mp4"

        local do_download=1
        [[ -f $filename ]] &&
            do_download=0
        do_download=$(bluer_ai_option_int "$options" download $do_download)

        if [[ "$do_download" == 1 ]]; then
            mkdir -pv $ABCLI_OBJECT_ROOT/$object_name
            bluer_ai_eval - \
                wget -O $filename $url -v
            [[ $? -ne 0 ]] && return 1
        fi

        video_source="$ABCLI_OBJECT_ROOT/$object_name/slow_traffic_small.mp4"
    fi

    bluer_ai_eval - \
        python3 $abcli_path_git/bluer-algo/sandbox/mean-cam-shift/$algo-$version.py \
        --source $video_source \
        --title $algo-$version \
        "${@:2}"
}
