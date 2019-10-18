import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from collections import defaultdict

def reduce_max(max_val, curr):
    if curr > max_val:
        max_val = curr
    return max_val


# def init_stat(analyze_name, stat_dict, default_value):
#     if analyze_name not in stat_dict:
#         stat_dict[analyze_name] = default_value

#     return stat_dict[analyze_name]


def get_ref_dist(content, ref_dist):

    calc_seq(content, ref_dist, seq_name="ref")

    return ref_dist


def get_alt_dist(content, alt_dist):

    calc_seq(content, alt_dist, seq_name="alt")
    return alt_dist



def calc_seq(content, seq_distribution, seq_name):
    if seq_name == "ref":
        seqs = content[3]
    elif seq_name == "alt":
        seqs = content[4]

    for seq in seqs.split(","):
        seq_distribution[seq] += 1


def get_max_pos(content, max_pos):
    if len(content) < 2:
        return
    pos = content[1]
    pos = int(pos)
    max_pos = reduce_max(max_pos, pos)
    return max_pos


def analyze_file(input_txt, analyze_funcs: dict, stat_by_analyze):
    #input_txt = "./dbsnp/1.txt"
    print("reading %s" % input_txt)
    with open(input_txt, 'r') as f:
        line_count = 0
        for content in f:
            # read content and split
            content = content.strip().split("\t")

            # apply all analyze methods on single line
            for analyze_name, analyze_func in analyze_funcs.items():
                stat_by_analyze[analyze_name] = analyze_func(content, stat_by_analyze[analyze_name])

            # print log
            if line_count % 10000000 == 0:
                print("%d line read in %s" % (line_count, input_txt))
            line_count += 1


def save_stat_to_file(stat, stat_type, output_file):
    if stat_type == "dict":
        with open(output_file, 'w') as fw:
            for k, v in stat.items():
                fw.write(f"{k}\t{v}\n")
    elif stat_type == "int":
        print("stat for {} is {}".format(output_file, stat))


def pos_and_seq_count():
    input_dir = "./dbsnp"
    analyze_funcs = {
        "max_pos": get_max_pos, 
        "ref_dist": get_ref_dist, 
        "alt_dist": get_alt_dist
    }
    init_vals = {
        "max_pos": 0, 
        "ref_dist": defaultdict(int), 
        "alt_dist": defaultdict(int)
    }

    stat_types = {
        "max_pos": "int", 
        "ref_dist": "dict", 
        "alt_dist": "dict"
    }

    output_files = {
        "max_pos": "max_pos.console", 
        "ref_dist": "./ref_dist.txt",
        "alt_dist": "./alt_dist.txt"
    } 

    # for file_name in glob.glob(os.path.join(input_dir, "*.txt")):
    for file_name in ["X.txt", "Y.txt"]:
        # skip all other files
        # if file_name != "22.txt":
        #     continue

        # stat_dict init
        stat_by_analyze = dict()
        
        for analyze_name, init_val in init_vals.items():
            # print("initing {} as {}".format(analyze_name, init_val))
            stat_by_analyze[analyze_name] = init_val


        input_txt = os.path.join(input_dir, file_name)

        analyze_file(input_txt, analyze_funcs, stat_by_analyze)
    
        for stat_name, stat in stat_by_analyze.items():
            save_stat_to_file(stat, stat_types[stat_name], output_files[stat_name]+"."+file_name)


def get_ref_alt_len(row:list, stat:dict):
    ref = row[3]
    alt = row[4]
    combined_len = len(ref+alt)
    stat[combined_len] += 1
    return stat


def get_short_and_rest_stat(row:list, stat:dict):
    len_limit = 2
    ref = row[3]
    alt = row[4]
    combined_len = len(ref+alt)
    if combined_len <= len_limit:
        stat[f"<={len_limit}"] += 1
    else:
        stat[f">{len_limit}"] += 1

    return stat


def short_vs_rest():
    input_dir = "./dbsnp"
    analyze_funcs = {
        "short_vs_rest": get_short_and_rest_stat, 
    }
    init_vals = {
        "short_vs_rest": defaultdict(int)
    }

    stat_types = {
        "short_vs_rest": "dict"
    }

    output_files = {
        "short_vs_rest": "./short_vs_rest.txt"
    } 

    # for file_name in ["Y.txt"]:
    for input_txt in glob.glob(os.path.join(input_dir, "*.txt")):
        # skip all other files
        # if file_name != "22.txt":
        #     continue

        # stat_dict init
        stat_by_analyze = dict()
        file_name = os.path.basename(input_txt)
        
        for analyze_name, init_val in init_vals.items():
            # print("initing {} as {}".format(analyze_name, init_val))
            stat_by_analyze[analyze_name] = init_val



        analyze_file(input_txt, analyze_funcs, stat_by_analyze)
    
        for stat_name, stat in stat_by_analyze.items():
            save_stat_to_file(stat, stat_types[stat_name], output_files[stat_name]+"."+file_name)



