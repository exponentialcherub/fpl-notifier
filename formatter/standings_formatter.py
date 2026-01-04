TEAM_OWNERS = {
	51777: "Andy",
	51792: "Ali",
	51771: "Jim",
	51755: "Sam",
	51778: "Rhys",
	51773: "Roz",
	51753: "Steve",
	51760: "Jord",
	51690: "Joe",
	51757: "Liam"
}

def format_standings(standings, teams):
	message_lines = ["📊 *Current League Standings* 📊\n"]
	for row in standings:
		entry_id = row["league_entry"]
		team_name = teams.get(entry_id, f"Team {entry_id}")
		rank = row["rank"]
		pts = row["total"]
		# played = row["matches_played"]

		if rank == 1:
			medal = "🥇"
		elif rank == 2:
			medal = "🥈"
		elif rank == 3:
			medal = "🥉"
		else:
			medal = "⚽"

		message_lines.append(f"{medal} {rank}. *{TEAM_OWNERS[entry_id]}* {team_name} — {pts} pts")

	return "\n".join(message_lines)