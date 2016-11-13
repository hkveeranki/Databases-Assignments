LOG_PREFIX = '../log/'
LOG_EXT = '.txt_'


def init(Xns):
    commit_undo = []
    for t in Xns:
        commit_undo.append(len(t))
    globalvars = {
        'A': 8,
        'B': 8,
        'C': 5,
        'D': 10
    }
    return commit_undo, globalvars
    pass


def get_string_from_dict(dict):
    return_str = ''
    for key, val in sorted(dict.items()):
        return_str += ' ' + str(key) + ' ' + str(val)
    return return_str


def get_dict_from_string(str):
    items = str.split(' ')
    length = len(items)
    i = 0
    dict = {}
    while i < length:
        dict[items[i]] = items[i + 1]
        i += 2
    return dict


def check_correctness(total_number, correct_vals):
    for quantum in xrange(1, total_number):
        undo_file_name = LOG_PREFIX + str(quantum) + LOG_EXT + 'undo'
        redo_file_name = LOG_PREFIX + str(quantum) + LOG_EXT + 'redo'
        undo_file = open(undo_file_name, 'ra')
        value_string = undo_file.readlines()[-1].split('>')[1].strip(' \n')
        undo_file.close()
        val_dict = get_dict_from_string(value_string)
        if val_dict == correct_vals:
            undo_file = open(undo_file_name, 'a')
            redo_file = open(redo_file_name, 'a')
            undo_file.write(str(quantum) + '\n')
            redo_file.write(str(quantum) + '\n')
            undo_file.close()
            redo_file.close()


def write_to_logfiles(undo_log, redo_log, quantum):
    # print undo_log
    # print redo_log
    undo_file_name = LOG_PREFIX + str(quantum) + LOG_EXT + 'undo'
    redo_file_name = LOG_PREFIX + str(quantum) + LOG_EXT + 'redo'
    undo_file = open(undo_file_name, 'w')
    redo_file = open(redo_file_name, 'w')
    undo_log_data = '\n'.join(undo_log) + '\n'
    redo_log_data = '\n'.join(redo_log) + '\n'
    # print undo_log_data, quantum
    undo_file.write(undo_log_data)
    redo_file.write(redo_log_data)
    undo_file.close()
    redo_file.close()


def round_robin(transacts, quantum):
    over = 0
    inst_order = []
    iter = [0, 0, 0]
    redo_commit = [0, 0, 0]
    commited = []
    cur = 0
    while over < len(transacts):
        rem = quantum
        while rem > 0:
            if iter[cur] == len(transacts[cur]):
                break
            action = transacts[cur][iter[cur]]
            if 'OUTPUT' in action and cur not in commited:
                commited.append(cur)
                redo_commit[cur] = iter[cur] + 1
            inst_order.append([action, cur])
            iter[cur] += 1
            if iter[cur] == len(transacts[cur]):
                # print 'over', cur
                over += 1
                break
            rem -= 1
        cur = (cur + 1) % 3
    return inst_order, redo_commit


def generate_log(transactions, quantum):
    inst_order, commit_redo = round_robin(transactions, quantum)
    # print 'roundrobin done for', quantum
    commit_undo, global_var = init(transactions)
    log_undo = []
    log_redo = []
    local_var = {}
    started = []
    so_far = [0 for i in xrange(len(transactions))]
    for inst in inst_order:
        action, trans = inst[0], inst[1]
        so_far[trans] += 1
        if trans not in started:
            values_string = get_string_from_dict(global_var)
            log_undo.append('<START T' + str(trans + 1) + '>' + values_string)
            log_redo.append('<START T' + str(trans + 1) + '>' + values_string)
            started.append(trans)
        if 'READ' in action:
            # Read Action so adjust the global variables
            rem, dest = action.split(',')
            src = rem.split('(')[1]
            dest = dest.strip(')')
            local_var[dest] = global_var[src]
        elif 'WRITE' in action:
            rem, src = action.split(',')
            dest = rem.split('(')[1]
            src = src.strip(')')
            prev = global_var[dest]
            global_var[dest] = local_var[src]
            values_string = get_string_from_dict(global_var)
            log_redo.append('<T' + str(trans + 1) + ', ' + str(dest) + ', ' + str(local_var[src]) + '>' + values_string)
            log_undo.append('<T' + str(trans + 1) + ', ' + str(dest) + ', ' + str(prev) + '>' + values_string)
        elif 'OUTPUT' in action:
            values_string = get_string_from_dict(global_var)
            if so_far[trans] == commit_undo[trans]:
                log_undo.append('<COMMIT T' + str(trans + 1) + '>' + values_string)
            if so_far[trans] == commit_redo[trans]:
                log_redo.append('<COMMIT T' + str(trans + 1) + '>' + values_string)
        else:
            # Do the eval
            lhs, rhs = action.split(':=')
            t = 0
            t1 = 0
            t2 = 0
            if 't' in rhs:
                t = local_var['t']
            if 't1' in rhs:
                t1 = local_var['t1']
            if 't2' in rhs:
                t2 = local_var['t2']
            local_var[lhs] = eval(rhs)

    # print 'Logfiles are',
    write_to_logfiles(log_undo, log_redo, quantum)
    pass


if __name__ == '__main__':
    t1 = ['READ(A,t)', 't:=t*2', 'WRITE(A,t)', 'READ(B,t)', 't:=t*2', 'WRITE(B,t)', 'OUTPUT(A)', 'OUTPUT(B)']
    t2 = ['READ(C,t1)', 'READ(D,t2)', 't1:=t1+t2', 'WRITE(C,t1)', 't1:=t1-t2', 't1:=t1+t2', 'WRITE(D,t1)', 'OUTPUT(C)',
          'OUTPUT(D)']
    t3 = ['READ(D,t)', 't:=t+1', 'WRITE(C,t)', 'READ(C,t)', 't:=t+1', 'WRITE(D,t)', 'OUTPUT(C)', 'OUTPUT(D)']
    transactions = [t1, t2, t3]
    total = max(len(t1), len(t2), len(t3))
    for num in xrange(1, total + 1):
        generate_log(transactions, num)
    last_file = open(LOG_PREFIX + str(total) + '.txt_undo', 'r')
    value_line = last_file.readlines()[-1].split('>')[1].strip(' \n')
    correct_dict = get_dict_from_string(value_line)
    last_file.close()
    check_correctness(total + 1, correct_dict)
