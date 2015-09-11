#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    dbConnection = connect()
    cursor = dbConnection.cursor()
    cursor.execute("DELETE FROM matches")
    dbConnection.commit()
    dbConnection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    dbConnection = connect()
    cursor = dbConnection.cursor()
    cursor.execute("DELETE FROM players")
    dbConnection.commit()
    dbConnection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    dbConnection = connect()
    cursor = dbConnection.cursor()
    cursor.execute("SELECT COUNT(*) FROM players")
    playerCount = cursor.fetchall()[0][0]
    dbConnection.close()
    return playerCount


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    dbConnection = connect()
    cursor = dbConnection.cursor()
    cursor.execute("INSERT INTO players (player_name) VALUES (%s)", (name,))
    dbConnection.commit()
    dbConnection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    on the chance of tie on any given place, the players are ranked
    according to OMW (Opponent Match Wins), the total number of wins
    by players they have played against.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    dbConnection = connect()
    cursor = dbConnection.cursor()
    cursor.execute("SELECT id, name, wins, matches FROM standings")
    standings = cursor.fetchall()
    dbConnection.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    dbConnection = connect()
    cursor = dbConnection.cursor()
    cursor.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)",
                   (winner, loser))
    dbConnection.commit()
    dbConnection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    playerCount = countPlayers()
    pairings = []
    # Starting from the first player and for the total of players
    # in the list, every other player gets paired with the next one.
    for i in range(0, playerCount, 2):
        pair = (standings[i][0], standings[i][1], standings[i+1][0],
                standings[i+1][1])
        pairings.append(pair)
    return pairings
