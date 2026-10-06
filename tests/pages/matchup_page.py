from playwright.sync_api import Page

class MatchupPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "http://localhost:8501"
        self.page_heading = page.locator("h1")

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def _get_metric_value(self, label: str) -> str:
        metric_container = self.page.locator("div[data-testid='stMetric']").filter(has_text=label)
        return metric_container.locator("div[data-testid='stMetricValue']").inner_text().strip()

    def select_dropdown_option(self, label: str, option_text: str):
        # 1. Target the selectbox container by its label
        container = self.page.locator("div[data-testid='stSelectbox']").filter(has_text=label)
        input_field = container.locator("input")

        # 2. Focus and type the target option into the search input
        input_field.click()
        input_field.fill(option_text)

        # 3. If an option element matching role='option' is visible, click it; otherwise press Enter
        option = self.page.locator("[role='option']").filter(has_text=option_text).first
        try:
            option.wait_for(state="visible", timeout=1200)
            option.click()
        except Exception:
            input_field.press("Enter")

        # 4. Wait for Streamlit WebSocket to recalculate and update the UI
        self.page.wait_for_timeout(800)

    def get_runs(self) -> int:
        return int(self._get_metric_value("Runs Scored"))

    def get_balls(self) -> int:
        return int(self._get_metric_value("Balls Faced"))

    def get_strike_rate(self) -> float:
        return float(self._get_metric_value("Strike Rate"))

    def get_dismissals(self) -> int:
        return int(self._get_metric_value("Dismissals"))