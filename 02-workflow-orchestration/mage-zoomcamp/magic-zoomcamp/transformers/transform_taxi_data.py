if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Processing {len(data[data.passenger_count == 0])} rows with zero passengers")

    return data[data.passenger_count > 0]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(output[output.passenger_count == 0]) == 0, 'There are rides with zero passengers'
