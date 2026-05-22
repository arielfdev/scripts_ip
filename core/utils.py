"""Shared project helpers."""

from datetime import datetime
from pathlib import Path


def save_scan_history(
    network_range: str,
    desired_quantity: int,
    sequence: list[str] | None,
    elapsed_time: float,
) -> None:
    """Append one scan result to the local history file."""
    history_path = Path("logs") / "scan_history.txt"
    history_path.parent.mkdir(exist_ok=True)

    # Store a readable snapshot so past terminal scans can be inspected later.
    result = ", ".join(sequence) if sequence else "Nenhuma sequencia encontrada"
    entry = (
        f"Data/hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Rede escaneada: {network_range}\n"
        f"Quantidade solicitada: {desired_quantity}\n"
        f"Resultado encontrado: {result}\n"
        f"Tempo total: {elapsed_time:.2f} segundos\n"
        "\n"
    )

    with history_path.open("a", encoding="utf-8") as history_file:
        history_file.write(entry)