def ref_alt_len_dist():
    input_dir = "./dbsnp"
    analyze_funcs = {
        "ref_alt_len_dist": get_ref_alt_len, 
    }
    init_vals = {
        "ref_alt_len_dist": defaultdict(int), 
    }

    stat_types = {
        "ref_alt_len_dist": "dict", 
    }

    output_files = {
        "ref_alt_len_dist": "./refalt_len_dist.txt", 
    } 

    # for file_name in ["Y.txt"]:
    for input_txt in glob.glob(os.path.join(input_dir, "*.txt")):
        # skip all other files
        # if file_name != "22.txt":
        #     continue

        # stat_dict init
        stat_by_analyze = dict()
        file_name = os.path.basename(input_txt)
        
        for analyze_name, init_val in init_vals.items():
            # print("initing {} as {}".format(analyze_name, init_val))
            stat_by_analyze[analyze_name] = init_val



        analyze_file(input_txt, analyze_funcs, stat_by_analyze)
    
        for stat_name, stat in stat_by_analyze.items():
            save_stat_to_file(stat, stat_types[stat_name], output_files[stat_name]+"."+file_name)


def plot_hist(ax:plt.Axes, d:dict):
    d = sorted(list(d.items()), key=lambda x: x[1], reverse=True)[:20]
    # tick_label = [row[0] for row in d]
    x = [row[1] for row in d]
    ax.bar(
        np.arange(len(x)), 
        x
        # tick_label=tick_label
    )


def read_dist_file(dist_file:str):
    print("reading {}".format(dist_file))
    seq_dist = dict()
    with open(dist_file, 'r') as f:
        for content in f:
            content = content.strip().split("\t")
            seq = content[0]
            count = int(content[1])
            seq_dist[seq] = count

    return seq_dist


def plot_seq_dist(seq_type):
    if seq_type == "ref":
        files_lookup = "./ref_dist*.txt"
    elif seq_type == "alt":
        files_lookup = "./alt_dist*.txt"
    else:
        files_lookup = seq_type

    plt_id = 1
    for seq_dist_file in glob.glob(files_lookup):
        seq_dist = read_dist_file(seq_dist_file)
        ax = plt.subplot(5, 6, plt_id)
        ax.set_xlabel(seq_dist_file)
        plot_hist(ax, seq_dist)
        plt_id += 1
    plt.show()


def plot_ref_seq_dist():
    plot_seq_dist("ref")


def plot_alt_seq_dist():
    plot_seq_dist("alt")


def read_pie_from_dist_with_top(dist:dict, top_k:int):
    dist = sorted(list(dist.items()), key=lambda x: x[1], reverse=True)
    names = [
        "-".join([row[0] for row in dist[:top_k]]), 
        "others"
    ]
    vals = [
        sum([row[1] for row in dist[:top_k]]), 
        sum([row[1] for row in dist[top_k:]])
    ]

    return names, vals


def read_pie(pie_file:str):
    names = []
    vals = []
    with open(pie_file) as f:
        for row in f:
            row = row.strip().split("\t")
            names.append(row[0])
            vals.append(int(row[1]))
    return names, vals


def pie_short_vs_rest():
    plt_id = 1
    for pie_file in glob.glob("./short_vs_rest*.txt"):
        pie_names, pie_vals = read_pie(pie_file)
        ax:plt.Axes = plt.subplot(5, 6, plt_id)
        ax.set_xlabel(pie_file)
        ax.pie(pie_vals, labels=pie_names, autopct="%1.1f%%")
        plt_id += 1
    plt.show()


def pie_top_k_char(top_k):
    plt_id = 1
    for dist_file in glob.glob("./refalt_len_dist*.txt"):
        char_len_dist = read_dist_file(dist_file)
        pie_names, pie_vals = read_pie_from_dist_with_top(char_len_dist, top_k)
        ax:plt.Axes = plt.subplot(5, 6, plt_id)
        ax.set_xlabel(dist_file)
        ax.pie(pie_vals, labels=pie_names, autopct="%1.1f%%")
        plt_id += 1
    plt.show()


def main():
    # plot_ref_seq_dist()
    # short_vs_rest()
    # pie_short_vs_rest()
    # plot_seq_dist("./refalt_len_dist*.txt")
    pie_top_k_char(20)


if __name__ == "__main__":
    main()