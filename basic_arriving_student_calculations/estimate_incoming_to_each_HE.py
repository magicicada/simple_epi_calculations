import pandas as pd
import sys

def read_flow_table(filename):
    he_col = "HE provider "
    flow_df = pd.read_csv(filename)
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
            "Wales",
            "Scotland"
        ]
    ]

    HE_providers = list(flow_df[he_col])
    flow_df = flow_df.set_index(he_col)
    flow_df = flow_df.T
    flow_df = flow_df.reset_index()
    return flow_df, HE_providers


def read_pos_table(filename):
    perc_pos_df = pd.read_csv(filename)
    perc_pos_df.columns = ["Region", "estimate", "lower", "upper"]
    perc_pos_df["estimate"] = perc_pos_df["estimate"].astype(float)
    regions = list(perc_pos_df["Region"])
    return perc_pos_df, regions


def generate_number_incoming(
    flow_df, perc_pos_df, regions, HE_providers, col_of_pos="estimate", result_name = ' No Description Given'
):
    flow_df = flow_df.merge(
        perc_pos_df, how="outer", left_on="index", right_on="Region"
    )

    incoming_cols = []
    for he_provider in HE_providers:
        thisName = he_provider + result_name
        incoming_cols.append(thisName)
        flow_df[thisName] = flow_df[he_provider] * flow_df[col_of_pos] / 100

    flow_df = flow_df.set_index("index")
    flow_df = flow_df[incoming_cols]

    flow_df = flow_df.T
    # print(flow_df)
    flow_df["Total Regions"] = flow_df.loc[:, regions].sum(axis=1)
    return flow_df


def main():
    flowsFile = sys.argv[1]
    prevFile = sys.argv[2]
    outputFile = sys.argv[3]
    add_to_results = sys.argv[4]
    
    for col in ["estimate", "lower", "upper"]:
        perc_pos_df, regions = read_pos_table(prevFile)
        flow_df, he_provers = read_flow_table(flowsFile)
        flow_df = generate_number_incoming(
            flow_df, perc_pos_df, regions, he_provers, col_of_pos=col, result_name=add_to_results
        )
        flow_df.to_csv(
            outputFile + col + ".csv"
        )


if __name__ == "__main__":
    main()
