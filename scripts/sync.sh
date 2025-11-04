note_name=$1
current_dir=$(pwd)
echo "current_dir: ${current_dir}"


python3 scripts/sync_cultural_notes.py ${note_name}.md
npx quartz sync