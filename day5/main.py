import sys
sys.path.append('../')

from tools.parsing import read_with_delimeter

# I did not check that mappings where going one way so I parsed this into a dict
# of dicts that would correspond to each conversion rate.
#
# Would have been faster just to get a list of list for the conversions and
# iterate one conversion as a time.
def create_conv_tables(map_data):
    conv_map = dict()
    for data in map_data:
        stuff = data.split(" map:\n")
        conv_types = stuff[0].split("-to-")
        from_type, to_type = conv_types[0], conv_types[1]
        if from_type not in conv_map.keys():
            conv_map[from_type] = dict()
        conv_data = [[int(y)for y in x.split(" ") if y != ''] for x in stuff[1].split("\n") if x != '']
        conv_map[from_type][to_type] = conv_data
    return conv_map

# Find the locations for all the seeds one by one
def find_locations(seeds, conv_tables:dict):
    start = "seed"
    locations = []
    for seed in seeds:
        curr = start
        val = seed
        while curr != "location":
            conv_mappings = conv_tables[curr]
            conv_to = list(conv_mappings.keys())[0]
            for dest_start, source_start, range_len in conv_mappings[conv_to]:
                if val >= source_start and val < source_start + range_len:
                    val = dest_start + val-source_start
                    break
            curr = conv_to
        locations.append(val)
    return locations

def find_min_location_from_ranges(seed_ranges, conv_tables:dict):
    # Assume the smallest locations found is larger than this
    min_location = 10**12
    curr = "seed"
    curr_ranges = seed_ranges
    while curr != "location":
        conv_mappings = conv_tables[curr]
        conv_to = list(conv_mappings.keys())[0]
        new_ranges = []
        for dest_start, src_start, range_len in conv_mappings[conv_to]:
            src_end = src_start + range_len
            put_back_ranges = []
            for range_start, range_end in curr_ranges:
                unconverted_ranges, to_convert_ranges = splitRanges(range_start,
                                                                    range_end,
                                                                    src_start,
                                                                    src_end)
                # Add unconverted ranges to be compadre with the coming conversions
                for old_range in unconverted_ranges:
                    put_back_ranges.append(old_range)
                # Add the already converted changes to be readded once we move to
                # the next conversion
                for conv_start, conv_end in to_convert_ranges:
                    new_start = dest_start + conv_start-src_start
                    new_end = dest_start + conv_end-src_start
                    new_ranges.append((new_start, new_end))
            # Only keep comparing to the ranges that are not converted yet
            curr_ranges = put_back_ranges
        # Add the new ranges for the next type conversion
        for converted_range in new_ranges:
            curr_ranges.append(converted_range)
        # Update which the current type is
        curr = conv_to

    for range_start, _ in curr_ranges:
        if range_start < min_location:
            min_location = range_start
    return min_location

# Find if there are any overlaps and if so, split the range in into
# subranges of what should be converted or not
def splitRanges(in_start, in_end, r_start, r_end):
    unconverted_ranges = []
    to_convert_ranges = []
    # Ranges do not touch, return the original range
    if r_start >= in_end or r_end < in_start:
        unconverted_ranges.append((in_start, in_end))
        return unconverted_ranges, to_convert_ranges
    if r_start <= in_start:
        # Simplest case, all in the input range should be converted
        if r_end >= in_end:
            to_convert_ranges.append((in_start, in_end))
            return unconverted_ranges, to_convert_ranges
        #  r_s --------- r_e
        #         in_s ----------in_e
        # Split into range from [in_s, r_e) to be converted
        # and range [r_e, in_e) stays unconverted
        if r_end > in_start:
            to_convert_ranges.append((in_start, r_end))
            unconverted_ranges.append((r_end, in_end))
            return unconverted_ranges, to_convert_ranges

    # in_s --------- in_e
    #         r_s -----------r_e
    # Split into range from [r_s, in_e) to be converted
    # and range [in_s, r_s) stays unconverted
    if r_end >= in_end:
        to_convert_ranges.append((r_start, in_end))
        unconverted_ranges.append((in_start, r_start))
        return unconverted_ranges, to_convert_ranges
    
    # in_s ------------------------- in_e
    #        r_s -----------r_e
    # Split into 3 intervals where [r_s, r_e) is converted and
    # [in_s, r_s) + [r_e, in_e) stays unconverted
    to_convert_ranges.append((r_start, r_end))
    unconverted_ranges.append((in_start, r_start))
    unconverted_ranges.append((r_end, in_end))
    return unconverted_ranges, to_convert_ranges

def run():
    data = read_with_delimeter("input.txt", "\n\n")
    seeds, data = [int(x) for x in data[0].split(":")[1].split(" ") if x != ''], data[1:]
    conv_tables = create_conv_tables(data)
    locations = find_locations(seeds, conv_tables)
    print(min(locations))
    # Create the ranges of seeds to look at
    seed_ranges = []
    for i in range(0, len(seeds),2):
        seed_ranges.append((seeds[i], seeds[i]+seeds[i+1]))
    print(find_min_location_from_ranges(seed_ranges, conv_tables))

if __name__ == "__main__":
    run()