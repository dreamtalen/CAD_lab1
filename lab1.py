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
    input_port_list = []
    output_port_list = []
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

    with open('test.val') as file_val:
        for line in file_val.readlines():
            input_port, val = line.split()
            input_port_list.append(input_port)
            value_dict[input_port] = int(val)

    with open('test.bench') as file_bench:
        for line in file_bench.readlines():
            line = line.strip()
            if line.startswith('#'):    pass
            elif line.startswith('INPUT'): pass
            elif line.startswith('OUTPUT'): output_port_list.append(line[7:-1])
            elif line:
                left, right = [x.strip() for x in line.split('=')]
                # left_part = line[:line.find('=')].strip()
                # right_part = line[line.find('=')+1:].strip()
                function_name, operand_list = right[:right.find('(')], [i.strip() for i in right[right.find('(')+1:-1].split(',')]
                # print function_name, operand_list
                value_dict[left] = function_dict[function_name.lower()]([value_dict[port] for port in operand_list])
            else:   pass

    with open('test_1.out', 'w') as file_out:
        for output_port in output_port_list:
            file_out.write(output_port+' '+str(value_dict[output_port])+'\n')

    # print input_port_list, output_port_list, value_dict

if __name__ == '__main__':
    main()