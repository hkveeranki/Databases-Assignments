import sys
import timeit

from Btree import Btree
from Hashing import MyHashStore


def open_file(relation_name):
    """Opens the file and sets up the iterator
    :param relation_name: name of the csv file having data`
    :return: returns file descriptors to input and output files
    """
    try:
        fd = open(relation_name, 'r')
        return fd
    except IOError:
        sys.stderr.write("No File for the Relation " + relation_name
                         + " exists\n")
        sys.exit(-1)


def get_next(fd, store, input_buffers, buffer_size):
    """
    Performs the Get Next Operation
    :param fd: file_descriptor to the input csv file
    :param store: index structure we are using
    :param input_buffers: all the input buffers
    :param output_buffer: output buffer
    :param buffer_size: size of each buffer (in length)
    """
    # check if the file is completely done
    current = 0
    while True:
        current_record = fd.readline().strip()
        if len(current_record) == 0:
            #sys.stderr.write("Reached End. Processing Now\n")
            do_process(store, input_buffers)
            break
        if len(input_buffers[current]) == buffer_size:
            prev_current = current
            current += 1
            #sys.stderr.write("Current changed from: " + str(prev_current) + " to " + str(current) + "\n")
        # Check whether the buffers are full
        if (current == len(input_buffers) - 1
            and len(input_buffers[current]) == buffer_size - 1):
            input_buffers[current].append(current_record)
            #sys.stderr.write("Reached limit. Processing Now\n")
            do_process(store, input_buffers)
            global total
            #sys.stderr.write("Processing Done. Total so_far is " + str(total) + "\n")
            continue
            # DO the processing and return
        else:
            input_buffers[current].append(current_record)


def close(fd):
    """
    performs close the iterator operations
    :param fd: File descriptor of input file
    """
    fd.close()


def do_process(store, input_buffers):
    """
    Process the data in input buffers
    :param store: index structure we are using
    :param input_buffers: input buffers
    """
    global total
    done = 0
    prev_done = 0
    for buffer_index in range(len(input_buffers)):
        for j in input_buffers[buffer_index]:
            done += 1
            if done - prev_done == 10000:
               # sys.stderr.write("Done so far:" + str(done) + "\n")
                prev_done = done
            if not store.search(j):
                store.insert(j)
                total += 1
    for input_buffer in input_buffers:
        del input_buffer[:]


def duplicate(relation_name, input_buffers, type_of_index, buffer_size, degree):
    """
    Function to perform duplicate elimination
    :param degree: the minimum degree if needed for B-Tree
    :param relation_name: name of csv file having relation
    :param input_buffers: the input buffers
    :param type_of_index: the type of index we gonna use
    :param buffer_size: the size of each buffer in terms of length
    """

    store = Btree(degree)
    if type_of_index == "hash":
        store = MyHashStore()
    fd = open_file(relation_name)
    get_next(fd, store, input_buffers, buffer_size)
    close(fd)


if __name__ == "__main__":
    args = sys.argv[1].split(" ")
    if len(args) != 4:
        sys.stderr.write("Incorrect Parameters passed")
        sys.exit(-1)
    file_name = args[0]
    n = int(args[1])
    s = int(args[2])
    index_type = int(args[3])
    index = "B-Tree"
    p = len(open(file_name, 'r').readline().strip().split(',')) * 8  # Get the Size of the record
    buffer_length = int(s / p)  # Assuming 32 bit integers
    t = int(max(s / (2 * p + p), 3))
    #sys.stderr.write("Taken t as:" + str(t) + "\n")
    #sys.stderr.write("Taken buffer_len as:" + str(buffer_length) + "\n")
    global LIM, cnt
    cnt = 0
    LIM = 10000 - 100  # Safety
    sys.setrecursionlimit(10000)
    if index_type == 1:
        index = "hash"
    buffers = []

    for i in range(n - 1):
        buffers.append([])
    global total

    total = 0
    start_time = timeit.default_timer()
    duplicate(file_name, buffers, index, buffer_length, t)
    time_taken = timeit.default_timer() - start_time
    print(time_taken, total)
