import os
import subprocess
from datetime import datetime

print("🧪 Running scraper...")
os.system("python scraper.py")

print("📦 Committing props_cache.json to GitHub...")
commit_message = f"Auto update: props @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

subprocess.run(["git", "add", "props_cache.json"])
subprocess.run(["git", "commit", "-m", commit_message])
subprocess.run(["git", "push"])

print("✅ Done! Props updated to GitHub.")
