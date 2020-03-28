# Collaborators: Fill in names and SUNetIDs here

def query_one():
    """Query for Stanford's venue"""
    return """
       SELECT
         venue_name,
         venue_capacity
       FROM `bigquery-public-data.ncaa_basketball.mbb_teams`
       WHERE
         school_ncaa = 'Stanford'
    """

def query_two():
    """Query for games in Stanford's venue"""
    return """
       SELECT
         COUNT(venue_city) games_at_stanford
       FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr`
       WHERE
         venue_city = 'Stanford'
         AND season = 2013
    """

def query_three():
    """Query for maximum-red-intensity teams"""
    return """
       SELECT
         market,
         color
       FROM `bigquery-public-data.ncaa_basketball.team_colors`
       WHERE
         color LIKE '#ff%'
         OR color LIKE '#Ff%'
         OR color LIKE '#FF%'
         OR color LIKE '#fF%'
       ORDER BY
         market ASC
    """

def query_four():
    """Query for Stanford's wins at home"""
    return """
       SELECT
         COUNT(game_id) number,
         ROUND(AVG(points_game), 2) avg_stanford,
         ROUND(AVG(opp_points_game), 2) avg_opponent
       FROM `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`
       WHERE
         market = 'Stanford'
         AND home_team = true
         AND win = true
         AND season BETWEEN 2013 AND 2017
    """

def query_five():
    """Query for players for birth city"""
    return """
       SELECT
         COUNT(DISTINCT p.player_id) num_players
       FROM `bigquery-public-data.ncaa_basketball.mbb_players_games_sr` p,
         `bigquery-public-data.ncaa_basketball.mbb_teams` t
       WHERE
         p.team_id = t.id
         AND p.birthplace_city = t.venue_city
         AND p.birthplace_state = t.venue_state
    """

def query_six():
    """Query for biggest blowout"""
    return """
       SELECT
         win_name,
         lose_name,
         win_pts,
         lose_pts,
         (win_pts-lose_pts) margin
       FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games`
       WHERE
         win_pts-lose_pts = (
           SELECT MAX(win_pts-lose_pts)
           FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games`)
    """

def query_seven():
    """Query for historical upset percentage"""
    return """
       SELECT
         ROUND(COUNT(win_seed)*100/(SELECT COUNT(*) FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games`), 2) AS upset_percentage
       FROM `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games`
       WHERE
         win_seed > lose_seed
    """

def query_eight():
    """Query for teams with same states and colors"""
    return """
       SELECT
         a1.name AS teamA,
         a2.name AS teamB,
         a1.venue_state AS state
       FROM `bigquery-public-data.ncaa_basketball.mbb_teams` AS a1
       INNER JOIN `bigquery-public-data.ncaa_basketball.team_colors` AS b1
       ON a1.id = b1.id, `bigquery-public-data.ncaa_basketball.mbb_teams` AS a2
         INNER JOIN `bigquery-public-data.ncaa_basketball.team_colors` AS b2
         ON a2.id = b2.id
       WHERE b1.color = b2.color
         AND a1.venue_state = a2.venue_state
         AND a1.name != a2.name
         AND a1.name < a2.name
       ORDER BY teamA
    """

def query_nine():
    """Query for top geographical locations"""
    return """
       SELECT
         p.birthplace_city AS city,
         p.birthplace_state AS state,
         p.birthplace_country AS country,
         SUM(p.points) AS total_points
       FROM `bigquery-public-data.ncaa_basketball.mbb_players_games_sr` AS p
       WHERE
         p.team_market = 'Stanford'
         AND p.season BETWEEN 2013 AND 2017
       GROUP BY p.birthplace_city, p.birthplace_state, p.birthplace_country
       ORDER BY SUM(p.points) DESC
       LIMIT 3
    """

def query_ten():
    """Query for teams with lots of high-scorers"""
    return """
       SELECT
         team_market,
         COUNT(DISTINCT player_id) AS num_players
       FROM (SELECT player_id, team_market
               FROM `bigquery-public-data.ncaa_basketball.mbb_pbp_sr`
               WHERE
                 period = 1
               GROUP BY game_id, player_id, team_market
               HAVING SUM(points_scored) >= 15)
       GROUP BY team_market
       HAVING COUNT(DISTINCT player_id) > 5
       ORDER BY num_players DESC, team_market
       LIMIT 5
    """

def query_eleven():
    """Query for highest-winner teams"""
    return """
       SELECT market AS team_market,
        COUNT(market) AS top_performer_count
       FROM(SELECT
              a.season,
              a.market,
              a.wins
            FROM `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons` a
            INNER JOIN(
              SELECT season, MAX(wins) AS max_wins
              FROM `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons`
              WHERE
                season BETWEEN 1900 AND 2000
              GROUP BY season
            ) b ON a.season = b.season AND a.wins = b.max_wins)
       GROUP BY market
       HAVING market IS NOT NULL
       ORDER BY top_performer_count DESC, team_market
       LIMIT 5
    """
