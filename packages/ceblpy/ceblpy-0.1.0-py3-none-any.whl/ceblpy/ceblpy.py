import pandas as pd
from . import helpers as h
from datetime import datetime


def load_cebl_schedule(seasons=None):
    """
    Load cleaned CEBL schedule data from the cebl data repository.

    Parameters
    ----------
    seasons : int, list of int, or None, optional
        Season(s) to load. By default, None loads all available seasons.
        - int : Single season year (e.g., 2020)
        - list of int : Multiple seasons (e.g., [2019, 2020, 2021])
        - None : Load all available seasons

        All years must be 2019 or later.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the schedule with the following columns:

        ================================  ===========
        Column Name                        Type
        ================================  ===========
        fiba_id                            int
        season                             int
        start_time_utc                     datetime
        status                             str
        competition                        str
        venue_name                         str
        period                             float
        home_team_id                       int
        home_team_name                     str
        home_team_score                    float
        home_team_logo_url                 str
        home_team_url_stats_en             str
        home_team_url_stats_fr             str
        away_team_id                       int
        away_team_name                     str
        away_team_score                    float
        away_team_logo_url                 str
        away_team_url_stats_en             str
        away_team_url_stats_fr             str
        stats_url_en                       str
        stats_url_fr                       str
        cebl_stats_url_en                  str
        cebl_stats_url_fr                  str
        tickets_url_en                     str
        tickets_url_fr                     str
        id                                 int
        fiba_json_url                      str
        ================================  ===========


    Examples
    --------
    >>> load_cebl_schedule(2020)
    >>> load_cebl_schedule([2019, 2020, 2021])
    >>> load_cebl_schedule()
    """
    if isinstance(seasons, int):
        seasons = [seasons]
    if isinstance(seasons, list):
        h.validate_seasons(seasons)
    elif seasons is None:
        seasons = list(range(2019, datetime.now().year + 1))
    else:
        raise TypeError(f"Expected seasons to be an int, list of ints, or None, got {type(seasons).__name__}")
    
    schedule = pd.read_csv("https://github.com/ryanndu/cebl-data/releases/download/schedule/cebl_schedule.csv")
    schedule = schedule[schedule['season'].isin(seasons)]
    return schedule


def load_cebl_team_boxscore(seasons=None):
    """
    Load cleaned CEBL team boxscore data from the cebl data repository.

    Parameters
    ----------
    seasons : int, list of int, or None, optional
        Season(s) to load. By default, None loads all available seasons.
        - int : Single season year (e.g., 2020)
        - list of int : Multiple seasons (e.g., [2019, 2020, 2021])
        - None : Load all available seasons

        All years must be 2019 or later.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the team boxscore with the following columns:

        ==============================================  ===========
        Column Name                                      Type
        ==============================================  ===========
        game_id                                          int
        season                                           int
        team_name                                        str
        short_name                                       str
        code                                             str
        team_score                                       int
        minutes                                          str
        field_goals_made                                 int
        field_goals_attempted                            int
        field_goal_percentage                            int
        two_point_field_goals_made                       int
        two_point_field_goals_attempted                  int
        two_point__percentage                            int
        three_point_field_goals_made                     int
        three_point_field_goals_attempted                int
        three_point_percentage                           int
        free_throws_made                                 int
        free_throws_attempted                            int
        free_throw_percentage                            int
        offensive_rebounds                               int
        defensive_rebounds                               int
        rebounds                                         int
        assists                                          int
        steals                                           int
        turnovers                                        int
        blocks                                           int
        blocks_received                                  int
        personal_fouls                                   int
        fouls_drawn                                      int
        total_fouls                                      int
        bonus_fouls                                      int
        points_in_the_paint                              int
        second_chance_points                             int
        points_from_turnovers                            int
        bench_points                                     int
        fast_break_points                                int
        team_index_rating                                int
        team_index_rating_2                              int
        team_index_rating_3                              float
        team_index_rating_4                              float
        team_index_rating_5                              int
        team_index_rating_6                              int
        team_index_rating_7                              int
        team_fouls                                       int
        team_turnovers                                   int
        team_rebounds                                    int
        team_defensive_rebounds                          int
        team_offensive_rebounds                          int
        period_1_score                                   int
        period_2_score                                   float
        period_3_score                                   float
        period_4_score                                   float
        biggest_lead                                     float
        biggest_scoring_run                              float
        time_leading                                     float
        lead_changes                                     int
        times_scores_level                               int
        timeouts_left                                    int
        head_coach                                       str
        assistant_coach_1                                str
        assistant_coach_2                                str
        international_team_name                          str
        international_short_name                         str
        international_code                               str
        logo                                             str
        logo_t_url                                       str
        logo_t_size                                      str
        logo_t_height                                    int
        logo_t_width                                     int
        logo_t_bytes                                     int
        logo_s_url                                       str
        logo_s_size                                      str
        logo_s_height                                    int
        logo_s_width                                     int
        logo_s_bytes                                     int
        ==============================================  ===========

    Examples
    --------
    >>> load_cebl_team_boxscore(2020)
    >>> load_cebl_team_boxscore([2019, 2020, 2021])
    >>> load_cebl_team_boxscore()
    """
    if isinstance(seasons, int):
        seasons = [seasons]
    if isinstance(seasons, list):
        h.validate_seasons(seasons)
    elif seasons is None:
        seasons = list(range(2019, datetime.now().year + 1))
    else:
        raise TypeError(f"Expected seasons to be an int, list of ints, or None, got {type(seasons).__name__}")
    
    team_boxscore = pd.read_csv("https://github.com/ryanndu/cebl-data/releases/download/team-boxscore/cebl_teams.csv")
    team_boxscore = team_boxscore[team_boxscore['season'].isin(seasons)]
    return team_boxscore


