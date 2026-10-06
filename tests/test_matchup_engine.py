import pytest
from playwright.sync_api import Page, expect
from pages.matchup_page import MatchupPage

class TestMatchupStrategyEngine:

    def test_page_loads_successfully(self, page: Page):
        """Verify dashboard header and default components load cleanly."""
        matchup = MatchupPage(page)
        matchup.navigate()

        expect(matchup.page_heading).to_contain_text("T20 Matchup Strategy Engine")
        assert matchup.get_runs() >= 0
        assert matchup.get_balls() >= 0

    def test_filter_selection_updates_metrics(self, page: Page):
        """Verify changing dropdown options updates the displayed score cards."""
        matchup = MatchupPage(page)
        matchup.navigate()

        matchup.select_dropdown_option("Select Batter", "MS Dhoni")
        matchup.select_dropdown_option("Select Bowler", "JJ Bumrah")
        matchup.select_dropdown_option("Match Phase", "All")

        assert matchup.get_runs() == 14
        assert matchup.get_balls() == 6
        assert matchup.get_dismissals() == 0

    def test_strike_rate_mathematical_integrity(self, page: Page):
        """Verify that UI Strike Rate matches (Runs / Balls) * 100."""
        matchup = MatchupPage(page)
        matchup.navigate()

        matchup.select_dropdown_option("Select Batter", "MS Dhoni")
        matchup.select_dropdown_option("Select Bowler", "JJ Bumrah")
        matchup.select_dropdown_option("Match Phase", "All")

        runs = matchup.get_runs()
        balls = matchup.get_balls()
        rendered_sr = matchup.get_strike_rate()

        expected_sr = round((runs / balls * 100), 2)
        assert rendered_sr == expected_sr, f"Expected SR {expected_sr}, but UI displayed {rendered_sr}"

    def test_phase_breakdown_filtering(self, page: Page):
        """Verify switching phase to 'Death' isolates death-over deliveries."""
        matchup = MatchupPage(page)
        matchup.navigate()

        matchup.select_dropdown_option("Select Batter", "MS Dhoni")
        matchup.select_dropdown_option("Select Bowler", "JJ Bumrah")
        matchup.select_dropdown_option("Match Phase", "Death")

        assert matchup.get_runs() == 13
        assert matchup.get_balls() == 4
        assert matchup.get_strike_rate() == 325.0