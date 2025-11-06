# Contribuindo — Git Flow e boas práticas

Este projeto usa um fluxo de trabalho baseado em Git Flow (branching model). O objetivo é manter branches claros e PRs pequenos.

Branches principais
- `main`: branch protegida com o código pronto para produção.
- `develop`: (opcional) integração de features antes de release.

Branches de desenvolvimento
- `feature/<short-description>` — novas funcionalidades.
- `bugfix/<short-description>` — correções em desenvolvimento.
- `hotfix/<short-description>` — correções críticas diretamente em `main`.

Fluxo de PR
1. Crie a branch a partir de `develop` ou `main` conforme o caso.
2. Faça commits pequenos e atômicos com mensagens descritivas.
3. Abra Pull Request contra `develop` (ou `main` para hotfix).
4. Peça review e marque reviewers. Inclua descrição, screenshots e lista de checagem de testes.

Regras sugeridas (manuais)
- Execute testes localmente antes de abrir PR: `python -m pytest -q`.
- Execute linter/formatador: `ruff .` / `black .` (se configurado).

Pull Request template: use o arquivo `.github/PULL_REQUEST_TEMPLATE.md` ao abrir PR.

Se precisar, posso automatizar validações (branch-name check, lint, testes) via GitHub Actions.
