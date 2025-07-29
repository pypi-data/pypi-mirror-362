import re
from typing import List, Dict, Union, Any


def parse_system_output_json(cli_output: str) -> Dict[str, Union[str, dict]]:
    """
    Parses CLI output with section headers and key-value pairs into a nested dictionary.

    :param cli_output: Raw CLI output as a string
    :return: Dictionary representing parsed output
    """
    data = {}
    current_section = None
    section_indent = None

    lines = cli_output.strip().splitlines()

    for line in lines:
        indent_match = re.match(r'^(\s+)', line)
        indent = len(indent_match.group(1)) if indent_match else 0
        line = line.strip().rstrip(',')

        if line.endswith(':') and ':' not in line[:-1]:
            section_name = line[:-1].strip()
            data[section_name] = {}
            current_section = data[section_name]
            section_indent = indent
            continue

        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            if current_section is not None and indent > section_indent:
                current_section[key] = value
            else:
                data[key] = value
                current_section = None
                section_indent = None

    return data


def parse_output_json(output: str) -> List[Dict[str, str]]:
    """
    Parses CLI table output with headers and fixed-format rows.

    :param output: Raw CLI output as a string
    :return: List of dictionaries mapping headers to values
    """
    lines = output.strip().splitlines()
    headers = re.split(r"\s{2,}", lines[0].strip())
    vlan_list = []

    for line in lines[2:]:
        if not line.strip():
            continue
        parts = re.split(r"\s{2,}", line.strip())
        vlan_list.append(dict(zip(headers, parts)))

    return vlan_list


def parse_vlan_output_json(output: str) -> List[Dict[str, str]]:
    """
    Parses VLAN CLI output in table format.

    :param output: Raw CLI output as a string
    :return: List of dictionaries per VLAN entry
    """
    return parse_output_json(output)


def parse_interface_status(cli_output: str) -> List[Dict[str, str]]:
    """
    Parses 'show interfaces' status CLI output.

    :param cli_output: Raw CLI output as a string
    :return: List of dictionaries per interface row
    """
    lines = cli_output.strip().splitlines()
    data_lines = []
    in_data = False

    for line in lines:
        if re.match(r"^\s*\d+/\d+/\d+", line):
            in_data = True
        if in_data:
            data_lines.append(line.strip())

    parsed = []
    for line in data_lines:
        parts = re.split(r'\s{2,}', line)
        if len(parts) < 13:
            continue
        parsed.append({
            "port": parts[0],
            "admin_status": parts[1],
            "auto_nego": parts[2],
            "det_speed": parts[3],
            "det_duplex": parts[4],
            "det_pause": parts[5],
            "det_fec": parts[6],
            "cfg_speed": parts[7],
            "cfg_duplex": parts[8],
            "cfg_pause": parts[9],
            "cfg_fec": parts[10],
            "link_trap": parts[11],
            "eee": parts[12],
        })

    return parsed


