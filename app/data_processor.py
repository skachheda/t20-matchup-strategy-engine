import json
import pandas as pd

def parse_matchup_data(json_path: str) -> pd.DataFrame:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for inning in data.get("innings", []):
        for over_data in inning.get("overs", []):
            over_num = over_data.get("over", 0)
            
            # Categorize T20 Phase
            if over_num < 6:
                phase = "Powerplay"
            elif over_num < 15:
                phase = "Middle"
            else:
                phase = "Death"

            for ball in over_data.get("deliveries", []):
                runs_info = ball.get("runs", {})
                extras_info = ball.get("extras", {})
                
                # Check for extras that do not count as balls faced by batter
                is_wide = "wides" in extras_info
                
                records.append({
                    "batter": ball.get("batter"),
                    "bowler": ball.get("bowler"),
                    "phase": phase,
                    "runs_batter": runs_info.get("batter", 0),
                    "total_runs": runs_info.get("total", 0),
                    "is_ball_faced": 0 if is_wide else 1,
                    "is_dot": 1 if runs_info.get("total", 0) == 0 else 0,
                    "is_four": 1 if runs_info.get("batter", 0) == 4 else 0,
                    "is_six": 1 if runs_info.get("batter", 0) == 6 else 0,
                    "is_wicket": 1 if "wickets" in ball else 0
                })

    return pd.DataFrame(records)

def calculate_metrics(df: pd.DataFrame, batter: str, bowler: str, phase: str = "All") -> dict:
    filtered = df[(df["batter"] == batter) & (df["bowler"] == bowler)]
    
    if phase != "All":
        filtered = filtered[filtered["phase"] == phase]

    balls_faced = int(filtered["is_ball_faced"].sum())
    runs_scored = int(filtered["runs_batter"].sum())
    dismissals = int(filtered["is_wicket"].sum())
    dots = int(filtered["is_dot"].sum())
    boundaries = int(filtered["is_four"].sum() + filtered["is_six"].sum())

    strike_rate = round((runs_scored / balls_faced * 100), 2) if balls_faced > 0 else 0.0
    dot_pct = round((dots / balls_faced * 100), 2) if balls_faced > 0 else 0.0

    return {
        "runs": runs_scored,
        "balls": balls_faced,
        "dismissals": dismissals,
        "strike_rate": strike_rate,
        "dot_pct": dot_pct,
        "boundaries": boundaries
    }