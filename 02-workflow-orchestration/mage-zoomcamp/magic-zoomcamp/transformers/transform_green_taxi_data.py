if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(s):
    result = ''

    # Iterate through the rest of the characters
    for i, char in enumerate(s[:-1]):
        # Convert the first character to lower case
        if i == 0:
            result += char.lower()

        # If the character is upper and in between other uppercase dont add _
        elif char.isupper() and s[i - 1].isupper() and s[i + 1].isupper():
            result += char.lower()

        # If the character is uppercase followed by lowercase, insert an underscore before it and convert to lower case
        elif char.isupper() and s[i - 1].isupper() and s[i + 1].islower():
            result += '_'
            result += char.lower()

        # If the character is uppercase preceded by lowercase, insert an underscore before it and convert to lower case
        elif char.isupper() and s[i - 1].islower():
            result += '_'
            result += char.lower()
        else:
            result += char

    result += s[-1]
    result = result.lower()
    return result



@transformer
def transform(data, *args, **kwargs):
    print(f"Dropping {len(data[(data.passenger_count == 0) | (data.passenger_count.isna()) | (data.trip_distance == 0) | (data.trip_distance.isna())])} rows with zero or null passengers or trip distance")
    print(f"Unique values for vendor id are: {data.VendorID.unique().tolist()}")
    
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    camel_case_columns = list(data.columns)
    snake_case_columns = [camel_to_snake(col) for col in camel_case_columns]
    
    data.columns = snake_case_columns

    changed_columns = set(camel_case_columns) - set(snake_case_columns)
    print(f"Changed {len(changed_columns)} columns: ({changed_columns}) to snake case")

    

    return data[(data.passenger_count > 0) & (data.trip_distance > 0)]


@test
def test_output(output, *args) -> None:
    assert "vendor_id" in output.columns, 'vendor_id isnt one of the columns'
@test
def test_output(output, *args) -> None:
    assert len(output[output.passenger_count == 0]) == 0, 'There are rides with zero passengers'
@test
def test_output(output, *args) -> None:
    assert len(output[output.trip_distance == 0]) == 0, 'There are rides with zero travel distance'
