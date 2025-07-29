#! /usr/bin/env bash

function test_bluer_algo_tracker_sandbox() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_algo_tracker_sandbox \
        algo=void
    [[ $? -eq 0 ]] && return 1
    bluer_ai_hr

    bluer_ai_eval ,$options \
        bluer_algo_tracker_sandbox \
        algo=camshift,$options \
        --frame_count 5 \
        --show_gui 0 \
        --log 1
    [[ $? -ne 0 ]] && return 1
    bluer_ai_hr

    bluer_ai_eval ,$options \
        bluer_algo_tracker_sandbox \
        algo=meanshift,$options \
        --frame_count 5 \
        --show_gui 0 \
        --log 1
}
