from datetime import datetime

# Convert string to minutes
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

# Convert minutes to string
def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

# Find intersection of two intervals
def intersect_intervals(intervals1, intervals2):
    i, j = 0, 0
    intersections = []
    
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]

        # Calculate the overlap between two intervals
        start_overlap = max(start1, start2)
        end_overlap = min(end1, end2)

        if start_overlap < end_overlap:
            intersections.append((start_overlap, end_overlap))

        if end1 < end2:
            i += 1
        else:
            j += 1

    return intersections

# Find available meeting slots
def find_available_slots(busy_schedules, daily_act, meeting_duration):
    all_availabilities = []
    
    for schedule in busy_schedules:
        start_of_day, end_of_day = map(time_to_minutes, daily_act)
        free_intervals = []
        current_start = start_of_day
        
        # Sort busy times
        sorted_schedule = sorted(schedule, key=lambda x: time_to_minutes(x[0]))

        # Identify free intervals between busy schedules
        for start, end in sorted_schedule:
            start, end = time_to_minutes(start), time_to_minutes(end)
            
            if current_start < start:
                free_intervals.append((current_start, start))
                
            current_start = max(current_start, end)

        # Add free interval after last busy period
        if current_start < end_of_day:
            free_intervals.append((current_start, end_of_day))

        all_availabilities.append(free_intervals)

    # Find common free intervals
    common_intervals = all_availabilities[0]
    for person_avail in all_availabilities[1:]:
        common_intervals = intersect_intervals(common_intervals, person_avail)

    # Filter intervals
    min_duration = int(meeting_duration)
    valid_intervals = [
        (start, end) for start, end in common_intervals
        if end - start >= min_duration  # Ensure the interval is long enough
    ]

    # Convert intervals to string
    available_slots = [
        [minutes_to_time(start), minutes_to_time(end)] for start, end in valid_intervals
    ]
    
    return available_slots

# Read input from file and write output to file
def process_input_output(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Read number of test cases
        test_cases = int(infile.readline().strip())
        
        for _ in range(test_cases):
            # Read schedules and daily activities
            person1_schedule = []
            person2_schedule = []
            
            person1_daily_act = infile.readline().strip().split()
            person2_daily_act = infile.readline().strip().split()
            
            n1 = int(infile.readline().strip())  # Number of busy periods for person 1
            for _ in range(n1):
                start, end = infile.readline().strip().split()
                person1_schedule.append([start, end])
            
            n2 = int(infile.readline().strip())  # Number of busy periods for person 2
            for _ in range(n2):
                start, end = infile.readline().strip().split()
                person2_schedule.append([start, end])

            meeting_duration = int(infile.readline().strip())

            # Find overlapping hours
            start_of_day = max(time_to_minutes(person1_daily_act[0]), time_to_minutes(person2_daily_act[0]))
            end_of_day = min(time_to_minutes(person1_daily_act[1]), time_to_minutes(person2_daily_act[1]))

            if start_of_day >= end_of_day:
                available_slots = []
            else:
                daily_act = [minutes_to_time(start_of_day), minutes_to_time(end_of_day)]

            busy_schedules = [person1_schedule, person2_schedule]
            available_slots = find_available_slots(busy_schedules, daily_act, meeting_duration)

            # Write result to file
            if available_slots:
                for slot in available_slots:
                    outfile.write(f"{slot[0]}-{slot[1]}\n")
            else:
                outfile.write("No available slots\n")

if __name__ == "__main__":
    process_input_output("Input.txt", "Output.txt")
