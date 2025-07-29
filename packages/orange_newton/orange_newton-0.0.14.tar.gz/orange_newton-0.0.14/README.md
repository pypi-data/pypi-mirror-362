# Welcome to Hoge13

A Simple Orange Newton Project

## 開発用セットアップ
プロジェクト構築後に、以下の手順で実行環境を構築します

```bash
cd <your-project-name>

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Run formatting and linting (automatically runs on commit)
uv run ruff format .
uv run ruff check .
# Auto Fix
uv run ruff check . --fix

```

## ビルドとリリース
ビルドして、リリースします

```bash
# Git tag
git tag vX.X.X

# Build
uv build

# Publish testpypi
uv publish --publish-url https://test.pypi.org/legacy/ --token <TOKEN>
OR
uv publish --index testpypi --token <TOKEN>

# To install testpypi
pip install -i https://test.pypi.org/simple/ <PACKAGE_NAME>

# Publish pypi
uv publish --token <TOKEN>

# To install pypi
pip install <PACKAGE_NAME>
OR
uv add <PACKAGE_NAME>

```

## Github actionでのリリース
Githubアクションを経由してリリースします

```
# Test-Pypiへのリリース
git tag release-test/vX.X.X
git push origin release-test/vX.X.X

# Pypiへのリリース
git tag release/vX.X.X
git push origin release/vX.X.X

```

## VSCodeでのDevcontainerを利用した開発用セットアップ
VSCodeの場合、Devcontainerを開きます

