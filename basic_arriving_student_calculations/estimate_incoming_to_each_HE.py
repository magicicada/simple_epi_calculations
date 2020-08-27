import pandas as pd


def read_flow_table():
    he_col = "HE provider "
    flow_df = pd.read_csv("150091_Data_header_trimmed.csv")
    flow_df = flow_df[
        [
            he_col,
            "North East",
            "North West",
            "Yorkshire and The Humber",
            "East Midlands",
            "West Midlands",
            "East of England",
            "London",
            "South East",
            "South West",
        ]
    ]

    HE_providers = list(flow_df[he_col])
    flow_df = flow_df.set_index(he_col)
    flow_df = flow_df.T
    flow_df = flow_df.reset_index()
    return flow_df, HE_providers


def read_pos_table():
    perc_pos_df = pd.read_csv("august_6_perc_testing_pos.csv")
    perc_pos_df.columns = ["Region", "perc_pos", "lower", "upper"]
    perc_pos_df["perc_pos"] = perc_pos_df["perc_pos"].astype(float)
    regions = list(perc_pos_df["Region"])
    return perc_pos_df, regions


def generate_number_incoming(
    flow_df, perc_pos_df, regions, HE_providers, col_of_pos="perc_pos"
):
    flow_df = flow_df.merge(
        perc_pos_df, how="outer", left_on="index", right_on="Region"
    )

    incoming_cols = []
    for he_provider in HE_providers:
        thisName = he_provider + " Est. Infectious Incoming"
        incoming_cols.append(thisName)
        flow_df[thisName] = flow_df[he_provider] * flow_df[col_of_pos] / 100

    flow_df = flow_df.set_index("index")
    flow_df = flow_df[incoming_cols]

    flow_df = flow_df.T

    flow_df["Total Regions"] = flow_df.loc[:, regions].sum(axis=1)
    return flow_df


def main():

    for col in ["perc_pos", "lower", "upper"]:
        perc_pos_df, regions = read_pos_table()
        flow_df, he_provers = read_flow_table()
        flow_df = generate_number_incoming(
            flow_df, perc_pos_df, regions, he_provers, col_of_pos=col
        )
        flow_df.to_csv(
            "estimate_number_incoming_infected_from_regions_using_" + col + ".csv"
        )


if __name__ == "__main__":
    main()
