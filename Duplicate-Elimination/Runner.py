import sys

from Btree import Btree
from Hashing import MyHashStore


def openFile(relation_name):
    """Opens the file and sets up the iterator
    :param relation_name: name of the csv file having data`
    :return: returns file descriptors to input and output files
    """
    try:
        fd = open(relation_name + '.csv', 'rb')
        output = open('result.csv', 'w')
        return fd, output
    except IOError:
        sys.stderr.write("No File for the Relation " + relation_name
                         + " exists\n")
        sys.exit(-1)


def GetNext(fd, store, input_buffers, output_buffer, buffer_size, output):
    """
    Performs the Get Next Operation
    :param output: file descriptor for Output file
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
        do_process(store, input_buffers, output_buffer, buffer_size, output)
        return False
    current_record = tuple(map(int, current_record.split(',')))

    # Check whether the buffers are full
    current = -1
    for buffer_index in range(len(input_buffers)):
        if len(input_buffers[buffer_index]) < buffer_size:
            current = buffer_index
            break
    if cnt >= LIM or (current == len(input_buffers) - 1 and
                              len(input_buffers[current]) == buffer_size - 1):
        input_buffers[current].append(current_record)
        do_process(store, input_buffers, output_buffer, buffer_size, output)
        cnt = 0
        return True
        # DO the processing and return
    input_buffers[current].append(current_record)
    return GetNext(fd, store, input_buffers, output_buffer, buffer_size, output)


def close(fd, output):
    """
    performs close the iterator operations
    :param output: File descriptor of  output file
    :param fd: File descriptor of input file
    """
    fd.close()
    output.close()


def empty_output(output_buffer, output):
    """
    Flush the output buffer onto the file
    :param output: file descriptor to the output file
    :param output_buffer: the output buffer
    """
    for out in output_buffer:
        output.write(','.join(map(str, out)) + '\n')
    del output_buffer[:]


def do_process(store, input_buffers, output_buffer, buffer_size, output):
    """
    Process the data in input buffers
    :param output: file descriptor to the output file
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
                    empty_output(output_buffer, output)
    empty_output(output_buffer, output)
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
    fd, output = openFile(relation_name)
    finished = False
    output_buffer = []
    while not finished:
        finished = not GetNext(fd, store, input_buffers, output_buffer, buffer_size, output)
    close(fd, output)


if __name__ == "__main__":
    file_name = raw_input('Enter the file name: ')
    s = int(raw_input("Size of Buffer: "))

    n = int(raw_input("Number of Buffers: "))
    index_type = int(raw_input("Do you want hash or B-Tree\n1-hash 2-B-Tree: "))
    index = "B-Tree"
    p = len(open(file_name + '.csv', 'r').readline().strip().split(','))  # Get the Size of the record
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
    duplicate(file_name, buffers, index, buffer_length, t)
