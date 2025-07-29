from unittest import TestSuite


def flatten_specifications(specs: list[list[TestSuite]] | list[TestSuite]) -> list[TestSuite]:
    """
    Flattens specification lists by rearranging the list and returning the list with nested lists removed.
    Removes extra list and returns a flat list of TestSuite objects.
    Args:
        specs (list[list[TestSuite]] | list[TestSuite]): List of nested (or not) TestSuite objects.
    
    Returns:
        list[TestSuite]: Flattened list of TestSuite objects.
    """
    flat_specs: list[TestSuite] = []
    for spec in specs:
        if isinstance(spec, list):
            flat_specs.extend(flatten_specifications(spec))
            continue

        flat_specs.append(spec)
    
    return flat_specs