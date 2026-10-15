#!/usr/bin/env bash
# This file is being executed before committing to git.
# This script focuses on verifying whenever commit message is matching
# Conventional Commits standard: https://www.conventionalcommits.org/

commit_msg_file="$1"
header="$(grep -v '^#' "$commit_msg_file" | grep -v '^[[:space:]]*$' | head -n 1 || true)"

if [ -z "$header" ]; then
	echo "error: commit message is empty." >&2
	echo "Commit messages must follow Conventional Commits: https://www.conventionalcommits.org/" >&2
	echo "" >&2
	echo "  <type>[optional scope][optional !]: <description>" >&2
	echo "" >&2
	echo "Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert" >&2
	exit 1
fi

case "$header" in
	Merge\ *)
		exit 0
		;;
esac

# Types that are allowed in the commit message.
types='feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert'
# Regex pattern to match the commit message.
pattern="^(${types})(\\([^()]+\\))?(!)?: [^[:space:]].*$"

if ! printf '%s\n' "$header" | grep -Eq "$pattern"; then
	echo "error: commit message does not follow Conventional Commits." >&2
	echo "See https://www.conventionalcommits.org/" >&2
	echo "" >&2
	echo "  <type>[optional scope][optional !]: <description>" >&2
	echo "" >&2
	echo "Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert" >&2
	echo "" >&2
	echo "Received header:" >&2
	echo "  $header" >&2
	exit 1
fi
