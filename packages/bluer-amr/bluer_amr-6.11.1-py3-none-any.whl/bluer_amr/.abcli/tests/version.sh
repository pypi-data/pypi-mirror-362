#! /usr/bin/env bash

function test_bluer_amr_version() {
    local options=$1

    bluer_ai_eval ,$options \
        "bluer_amr version ${@:2}"
}
