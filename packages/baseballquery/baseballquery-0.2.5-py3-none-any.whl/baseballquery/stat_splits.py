import pandas as pd 
from .stat_calculator import BattingStatsCalculator, PitchingStatsCalculator
from .utils import get_years, get_linear_weights
from collections import defaultdict


class StatSplits:
    def __init__(self, start_year: int = 0, end_year: int = 0, years_list: list[int] | None = None, events: pd.DataFrame | None = None):
        """
        Parent class. Should not be instantiated directly
        """

        self.linear_weights = get_linear_weights()  # type: ignore
        self.sql_query_where = defaultdict(str)

        years = get_years()
        if years_list is not None:
            all_years = set(years_list)
            years = [year for year in years if year in all_years]
            self.sql_query_where["year"] = f"events.year IN ({', '.join([str(year) for year in years])})"
        else:
            if start_year not in years:
                raise ValueError(
                    f"Start year {start_year} not found in database. Did you remember to run baseballquery.update_data()?"
                )
            if end_year not in years:
                raise ValueError(
                    f"End year {end_year} not found in database. Did you remember to run baseballquery.update_data()"
                )
            self.sql_query_where["year"] = f"{start_year} <= events.year AND events.year <= {end_year}"

        self.stats: pd.DataFrame = pd.DataFrame()
        self.split = "year"
        self.find = "player"

    def set_split(self, split: str):
        """
        Set the split to be used for calculating pitching stats.

        Parameters:
        split (str): 'year', 'month', 'career', 'game'
        """
        split = split.lower()
        assert split in [
            "year",
            "month",
            "career",
            "game",
        ], f"Invalid split {split}. Valid splits are 'year', 'month', 'career', 'game'"
        self.split = split

    def set_subdivision(self, subdivision: str):
        """
        Set the sub-division to be used for calculating pitching stats.

        Parameters:
        subdivision (str): 'player' for individual players, 'team' for team totals
        """
        subdivision = subdivision.lower()
        assert subdivision in [
            "player",
            "team",
        ], f"Invalid sub-division {subdivision}. Valid sub-divisions are 'player', 'team'"
        self.find = subdivision

    def set_days_of_week(self, days_of_week: list[str]):
        """
        Limit the data to only include games played on certain days of the week.

        Parameters:
        days_of_week (list): List of days of the week to include. Valid values are "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        """
        if len(days_of_week) == 0:
            self.sql_query_where.pop("day_week", None)
            return
        assert all(
            day.capitalize()
            in [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            for day in days_of_week
        ), "Invalid day of week"
        for idx, day in enumerate(days_of_week):
            days_of_week[idx] = day.capitalize()
        self.sql_query_where["day_week"] = f"cwgame.GAME_DY IN ({', '.join([f'\'{day}\'' for day in days_of_week])})"

    def set_batter_handedness_pa(self, handedness: str):
        """
        Limit the data to only include plate appearances with batters hitting on a certain side of the plate.
        Switch hitters are considered the handedness they're currently hitting with.
        If data is unknown (not likely to happen after ~1970s or 1980s) it will be excluded.

        Parameters:
        handedness (str): 'R' for right-handed batters, 'L' for left-handed batters
        """
        handedness = handedness.upper()
        assert handedness in [
            "R",
            "L",
        ], "Invalid handedness. Valid values are 'R' and 'L'"
        self.sql_query_where["bat_hand_pa"] = f"events.RESP_BAT_HAND_CD = '{handedness}'"

    def set_pitcher_handedness(self, handedness: str):
        """
        Limit the data to only include plate appearances with pitchers pitching with a certain hand
        If data is unknown (not likely to happen after ~1970s or 1980s) it will be excluded.

        If someone is still using this by the time switch pitchers start to dominate pitching, open an issue on GitHub.

        Parameters:
        handedness (str): 'R' for right-handed pitchers, 'L' for left-handed pitchers
        """
        handedness = handedness.upper()
        assert handedness in [
            "R",
            "L",
        ], "Invalid handedness. Valid values are 'R' or 'L'"
        self.sql_query_where["pit_hand_pa"] = f"events.RESP_PIT_HAND_CD = '{handedness}'"

    def set_batter_starter(self, starter: bool):
        """
        Limit the data to only include plate appearances with batters who started the game.

        Parameters:
        starter (bool): True for starters, False for non-starters
        """
        self.sql_query_where["bat_starter"] = f"events.RESP_BAT_START_FL = '{str(starter).upper()}'"

    def set_pitcher_starter(self, starter: bool):
        """
        Limit the data to only include plate appearances with pitchers who started the game.

        Parameters:
        starter (bool): True for starters, False for non-starters
        """
        self.sql_query_where["pit_starter"] = f"events.RESP_PIT_START_FL = '{str(starter).upper()}'"

    def set_batter_lineup_pos(self, lineup_pos: list[int]):
        """
        Limit the data to only include plate appearances with batters who batted in a certain lineup position.

        Parameters:
        lineup_pos (int): 1-9 for lineup position
        """
        assert all(1 <= i <= 9 for i in lineup_pos), "Invalid lineup position"
        self.sql_query_where["bat_lineup_pos"] = f"events.BAT_LINEUP_ID IN ({', '.join([str(pos) for pos in lineup_pos])})"

    def set_player_field_position(self, field_pos: list[int]):
        """
        Limit the data to only include plate appearances with players who played a certain field position.

        Parameters:
        field_pos (int): 1-12 for field position.
            - 1-9 are the standard fielding positions, 10 is the DH, 11 is a pinch hitter, 12 is a pinch runner (this last one almost certainly will return 0 results)
        """
        assert all(1 <= i <= 12 for i in field_pos), "Invalid field position"
        self.sql_query_where["bat_fld_pos"] = f"events.BAT_FLD_CD IN ({', '.join([str(pos) for pos in field_pos])})"

    def set_batter_home(self, home: bool):
        """
        Limit the data to only include plate appearances with batters who batted at home or away.

        Parameters:
        home (bool): True for home, False for away
        """
        if home:
            self.sql_query_where["bat_team_home"] = "events.HOME_TEAM_ID = events.BAT_TEAM_ID"
        else:
            self.sql_query_where["bat_team_away"] = "events.HOME_TEAM_ID != events.BAT_TEAM_ID"

    def set_pitcher_home(self, home: bool):
        """
        Limit the data to only include plate appearances with pitchers who pitched at home or away.

        Parameters:
        home (bool): True for home, False for away
        """
        if home:
            self.sql_query_where["pit_team_home"] = "events.HOME_TEAM_ID = events.FLD_TEAM_ID"
        else:
            self.sql_query_where["pit_team_away"] = "events.HOME_TEAM_ID != events.FLD_TEAM_ID"

    def set_pitching_team(self, teams: list[str]):
        """
        Limit the data to only include games with certain teams pitching.

        Parameters:
        teams (list): List of team abbreviations (the retrosheet ones, e.g. "BOS", "NYA")
        """
        if len(teams) == 0:
            self.sql_query_where.pop("fld_team_id", None)
            return
        assert all(len(team) == 3 for team in teams), "Invalid team abbreviation. Team abbreviations must be exactly 3 uppercase alphabetic characters."
        assert all(len(team) == 3 for team in teams), "Invalid team abbreviation"
        assert all(team.isupper() for team in teams), "Team abbreviations must be uppercase"
        assert all(team.isalpha() for team in teams), "Team abbreviations must be alphabetic"
        self.sql_query_where["fld_team_id"] = f"events.FLD_TEAM_ID IN ({', '.join(f'\'{team}\'' for team in teams)})"

    def set_batting_team(self, teams: list[str]):
        """
        Limit the data to only include PAs with certain teams batting.

        Parameters:
        teams (list): List of team abbreviations (the retrosheet ones, e.g. "BOS", "NYA")
        """
        if len(teams) == 0:
            self.sql_query_where.pop("bat_team_id", None)
            return
        assert all(len(team) == 3 for team in teams), "Invalid team abbreviation. Team abbreviations must be exactly 3 uppercase alphabetic characters."
        assert all(len(team) == 3 for team in teams), "Invalid team abbreviation"
        assert all(team.isupper() for team in teams), "Team abbreviations must be uppercase"
        assert all(team.isalpha() for team in teams), "Team abbreviations must be alphabetic"
        self.sql_query_where["bat_team_id"] = f"events.BAT_TEAM_ID IN ({', '.join(f'\'{team}\'' for team in teams)})"

    def set_innings(self, innings: list[int]):
        """
        Limit the data to only include PAs with certain innings.

        Parameters:
        innings (list[int]): 1-infinity for the inning number
        """
        if len(innings) == 0:
            self.sql_query_where.pop("inn_ct", None)
            return
        assert all(1 <= inning for inning in innings), "Invalid inning"
        self.sql_query_where["inn_ct"] = f"events.INN_CT IN ({', '.join([str(inning) for inning in innings])})"

    def set_outs(self, outs: list[int]):
        """
        Limit the data to only include PAs with certain number of outs.

        Parameters:
        outs (list[int]): 0-2 for the number of outs
        """
        if len(outs) == 0:
            self.sql_query_where.pop("outs_ct", None)
            return
        assert all(0 <= out < 3 for out in outs), "Invalid number of outs"
        self.sql_query_where["outs_ct"] = f"events.OUTS_CT IN ({', '.join([str(out) for out in outs])})"

    def set_count(self, counts: list[str]):
        """
        Limit the data to only include PAs which contain certain counts.

        Parameters:
        count (list[str]): List of counts in the format "balls-strikes" (e.g. "0-0", "1-2", "3-2")
        """
        if len(counts) == 0:
            self.sql_query_where.pop("count", None)
            return
        assert all(len(c) == 3 and c[1] == '-' for c in counts), "Invalid count format. Must be in the format 'balls-strikes' (e.g. '0-0', '1-2', '3-2')"
        assert all(c[0].isdigit() and c[2].isdigit() for c in counts), "Invalid count format. Must be in the format 'balls-strikes' (e.g. '0-0', '1-2', '3-2')"
        queries_count = []
        for count in counts:
            balls, strikes = count.split('-')
            queries_count.append(f"events.\"{balls}-{strikes}\" = 1")
        self.sql_query_where["count"] = f"({' OR '.join(queries_count)})"

    def set_strikes_end(self, strikes: list[int]):
        """
        Limit the data to only include PAs that end with certain number of strikes (e.g. 3 for a strikeout, 1 for a hit on a 3-1 count).

        With these functions, if you want to get at bats which ended on an 0-2 count, you would use set_strikes_end([2, 3]) and set_balls_end([0,]).

        Parameters:
        strikes (list[int]): 0-3 for the number of strikes
        """
        if len(strikes) == 0:
            self.sql_query_where.pop("strikes_ct", None)
            return
        assert all(0 <= strike <= 3 for strike in strikes), "Invalid number of strikes"
        self.sql_query_where["strikes_ct"] = f"events.STRIKES_CT IN ({', '.join([str(strike) for strike in strikes])})"

    def set_balls_end(self, balls: list[int]):
        """
        Limit the data to only include PAs that end with certain number of balls (e.g. 4 for a walk, 3 for a hit on a 3-2 count).

        Parameters:
        balls (list[int]): 0-4 for the number of balls
        """
        if len(balls) == 0:
            self.sql_query_where.pop("balls_ct", None)
            return
        assert all(0 <= ball <= 4 for ball in balls), "Invalid number of balls"
        self.sql_query_where["balls_ct"] = f"events.BALLS_CT IN ({', '.join([str(ball) for ball in balls])})"

    def set_home_score(self, scores: list[int]):
        """
        Limit the data to only include PAs with a certain home team score.

        Parameters:
        scores (list[int]): Any integer for the home team score
        """
        if len(scores) == 0:
            self.sql_query_where.pop("home_score_ct", None)
            return
        assert all(score >= 0 for score in scores), "Invalid home team score"
        self.sql_query_where["home_score_ct"] = f"events.HOME_SCORE_CT IN ({', '.join([str(score) for score in scores])})"

    def set_away_score(self, scores: list[int]):
        """
        Limit the data to only include PAs with a certain away team score.

        Parameters:
        scores (list[int]): Any integer for the away team score
        """
        if len(scores) == 0:
            self.sql_query_where.pop("away_score_ct", None)
            return
        assert all(score >= 0 for score in scores), "Invalid away team score"
        self.sql_query_where["away_score_ct"] = f"events.AWAY_SCORE_CT IN ({', '.join([str(score) for score in scores])})"

    def set_base_situation(self, base_situations: list[int]):
        """
        Limit the data to only include PAs with certain base situations at the start of the play (e.g. if a runner on first steals second, the base situation would be 0b001 at the start of the play).

        Parameters:
        base_situation (list[int]): List of integers no more than 2^3 for the base situation. 0 is empty, 1 is occupied. For example, 0b111 = 7 = bases loaded, 0b000 = 0 = bases empty, 0b001 = 1 = runner on first, 0b100 = 4 = runner on third
        """
        if len(base_situations) == 0:
            self.sql_query_where.pop("start_bases_cd", None)
            return
        assert all((0 <= base_situation < 8) for base_situation in base_situations), "Invalid base situation"  # type: ignore
        self.sql_query_where["start_bases_cd"] = f"events.START_BASES_CD IN ({', '.join([str(base_situation) for base_situation in base_situations])})"


class BattingStatSplits(StatSplits):
    def __init__(self, start_year: int = 0, end_year: int = 0, years_list: list[int] | None = None, events: pd.DataFrame | None = None):
        """
        Class to calculate batting splits.
        """
        super().__init__(start_year, end_year, years_list=years_list, events=events)
        self.batting_calculator: BattingStatsCalculator | None = None

    def calculate_stats(self):
        """
        Calculate batting stats based on the set splits.
        This method should be run after all splits have been set.
        """
        # Formulate "WHERE" clause for SQL query
        where_clauses = [self.sql_query_where[key] for key in self.sql_query_where]
        where_clause = " AND ".join(where_clauses)

        self.batting_calculator = BattingStatsCalculator(self.linear_weights, find=self.find, split=self.split, query_where=where_clause)  # type: ignore
        self.batting_calculator.calculate_all_stats()
        self.stats = self.batting_calculator.stats

    def set_score_diff(self, score_diff: list[int]):
        """
        Limit the data to only include PAs with a certain score difference (positive means batting team is leading).

        Parameters:
        score_diff (list[int]): Any integer for the score difference
        """
        if len(score_diff) == 0:
            self.sql_query_where.pop("score_diff", None)
            return
        assert all(isinstance(diff, int) for diff in score_diff), "Invalid score difference. Must be a list of integers."
        self.sql_query_where["score_diff"] = f"CASE WHEN events.BAT_TEAM_ID = events.HOME_TEAM_ID THEN (events.HOME_SCORE_CT - events.AWAY_SCORE_CT) ELSE (events.AWAY_SCORE_CT - events.HOME_SCORE_CT) END IN ({', '.join([str(diff) for diff in score_diff])})"


class PitchingStatSplits(StatSplits):
    def __init__(self, start_year: int = 0, end_year: int = 0, years_list: list[int] | None = None, events: pd.DataFrame | None = None):
        """
        Class to calculate pitching splits.
        """
        super().__init__(start_year, end_year, years_list=years_list, events=events)
        self.pitching_calculator: PitchingStatsCalculator | None = None

    def calculate_stats(self):
        """
        Calculate batting stats based on the set splits.
        This method should be run after all splits have been set.
        """
        # Formulate "WHERE" clause for SQL query
        where_clauses = [self.sql_query_where[key] for key in self.sql_query_where]
        where_clause = " AND ".join(where_clauses)

        self.pitching_calculator = PitchingStatsCalculator(self.linear_weights, find=self.find, split=self.split, query_where=where_clause)  # type: ignore
        self.pitching_calculator.calculate_all_stats()
        self.stats = self.pitching_calculator.stats

    def set_score_diff(self, score_diff: list[int]):
        """
        Limit the data to only include PAs with a certain score difference (positive means batting team is leading).

        Parameters:
        score_diff (list[int]): Any integer for the score difference
        """
        if len(score_diff) == 0:
            self.sql_query_where.pop("score_diff", None)
            return
        assert all(isinstance(diff, int) for diff in score_diff), "Invalid score difference. Must be a list of integers."
        self.sql_query_where["score_diff"] = f"CASE WHEN events.FLD_TEAM_ID = events.HOME_TEAM_ID THEN (events.HOME_SCORE_CT - events.AWAY_SCORE_CT) ELSE (events.AWAY_SCORE_CT - events.HOME_SCORE_CT) END IN ({', '.join([str(diff) for diff in score_diff])})"
