from playwright.sync_api import sync_playwright

def get_element_text(element):
    """Returns the text of an element, or an empty string if the element doesn't exist."""
    return element.text_content().strip() if element else ''

def get_match_data(table):
    """Extract match data from a single table."""
    matches = []
    date_caption = get_element_text(table.query_selector('caption'))  # Extract the date from the caption
    rows = table.query_selector_all('tbody tr')
    for row in rows:
        home_team = get_element_text(row.query_selector('td.team.home span'))
        away_team = get_element_text(row.query_selector('td.team.away span'))
        home_score = get_element_text(row.query_selector('td.result .score span:nth-child(1)'))
        away_score = get_element_text(row.query_selector('td.result .score span:nth-child(2)'))
        
        # Check if the match data is valid
        if home_team and away_team:
            match = {
                "date": date_caption,
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score
            }
            matches.append(match)
    return matches

def get_main_data():
    """Fetches standings data and match data from the website."""
    with sync_playwright() as p:
        # Launch the Chromium browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the URL
        page.goto('http://okcat.cat/competicions/3/lliga-nacional-catalana/2025/')

        # Wait for the standings table to load
        page.wait_for_selector('mat-card .standings-wrapper table tbody tr', timeout=10000)

        # Extract standings data
        rows = page.query_selector_all('mat-card .standings-wrapper table tbody tr')
        standings_data = []
        for row in rows:
            team_data = {
                "rank": get_element_text(row.query_selector('td:nth-child(2)')),
                "team_name": get_element_text(row.query_selector('td:nth-child(3)')),
                "points": get_element_text(row.query_selector('td:nth-child(4)')),
                "games_played": get_element_text(row.query_selector('td:nth-child(5)')),
                "wins": get_element_text(row.query_selector('td:nth-child(6)')),
                "draws": get_element_text(row.query_selector('td:nth-child(7)')),
                "losses": get_element_text(row.query_selector('td:nth-child(8)')),
                "goals_for": get_element_text(row.query_selector('td:nth-child(9)')),
                "goals_against": get_element_text(row.query_selector('td:nth-child(10)'))
            }
            
            # Check if team_data is valid
            if team_data["team_name"]:
                standings_data.append(team_data)

        # Extract match data
        match_tables = page.query_selector_all('mat-card-content table.extensive')
        matches_data = []
        for table in match_tables:
            matches_data.extend(get_match_data(table))

        # Close the browser
        browser.close()

        # Return both datasets
        return standings_data, matches_data

# Calls the function to get the data
standings, matches = get_main_data()

# Prints the data
print("Standings:")
for team in standings:
    print(team)

print("\nMatches:")
for match in matches:
    print(match)
