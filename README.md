# scripts_ip

Estrutura inicial de um projeto Python para utilitarios de ping e varredura.

## Estrutura

```text
.
|-- core/
|   |-- ping.py
|   |-- scanner.py
|   `-- utils.py
|-- logs/
|-- main.py
`-- requirements.txt
```

## Execucao

Crie e ative um ambiente virtual antes de instalar dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Ping

O modulo `core.ping` valida se um IP responde a um ping no Windows:

```python
from core.ping import ping_ip

is_online = ping_ip("127.0.0.1")
```

Internamente a funcao executa `ping -n 1 -w 300 IP` e retorna `True` quando
o comando recebe resposta. Falhas de execucao e alvos sem resposta retornam
`False`.
