#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/mobile"

if ! command -v flutter &>/dev/null; then
  echo "Flutter not installed. See https://docs.flutter.dev/get-started"
  exit 1
fi

flutter create . --project-name clarity --org com.clarity.learn
flutter pub get

echo "Mobile ready. Run: flutter run"
