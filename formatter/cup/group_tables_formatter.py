# formatter/group_tables_formatter.py
from config.manager_config import ManagerConfig

SEPARATOR_WIDTH = 50

def format_group_table(group_name, table):
    output = []
    output.append(f"\n{'=' * SEPARATOR_WIDTH}")
    output.append(f"GROUP {group_name}")
    output.append(f"{'=' * SEPARATOR_WIDTH}")

    output.append(
        f"\n{'Pos':<3} {'Team':<5} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'PF':<4} {'PA':<4} {'Diff':<4} {'Pts'}")
    output.append("-" * SEPARATOR_WIDTH)

    for pos, (team, stats) in enumerate(table, 1):
        output.append(
            f"{pos:<3} {team:<5} {stats['played']:<4} {stats['won']:<4} {stats['drawn']:<4} {stats['lost']:<4} "
            f"{stats['points_for']:<4} {stats['points_against']:<4} {stats['points_diff']:<+4} {stats['match_points']}"
        )

    return "\n".join(output)

def format_group_tables(tableA, tableB, current_gameweek):
    """Return current league tables for all groups as a formatted string"""
    output = []
    output.append("=" * SEPARATOR_WIDTH)
    output.append(f"GROUPS (Current: GW{current_gameweek})")
    output.append("=" * SEPARATOR_WIDTH)

    output.append(format_group_table('A', tableA))
    output.append(format_group_table('B', tableB))

    output.append("\n" + "=" * SEPARATOR_WIDTH)
    return "\n".join(output)
