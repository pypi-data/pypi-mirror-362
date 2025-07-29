from collections import Counter

def get_mode(data):
    '''Return a single mode. when there are multiple, return the samllest'''
    if not data:
        raise ValueError("The data list is empty")

    # Count the frequency of each item
    counts = Counter(data)

    # Find the maximum frequency
    max_frequency = max(counts.values())

    # Extract items with the maximum frequency and take the minimum
    mode = min(item for item, count in counts.items() if count == max_frequency)
    return mode