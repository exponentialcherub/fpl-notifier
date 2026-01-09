# formatter/group_tables_formatter.py
from config.manager_config import ManagerConfig


def format_group_table(group_name, table):
    output = []
    output.append(f"\n{'=' * 100}")
    output.append(f"GROUP {group_name}")
    output.append(f"{'=' * 100}")

    output.append(
        f"\n{'Pos':<5} {'Team':<20} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'PF':<6} {'PA':<6} {'Diff':<7} {'Pts':<5}")
    output.append("-" * 75)

    for pos, (team, stats) in enumerate(table, 1):
        output.append(
            f"{pos:<5} {team:<20} {stats['played']:<4} {stats['won']:<4} {stats['drawn']:<4} {stats['lost']:<4} "
            f"{stats['points_for']:<6} {stats['points_against']:<6} {stats['points_diff']:<+7} {stats['match_points']:<5}")

    return "\n".join(output)

def format_group_tables(tableA, tableB, current_gameweek):
    """Return current league tables for all groups as a formatted string"""
    output = []
    output.append("=" * 100)
    output.append(f"FPL DRAFT CUP - LEAGUE TABLES (Current: GW{current_gameweek})")
    output.append("=" * 100)

    output.append(format_group_table('A', tableA))
    output.append(format_group_table('B', tableB))

    output.append("\n" + "=" * 100)
    return "\n".join(output)
