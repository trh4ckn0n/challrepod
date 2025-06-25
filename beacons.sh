#!/bin/bash

DB="beacons.db"

if [[ ! -f "$DB" ]]; then
  echo "Fichier $DB introuvable"
  exit 1
fi

sqlite3 "$DB" "SELECT id, ip, user, timestamp FROM beacons;" | \
  column -s '|' -t | \
  fzf --preview="echo {}" --header="Sélectionne une entrée reçue"
