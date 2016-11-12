def init(transactions):
    commit_undo = []
    log_u = []
    log_r = []
    for t in transactions:
        commit_undo.append(len(t) - 1)
        log_u.append([])
        log_r.append([])
    globalvars = {
        "A": 8,
        "B": 8,
        "C": 5,
        "D": 10
    }
    return commit_undo, globalvars, log_u, log_r
    pass


def write_to_logfiles(undo_log, redo_log):
    pass


def round_robin(transactions, quantum):
    over = 0
    inst_order = []
    iter = [0, 0, 0]
    redo_commit = [0, 0, 0]
    commited = []
    cur = 0
    while over < len(transactions):
        rem = quantum
        while rem > 0:
            action = transactions[cur][iter[cur]]
            if "OUTPUT" in action and cur not in commited:
                commited.append(cur)
                redo_commit[cur] = iter[cur]
            inst_order.append([action, cur])
            iter[cur] += 1
            if iter[cur] == len(transactions[cur]):
                over += 1
                break
            rem -= 1
        cur = (cur + 1) % 3
    return inst_order, redo_commit


def generate_log(transactions, quantum):
    inst_order, commit_redo = round_robin(transactions, quantum)
    global_var, commit_undo, log_undo, log_redo = init(transactions)
    local_var = {}
    so_far = [0 for i in len(transactions)]
    for inst in inst_order:
        action, trans = inst[0], inst[1]
        if "READ" in action:
            # Read Action so adjust the global variables
            rem, dest = action.split(",")
            src = rem.split(",")[1]
            local_var[dest] = global_var[src]
        elif "WRITE" in action:
            rem, src = action.split(",")
            dest = rem.split(",")[1]
            log_redo[trans].append("<" + "," + dest + "," + local_var[src] + ">")
            log_undo[trans].append("<" + "," + dest + "," + global_var[dest] + ">")
            global_var[dest] = local_var[src]
            pass
        elif "OUTPUT" in action:
            if so_far[trans] == commit_undo[trans]:
                log_undo[trans].append("<commit>")
            elif so_far[trans] == commit_redo[trans]:
                log_redo[trans].append("<commit>")
        else:
            # Do the eval
            src, dest = action.split("=")
    write_to_logfiles(log_undo, log_redo)
    pass


if __name__ == "__main__":
    t1 = ['READ(A,t)', 't:=t*2', 'WRITE(A,t)', 'READ(B,t)', 't:=t*2', 'WRITE(B,t)', 'OUTPUT(A)', 'OUTPUT(B)']
    t2 = ['READ(C,t1)', 'READ(D,t2)', 't1:=t1+t2', 'WRITE(C,t1)', 't1:=t1-t2', 't1:=t1+t2', 'WRITE(D,t1)', 'OUTPUT(C)',
          'OUTPUT(D)']
    t3 = ['READ(D,t)', 't:=t+1', 'WRITE(C,t)', 'READ(C,t)', 't:=t+1', 'WRITE(D,t)', 'OUTPUT(C)', 'OUTPUT(D)']
    transactions = [t1, t2, t3]
    for num in range(max(len(t1), len(t2), len(t3))):
        generate_log(transactions, num)
