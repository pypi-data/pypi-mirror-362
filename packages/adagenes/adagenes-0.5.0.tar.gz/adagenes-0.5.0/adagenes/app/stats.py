import traceback, re
import adagenes as ag


def get_max_score(score):
    elements = score.split(";")
    score_max = 0
    for el in elements:
        if el !=".":
            try:
                if float(el) > score_max:
                    score_max = float(el)
            except:
                print(traceback.format_exc())
    return score_max

def contains_alphabetic_characters(s):
    # Regular expression pattern to match any alphabetic character (A-Z or a-z)
    pattern = re.compile(r'[A-Za-z]')
    return bool(pattern.search(s))

def sort_protein_domains_genes(prot_domains, x_title = "protein_domains", y_title="domain_mutations"):
    gene_mutation_array = list(prot_domains.items())

    # Sort the array by the number of mutations in descending order
    gene_mutation_array.sort(key=lambda x: x[1], reverse=True)

    # Take the top N genes
    top_n = 10
    top_genes = gene_mutation_array[:top_n]

    # Separate the genes and mutations into two arrays
    genes = [entry[0] for entry in top_genes]
    mutations = [entry[1] for entry in top_genes]

    return {
        x_title: genes,
        y_title: mutations
    }

def sort_protein_domains(prot_domains, x_title = "protein_domains", y_title="domain_mutations"):
    gene_mutation_array = list(prot_domains.items())

    # Sort the array by the number of mutations in descending order
    gene_mutation_array.sort(key=lambda x: x[1], reverse=True)

    # Take the top N genes
    top_n = 10
    top_genes = gene_mutation_array[:top_n]

    # Separate the genes and mutations into two arrays
    genes = [entry[0] for entry in top_genes]
    mutations = [entry[1] for entry in top_genes]

    return {
        x_title: genes,
        y_title: mutations
    }

def sort_gene_mut_freq(prot_domains, x_title="genes", y_title="mutations"):
    gene_mutation_array = []

    for gene, data in prot_domains.items():
        mutations = len(data['mutations'])
        pathogenicity = data['pathogenicity']
        avg_pathogenicity = sum(pathogenicity) / len(pathogenicity) if pathogenicity else 0
        gene_mutation_array.append((gene, mutations, avg_pathogenicity))

    # Sort the array by the number of mutations in descending order
    gene_mutation_array.sort(key=lambda x: x[1], reverse=True)

    # Take the top N genes
    top_n = 10
    top_genes = gene_mutation_array[:top_n]

    # Separate the genes, mutations, and average pathogenicity into arrays
    genes = [entry[0] for entry in top_genes]
    mutations = [entry[1] for entry in top_genes]
    avg_pathogenicity = [entry[2] for entry in top_genes]

    return {
        x_title: genes,
        y_title: mutations,
        'avg_pathogenicity': avg_pathogenicity
    }

#def sort_gene_mut_freq(gene_mutations):
#    gene_mutation_array = list(gene_mutations.items())#
#
#    # Sort the array by the number of mutations in descending order
#    gene_mutation_array.sort(key=lambda x: x[1], reverse=True)#
#
#    # Take the top N genes
#    top_n = 10
#    top_genes = gene_mutation_array[:top_n]
#
#    # Separate the genes and mutations into two arrays
#    genes = [entry[0] for entry in top_genes]
#    mutations = [entry[1] for entry in top_genes]#
#
#    return {
#        'genes': genes,
#        'mutations': mutations
#    }

