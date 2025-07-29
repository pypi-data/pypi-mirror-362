#! /bin/bash

sudo chown -R vscode /workspaces
sudo chgrp -R vscode /workspaces

if [ ! -d ".git" ]; then
  echo "'.git' フォルダが見つかりません。git init を実行します..."
  git init
  git branch --move main
  echo "git init が完了しました。"
else
  echo "'.git' フォルダが既に存在します。git init はスキップします。"
fi

uv sync