def load_cebl_player_boxscore(seasons=None):
    """
    Load cleaned CEBL player boxscore data from the cebl data repository.

    Parameters
    ----------
    seasons : int, list of int, or None, optional
        Season(s) to load. By default, None loads all available seasons.
        - int : Single season year (e.g., 2020)
        - list of int : Multiple seasons (e.g., [2019, 2020, 2021])
        - None : Load all available seasons

        All years must be 2019 or later.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the player boxscore with the following columns:

        ======================================  ===========
        Column Name                              Type
        ======================================  ===========
        game_id                                  int
        season                                   int
        team_name                                str
        player_number                            int
        player_name                              str
        player_position                          str
        minutes                                  str
        points                                   int
        field_goals_made                         int
        field_goals_attempted                    int
        field_goal_percentage                    int
        two_point_field_goals_made               int
        two_point_field_goals_attempted          int
        two_point__percentage                    int
        three_point_field_goals_made             int
        three_point_field_goals_attempted        int
        three_point_percentage                   int
        free_throws_made                         int
        free_throws_attempted                    int
        free_throw_percentage                    int
        offensive_rebounds                       int
        defensive_rebounds                       int
        rebounds                                 int
        assists                                  int
        turnovers                                int
        steals                                   int
        blocks                                   int
        blocks_received                          int
        personal_fouls                           int
        fouls_drawn                              int
        plus_minus                               int
        index_rating                             int
        index_rating_2                           int
        index_rating_3                           float
        index_rating_4                           float
        index_rating_5                           int
        index_rating_6                           int
        index_rating_7                           int
        second_chance_points                     int
        fast_break_points                        int
        points_in_the_paint                      int
        first_name                               str
        first_name_initial                       str
        last_name                                str
        last_name_initial                        str
        international_first_name                 str
        international_first_name_initial         str
        international_last_name                  str
        international_last_name_initial          str
        scoreboard_name                          str
        active                                   bool
        starter                                  bool
        captain                                  bool
        photo_t                                  str
        photo_s                                  str
        ======================================  ===========

    Examples
    --------
    >>> load_cebl_player_boxscore(2020)
    >>> load_cebl_player_boxscore([2019, 2020, 2021])
    >>> load_cebl_player_boxscore()
    """
    if isinstance(seasons, int):
        seasons = [seasons]
    if isinstance(seasons, list):
        h.validate_seasons(seasons)
    elif seasons is None:
        seasons = list(range(2019, datetime.now().year + 1))
    else:
        raise TypeError(f"Expected seasons to be an int, list of ints, or None, got {type(seasons).__name__}")
    
    player_boxscore = pd.read_csv("https://github.com/ryanndu/cebl-data/releases/download/player-boxscore/cebl_players.csv")
    player_boxscore = player_boxscore[player_boxscore['season'].isin(seasons)]
    return player_boxscore


