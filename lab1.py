import argparse
parser = argparse.ArgumentParser()
parser.add_argument('bench_file')
parser.add_argument('val_file')

args = parser.parse_args()

bench_file = args.bench_file
val_file = args.val_file

def and_gate(operand_list):
    return operand_list[0] and and_gate(operand_list[1:]) if len(operand_list) > 1 else operand_list[0]

def or_gate(operand_list):
    return operand_list[0] or or_gate(operand_list[1:]) if len(operand_list) > 1 else operand_list[0]

def nand_gate(operand_list):
    return 0 if and_gate(operand_list) else 1

def nor_gate(operand_list):
    return 0 if or_gate(operand_list) else 1

def xor_gate(operand_list):
    return operand_list[0] ^ xor_gate(operand_list[1:]) if len(operand_list) > 1 else operand_list[0]

def xnor_gate(operand_list):
    return 0 if xor_gate(operand_list) else 1

def inverter(operand_list):
    return not operand_list[0]

def buffer_gate(operand_list):
    return operand_list[0]

def main():
    input_port_list, output_port_list = [], []
    DAG, in_degree_dict = {}, {}
    operand_list_dict, port_function_dict = {}, {}
    value_dict = {}

    function_dict = {
        'and': and_gate,
        'or': or_gate,
        'nand': nand_gate,
        'nor': nor_gate,
        'xor': xor_gate,
        'xnor': xnor_gate,
        'not': inverter,
        'buf': buffer_gate
    }

    with open(val_file) as file_val:
        for line in file_val.readlines():
            input_port, val = line.split()
            input_port_list.append(input_port)
            DAG[input_port] = []
            in_degree_dict[input_port] = []
            value_dict[input_port] = int(val)

    with open(bench_file) as file_bench:
        for line in file_bench.readlines():
            line = line.strip().replace(' ', '')
            if line.startswith('#'):    pass
            elif line.startswith('INPUT'): pass
            elif line.startswith('OUTPUT'): output_port_list.append(line[7:-1])
            elif line:
                left, right = line.split('=')
                function_name, operand_list = right[:right.find('(')], right[right.find('(')+1:-1].split(',')
                # print left, function_name, operand_list
                for operand in operand_list:
                    if operand not in DAG: DAG[operand] = [left]
                    else: DAG[operand].append(left)
                port_function_dict[left] = function_name
                if left not in DAG: DAG[left] = []
                in_degree_dict[left] = operand_list
                operand_list_dict[left] = operand_list[:]
            else:   pass

    # print DAG, in_degree_dict, port_function_dict, operand_list_dict

    # TopoSort
    topo_result = []
    while in_degree_dict:
        for port in [i for i in in_degree_dict.keys() if not in_degree_dict[i]]:
            topo_result.append(port)
            for next_port in DAG[port]:
                in_degree_dict[next_port].remove(port)
            in_degree_dict.pop(port)
    # print topo_result

    for port in topo_result:
        if port in port_function_dict:
            value_dict[port] = 1 if function_dict[port_function_dict[port].lower()]([value_dict[i] for i in operand_list_dict[port]]) else 0

    for output_port in output_port_list:
        print output_port + ' ' + str(value_dict[output_port])

if __name__ == '__main__':
    main()
