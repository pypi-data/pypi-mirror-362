#! /usr/bin/env bash

function bluer_amr_action_git_before_push() {
    bluer_amr build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(bluer_ai_git get_branch)" != "main" ]] &&
        return 0

    bluer_amr pypi build
}
