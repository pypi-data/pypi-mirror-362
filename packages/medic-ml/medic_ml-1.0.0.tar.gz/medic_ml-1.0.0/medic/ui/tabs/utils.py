import numpy as np

from ...conf import parameters as cfg


def update_marks(custom_value: int, add_all_value: bool = False) -> dict:
    """
    Update the marks of the features slider to include a custom value.
    
    If the custom value is already in the default marks, it will be used and
    marked as "(used)".
    
    If the custom value is not in the default marks, it will be added to the
    marks at a position that is the closest to its value.
    
    If add_all_value is True, the "All" mark will be added to the marks.
    
    Returns a tuple containing the updated marks and the location of the custom
    value.
    """
    locations = [int(l) for l in cfg.default_marks.keys()]
    values = np.array([int(v) for v in cfg.default_marks.values()])
    
    # If the custom value is already there, we use it a used feature
    if custom_value in values:
        marks = cfg.default_marks.copy()
        idx = np.where(values == custom_value)[0].item()
        location_key = str(locations[idx])
        marks[location_key] = marks[location_key] + " (used)"
        
        if add_all_value:
            marks.update(cfg.all_mark)
        
        return marks, location_key
    
    greater_indicator = values > custom_value
    if np.all(greater_indicator):
        # The value is on the far left
        custom_location = locations[0] - cfg.custom_mark_offset
    elif not np.any(greater_indicator):
        # The value is on the far right
        custom_location = locations[-1] + cfg.custom_mark_offset
    else:
        greater_idx = np.argmax(greater_indicator)
        distance_from_greater = values[greater_idx] - custom_value
        distance_from_smaller = custom_value - values[greater_idx - 1]
        if distance_from_smaller < distance_from_greater:
            # Closer to the left, we will add the offset on the left mark
            custom_location = locations[greater_idx - 1] + cfg.custom_mark_offset
        elif distance_from_smaller == distance_from_greater:
            # Equal distance
            custom_location = (locations[greater_idx - 1] + locations[greater_idx]) / 2
        else:
            # Closer the the right, we will remove the offset from the right mark
            custom_location = locations[greater_idx] - cfg.custom_mark_offset
    
    marks = cfg.default_marks.copy()
    value_label = {
        'label': str(custom_value) + ' (used)', 
        'style': {
            "top": "-3em"
        }
    }
    marks[str(custom_location)] = value_label

    if add_all_value:
        marks = {**marks, **cfg.all_mark}

    return marks, custom_location



def get_index_from_marks(number: float, marks: dict) -> int:
    """This is really specific to how the results are saved. 
    See medic.domain.Results._produce_PCA (or _produce_UMAP).

    The first results are from cfg.features, then used_features, then all.

    The result differs when there is "All" features (e.g. strip chart doesnt not include All).
    """
    contain_all = False
    for v in marks.values():
        if isinstance(v, str) and v == "All":
            contain_all = True

    match marks[str(number)]:
        case dict(value):
            # We have the used feature case, index is -2 or -1 when 
            index = -2 if contain_all else -1
        case "All":
            # We have the "All" case, index is -1
            index = -1
        case str(value) if "used" in value:
            # We have the feature case
            index = -2 if contain_all else -1
        case _:
            # The number is the index
            index = int(number)


    return index
