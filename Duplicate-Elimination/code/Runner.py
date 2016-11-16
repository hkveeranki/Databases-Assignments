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
        fd = open(relation_name, 'rb')
        return fd
    except IOError:
        sys.stderr.write("No File for the Relation " + relation_name
                         + " exists\n")
        sys.exit(-1)


def get_next(fd, store, input_buffers, output_buffer, buffer_size):
    """
    Performs the Get Next Operation
    :param fd: file_descriptor to the input csv file
    :param store: index structure we are using
    :param input_buffers: all the input buffers
    :param output_buffer: output buffer
    :param buffer_size: size of each buffer (in length)
    :return: False if file is finished else true
    """
    # check if the file is completely done
    global cnt, LIM
    cnt += 1
    current_record = fd.readline().strip()
    if len(current_record) == 0:
        do_process(store, input_buffers, output_buffer, buffer_size)
        return False
    current_record = tuple(map(int, current_record.split(',')))

    # Check whether the buffers are full
    current = -1
    for buffer_index in range(len(input_buffers)):
        if len(input_buffers[buffer_index]) < buffer_size:
            current = buffer_index
            break
    if cnt >= LIM or (current == len(input_buffers) - 1
                      and len(input_buffers[current]) == buffer_size - 1):
        input_buffers[current].append(current_record)
        do_process(store, input_buffers, output_buffer, buffer_size)
        cnt = 0
        return True
        # DO the processing and return
    input_buffers[current].append(current_record)
    return get_next(fd, store, input_buffers, output_buffer, buffer_size)


def close(fd):
    """
    performs close the iterator operations
    :param fd: File descriptor of input file
    """
    fd.close()


def empty_output(output_buffer):
    """
    Flush the output buffer onto the file
    :param output_buffer: the output buffer
    """
    global total
    total += len(output_buffer)
    del output_buffer[:]


def do_process(store, input_buffers, output_buffer, buffer_size):
    """
    Process the data in input buffers
    :param store: index structure we are using
    :param input_buffers: input buffers
    :param output_buffer: the output buffer
    :param buffer_size: size of each buffer in length
    """
    for buffer_index in range(len(input_buffers)):
        for j in input_buffers[buffer_index]:
            if not store.search(j):
                store.insert(j)
                output_buffer.append(j)
                if len(output_buffer) == buffer_size:
                    empty_output(output_buffer)
    empty_output(output_buffer)
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
    finished = False
    output_buffer = []
    while not finished:
        finished = not get_next(fd, store, input_buffers, output_buffer, buffer_size)
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
    p = len(open(file_name, 'r').readline().strip().split(','))  # Get the Size of the record
    buffer_length = s / p * 4  # Assuming 32 bit integers
    t = max(s / (16 + 8 * p), 3)
    # noinspection PyGlobalUndefined
    global LIM, cnt
    cnt = 0
    LIM = 800
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
    print time_taken, total
