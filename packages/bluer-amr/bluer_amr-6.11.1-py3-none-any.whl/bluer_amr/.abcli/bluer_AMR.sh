#! /usr/bin/env bash

function bluer_amr() {
    local task=$1

    bluer_ai_generic_task \
        plugin=bluer_amr,task=$task \
        "${@:2}"
}

bluer_ai_log $(bluer_amr version --show_icon 1)
