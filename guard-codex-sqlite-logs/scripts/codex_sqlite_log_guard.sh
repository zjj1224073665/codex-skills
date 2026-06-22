#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: codex_sqlite_log_guard.sh <status|block|verify|unblock> [options]

Options:
  --db PATH       Override the logs_2.sqlite path.
  --seconds N     Verification interval in seconds (default: 20).
  -h, --help      Show this help.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

file_size() {
  local path=$1
  if [[ ! -e "$path" ]]; then
    printf 'missing'
  elif stat -c '%s' "$path" >/dev/null 2>&1; then
    stat -c '%s' "$path"
  else
    stat -f '%z' "$path"
  fi
}

file_mtime() {
  local path=$1
  if [[ ! -e "$path" ]]; then
    printf 'missing'
  elif stat -c '%Y' "$path" >/dev/null 2>&1; then
    stat -c '%Y' "$path"
  else
    stat -f '%m' "$path"
  fi
}

ACTION=${1:-status}
if [[ $# -gt 0 ]]; then
  shift
fi

DB=''
VERIFY_SECONDS=20
while [[ $# -gt 0 ]]; do
  case "$1" in
    --db)
      [[ $# -ge 2 ]] || die '--db requires a path'
      DB=$2
      shift 2
      ;;
    --seconds)
      [[ $# -ge 2 ]] || die '--seconds requires an integer'
      VERIFY_SECONDS=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

[[ "$VERIFY_SECONDS" =~ ^[0-9]+$ ]] || die '--seconds must be a non-negative integer'
command -v sqlite3 >/dev/null 2>&1 || die 'sqlite3 is required'

if [[ -z "$DB" ]]; then
  SQLITE_ROOT=${CODEX_SQLITE_HOME:-${CODEX_HOME:-$HOME/.codex}}
  DB="$SQLITE_ROOT/logs_2.sqlite"
fi
WAL="${DB}-wal"
SHM="${DB}-shm"

[[ -f "$DB" ]] || die "database not found: $DB"

read_query() {
  sqlite3 -readonly -cmd '.timeout 30000' "$DB" "$1"
}

write_query() {
  sqlite3 -cmd '.timeout 30000' "$DB" "$1"
}

logs_table_exists() {
  [[ "$(read_query "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='logs';")" == '1' ]]
}

trigger_exists() {
  [[ "$(read_query "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name='block_log_inserts';")" == '1' ]]
}

logs_table_exists || die "logs table not found in: $DB"

case "$ACTION" in
  status)
    printf 'database=%s\n' "$DB"
    printf 'database_bytes=%s\n' "$(file_size "$DB")"
    printf 'wal_bytes=%s\n' "$(file_size "$WAL")"
    printf 'shm_bytes=%s\n' "$(file_size "$SHM")"
    if trigger_exists; then
      printf 'block_trigger=present\n'
    else
      printf 'block_trigger=absent\n'
    fi
    read_query "SELECT 'max_id', COALESCE(MAX(id), 0) FROM logs; SELECT 'sequence', COALESCE((SELECT seq FROM sqlite_sequence WHERE name='logs'), 0);"
    read_query "SELECT 'level', level, COUNT(*), COALESCE(SUM(estimated_bytes), 0) FROM logs GROUP BY level ORDER BY COUNT(*) DESC;"
    read_query "SELECT 'page_size', page_size FROM pragma_page_size; SELECT 'page_count', page_count FROM pragma_page_count; SELECT 'freelist_count', freelist_count FROM pragma_freelist_count; SELECT 'journal_mode', journal_mode FROM pragma_journal_mode;"
    if command -v lsof >/dev/null 2>&1; then
      lsof "$DB" "$WAL" "$SHM" 2>/dev/null || true
    fi
    ;;
  block)
    write_query "CREATE TRIGGER IF NOT EXISTS block_log_inserts BEFORE INSERT ON logs BEGIN SELECT RAISE(IGNORE); END;"
    trigger_exists || die 'trigger creation did not persist'
    printf 'block_trigger=present\n'
    ;;
  verify)
    trigger_exists || die 'block_log_inserts is absent; run block first'
    start_id=$(read_query 'SELECT COALESCE(MAX(id), 0) FROM logs;')
    start_seq=$(read_query "SELECT COALESCE((SELECT seq FROM sqlite_sequence WHERE name='logs'), 0);")
    start_wal_size=$(file_size "$WAL")
    start_wal_mtime=$(file_mtime "$WAL")
    sleep "$VERIFY_SECONDS"
    end_id=$(read_query 'SELECT COALESCE(MAX(id), 0) FROM logs;')
    end_seq=$(read_query "SELECT COALESCE((SELECT seq FROM sqlite_sequence WHERE name='logs'), 0);")
    end_wal_size=$(file_size "$WAL")
    end_wal_mtime=$(file_mtime "$WAL")
    printf 'seconds=%s\n' "$VERIFY_SECONDS"
    printf 'max_id=%s -> %s\n' "$start_id" "$end_id"
    printf 'sequence=%s -> %s\n' "$start_seq" "$end_seq"
    printf 'wal_bytes=%s -> %s\n' "$start_wal_size" "$end_wal_size"
    printf 'wal_mtime=%s -> %s\n' "$start_wal_mtime" "$end_wal_mtime"
    if [[ "$start_id" == "$end_id" && "$start_seq" == "$end_seq" ]]; then
      printf 'result=blocked\n'
    else
      printf 'result=unexpected-log-inserts\n'
      exit 2
    fi
    ;;
  unblock)
    write_query 'DROP TRIGGER IF EXISTS block_log_inserts;'
    if trigger_exists; then
      die 'trigger removal did not persist'
    fi
    printf 'block_trigger=absent\n'
    ;;
  -h|--help)
    usage
    ;;
  *)
    usage >&2
    die "unknown action: $ACTION"
    ;;
esac
