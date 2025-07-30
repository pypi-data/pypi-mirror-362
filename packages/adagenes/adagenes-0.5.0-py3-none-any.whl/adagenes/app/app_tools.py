import re, datetime, os
import adagenes
import adagenes.tools.maf_mgt


def generate_annotations_db(srv_prefix, vcf_obj, extract_keys, labels):
    """

    :param srv_prefix:
    :param vcf_obj:
    :param extract_keys:
    :return:
    """
    #print("extract keys ",srv_prefix,": ",extract_keys,": ",vcf_obj)

    annotations = {}
    if isinstance(srv_prefix, str):
        if srv_prefix in vcf_obj:
            service_output = vcf_obj[srv_prefix]
            for k in extract_keys:
                if k in service_output:
                    #annotations.append('{}_{}={}'.format(srv_prefix, k, service_output[k]))
                    annotations[srv_prefix + "_" + k] = service_output[k]
    elif isinstance(srv_prefix, list):
        for i,pref in enumerate(srv_prefix):
            #print("pref ",pref," in ",vcf_obj.keys())
            if pref in vcf_obj.keys():
                service_output = vcf_obj[pref]
                k_list = extract_keys
                #print("extract ",pref,": ",extract_keys," from ",service_output)
                if isinstance(k_list,list):
                    for k in k_list:
                        if k in service_output:
                            #annotations.append('{}_{}={}'.format(pref, k, service_output[k]))
                            annotations[k] = service_output[k]
                elif isinstance(k_list, str):
                    for j,k in enumerate(extract_keys):
                        if k in service_output:
                            if labels is not None:
                                label = labels[j]
                                #annotations.append('{}={}'.format(label, service_output[k]))
                                annotations[label] = service_output[k]
                            else:
                                #annotations.append('{}_{}={}'.format(pref, k, service_output[k]))
                                annotations[pref + "_" + k] = service_output[k]
    return annotations


def delete_files_with_higher_number(directory, infile):
    # Regular expression to match the number at the beginning of the filename
    pattern = re.compile(r'^(\d+)_')

    # Extract the number from the reference file path
    reference_filename = os.path.basename(infile)
    match = pattern.match(reference_filename)
    if not match:
        print(f"Error: The reference file '{infile}' does not match the expected pattern.")
        return

    threshold_number = int(match.group(1))

    if threshold_number >= 2:

        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                # Extract the number from the filename
                file_number = int(match.group(1))
                if file_number > threshold_number:
                    # Construct the full file path
                    file_path = os.path.join(directory, filename)
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                elif file_number == threshold_number:
                    if "processed" not in filename:
                        file_path = os.path.join(directory, filename)
                        # Delete the file
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")

def increment_file_number(file_path, increase_count=True):
    # Split the file path into directory and filename
    directory, filename = os.path.split(file_path)

    # Define the regular expression pattern to match the number at the beginning of the filename
    pattern = r'^(\d+)_'

    # Search for the pattern in the filename
    match = re.search(pattern, filename)
    print("increase file number ", filename)

    if match:
        # Extract the number and the rest of the filename
        number = int(match.group(1))
        rest_of_filename = filename[match.end():]

        # Increment the number
        if increase_count is True:
            new_number = number + 1
        else:
            new_number = number

        # Construct the new filename
        new_filename = f"{new_number}_{rest_of_filename}"

        # Reconstruct the full file path with the new filename
        new_file_path = os.path.join(directory, new_filename)
        return new_file_path
    else:
        # If no number is found, return the original file path
        print("Could not find file number")
        return file_path



def update_filename_with_current_datetime(file_name, action="sort", datetime_str=None, increase_count=True):
    print("Update file name ",file_name)

    if (file_name.endswith("_processed.vcf")) and (action != "processed"):
        file_name = file_name.replace("_processed.vcf", ".vcf")

    # Regular expression to match the timestamp in the filename
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})')
    #pattern = re.compile("[0-9]+-[0-9]+-[0-9]_[0-9]+-[0-9]+")
    match = pattern.search(file_name)

    if datetime_str is None:
        current_datetime = datetime.datetime.now()
        #datetime_str = str(datetime.datetime.now())
        #datetime_str = datetime.datetime.now()
        #datetime_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        datetime_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')#[:-3]

    datetime_found = False
    if match:
        # Get the current datetime and format it
        current_datetime = datetime.datetime.now()
        #current_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
        current_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        # Replace the old timestamp with the current datetime
        new_file_name = pattern.sub(current_datetime, file_name)
        datetime_found = True
    else:
        new_file_name = file_name

    # outfile = infile_name.strip() + ".sort." + datetime_str + "." + output_format
    new_file_name = new_file_name.replace(" ", "_")
    new_file_name = new_file_name.replace(":", "-")

    if datetime_found is False:
        new_file_name = new_file_name.replace(".vcf","")
        new_file_name += '_' + datetime_str
        new_file_name += ".vcf"

    if action == "sort":
        new_file_name = new_file_name.replace("_processed", "_sort")
        new_file_name = new_file_name.replace("_filter", "_sort")
        if "_sort" not in new_file_name:
            new_file_name = new_file_name.replace(".vcf", "")
            new_file_name += '_' + "sort"
            new_file_name += ".vcf"
    elif action == "filter":
        new_file_name = new_file_name.replace("_processed", "_sort")
        new_file_name = new_file_name.replace("_sort", "_filter")
        if "_filter" not in new_file_name:
            new_file_name = new_file_name.replace(".vcf", "")
            new_file_name += '_' + "filter"
            new_file_name += ".vcf"
    elif action == "processed":
        new_file_name = new_file_name.replace("_filter", "_processed")
        new_file_name = new_file_name.replace("_sort", "_processed")
        if "_processed" not in new_file_name:
            new_file_name = new_file_name.replace(".vcf", "")
            new_file_name += '_' + "processed"
            new_file_name += ".vcf"

    #elif action == "processed":
    #    new_file_name = new_file_name.replace("_processed", "_sort")
    #    new_file_name = new_file_name.replace("_processed", "_sort")

    # increase file count
    new_file_name = increment_file_number(new_file_name, increase_count=increase_count)
    print("increased file name ",new_file_name)

    return new_file_name

