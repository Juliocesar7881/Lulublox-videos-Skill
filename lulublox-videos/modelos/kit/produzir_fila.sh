#!/bin/bash
# Daemon: grava os projetos de fila_producao.txt, um por vez, na ordem. Ctrl: apagar fila.on para parar.
cd "$(dirname "$0")"
L=$(basename "$PWD")
cd ..
touch $L/fila.on $L/fila_producao.txt
feitos=$L/fila_feitos.txt; touch $feitos
while [ -f $L/fila.on ]; do
  p=$(grep -vxFf $feitos $L/fila_producao.txt | head -1)
  if [ -z "$p" ]; then sleep 10; continue; fi
  bash ~/.claude/skills/lulublox-videos/scripts/produzir_lote.sh $L/$p
  echo "$p" >> $feitos
done
