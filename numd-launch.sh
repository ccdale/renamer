#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/home/chris/src/renamer"
CALLER_DIR="$PWD"

has_path=false
expect_value=false
after_double_dash=false

for arg in "$@"; do
	if [[ "$after_double_dash" == true ]]; then
		has_path=true
		continue
	fi

	if [[ "$expect_value" == true ]]; then
		expect_value=false
		continue
	fi

	case "$arg" in
		-w|--width|-s|--start|-p|--prefix)
			expect_value=true
			;;
		-D|--dry-run|-r|--randomise)
			;;
		--)
			after_double_dash=true
			;;
		-*)
			;;
		*)
			has_path=true
			;;
	esac
done

cd "$PROJECT_DIR"

if [[ "$has_path" == true ]]; then
	exec uv run numd "$@"
fi

exec uv run numd "$@" --dry-run "$CALLER_DIR"