def convert_data_to_json(data_page, header_lines):
    data = []
    reserved_keys = ["_id",  "row_number"]

    for var in data_page:
        json_obj = {}

        for key in var.keys():
            if key not in reserved_keys:
                json_obj[key] = str(var[key])

        data.append(json_obj)
    return data

def convert_data_to_maf(data_page, header_lines, sep="\t"):
    data = []

    line = ""
    for col in adagenes.tools.maf_mgt.maf_columns:
        line += col + sep
    line += '\n'

    reserved_keys = ["_id", "chrom", "pos", "id", "ref", "alt", "qual", "filter", "variant_data",
                     "mutation_type_details",
                     "frameshift", "orig_id", "mutation_type_desc", "mutation_type", "qid", "row_number", "type",
                     "mdesc"]

    # TODO add additional columns

    data.append(line)

    for var in data_page:
        line = ""

        for col in adagenes.tools.maf_mgt.maf_columns:
            ag_col = adagenes.tools.maf_mgt.maf_ag_mapping[col]
            if ag_col != "":
                if ag_col not in reserved_keys:
                    if ag_col in var.keys():
                        line += str(var[ag_col]) + sep

        line = line.rstrip(sep)
        data.append(line + '\n')
    return data

def convert_data_to_csv(data_page, header_lines, sep=","):
    data = []
    reserved_keys = ["_id", "chrom", "pos", "id", "ref", "alt", "qual", "filter", "variant_data",
                     "mutation_type_details",
                     "frameshift", "orig_id", "mutation_type_desc", "mutation_type", "qid", "row_number", "type",
                     "mdesc"]

    line = ""
    line += "CHROM" + sep + "POS" + sep + "ID" + sep + "REF" + sep + "ALT" + sep + "QUAL" + sep + "FILTER" + sep
    for header_line in header_lines:
        #data.append(header_line + '\n')
        match = re.match(r'##INFO=<ID=([^,]+),Number=([^,]+),Type=([^,]+),Description="([^"]+)"', header_line)
        if match:
            column_id, number, type_, description = match.groups()
            line += column_id + sep
    line = line.rstrip(sep)
    line += '\n'

    # TODO add additional columns

    data.append(line)

    for var in data_page:
        line = ""
        if "chrom" in var.keys():
            line += str(var["chrom"]) + sep
        if "pos" in var.keys():
            line += str(var["pos"]) + sep
        if "id" in var.keys():
            line += str(var["id"]) + sep
        if "ref" in var.keys():
            line += str(var["ref"]) + sep
        if "alt" in var.keys():
            line += str(var["alt"]) + sep
        if "qual" in var.keys():
            line += str(var["qual"]) + sep
        if "filter" in var.keys():
            line += str(var["filter"]) + sep

        for key in var.keys():
            if key not in reserved_keys:
                line += str(var[key]) + sep

        line = line.rstrip(sep)
        data.append(line + '\n')
    return data

def convert_data_to_vcf(data_page:list, header_lines:list):
    #print("data page ",data_page)

    data= []
    reserved_keys = ["_id", "chrom", "pos", "id", "ref", "alt", "qual", "filter", "variant_data", "mutation_type_details",
                     "frameshift", "orig_id", "mutation_type_desc", "mutation_type","qid","row_number","type","mdesc"]

    for header_line in header_lines:
        data.append(header_line + '\n')

    for var in data_page:
        info_line = ""
        for key in var.keys():
            if key not in reserved_keys:
                info_line += str(key) + '=' + str(var[key]) + ';'

        info_line = info_line.rstrip(";")
        line = var["chrom"] + '\t' + var["pos"] + '\t' + var['id'] + '\t' \
            + var['ref'] + '\t' + var['alt'] + '\t' + var['qual'] + '\t' \
            + var['filter'] + '\t' + info_line
        data.append(line + '\n')
    return data