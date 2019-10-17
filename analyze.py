import os

def reduce_max(max_val, curr):
    if curr > max_val:
        max_val = curr
    return max_val


def analyze_file(input_txt):
    #input_txt = "./dbsnp/1.txt"
    with open(input_txt, 'r') as f:
        max_pos = 0
        line_count = 0
        for content in f:
            content = content.strip().split("\t")
            if len(content) < 2:
                break
            pos = content[1]
            pos = int(pos)
            max_pos = reduce_max(max_pos, pos)
            line_count += 1
            if line_count % 10000000 == 0:
                print("%d line read in %s" % (line_count, input_txt))

        print("%s max_pos: %d" % (input_txt, max_pos))
        return max_pos


def main():
    input_dir = "./dbsnp"
    max_pos_dict = dict()

    for file_name in os.listdir(input_dir):
        input_txt = os.path.join(input_dir, file_name)
        max_pos = analyze_file(input_txt)
        max_pos_dict[input_txt] = max_pos
    
    for file_path, max_pos in max_pos_dict:
        print("%s has %d lines" % (file_path, max_pos))


if __name__ == "__main__":
    main()