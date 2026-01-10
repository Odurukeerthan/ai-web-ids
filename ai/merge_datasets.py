import pandas as pd

time_df = pd.read_csv("ids_dataset_day5.csv")
sliding_df = pd.read_csv("ids_dataset_sliding.csv")

final_df = pd.concat([time_df, sliding_df], ignore_index=True)

print("Final dataset size:", len(final_df))
print("\nFinal label distribution:")
print(final_df["label"].value_counts())

final_df.to_csv("ids_dataset_final.csv", index=False)
print("\nSaved ids_dataset_final.csv")
