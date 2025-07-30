#! /usr/bin/env bash

function test_bluer_amr_README() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_amr build_README
}
