note_name=$1
run_quartz=${2:-"true"}
current_dir=$(pwd)
echo "current_dir: ${current_dir}"


if [ -n "${note_name}" ]; then
  python3 scripts/sync_cultural_notes.py "${note_name}.md"
else
  python3 scripts/sync_cultural_notes.py
fi

case "${run_quartz}" in
  0|[Ff]alse|[Nn]o|skip)
    ;;
  *)
    npx quartz sync
    ;;
esac