def parse_interface_detail(cli_output: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Parses 'show interface detail' CLI output including Rx and Tx subsections.

    :param cli_output: Raw CLI output as a string
    :return: Dictionary with top-level and Rx/Tx values
    """
    data = {}
    rx_section = {}
    tx_section = {}

    lines = cli_output.strip().splitlines()
    current_section = "general"

    for line in lines:
        line = line.strip()
        if line.startswith("ACSW"):
            continue
        if line.startswith("Rx"):
            current_section = "rx"
            continue
        elif line.startswith("Tx"):
            current_section = "tx"
            continue

        if ":" in line:
            parts = line.split(":")
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip().rstrip(",")

            if "," in value:
                sub_parts = [v.strip() for v in value.split(",")]
                for sub_part in sub_parts:
                    if ":" in sub_part:
                        sub_key, sub_val = map(str.strip, sub_part.split(":", 1))
                        key = f"{key} / {sub_key}"
                        value = sub_val

            if current_section == "rx":
                rx_section[key] = value
            elif current_section == "tx":
                tx_section[key] = value
            else:
                data[key] = value

    if rx_section:
        data["Rx"] = rx_section
    if tx_section:
        data["Tx"] = tx_section

    return data


def parse_ip_interface_output(cli_output: str) -> List[Dict[str, str]]:
    """
    Parses the 'show ip interface' CLI output into a list of dictionaries.

    :param cli_output: Raw CLI output as a string
    :return: List of dictionaries with parsed interface data
    """
    lines = cli_output.strip().splitlines()
    data_lines = []
    start_parsing = False

    for line in lines:
        if re.match(r'-{10,}', line):
            start_parsing = True
            continue
        if start_parsing and line.strip():
            data_lines.append(line.strip())

    interfaces = []
    for line in data_lines:
        parts = re.split(r'\s{2,}', line)
        if len(parts) >= 5:
            interfaces.append({
                "name": parts[0],
                "ip_address": parts[1],
                "subnet_mask": parts[2],
                "status": parts[3],
                "forward": parts[4],
                "device": parts[5] if len(parts) > 5 else None
            })

    return interfaces

def parse_violation_output_to_json(output: str) -> List[Dict]:
    lines = output.strip().splitlines()

    # Skip header and find data lines
    data_lines = [
        line.strip() for line in lines
        if re.match(r"^\d+/\d+/\d+", line.strip())  # Matches lines starting with port format
    ]

    parsed = []
    for line in data_lines:
        # Example: "1/1/23    AG         admin down          lps shutdown    0     300         10/1 0"
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) < 7:
            continue  # Skip if line is malformed

        # Unpack parts
        port, source, action, reason, wtr, time, max_remain = parts[:7]

        # Handle max/remainder split (e.g., "10/1 0" may come split)
        if '/' in max_remain:
            max_violations, remaining = max_remain.split('/')
        elif len(parts) >= 8 and '/' in parts[6]:
            max_violations, remaining = parts[6].split('/')
        else:
            max_violations = remaining = None

        parsed.append({
            "port": port,
            "source": source,
            "action": action,
            "reason": reason,
            "wait_to_restore": int(wtr),
            "recovery_time": int(time),
            "max_violations": int(max_violations) if max_violations is not None else None,
            "remaining_violations": int(remaining) if remaining is not None else None
        })

    return parsed

def parse_violation_recovery_configuration(cli_output: str) -> Dict[str, Any]:
    result = {
        "global": {},
        "ports": []
    }

    lines = cli_output.strip().splitlines()

    # Parse global values
    for line in lines:
        if "Global Violation Trap" in line:
            match = re.search(r"Global Violation Trap\s*:\s*(\w+)", line)
            if match:
                result["global"]["trap"] = match.group(1)
        elif "Global Recovery Maximum" in line:
            match = re.search(r"Global Recovery Maximum\s*:\s*(\d+)", line)
            if match:
                result["global"]["recovery_maximum"] = int(match.group(1))
        elif "Global Recovery Time" in line:
            match = re.search(r"Global Recovery Time\s*:\s*(\d+)", line)
            if match:
                result["global"]["recovery_time"] = int(match.group(1))

    # Parse port-specific values
    port_data_started = False
    for line in lines:
        if re.match(r"^\s*Port\s+Recovery Max\s+Recovery Time", line):
            port_data_started = True
            continue
        if port_data_started and re.match(r"^\s*\d+/\d+/\d+", line):
            parts = line.strip().split()
            if len(parts) >= 3:
                port_entry = {
                    "port": parts[0],
                    "recovery_maximum": int(parts[1]),
                    "recovery_time": int(parts[2])
                }
                result["ports"].append(port_entry)

    return result

import re
from typing import List, Dict

def parse_interfaces_capability(cli_output: str) -> List[Dict[str, str]]:
    lines = cli_output.strip().splitlines()
    result = []
    
    # Skip headers
    header_regex = re.compile(r"^\s*Ch/Slot/Port\s+AutoNeg\s+Pause\s+Crossover", re.IGNORECASE)
    cap_entries = {}
    
    for line in lines:
        line = line.strip()
        if not line or header_regex.match(line):
            continue

        parts = line.split()

        # Match CAP lines
        if len(parts) >= 9 and parts[1] == "CAP":
            port_id = parts[0]
            cap_entries[port_id] = {
                "port": port_id,
                "autoneg_cap": parts[2],
                "pause_cap": parts[3],
                "crossover_cap": parts[4],
                "speed_cap": parts[5],
                "duplex_cap": parts[6],
                "macsec_cap": parts[7],
                "macsec_256_cap": parts[8]
            }

        # Match DEF lines
        elif len(parts) >= 6 and parts[1] == "DEF":
            port_id = parts[0]
            if port_id in cap_entries:
                cap_entries[port_id].update({
                    "autoneg_default": parts[2],
                    "pause_default": parts[3],
                    "crossover_default": parts[4],
                    "speed_default": parts[5],
                    "duplex_default": parts[6] if len(parts) > 6 else None
                })

    return list(cap_entries.values())


def parse_interface_accounting(output: str) -> Dict[str, int]:
    """
    Parses the CLI output of 'show interfaces port <port> accounting' into a dictionary.

    Args:
        output: CLI output as a string.

    Returns:
        Dictionary mapping each metric to its integer value.
    """
    metrics = {}
    lines = output.splitlines()

    # Skip the port line (e.g., "1/1/2:")
    for line in lines[1:]:
        # Normalize line: remove trailing commas and split on commas
        parts = [p.strip().rstrip(',') for p in line.strip().split(',') if p.strip()]
        for part in parts:
            # Match patterns like: "Rx Undersize             =                    0"
            match = re.match(r"(.+?)=\s*(\d+)", part)
            if match:
                key = match.group(1).strip().replace(" ", "_")
                value = int(match.group(2))
                metrics[key] = value

    return metrics

def parse_interface_counters(output: str) -> Dict[str, int]:
    """
    Parses 'show interfaces port <port> counters' CLI output into a dictionary.

    Args:
        output: CLI raw string from the command.

    Returns:
        Dictionary of counters with their values.
    """
    counters = {}
    lines = output.splitlines()

    for line in lines:
        # Remove trailing commas, split by commas, and clean up
        parts = [p.strip().rstrip(',') for p in line.strip().split(',') if p.strip()]
        for part in parts:
            match = re.match(r"(.+?)=\s*([\d]+)", part)
            if match:
                key = match.group(1).strip().replace(" ", "_")
                value = int(match.group(2))
                counters[key] = value

    return counters

def parse_interface_counters_errors(output: str) -> Dict[str, float]:
    """
    Parses 'show interfaces port <port> counters errors' CLI output into a dictionary.

    Args:
        output: CLI output string.

    Returns:
        Dictionary with error counter names and numeric values (float or int).
    """
    errors = {}
    lines = output.splitlines()

    for line in lines:
        # Split on commas
        parts = [part.strip() for part in line.split(',') if part.strip()]
        for part in parts:
            match = re.match(r"(.+?)\s*=\s*([\d.Ee+-]+)", part)
            if match:
                key = match.group(1).strip().replace(" ", "_")
                value_str = match.group(2)
                value = float(value_str) if 'e' in value_str.lower() or '.' in value_str else int(value_str)
                errors[key] = value

    return errors


