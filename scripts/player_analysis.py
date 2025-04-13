import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Part 01 Analyzing Runs Scored in each Over across Matches

def run_distribution_per_over(df):
    df_copy = df.copy()
    df_copy = df_copy.groupby(["match_id", "over"])["total_runs"].sum().reset_index()
    df_copy.columns = ["Match_ID", "Over", "Runs"]
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Over', y='Runs', data=df_copy, palette='viridis', linewidth=2)
    plt.title('Runs Distribution Per Over', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Over', fontsize=14, labelpad=10)
    plt.ylabel('Runs Scored in that Over', fontsize=14, labelpad=10)
    plt.xticks(ticks=range(0, 20), labels=[str(i + 1) for i in range(20)])
    plt.tight_layout()
    plt.show()

#Part 02 Analyzing Common Dismissals

def dismissal_type_dist(df):
    df_copy = df.copy()
    dismissal = ['caught', 'bowled', 'run out', 'lbw', 'stumped'
        , 'caught and bowled', 'hit wicket', 'obstructing the field', ]
    df_copy = df_copy.dropna(subset=["dismissal_kind"])
    df_copy = df_copy[df_copy["dismissal_kind"].isin(dismissal)]
    df_copy = df_copy.groupby("dismissal_kind").size().reset_index()
    df_copy.columns = ["Dismissal_Kind", "Count"]
    df_copy["Dismissal_Kind"] = df_copy["Dismissal_Kind"].str.capitalize()
    df_copy["Total_Dismissal"] = df_copy["Count"].sum()
    df_copy["Dismissal_Percentage"] = (df_copy["Count"] / df_copy["Total_Dismissal"]) * 100
    df_copy["Dismissal_Percentage"] = df_copy["Dismissal_Percentage"].round(2)
    df_copy = df_copy[(df_copy["Dismissal_Kind"] != "Obstructing the field") & (df_copy["Dismissal_Kind"] != "Hit wicket")]
    fig, axis = plt.subplots(figsize=(12, 10))
    wp = {"edgecolor": "black", "linewidth": 1}
    colors = ["#586BA4", "#ED254E", "#F68E5F", "#F76C5E", "#DC0073", "#07393C"]
    length = df_copy.shape[0]
    explode = [0.05] * length
    wedges, texts, autotexts = axis.pie(df_copy["Dismissal_Percentage"], autopct="%0.1f%%", startangle=45, wedgeprops=wp,
                                        explode=explode, pctdistance=0.75, textprops={"fontsize": 12}, colors=colors)
    axis.axis("equal")
    for i in autotexts:
        i.set_color("white")

    axis.legend(wedges, df_copy["Dismissal_Kind"], title="Dismissal Types", loc="center left", fontsize=12,
                title_fontsize=13, bbox_to_anchor=(1, 0.5))
    plt.title("Dismissal Types in IPL", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main_df = pd.read_csv("../data/deliveries.csv")
    run_distribution_per_over(main_df)
    dismissal_type_dist(main_df)
