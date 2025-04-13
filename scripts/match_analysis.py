import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Part 01 Analyzing No of Matches Played each Season

def seasonal_match_analysis(df):
    df_copy = df.copy()

    df_copy = df_copy.groupby("season").size().reset_index()
    df_copy.columns = ["Season", "Matches"]
    fig, ax = plt.subplots(figsize=(12, 8))
    a = sns.barplot(df_copy, x="Season", y="Matches", ax=ax, edgecolor="#1C0221", linewidth=1, palette="flare")
    for i in a.containers:
        a.bar_label(i, label_type="center", padding=10, color="white")
    plt.title("No of Matches Played Per Season", fontsize=20, pad=20)
    plt.xlabel('Season', labelpad=15, fontsize=14)
    plt.ylabel('Number of Matches', labelpad=15, fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout(pad=2)
    ax.set_axisbelow(True)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

#Part 02 Analyzing Win Percentage of Different Teams across Season

def team_performance_comparison(df,team_abbr):
    df_copy = df.copy()
    team1 = df_copy.groupby(["season", "team1"]).size().reset_index()
    team1.columns = ["Season", "Team", "Matches"]
    team2 = df_copy.groupby(["season", "team2"]).size().reset_index()
    team2.columns = ["Season", "Team", "Matches"]
    team = pd.concat([team1, team2])
    team= team.groupby(["Season", "Team"]).sum().reset_index()
    team.columns = ["Season", "Team", "Total Matches"]
    winner = df_copy.groupby(["season", "winner"]).size().reset_index()
    winner.columns = ["Season", "Team", "Matches_Won"]
    team = pd.merge(team, winner, on=["Season", "Team"], how="left")
    team["Win Percentage"] = (team["Matches_Won"] / team["Total Matches"]) * 100
    team["Win Percentage"] = team["Win Percentage"].round(1)

    team["Team"] = team["Team"].map(team_abbr)
    seasons = sorted(team["Season"].unique())
    n = len(seasons)
    rows = 6
    cols = 3
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(20, 35))
    axes = axes.flatten()
    for idx, season in enumerate(seasons):
        data = team[team["Season"] == season]
        sns.barplot(data=data, x="Team", y="Win Percentage", ax=axes[idx], edgecolor="#1C0221", linewidth=1,
                    palette="flare", hue="Team", legend=False)

        axes[idx].set_title(f"Season {season}", fontsize=18)
        for i in axes[idx].containers:
            axes[idx].bar_label(i, label_type="center", padding=5, color="white")
        axes[idx].set_axisbelow(True)
        axes[idx].grid(axis='y', linestyle='--', alpha=0.7)
        axes[idx].tick_params(axis='x', rotation=45)
        axes[idx].set_ylim(0, 100)
        axes[idx].set_xlabel("Teams", labelpad=10, fontsize=12)
        axes[idx].set_ylabel("Winning Percentage (%)", labelpad=10, fontsize=12)

    for j in range(idx + 1, rows * cols):
        fig.delaxes(axes[j])

    fig.suptitle("IPL Team Win Percentages Per Season (2008–2024)", fontsize=22, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])


    plt.show()

#Part 03 Analyzing Win Percentage of Different Teams at different Venues

def venue_analysis(df,team_abbr,active_teams):
    df_copy = df.copy()
    df_copy["venue"] = df_copy["venue"].astype("str")
    df_copy["stadium"] = df_copy["venue"].str.split(",").str[0]
    winner = df_copy.groupby(["stadium", "winner"]).size().reset_index()
    winner.columns = ["Stadium", "Team", "Matches_Won"]
    team1 = df_copy.groupby(["stadium", "team1"]).size().reset_index()
    team1.columns = ["Stadium", "Team", "Matches_Played"]
    team2 = df_copy.groupby(["stadium", "team2"]).size().reset_index()
    team2.columns = ["Stadium", "Team", "Matches_Played"]
    teams = pd.concat([team1, team2])
    teams = teams.groupby(["Stadium", "Team"]).sum().reset_index()
    teams.columns = ["Stadium", "Team", "Total_Matches"]
    team = pd.merge(teams, winner, on=["Stadium", "Team"], how="left").fillna(0)
    team["Matches_Won"] = team["Matches_Won"].astype("int")
    team["Team"] = team["Team"].map(team_abbr)
    team = team[team["Team"].isin(active_teams)]
    team["Winning_Percentage"] = (team["Matches_Won"] / team["Total_Matches"]) * 100
    team["Winning_Percentage"] = team["Winning_Percentage"].round(1)
    copy = team.copy()
    counted = copy.groupby(["Stadium"])["Total_Matches"].sum().reset_index()
    counted.columns = ["Stadium", "Count"]

    valid = counted[counted["Count"] >= 20]["Stadium"].to_numpy()

    team = team[team["Stadium"].isin(valid)]
    pivot = team.pivot_table(index="Stadium", columns="Team", values="Winning_Percentage").fillna(0)
    fig, axis = plt.subplots(figsize=(14, 10))
    axis.set_title("Win Percentages of Teams at different Venues", fontsize=18, pad=20, fontweight="bold")
    axis.set_xlabel("Teams", fontsize=12, labelpad=10)
    axis.set_ylabel("Stadium", fontsize=12)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=12)

    b = sns.heatmap(pivot, annot=True, fmt=".1f", cmap="flare", ax=axis, linecolor="white", annot_kws={"size": 10},
                    linewidth=1)
    plt.tight_layout()
    plt.show()

