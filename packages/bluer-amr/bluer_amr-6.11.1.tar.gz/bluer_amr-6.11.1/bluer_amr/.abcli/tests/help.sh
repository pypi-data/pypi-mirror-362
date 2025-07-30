#! /usr/bin/env bash

function test_bluer_amr_help() {
    local options=$1

    local module
    for module in \
        "@amr" \
        \
        "@amr pypi" \
        "@amr pypi browse" \
        "@amr pypi build" \
        "@amr pypi install" \
        \
        "@amr pytest" \
        \
        "@amr test" \
        "@amr test list" \
        \
        "bluer_amr"; do
        bluer_ai_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done

    return 0
}
