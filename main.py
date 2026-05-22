"""Terminal entry point for the scripts_ip project."""

from ipaddress import AddressValueError, IPv4Address
from time import perf_counter

from core.scanner import ScanResult, scan_available_sequence
from core.utils import save_scan_history


def main() -> None:
    """Collect scan options from the terminal and show the result."""
    print("Busca de sequencia de IPs livres")
    print("-" * 34)

    try:
        network_base = _read_network_base()
        start_ip = _read_positive_int("IP inicial: ")
        end_ip = _read_positive_int("IP final: ")
        desired_quantity = _read_positive_int("Quantidade desejada: ")

        started_at = perf_counter()
        result = scan_available_sequence(
            network_base,
            start_ip,
            end_ip,
            desired_quantity,
        )
        elapsed_time = perf_counter() - started_at
    except (AddressValueError, ValueError) as error:
        print(f"Entrada invalida: {error}")
        return
    except KeyboardInterrupt:
        print("\nBusca cancelada pelo usuario.")
        return
    except Exception as error:
        print(f"Erro ao executar a busca: {error}")
        return

    _show_result(result, elapsed_time)
    _save_history(
        f"{network_base}.{start_ip}-{network_base}.{end_ip}",
        desired_quantity,
        result,
        elapsed_time,
    )


def _read_network_base() -> str:
    """Read and validate the first three octets of the IPv4 network."""
    network_base = input("Base da rede: ").strip()

    # The boundary address verifies values such as "10.106.5" before scanning.
    IPv4Address(f"{network_base}.0")
    return network_base


def _read_positive_int(prompt: str) -> int:
    """Read a positive integer from the terminal."""
    value = int(input(prompt).strip())

    if value <= 0:
        raise ValueError(f"{prompt.strip(': ')} deve ser maior que zero.")

    return value


def _show_result(result: ScanResult, elapsed_time: float) -> None:
    """Print a compact and readable scan report."""
    print("\nResultado")
    print("-" * 34)

    if result.sequence:
        print("Sequencia encontrada:")
        for ip in result.sequence:
            print(f"  {ip}")
    else:
        print("Nenhuma sequencia livre foi encontrada nessa faixa.")

    print(f"Quantidade de IPs testados: {result.tested_quantity}")
    print(f"Tempo total: {elapsed_time:.2f} segundos")


def _save_history(
    network_range: str,
    desired_quantity: int,
    result: ScanResult,
    elapsed_time: float,
) -> None:
    """Save scan history without hiding an already completed result."""
    try:
        save_scan_history(
            network_range,
            desired_quantity,
            result.sequence,
            elapsed_time,
        )
    except OSError as error:
        print(f"Aviso: nao foi possivel salvar o historico: {error}")


if __name__ == "__main__":
    main()
