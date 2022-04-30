#!/usr/bin/env bash
set -o errexit -o pipefail -o nounset #-o xtrace

SCRIPT=$0
SCRIPTPATH="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

BOOL=false
FLAG=
REST=

function usage {
  cat <<EOF
usage: $SCRIPT [-b] [-f FLAG] [-h] ARGS
a template for bash scripts

  -b, --bool                    a boolean argument
  -f, --flag                    a flag with argument
  -h, --help                    display this message
EOF
}

function parse_args {
  while [ $# -gt 0 ]; do
    case $1 in
      -b|--bool)
        BOOL=true
        shift
        ;;
      -f|--flag)
        FLAG=$2
        shift 2
        ;;
      -|--|-h|--help)
        usage
        exit 1
        ;;
      *)
        REST=$*
        shift $#
        ;;
    esac
  done
}

function main {
  parse_args "$@"

  cat <<EOF
BOOL=$BOOL
FLAG=$FLAG
REST=$REST
SCRIPTPATH=$SCRIPTPATH
EOF
}

main "$@"
