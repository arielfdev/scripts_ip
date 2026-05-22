# scripts_ip

`scripts_ip` e um scanner sequencial de IPv4 para Windows. O projeto testa
enderecos de uma faixa informada no terminal e procura uma sequencia continua
de IPs que nao responderam ao ping.

## Objetivo

O objetivo e ajudar na triagem inicial de blocos de IPs aparentemente livres
antes de uma validacao de rede mais completa. O operador informa uma base de
rede, uma faixa de hosts e quantos IPs consecutivos precisa encontrar.

Exemplo de busca por quatro IPs:

```text
10.106.5.1
10.106.5.2
10.106.5.3
10.106.5.4
```

Se um IP da janela responder ao ping, o scanner descarta aquela sequencia e
continua testando a proxima possibilidade dentro da faixa.

## Requisitos

- Windows com o comando `ping` disponivel no terminal.
- Python 3.10 ou superior.
- Acesso autorizado a rede que sera testada.

## Instalacao

Clone o projeto, crie um ambiente virtual e instale as dependencias declaradas:

```powershell
git clone https://github.com/arielfdev/scripts_ip.git
cd scripts_ip
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No estado atual, o projeto usa apenas a biblioteca padrao do Python. O arquivo
`requirements.txt` permanece preparado para dependencias futuras.

## Execucao

Inicie a interface de terminal:

```powershell
python main.py
```

O programa solicita:

1. Base da rede, por exemplo `10.106.5`.
2. Host inicial, por exemplo `1`.
3. Host final, por exemplo `254`.
4. Quantidade de IPs consecutivos desejada.

## Exemplo no terminal

Exemplo com uma sequencia encontrada:

```text
Busca de sequencia de IPs livres
----------------------------------
Base da rede: 192.0.2
IP inicial: 1
IP final: 10
Quantidade desejada: 4

Resultado
----------------------------------
Sequencia encontrada:
  192.0.2.1
  192.0.2.2
  192.0.2.3
  192.0.2.4
Quantidade de IPs testados: 4
Tempo total: 0.42 segundos
```

Exemplo sem sequencia disponivel:

```text
Busca de sequencia de IPs livres
----------------------------------
Base da rede: 127.0.0
IP inicial: 1
IP final: 1
Quantidade desejada: 1

Resultado
----------------------------------
Nenhuma sequencia livre foi encontrada nessa faixa.
Quantidade de IPs testados: 1
Tempo total: 0.03 segundos
```

Cada busca concluida e registrada em `logs/scan_history.txt` com data e hora,
faixa escaneada, quantidade solicitada, resultado encontrado e tempo total.

## Exemplos por codigo

Validacao direta de um IP por ping:

```python
from core.ping import ping_ip

answered = ping_ip("127.0.0.1")
```

Busca por uma sequencia via scanner:

```python
from core.scanner import find_available_sequence

sequence = find_available_sequence("10.106.5", 1, 254, 4)
```

`find_available_sequence()` retorna uma lista com a primeira sequencia
encontrada ou `None` quando a faixa termina sem um bloco valido.

## Estrutura do projeto

```text
.
|-- core/
|   |-- __init__.py
|   |-- ping.py
|   |-- scanner.py
|   `-- utils.py
|-- logs/
|   |-- .gitkeep
|   `-- scan_history.txt
|-- .gitignore
|-- main.py
|-- README.md
`-- requirements.txt
```

- `main.py`: interface de terminal, validacao de entradas e exibicao final.
- `core/ping.py`: execucao do ping no Windows via `subprocess`.
- `core/scanner.py`: busca sequencial, contagem de IPs testados e resultado.
- `core/utils.py`: gravacao do historico das varreduras.
- `logs/scan_history.txt`: historico local das buscas concluidas.

## Explicacao tecnica

O helper `ping_ip()` executa o comando Windows abaixo com `subprocess`:

```text
ping -n 1 -w 300 IP
```

`-n 1` limita o teste a um pacote ICMP e `-w 300` define um timeout de 300
milissegundos para a resposta. Um codigo de saida `0` e interpretado como IP
que respondeu; falhas do processo, timeout inesperado ou codigo diferente de
zero sao tratados como ausencia de resposta.

O scanner monta cada IPv4 com `ipaddress.IPv4Address`, testa os hosts em ordem
e acumula uma janela corrente de IPs sem resposta. Quando um IP responde ao
ping, a janela e reiniciada. Quando a janela atinge a quantidade solicitada, a
primeira sequencia encontrada e retornada.

## Limitacoes do ping

Um IP sem resposta ao ping nao e garantia de que esteja livre. Alguns hosts,
firewalls e politicas de rede bloqueiam ICMP mesmo quando o endereco esta em
uso. Tambem podem existir respostas inconsistentes por latencia, perda de
pacotes, VPNs, roteamento ou timeout curto.

Use o resultado como indicio inicial. Antes de reservar ou atribuir enderecos
em producao, confirme a disponibilidade pelos processos da rede, como DHCP,
IPAM, inventario, ARP ou validacao com a equipe responsavel.

## Melhorias futuras

- Exportar historico em CSV ou JSON.
- Permitir timeout e tamanho da faixa via argumentos de linha de comando.
- Adicionar testes automatizados para scanner, validacao e logs.
- Suportar outras estrategias de verificacao alem de ICMP.
- Melhorar suporte multiplataforma para Linux e macOS.

## Uso autorizado

Execute varreduras apenas em redes que voce administra ou para as quais recebeu
autorizacao explicita. Testes de rede fora desse escopo podem violar politicas
internas, contratos ou legislacao aplicavel.
