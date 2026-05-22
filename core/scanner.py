"""Sequential IP scanning helpers."""

from ipaddress import IPv4Address

from core.ping import ping_ip


def find_available_sequence(
    network_base: str,
    start_ip: int,
    end_ip: int,
    desired_quantity: int,
) -> list[str] | None:
    """Find a consecutive sequence of IPs that do not answer ping requests."""
    _validate_scan_range(network_base, start_ip, end_ip, desired_quantity)

    occupied_ips: list[str] = []
    free_ips: list[str] = []
    current_sequence: list[str] = []
    tested_quantity = 0

    for host_number in range(start_ip, end_ip + 1):
        ip = str(IPv4Address(f"{network_base}.{host_number}"))
        tested_quantity += 1

        # A ping response marks the IP as occupied and breaks the current run.
        if ping_ip(ip):
            occupied_ips.append(ip)
            current_sequence.clear()
            continue

        # No ping response makes the IP apparently free for this scanner.
        free_ips.append(ip)
        current_sequence.append(ip)

        if len(current_sequence) == desired_quantity:
            _show_scan_summary(occupied_ips, free_ips, tested_quantity)
            return current_sequence

    # The range ended before a long enough free sequence was discovered.
    _show_scan_summary(occupied_ips, free_ips, tested_quantity)
    return None


def _validate_scan_range(
    network_base: str,
    start_ip: int,
    end_ip: int,
    desired_quantity: int,
) -> None:
    """Validate the host range before the scanner starts pinging addresses."""
    if desired_quantity <= 0:
        raise ValueError("desired_quantity must be greater than zero.")

    if start_ip > end_ip:
        raise ValueError("start_ip must be less than or equal to end_ip.")

    # Building the boundary addresses verifies the network prefix and host range.
    IPv4Address(f"{network_base}.{start_ip}")
    IPv4Address(f"{network_base}.{end_ip}")


def _show_scan_summary(
    occupied_ips: list[str],
    free_ips: list[str],
    tested_quantity: int,
) -> None:
    """Print the requested scan summary for the operator."""
    print(f"IPs ocupados: {occupied_ips}")
    print(f"IPs livres: {free_ips}")
    print(f"Quantidade testada: {tested_quantity}")
