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

Ao executar `main.py`, informe a base da rede, o IP inicial, o IP final e a
quantidade desejada para procurar uma sequencia livre pelo terminal.

## Ping

O modulo `core.ping` valida se um IP responde a um ping no Windows:

```python
from core.ping import ping_ip

is_online = ping_ip("127.0.0.1")
```

Internamente a funcao executa `ping -n 1 -w 300 IP` e retorna `True` quando
o comando recebe resposta. Falhas de execucao e alvos sem resposta retornam
`False`.

## Scanner

O scanner procura uma sequencia de IPs que nao responderam ao ping:

```python
from core.scanner import find_available_sequence

ips = find_available_sequence("10.106.5", 1, 254, 4)
```

O exemplo testa IPs entre `10.106.5.1` e `10.106.5.254` ate encontrar
quatro enderecos seguidos aparentemente livres. Ao finalizar, o scanner mostra
os IPs ocupados, os IPs livres testados e a quantidade total testada.
