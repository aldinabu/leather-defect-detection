import splitfolders


def split_dataset(loc_of_dataset, output_location):
    splitfolders.ratio(loc_of_dataset,  # The location of dataset
                       output=output_location,  # The output location
                       seed=42,  # The number of seed
                       ratio=(.7, .2, .1),  # The ratio of split dataset
                       group_prefix=None,  # If your dataset contains more than one file like ".jpg", ".pdf", etc
                       move=False  # If you choose to move, turn this into True
                       )
