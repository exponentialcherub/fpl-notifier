from api.fpl_api import FplTeams

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

def format_standings(standings, teams: FplTeams):
	message_lines = ["📊 *Current League Standings* 📊\n"]
	for row in standings:
		id = row["league_entry"]
		team_name = teams.by_id[id].name
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

		message_lines.append(f"{medal} {rank}. *{TEAM_OWNERS[id]}* {team_name} — {pts} pts")

	return "\n".join(message_lines)