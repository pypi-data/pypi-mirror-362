import copy
import traceback
import time
import pymongo
import uuid
import adagenes
import adagenes.conf.read_config as conf_reader
import adagenes.app.app_tools
import adagenes.app.stats

def apply_filter(raw_data, data, filter_model, filter_key, val):
    for i, dc in enumerate(raw_data):
        #print(dc)
        dc_keys = {str(item).lower(): item for item in list(dc.keys())}

        count = i
        if filter_key in dc_keys:
            key_orig = dc_keys[filter_key]
            # text filters
            if filter_model[filter_key]["type"] == "contains":
                if val in dc[key_orig]:
                    data.append(dc)
            if filter_model[filter_key]["type"] == "notContains":
                if val not in dc[key_orig]:
                    data.append(dc)
            if filter_model[filter_key]["type"] == "startsWith":
                if dc[key_orig].startswith(val):
                    data.append(dc)
            if filter_model[filter_key]["type"] == "endsWith":
                if dc[key_orig].endswith(val):
                    data.append(dc)
            if filter_model[filter_key]["type"] == "blank":
                if dc[key_orig] == "" or dc[key_orig] == ".":
                    data.append(dc)
            if filter_model[filter_key]["type"] == "notBlank":
                if dc[key_orig] != "" and dc[key_orig] != ".":
                    data.append(dc)
            # numeric filters
            elif filter_model[filter_key]["type"] == "equals":
                try:
                    if str(val) == str(dc[key_orig]):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "notEqual":
                if str(val) != str(dc[key_orig]):
                    data.append(dc)
            elif filter_model[filter_key]["type"] == "greaterThan":
                try:
                    if float(dc[key_orig]) > float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "lessThan":
                try:
                    if float(dc[key_orig]) < float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "greaterThanOrEqual":
                try:
                    if float(dc[key_orig]) >= float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "lessThanOrEqual":
                try:
                    if float(dc[key_orig]) <= float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "inRange":
                try:
                    val2 = filter_model[filter_key]["filterTo"]
                    if float(val2) > float(dc[key_orig]) < float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
    return data

