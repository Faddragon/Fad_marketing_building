# Pacote do coletor do Instagram

Copie por cima do repositório (mesmos caminhos). Novo: `andares/coletor/` (Dockerfile, compose.yml, coletor.py, README.md).
Trocados: `predio` (coletor entra nos andares e o `instalar` cria as pastas dele), `avaliar-referencias` (2.1.0, usa os dados do coletor) e `manual-do-predio` (3.2.0).

Na VPS, depois do upload:
```bash
cd /opt/predio && git pull && chmod +x predio && ./predio instalar
```
O resto (chave do app, token, subir o coletor) está em `andares/coletor/README.md`, seção "Configurar".