def generate_stats(variants):
    mut_types = {"SNP":0,"INS":0,"DEL":0,"CNV":0}

    stats = {}

    stats["variants"] = {}
    stats["variants"]["total"] = len(variants)


    graphs = {}
    graphs["mtype"] = {
        "data":[{
            "x": list(mut_types.keys()),
            "y": [],
            "type": "bar"
        }],
        "layout":{"title": "Variant types"}
    }

    #"data": [
    #    {
    #        "x": [1, 2, 3],
    #        "y": [4, 5, 6],
    #        "type": "scatter"
    #    }
    #],
    #"layout": {
    #    "title": "Sample Plot"
    #}
    vars_prot_coding = 0
    vars_patho_am = 0
    vars_patho_am_prot_coding = 0
    prot_domains = {}
    vars_benign_am = 0

    ref_aas = {}
    alt_aas = {}

    gene_muts = {  }

    for var in variants:
        #print(var)

        # mutation type
        if "mtype" in var:
            #stats["mtype"]["data"].append({"qid":var,"type": var["mtype"]})
            if var["mtype"] in mut_types:
                #stats["mtype"]["data"][0]["y"].append(var["mtype"])
                mut_types[var["mtype"]] += 1
        else:
            pass

        # count gene mutations
        if "UTA_Adapter_gene_name" in var:

            patho_AM = 0
            if "dbnsfp_AlphaMissense_score" in var:
                patho_AM = get_max_score(var["dbnsfp_AlphaMissense_score"])
            if var["UTA_Adapter_gene_name"] not in gene_muts:
                gene_muts[var["UTA_Adapter_gene_name"]] = {"mutations": [1], "pathogenicity": [patho_AM] }

            gene_muts[var["UTA_Adapter_gene_name"]]["mutations"].append(1)
            gene_muts[var["UTA_Adapter_gene_name"]]["pathogenicity"].append(patho_AM)
            vars_prot_coding += 1

            ve = var["UTA_Adapter_variant_exchange"]
            aaref, pos, aaalt = ag.parse_variant_exchange(ve)
            if aaref not in ref_aas.keys():
                ref_aas[aaref] = 0
            ref_aas[aaref] += 1
            if aaalt not in alt_aas.keys():
                alt_aas[aaalt] = 0
            alt_aas[aaalt] += 1

        if "dbnsfp_AlphaMissense_score" in var:
            try:
                if var["dbnsfp_AlphaMissense_score"] != ".":
                    am_score = get_max_score(var["dbnsfp_AlphaMissense_score"])
                    if float(am_score) > 0.8:
                        vars_patho_am += 1
                        if "UTA_Adapter_gene_name" in var:
                            vars_patho_am_prot_coding += 1
                    elif float(am_score) < 0.2:
                        vars_benign_am += 1
            except:
                print(traceback.format_exc())

        # protein domains
        if "dbnsfp_Interpro_domain" in var:
            domain = var["dbnsfp_Interpro_domain"]
            if contains_alphabetic_characters(domain) and domain != ".":
                domains = domain.split(";")
                for dom in domains:
                    domains_pipe = dom.split("|")
                    for dom_pipe in domains_pipe:
                        dom_cm = dom_pipe.split(",")
                        for d in dom_cm:
                            if d not in prot_domains.keys():
                                prot_domains[d] = 0
                            prot_domains[d] += 1



    ref_aas = sort_protein_domains(ref_aas, x_title="ref_aa", y_title="number")
    alt_aas = sort_protein_domains(alt_aas, x_title="alt_aa", y_title="number")

    # Overall variant stats
    stats["variants"]["protein_coding"] = vars_prot_coding
    stats["variants"]["patho_AM"] = vars_patho_am
    stats["variants"]["patho_AM_prot_coding"] = vars_patho_am_prot_coding
    stats["variants"]["benign_AM"] = vars_benign_am
    stats["variants"]["Ref_AA"] = ref_aas
    stats["variants"]["Alt_AA"] = alt_aas

    graphs["mtype"]["data"][0]["y"] = list(mut_types.values())
    stats["mtype"] = mut_types
    stats["gene_mutations"] = sort_gene_mut_freq(gene_muts)#gene_muts
    stats["protein_domains"] = sort_protein_domains(prot_domains)
    #bframe = ag.BiomarkerFrame(data=variants)
    graphs["pathogenicity_heatmap"] = ag.generate_protein_pathogenicity_plot_variantlist(variants)

    stats = {"stats": stats, "graphs": graphs}
    return stats