class DBConn:

    def __init__(self, file_id):
        db_name = conf_reader.__ADAGENES_DB_NAME__
        host = conf_reader.__ADAGENES_DB_SERVER__
        port = conf_reader.__ADAGENES_DB_PORT__
        self.client = self.connect_to_mongodb(host, port, db_name)
        self.db = self.client[db_name]
        self.collection = self.db[file_id]
        self.qid = file_id

    def close_connection(self):
        self.client.close()

    def connect_to_mongodb(self,host, port, db_name):
        time_start = time.time()
        print("Connect to MongoDB... ",host,": ",port)
        client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        #db = client[db_name]
        time_end = time.time()
        req_time = time_end - time_start
        print("connected ",req_time)
        return client

    def clear_collection(self,file_id):
        self.collection.drop()

    def insert_vcf(self,bframe, file_id, genome_version):

        #print("insert vcf ",genome_version,": ",bframe.data)

        collection = self.db[file_id]
        collection_header = self.db[file_id + '_' + 'headers']
        collection_add_cols = self.db[file_id + '_' + 'additional_columns']

        #print("add header lines ",bframe.header_lines)
        header_lines = bframe.header_lines
        collection_header.insert_one(
            {
                'headers': header_lines,
                'genome_version': genome_version,
                'annotations': [],
                'progress_msg': 'Uploading file',
                'progress_val': 0,
                'buffer_val': 0
            }
        )
        #print("")
        variants = []

        #print(bframe.data)

        for i, var in enumerate(bframe.data.keys()):
            variant = bframe.data[var]
            #print("insert variant ",variant)

            row_number = i+1
            chrom = variant["variant_data"]["CHROM"]
            pos = variant["variant_data"]["POS"]

            if "REF" in variant["variant_data"]:
                ref = variant["variant_data"]["REF"]
                alt = variant["variant_data"]["ALT"]
            else:
                pass
                #print("no ref ",var)

            if "ID" in variant["variant_data"]:
                q_id = variant["variant_data"]["ID"]
            else:
                q_id = '.'

            if "QUAL" in variant["variant_data"]:
                qual = variant["variant_data"]["QUAL"]
            else:
                qual = '.'

            if "FILTER" in variant["variant_data"]:
                filter = variant["variant_data"]["FILTER"]
            else:
                filter = '.'

            if "mutation_type_desc" in variant:
                mtype = variant["mutation_type_desc"]
            else:
                mtype=""

            #print("add variant ",variant)

            if "additional_columns" in variant:
                additional_columns = variant["additional_columns"]
                for add_col in additional_columns:
                    collection_add_cols.insert_one({add_col})

            variant_dc = {
                "row_number": row_number,
                "qid": var,
                "chrom": chrom,
                "pos": pos,
                "id": q_id,
                "ref": ref,
                "alt": alt,
                "qual": qual,
                "filter": filter,
                "mtype": mtype
            }

            #default_columns = ["CHROM","POS","REF","ALT","ID","FILTER","QUAL",""]
            if "info_features" in variant.keys():
                #print("info features ",variant["info_features"])
                for key in variant["info_features"]:
                    variant_dc[key] = variant["info_features"][key]

            # add pos columns
            if "POS_hg38" in variant["variant_data"]:
                variant_dc["pos_hg38"] = variant["variant_data"]["POS_hg38"]
            if "POS_hg19" in variant["variant_data"]:
                variant_dc["pos_hg19"] = variant["variant_data"]["POS_hg19"]
            if "POS_t2t" in variant["variant_data"]:
                variant_dc["pos_t2t"] = variant["variant_data"]["POS_t2t"]

            if "POS2" in variant["variant_data"]:
                variant_dc["pos2"] = variant["variant_data"]["POS2"]
                if "POS2_hg38" in variant["variant_data"]:
                    variant_dc["pos2_hg38"] = variant["variant_data"]["POS2_hg38"]
                if "POS2_hg19" in variant["variant_data"]:
                    variant_dc["pos2_hg19"] = variant["variant_data"]["POS2_hg19"]
                if "POS2_t2t" in variant["variant_data"]:
                    variant_dc["pos2_t2t"] = variant["variant_data"]["POS2_t2t"]

            # TODO: add additional columns

            #print("insert db data ",variant_dc)
            #collection.insert_one(variant)
            variants.append(variant_dc)

        if variants:
            collection.insert_many(variants)

        collection.create_index([("row_number", pymongo.ASCENDING), ("qid", pymongo.ASCENDING)])
        #print("db data ",file_id,": ",collection[file_id])

    def get_header_lines(self, file_id):
        collection_header = self.db[file_id + "_headers"]
        header_lines = collection_header.find_one()
        return header_lines

    def update_annotations(self,file_id, annotations):
        """

        :param file_id:
        :param annotations:
        :return:
        """
        #print("update annotations header ",file_id)
        collection_header = self.db[file_id + "_headers"]
        header_lines = collection_header.find_one()
        #print("header lines ",header_lines)
        if "annotations" in header_lines.keys():
            lines = header_lines["annotations"] + annotations
        else:
            lines = annotations
        #genome_version = header_lines["genome_version"]
        #info_lines = header_lines["headers"]
        #header_lines = {"headers": info_lines, 'genome_version': genome_version, 'annotations': lines}

        lines = header_lines["headers"]
        genome_version = header_lines["genome_version"]
        annotations = header_lines["annotations"] + annotations
        progress_msg = header_lines["progress_msg"]
        progress_val = header_lines["progress_val"]
        buffer_val = header_lines["buffer_val"]

        header_lines = {
            'headers': lines,
            'genome_version': genome_version,
            'annotations': annotations,
            'progress_msg': progress_msg,
            'progress_val': progress_val,
            'buffer_val': buffer_val
        }

        #print("Add new header ",header_lines)
        collection_header.drop()
        collection_header.insert_one(header_lines)

    def update_progress_msg(self, progress_msg, progress_val, buffer_val):
        """
        Updates the progress status and message of a request

        :param progress_msg:
        :param progress_val:
        :param buffer_val:
        :return:
        """
        collection_header = self.db[self.qid + "_headers"]
        header_lines = collection_header.find_one()
        if header_lines is not None:
            lines = header_lines["headers"]
            genome_version = header_lines["genome_version"]
            annotations = header_lines["annotations"]
            progress_msg = progress_msg
            progress_val = progress_val
            buffer_val = buffer_val

            header_lines = {
                'headers': lines,
                'genome_version': genome_version,
                'annotations': annotations,
                'progress_msg': progress_msg,
                'progress_val': progress_val,
                'buffer_val': buffer_val
            }
            collection_header.drop()
            collection_header.insert_one(header_lines)

    def query_progress_msg(self):
        collection_header = self.db[self.qid + "_headers"]
        header_lines = collection_header.find_one()
        print("headers: ",header_lines)
        if header_lines is not None:
            progress_msg = header_lines["progress_msg"]
            progress_val = header_lines["progress_val"]
            buffer_val = header_lines["buffer_val"]
            return progress_msg, progress_val, buffer_val
        else:
            return "Uploading file", 60, 70

    def update_progress_status(self, file_id, progress_msg, progress_val, buffer_val):
        collection_header = self.db[file_id + "_headers"]
        header_lines = collection_header.find_one()
        lines = header_lines["headers"]
        genome_version = header_lines["genome_version"]
        annotations = header_lines["annotations"]

        header_lines = {
            'headers': lines,
            'genome_version': genome_version,
            'annotations': annotations,
            'progress_msg': progress_msg,
            'progress_val': progress_val,
            'buffer_val': buffer_val
        }

        collection_header.drop()
        collection_header.insert_one(header_lines)

    def generate_new_header_lines(self, mapping):
        raw_data = self.collection.find()
        data = []
        for i, dc in enumerate(raw_data):
            data.append(dc)

        #if "gene" in mapping.keys():
        #    gene = mapping["gene"]
        #    variant = mapping["variant"]

        reserved_features = ['_id', 'row_number', 'type', 'mutation_type', 'mdesc', 'orig_identifier']

        info_lines_ids = []
        info_lines = []
        for dc in data:
            for feature in dc:
                if feature not in reserved_features:
                    #print(data)
                    field_id = feature.lower()
                    fiele_name = feature
                    info_line = f'##INFO=<ID={field_id},Number=1,Type=String,Description="">'
                    if field_id not in info_lines_ids:
                        info_lines.append(info_line)
                        info_lines_ids.append(field_id)

        print("transformed header lines ",info_lines)
        self.update_header_lines(self.qid, info_lines)

    def update_header_lines(self, file_id, info_lines):
        # update header lines
        collection_header = self.db[file_id + "_headers"]
        header_lines = collection_header.find_one()
        #print("Header lines ", header_lines)
        lines = header_lines["headers"] + info_lines
        genome_version = header_lines["genome_version"]
        annotations = header_lines["annotations"]
        progress_msg = header_lines["progress_msg"]
        progress_val = header_lines["progress_val"]
        buffer_val = header_lines["buffer_val"]

        header_lines = {
            'headers': lines,
            'genome_version': genome_version,
            'annotations': annotations,
            'progress_msg': progress_msg,
            'progress_val': progress_val,
            'buffer_val': buffer_val
        }
        collection_header.drop()
        collection_header.insert_one(header_lines)

    def transform_vcf(self, vcf_lines, genome_version):
        bulk_operations = []
        for i, var in enumerate(vcf_lines.keys()):

            print("to vcf: ",vcf_lines[var])

            #if hasattr(magic_obj, 'labels'):
            #    labels = magic_obj.labels
            #else:
            #    labels = None

            #annotations = adagenes.app.app_tools.generate_annotations_db(magic_obj.srv_prefix, vcf_lines[var],
            #                                                             magic_obj.extract_keys, labels)
            # print("generated annotations ",annotations)

            # variant_raw = self.collection[var]
            # print("update ",vcf_lines[var])
            filter = {"orig_identifier": vcf_lines[var]['orig_identifier']}

            variant_raw = self.collection.find_one(filter)

            #all_data = self.collection.find()
            #for var in all_data:
            #    print("all data ",var)

            variant = None
            if variant_raw:
                # print("var data ",variant)
                #variant = variant_raw
                variant = { "CHROM": vcf_lines[var]["variant_data"]["CHROM"],
                            "POS":vcf_lines[var]["variant_data"]["POS"],
                            "REF":vcf_lines[var]["variant_data"]["REF"],
                            "ALT":vcf_lines[var]["variant_data"]["ALT"],
                            }

                # for i, dc in enumerate(variant_raw):
                #    #print(dc)
                #    count = i
                #    variant = dc

                # print("add new annotations ",annotations)
                # print("add to dc ",variant)
                #for annotation in annotations.keys():
                #    variant[annotation] = annotations[annotation]
                # print("update db data ",variant)

                if genome_version == "hg19":
                    if "POS_t2t" in variant.keys():
                        variant["pos"] = variant["POS_hg19"]
                elif genome_version == "t2t":
                    if "POS_t2t" in variant.keys():
                        variant["pos"] = variant["POS_t2t"]

            else:
                print("Variant not found ", var)
                # variant =

            # print("var data ",variant)
            if variant is not None:
                bulk_operations.append(pymongo.UpdateOne(filter, {'$set': variant}, upsert=True))
            else:
                print("variant not found ",filter)

        start_time = time.time()
        if bulk_operations:
            self.collection.bulk_write(bulk_operations)
        end_time = time.time()
        print("Time for updates: ", end_time - start_time)
        self.collection.create_index([("row_number", pymongo.ASCENDING), ("qid", pymongo.ASCENDING)])

    def update_csv(self,vcf_lines, genome_version, magic_obj):
        """

                    :param bframe:
                    :param file_id:
                    :param annotations:
                    :return:
                    """
        bulk_operations = []
        for i, var in enumerate(vcf_lines.keys()):

            if hasattr(magic_obj, 'labels'):
                labels = magic_obj.labels
            else:
                labels = None

            annotations = adagenes.app.app_tools.generate_annotations_db(magic_obj.srv_prefix, vcf_lines[var],
                                                                         magic_obj.extract_keys, labels)
            # print("generated annotations ",annotations)

            # variant_raw = self.collection[var]
            # print("update ",vcf_lines[var])
            filter = {"orig_id": vcf_lines[var]['orig_identifier']}

            variant_raw = self.collection.find_one(filter)

            variant = None
            if variant_raw:
                # print("var data ",variant)
                variant = variant_raw

                # for i, dc in enumerate(variant_raw):
                #    #print(dc)
                #    count = i
                #    variant = dc

                # print("add new annotations ",annotations)
                # print("add to dc ",variant)
                for annotation in annotations.keys():
                    variant[annotation] = annotations[annotation]
                # print("update db data ",variant)

                if genome_version == "hg19":
                    if "POS_t2t" in variant.keys():
                        variant["pos"] = variant["POS_hg19"]
                elif genome_version == "t2t":
                    if "POS_t2t" in variant.keys():
                        variant["pos"] = variant["POS_t2t"]

                # collection.update_one(filter_criteria,variant)
                # print("update filter criteria ",filter_criteria)
                # print("db update ",variant)
                # result = self.collection.update_one(filter_criteria, {'$set': variant})
            else:
                print("Variant not found ", var)
                # variant =

            # print("var data ",variant)
            if variant is not None:
                bulk_operations.append(pymongo.UpdateOne(filter, {'$set': variant}, upsert=True))

        start_time = time.time()
        if bulk_operations:
            self.collection.bulk_write(bulk_operations)
        end_time = time.time()
        print("Time for updates: ", end_time - start_time)
        self.collection.create_index([("row_number", pymongo.ASCENDING), ("qid", pymongo.ASCENDING)])

    def update_vcf(self,vcf_lines, genome_version, magic_obj):
            """

            :param bframe:
            :param file_id:
            :param annotations:
            :return:
            """
            bulk_operations = []
            for i, var in enumerate(vcf_lines.keys()):

                if hasattr(magic_obj, 'labels'):
                    labels = magic_obj.labels
                else:
                    labels = None

                annotations = adagenes.app.app_tools.generate_annotations_db(magic_obj.srv_prefix, vcf_lines[var], magic_obj.extract_keys, labels)
                #print("generated annotations ",annotations)

                #variant_raw = self.collection[var]
                #print("update ",vcf_lines[var])
                filter = {"qid": var}

                variant_raw = self.collection.find_one(filter)

                variant = None
                if variant_raw:
                    #print("var data ",variant)
                    variant=variant_raw

                    # for i, dc in enumerate(variant_raw):
                    #    #print(dc)
                    #    count = i
                    #    variant = dc

                    #print("add new annotations ",annotations)
                    #print("add to dc ",variant)
                    for annotation in annotations.keys():
                        variant[annotation] = annotations[annotation]
                    #print("update db data ",variant)

                    if genome_version == "hg19":
                        if "POS_t2t" in variant.keys():
                            variant["pos"] = variant["POS_hg19"]
                    elif genome_version == "t2t":
                        if "POS_t2t" in variant.keys():
                            variant["pos"] = variant["POS_t2t"]

                    #collection.update_one(filter_criteria,variant)
                    #print("update filter criteria ",filter_criteria)
                    #print("db update ",variant)
                    #result = self.collection.update_one(filter_criteria, {'$set': variant})
                else:
                    print("Variant not found ",var)
                    #variant =

                #print("var data ",variant)
                if variant is not None:
                    bulk_operations.append(pymongo.UpdateOne(filter, {'$set': variant}, upsert=True))

            start_time = time.time()
            if bulk_operations:
                self.collection.bulk_write(bulk_operations)
            end_time = time.time()
            print("Time for updates: ",end_time - start_time)
            self.collection.create_index([("row_number", pymongo.ASCENDING), ("qid", pymongo.ASCENDING)])

    def import_vcf(self,bframe, file_id, genome_version):
        self.collection.drop()

        self.insert_vcf(bframe, file_id, genome_version)

    def import_csv(self,bframe, file_id, genome_version):
        collection = self.db[file_id]
        collection_header = self.db[file_id + '_' + 'headers']
        collection_add_cols = self.db[file_id + '_' + 'additional_columns']

        # print("add header lines ",bframe.header_lines)
        header_lines = ["CSV"]
        collection_header.insert_one({'headers': header_lines, 'genome_version': genome_version, 'annotations': []})
        variants = []

        for i, var in enumerate(bframe.data.keys()):
            print(var)
            variant = bframe.data[var]

            row_number = i + 1

            variant_dc = { "row_number": row_number }
            for key in variant.keys():
                variant_dc[key] = variant[key]

            print("insert ",variant_dc)
            variants.append(variant_dc)

        if variants:
            collection.insert_many(variants)

        collection.create_index([("row_number", pymongo.ASCENDING), ("qid", pymongo.ASCENDING)])
        # print("db data ",file_id,": ",collection[file_id])

    def parse_info_field(self,info_str):
        info = {}
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info[key] = value
            else:
                info[item] = True
        return info

    def generate_random_file_id(self):
        return str(uuid.uuid4())

    def get_header(self,db, file_id):
        collection_header = db[file_id + "_headers"]
        header_data = collection_header.find()

        genome_version = None
        header_lines = None
        for dc_header in header_data:
            if "genome_version" in dc_header.keys():
                genome_version = dc_header["genome_version"]
            if "headers" in dc_header.keys():
                header_lines = dc_header["headers"]

        return genome_version, header_lines

    def query_vcf(
            self,
            file_id,
            filter_model=None,
            sort_model=None,
            start_row=None,
            end_row=None,
            genome_version=None) -> (list, int, list):

        collection_header = self.db[file_id + '_' + 'headers']
        header_data = collection_header.find()

        header_lines=None
        for dc_header in header_data:
            #print("HEADER LINES ",dc_header)
            if "headers" in dc_header.keys():
                header_lines = dc_header["headers"]

        raw_data = self.collection.find()

        #print("return data for ", file_id, ": ", raw_data)
        data = []
        count=0
        #print("apply filter ", filter_model)

        # filter
        if not filter_model:
            for i, dc in enumerate(raw_data):
                data.append(dc)
        else:
            for filter_key in filter_model.keys():
                if "filter" in filter_model[filter_key]:
                    val = filter_model[filter_key]["filter"]
                    data = []

                    data = apply_filter(raw_data, data, filter_model, filter_key, val)
                    raw_data = copy.deepcopy(data)
                elif "conditions" in filter_model[filter_key]:
                    if filter_model[filter_key]["operator"] == "AND":
                        #print("Apply and filter")
                        for condition in filter_model[filter_key]["conditions"]:
                            val = condition["filter"]
                            data = apply_filter(raw_data, data, {filter_key : condition}, filter_key, val)
                            raw_data = copy.deepcopy(data)
                            data = []
                            #print("after filter ",len(raw_data)," ",len(data))
                        data = copy.deepcopy(raw_data)
                    elif filter_model[filter_key]["operator"] == "OR":
                        datasets = []
                        for condition in filter_model[filter_key]["conditions"]:
                            val = condition["filter"]
                            datasets.append(apply_filter(raw_data, data, {filter_key: condition}, filter_key, val))
                        data = []
                        for sublist in datasets:
                            data.extend(sublist)
                        raw_data = copy.deepcopy(data)

                #data_new = copy.deepcopy(data)
                #raw_data = copy.deepcopy(data)
            #data = copy.deepcopy(data_new)


        #print("Unsorted ",data)
        # sort
        if sort_model is not None:
            for sort_option in sort_model:
                if sort_option["sortable"] is True:
                    #print("sort option ",sort_option)
                    field = sort_option["field"]
                    if sort_option["sort"] is not None:
                        asc = sort_option["sort"]
                        field_orig = sort_option["headerName"]

                        if sort_option["filter"] == 'agNumberColumnFilter':
                            sorting_func = lambda x: sort_mixed_keys(x, field, field_orig)
                        else:
                            sorting_func = lambda x: sort_text(x, field, field_orig)

                        if asc == "desc":
                            reverse = True
                        elif asc == "asc":
                            reverse = False
                        data = sorted(data, reverse=reverse, key=sorting_func)

        count = len(data)

        stats = adagenes.app.stats.generate_stats(data)

        # start and end row
        # TODO
        data_page = []
        for dc in data:
            if start_row is not None and end_row is not None:
                row = dc["row_number"]

                if genome_version is not None:
                    #print("check for genome version ",genome_version,": ",dc)
                    if genome_version=="hg19" and "POS_hg19" in dc:
                        dc["pos"] = dc["POS_hg19"]
                    elif genome_version=="hg38" and "POS_hg38" in dc:
                        dc["pos"] = dc["POS_hg38"]
                    elif genome_version=="t2t" and "POS_t2t" in dc:
                        dc["pos"] = dc["POS_t2t"]

                if start_row <= row <= end_row:
                    data_page.append(dc)

            else:
                data_page.append(dc)

        #print("data page ",data_page)
        #print("query header lines ",header_lines)
        return data_page, count, header_lines, stats