def load_cebl_officials(seasons=None):
    """
    Load cleaned CEBL officials data from the cebl data repository.

    Parameters
    ----------
    seasons : int, list of int, or None, optional
        Season(s) to load. By default, None loads all available seasons.
        - int : Single season year (e.g., 2020)
        - list of int : Multiple seasons (e.g., [2019, 2020, 2021])
        - None : Load all available seasons

        All years must be 2019 or later.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the officials with the following columns:

        ================================  ===========
        Column Name                        Type
        ================================  ===========
        game_id                            int
        season                             int
        officials_type                     str
        officials_name                     str
        first_name                         str
        last_name                          str
        scoreboard_name                    str
        first_name_initial                 str
        last_name_initial                  str
        international_first_name           str
        international_first_name_initial   str
        international_last_name            str
        international_last_name_initial    str
        scoreboard_name                    str
        ================================  ===========
        
    Examples
    --------
    >>> load_cebl_officials(2020)
    >>> load_cebl_officials([2019, 2020, 2021])
    >>> load_cebl_officials_boxscore()
    """
    if isinstance(seasons, int):
        seasons = [seasons]
    if isinstance(seasons, list):
        h.validate_seasons(seasons)
    elif seasons is None:
        seasons = list(range(2019, datetime.now().year + 1))
    else:
        raise TypeError(f"Expected seasons to be an int, list of ints, or None, got {type(seasons).__name__}")
    
    officials = pd.read_csv("https://github.com/ryanndu/cebl-data/releases/download/officials/cebl_officials.csv")
    officials = officials[officials['season'].isin(seasons)]
    return officials


def load_cebl_coaches(seasons=None):
    """
    Load cleaned CEBL coaches data from the cebl data repository.

    Parameters
    ----------
    seasons : int, list of int, or None, optional
        Season(s) to load. By default, None loads all available seasons.
        - int : Single season year (e.g., 2020)
        - list of int : Multiple seasons (e.g., [2019, 2020, 2021])
        - None : Load all available seasons

        All years must be 2019 or later.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the coaches with the following columns:

        ================================  ===========
        Column Name                        Type
        ================================  ===========
        game_id                            int
        season                             int
        team_name                          str
        coach_name                         str
        coach_type                         str
        first_name                         str
        first_name_initial                 str
        last_name                          str
        last_name_initial                  str
        international_first_name           str
        international_first_name_initial   str
        international_last_name            str
        international_last_name_initial    str
        scoreboard_name                    str
        ================================  ===========
        
    Examples
    --------
    >>> load_cebl_coaches(2020)
    >>> load_cebl_coaches([2019, 2020, 2021])
    >>> load_cebl_coaches()
    """
    if isinstance(seasons, int):
        seasons = [seasons]
    if isinstance(seasons, list):
        h.validate_seasons(seasons)
    elif seasons is None:
        seasons = list(range(2019, datetime.now().year + 1))
    else:
        raise TypeError(f"Expected seasons to be an int, list of ints, or None, got {type(seasons).__name__}")
    
    coaches = pd.read_csv("https://github.com/ryanndu/cebl-data/releases/download/coaches/cebl_coaches.csv")
    coaches = coaches[coaches['season'].isin(seasons)]
    return coaches


def load_cebl_pbp(seasons=None):
    """
    Load cleaned CEBL pbp data from the cebl data repository.

    Parameters
    ----------
    seasons : int, list of int, or None, optional
        Season(s) to load. By default, None loads all available seasons.
        - int : Single season year (e.g., 2020)
        - list of int : Multiple seasons (e.g., [2019, 2020, 2021])
        - None : Load all available seasons

        All years must be 2019 or later.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the pbp with the following columns:

        ================================  ===========
        Column Name                        Type
        ================================  ===========
        game_id                            int
        season                             int
        game_time                          str
        home_score                         int
        away_score                         int
        home_lead                          int
        team_id                            int
        period                             int
        period_type                        str
        player_id                          int
        scoreboard_name                    str
        success                            int
        action_type                        str
        action_number                      float
        previous_action                    float
        sub_type                           str
        scoring                            int
        shirt_number                       float
        player_name                        str
        first_name                         str
        last_name                          str
        x                                  float
        y                                  float
        qualifier_0                        str
        qualifier_1                        str
        qualifier_2                        str
        qualifier_3                        str
        international_first_name           str
        international_last_name            str
        international_first_name_initial   str
        international_last_name_initial    str
        ================================  ===========
        
    Examples
    --------
    >>> load_cebl_pbp(2020)
    >>> load_cebl_pbp([2019, 2020, 2021])
    >>> load_cebl_pbp()
    """
    if isinstance(seasons, int):
        seasons = [seasons]
    if isinstance(seasons, list):
        h.validate_seasons(seasons)
    elif seasons is None:
        seasons = list(range(2019, datetime.now().year + 1))
    else:
        raise TypeError(f"Expected seasons to be an int, list of ints, or None, got {type(seasons).__name__}")
    
    pbp = pd.DataFrame()
    for season in seasons:
        pbp = pd.concat([pbp, pd.read_csv(f"https://github.com/ryanndu/cebl-data/releases/download/pbp/cebl_pbp_{season}.csv")])
    return pbp