#Part 04 Analyzing Outcome of Matches based on Toss Decisions taken by Winning Team

def toss_decision_impact(df,team_abbr,active_teams):
    df_copy = df.copy()
    df_copy["toss_winner"] = df_copy["toss_winner"].map(team_abbr)
    df_copy["winner"] = df_copy["winner"].map(team_abbr)
    df_copy = df_copy[(df_copy["winner"].isin(active_teams)) & (df_copy["toss_winner"].isin(active_teams))]
    df_copy["toss_winner_match_winner"] = df_copy["toss_winner"] == df_copy["winner"]
    df_copy = df_copy[df_copy["toss_winner_match_winner"] == True]
    df_copy = df_copy.groupby(["toss_winner", "toss_decision"]).size().unstack(fill_value=0).reset_index()
    df_copy.columns = ["Team", "Wins Batting First", "Wins Fielding First"]
    figure = plt.figure(figsize=(12, 10))
    bar1 = plt.bar(df_copy["Team"], df_copy["Wins Batting First"], label="Batting First", bottom=df_copy["Wins Fielding First"],
                   edgecolor="#272932", linewidth=2, color="#B3001B")
    bar2 = plt.bar(df_copy["Team"], df_copy["Wins Fielding First"], label="Fielding First", edgecolor="#272932", linewidth=2,
                   color="#FFD400")
    plt.tight_layout()
    plt.legend(title="Toss Decision", loc=0, fontsize=12, title_fontsize=13)
    plt.title("Matches Won based on Toss Decisions", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Team", fontsize=14, labelpad=10)
    plt.ylabel("Matches Won", fontsize=14, labelpad=10)
    plt.tight_layout()


    plt.show()


if __name__ == "__main__":
    main_df = pd.read_csv("../data/matches.csv")
    main_df["date"] = pd.to_datetime(main_df["date"], format="mixed", errors="coerce")
    main_df["season"] = main_df["date"].dt.year
    team_abbr = {
        "Chennai Super Kings": "CSK",
        "Deccan Chargers": "DC*",
        "Delhi Daredevils": "DD",
        "Kings XI Punjab": "KXIP",
        "Kolkata Knight Riders": "KKR",
        "Mumbai Indians": "MI",
        "Rajasthan Royals": "RR",
        "Royal Challengers Bangalore": "RCB",
        "Kochi Tuskers Kerala": "KTK",
        "Pune Warriors": "PW",
        "Sunrisers Hyderabad": "SRH",
        "Gujarat Lions": "GL",
        "Rising Pune Supergiants": "RPS",
        "Rising Pune Supergiant": "RPS",
        "Delhi Capitals": "DC",
        "Punjab Kings": "PBKS",
        "Gujarat Titans": "GT",
        "Lucknow Super Giants": "LSG",
        "Royal Challengers Bengaluru": "RCB"
    }
    active_teams = [
        "CSK", "DC", "GT", "KKR",
        "LSG", "MI", "PBKS",
        "RR", "RCB", "SRH"
    ]
    seasonal_match_analysis(main_df)
    team_performance_comparison(main_df,team_abbr)
    venue_analysis(main_df,team_abbr,active_teams)
    toss_decision_impact(main_df,team_abbr, active_teams)