def load_bframe_from_db_data(raw_data, genome_version,mapping=None):
        data = {}
        orig_ids = {}
        #print("load bframe from data ",genome_version)
        for i, dc in enumerate(raw_data):
            #print("dc ",dc)

            if genome_version == "hg19":
                if "POS_hg19" in dc.keys():
                    dc["pos"] = dc["POS_hg19"]
            elif genome_version == "t2t":
                if "POS_t2t" in dc.keys():
                    dc["pos"] = dc["POS_t2t"]
            elif genome_version == "hg38":
                if "POS_hg38" in dc.keys():
                    dc["pos"] = dc["POS_hg38"]

            if mapping is None:
                qid_orig = dc["qid"]
                qid = "chr" + str(dc["chrom"]) + ":" + str(dc["pos"]) + str(dc["ref"]) + ">" + str(dc["alt"])
                data[qid_orig] = dc
                data[qid_orig].pop("_id")
                data[qid_orig].pop("row_number")
                data[qid_orig].pop("qid")

                orig_ids[qid_orig] = qid
            else:
                if "gene" in mapping.keys():
                    qid = dc[mapping["gene"]] + ":" + dc[mapping["variant"]]
                    data[qid] = dc
                    if "gene" not in data[qid]:
                        data[qid]["gene"] = data[qid][mapping["gene"]]
                    if "variant" not in data[qid]:
                        data[qid]["variant"] = data[qid][mapping["variant"]]
                    data[qid]["type"] = "p"

        #bframe = adagenes.BiomarkerFrame(data)
        return data, orig_ids

    #data_dir = os.getenv("DATA_DIR")
    #filepath= data_dir + "/sample.vcf"
    #bframe = ag.read_file(filepath)
    #file_id = generate_random_file_id()
    #import_vcf(bframe, file_id)

    #data = query_vcf(file_id)
    #print("data ",data)

    #for dc in data:
    #    print(dc)

def sort_mixed_keys(x, field, field_orig):
    if field in x:
        key = x[field]
        if isinstance(key, int):
            return (0, key)  # Numeric values come first, sorted by their value
        else:
            return (1, key)  # Non-numeric values come after numeric values, sorted alphabetically
    elif field_orig in x:
        key = x[field_orig]
        if isinstance(key, int):
            return (0, key)  # Numeric values come first, sorted by their value
        else:
            return (1, key)  # Non-numeric values come after numeric values, sorted alphabetically
    else:
        return (2,)  # Field not present, these come last


def sort_text(x, field, field_orig):
    if field in x:
        key = x[field]
        if isinstance(key, str):
            return (0, key)
        else:
            return (1, key)
    elif field_orig in x:
        key = x[field_orig]
        if isinstance(key, str):
            return (0, key)
        else:
            return (1, key)
    else:
        return (2,)
