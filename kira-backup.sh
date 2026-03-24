#!/bin/bash
# Kira Backup/Restore Script
# Pindah VPS tanpa kehilangan personality & memory

WORKSPACE_DIR="$HOME/.openclaw/workspace"
REPO_URL="https://github.com/0xmultiserver-crypto/backupai.git"

restore() {
  echo "🔄 Restore Kira dari GitHub..."
  
  # Backup existing dulu (jaga-jaga)
  if [ -d "$WORKSPACE_DIR" ]; then
    mv "$WORKSPACE_DIR" "${WORKSPACE_DIR}.backup.$(date +%s)"
    echo "📦 Existing workspace dibackup dulu"
  fi
  
  # Clone repo
  git clone "$REPO_URL" "$WORKSPACE_DIR"
  
  echo "✅ Restore done!"
  echo "⚠️  Restart gateway: openclaw gateway restart"
}

backup() {
  echo "💾 Backup Kira ke GitHub..."
  
  cd "$WORKSPACE_DIR" || exit 1
  
  git add -A
  git commit -m "Auto backup: $(date '+%Y-%m-%d %H:%M')"
  git push origin master
  
  echo "✅ Backup done!"
}

if [ "$1" == "restore" ]; then
  restore
elif [ "$1" == "backup" ]; then
  backup
else
  echo "Usage: $0 [backup|restore]"
  echo ""
  echo "  backup  - Push workspace ke GitHub"
  echo "  restore - Clone dari GitHub ke workspace"
  echo ""
  echo "💡 Pindah VPS:"
  echo "  1. Install OpenClaw di VPS baru"
  echo "  2. Run: $0 restore"
  echo "  3. Restart: openclaw gateway restart"
fi
