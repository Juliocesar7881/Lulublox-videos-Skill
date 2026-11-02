#!/bin/bash
# fila.sh NN NN ...: põe (ou recoloca) os projetos na fila de produção, apagando o render anterior.
cd "$(dirname "$0")"
for n in "$@"; do
  p=$(ls -d $n-*/ | head -1); p=${p%/}
  rm -rf "$p/final-en"
  sed -i "/^$p$/d" fila_feitos.txt fila_producao.txt
  echo "$p" >> fila_producao.txt
done
