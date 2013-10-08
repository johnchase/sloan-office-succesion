def parse_sample_id(sample_id):
    if len(sample_id) != 12:
        raise ValueError('sample id %s is not in correct format!' % sample_id)
    cc = sample_id[0]
    if cc == 'S':
        city = 'san_diego'
    elif cc == 'F': 
        city = 'flagstaff'
    elif cc == 'T':
        city = 'toronto'
    else:
        raise ValueError('sample id %s is not in correct format!' % sample_id)
    office = sample_id[1]
    pl = sample_id[2]
    if pl == 'C': 
        plate_location = 'ceiling'
    elif pl == 'W': 
        plate_location = 'wall'
    elif pl == 'F': 
        plate_location = 'floor'
    else:
        raise ValueError('sample id %s is not in correct format!' % sample_id)
    row = sample_id[4]
    s = sample_id[6:8]
    if s == 'Ce':
        surface = 'ceiling'
    elif s == 'Ca':
        surface = 'carpet'
    elif s == 'Dr':
        surface = 'drywall'
    else:
        raise ValueError('sample id %s is not in correct format!' % sample_id)
    time_point = sample_id[9:12]
    int_time_point = int(time_point)
    if int_time_point < 5:
        time_point_category = 1
    elif int_time_point > 6 and int_time_point < 15:
        time_point_category = 2
    else: 
        time_point_category = 3
    time_point_category = str(time_point_category)
    return city, office, plate_location, row, surface, time_point, time_point_category
    
def correct_time(time):
    if len(time.split(':')) == 3:
        pass
    elif len(time.split(':')) == 2:
        time = time + ':00'
    else:
        time = time[:-2] + ':' + time[-2:] + ':00'
    for i in time.split(':'):
        try: 
            int(i)
        except:
            raise ValueError('%s is not a valid time, check mapping file' % time)
    return time

def add_line_data(line):
    line = line.strip()
    line = line.split('\t')
    try:
        if line[1] != '':
            date = line[1]
        else: 
            date = 'no_data'
    except:
        date = 'no_data'
    try:
        if line[2] != '':
            time = correct_time(line[2])
        else:
            time = 'no_data'
    except:
        time = 'no_data'
    try:
        if line[3] != '':
            notes = line[3]
        else: 
            notes = 'no_data'
    except:
        notes = 'no_data'
    try:
        if line[4] != '':
            cooler = line[4]
        else: 
            cooler = 'no_data'
    except:
        cooler = 'no_data'
    city, office, plate_location, row, surface, time_point, time_point_category =\
    parse_sample_id(line[0])
    new_line = line[0], date, time, notes, city, office, plate_location, row, surface,\
               time_point, time_point_category, cooler
    return '\t'.join(new_line)
    
def add_map_data(map_f, output_f):
    header = '#SampleID\tDateOfCollection\tTimeOfCollection\tNotes\tCity\tOffice\tOfficeLocation\tRow\tSurface\tTimePoint\tTimePointCategory\tCooler'
    for line in map_f:
        if line.startswith('#'):
            output_f.write(header)
            output_f.write('\n')
        else:
            new_line = add_line_data(line)
            output_f.write(new_line)
            output_f.write('\n')
    output_f.close()
    
def add_map_data_master(map_f, output_f):
    for line in map_f:
        if line.startswith('#'):
            line = line.strip() + '\t16S-sequencing-date'
            output_f.write(line)
            output_f.write('\n')
        else:
            if line.split()[1] == 'no_data':
                line = line.strip() + '\tno_data'
                output_f.write(line)
                output_f.write('\n')
            else:
                line = line.strip() + '\t9/18/13'
                output_f.write(line)
                output_f.write('\n')
    output_f.close()
    

    
# add_map_data(open('toronto_map.txt', 'U'), open('toronto_corrected.txt', 'w')) 
# add_map_data(open('flagstaff_map.txt', 'U'), open('flagstaff_corrected.txt', 'w')) 
# add_map_data(open('san_diego_map.txt', 'U'), open('san_diego_corrected.txt', 'w')) 
# add_map_data_master(open('master_office_map.txt', 'U'), open('master_office_map2.txt', 'w'))