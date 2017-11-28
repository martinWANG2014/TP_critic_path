# the MyObject class of a node in graphic.
class MyObject:
    def __init__(self, node_id, processing_time, predecessor_list):
        self.node_id = node_id
        self.processing_time = processing_time
        self.latest_start_time = float("-inf")
        self.earliest_finish_time = float("+inf")
        self.predecessor_list = predecessor_list
        self.rank = -1

    def update_latest_start_time(self, latest_start_time):
        self.latest_start_time = max(latest_start_time, self.latest_start_time)

    def update_earliest_finish_time(self, earliest_finish_time):
        self.earliest_finish_time = min(earliest_finish_time, self.earliest_finish_time)

    def update_rank(self, rank):
        self.rank = rank

    def get_predecessor_list(self):
        return self.predecessor_list

    def update_predecessor_list(self, predecessor_list):
        self.predecessor_list = predecessor_list

    def get_node_id(self):
        return self.node_id

    def get_rank(self):
        return self.rank

    def get_processing_time(self):
        return self.processing_time

    def get_latest_start_time(self):
        return self.latest_start_time

    def get_earliest_finish_time(self):
        return self.earliest_finish_time

    def clone(self):
        return MyObject(self.node_id, self.processing_time, self.predecessor_list[:])


# to calculate the rank of each node.
def calculate_rank(my_list_object):
    list_object_tmp = []
    for i in range(len(list_object)):
        list_object_tmp.append(list_object[i].clone())
    current_rank = 0
    last_length = len(list_object_tmp)
    while len(list_object_tmp) > 0:
        list_node_remove = []
        list_index_remove = []
        for i in range(len(list_object_tmp)):
            list_predecessor = list_object_tmp[i].get_predecessor_list()
            node_id = int(list_object_tmp[i].get_node_id())
            if len(list_predecessor) == 0:
                my_list_object[node_id - 1].update_rank(current_rank)
                list_node_remove.append(str(node_id))
                list_index_remove.append(i)

        # remove the empty array
        list_index_remove = sorted(list_index_remove, reverse=True)
        for index in list_index_remove:
            list_object_tmp.pop(index)

        # remove the element that has marked from the predecessor list.
        for i in range(len(list_object_tmp)):
            list_predecessor_new = list_object_tmp[i].get_predecessor_list()
            for node in list_node_remove:
                if node in list_predecessor_new:
                    list_predecessor_new.remove(node)
                    list_object_tmp[i].update_predecessor_list(list_predecessor_new)

        if len(list_object_tmp) == last_length:
            sorted(list_object_tmp, key=lambda x: len(x.get_predecessor_list()))
            node_id = int(list_object_tmp[0].get_node_id())
            my_list_object[node_id - 1].update_rank(current_rank)
            list_node_remove = list_object_tmp[0].get_predecessor_list()
            list_object_tmp[0].update_predecessor_list([])
            for i in range(len(list_object_tmp)):
                list_predecessor_new = list_object_tmp[i].get_predecessor_list()
                for node in list_node_remove:
                    if node in list_predecessor_new:
                        list_predecessor_new.remove(node)
                        list_object_tmp[i].update_predecessor_list(list_predecessor_new)
        else:
            current_rank += 1
        last_length = len(list_object_tmp)


# to sort the list of node by order of rank
def sort_by_rank(my_list_object, sense):
    return sorted(my_list_object, key=lambda x: x.get_rank(), reverse=sense)


# to calculate the critic path
def calculate_critic_path(my_list_object):
    my_list_object = sort_by_rank(my_list_object, False)
    # calculate the latest start time.
    for i in range(len(my_list_object)):
        list_predecessor = my_list_object[i].get_predecessor_list()
        if len(list_predecessor) == 0:
            my_list_object[i].update_latest_start_time(0)
        else:
            for node in list_predecessor:
                for j in range(0, i):
                    if node == my_list_object[j].get_node_id():
                        my_list_object[i].update_latest_start_time(int(my_list_object[j].get_processing_time()) +
                                                                   int(my_list_object[j].get_latest_start_time()))

    my_list_object = sort_by_rank(my_list_object, True)
    rank_highest = my_list_object[0].get_rank()
    # calculate the earliest finish time.
    for i in range(len(my_list_object)):
        list_predecessor = my_list_object[i].get_predecessor_list()

        if my_list_object[i].get_rank() == rank_highest:
            my_list_object[i].update_earliest_finish_time(my_list_object[i].get_latest_start_time())
        for node in list_predecessor:
            for j in range(i + 1, len(my_list_object)):
                if node == my_list_object[j].get_node_id():
                    my_list_object[j].update_earliest_finish_time(int(my_list_object[i].get_earliest_finish_time())
                                                                  - int(my_list_object[j].get_processing_time()))
    # get the critic path
    my_critic_path = []
    for i in range(len(my_list_object)):
        if my_list_object[i].get_earliest_finish_time() == my_list_object[i].get_latest_start_time():
            my_critic_path.append([my_list_object[i].get_node_id(), my_list_object[i].get_rank()])
    my_critic_path.reverse()
    return my_critic_path


# read data from file.
def read_from_file(filename):
    object_list = []
    with open(filename, "r") as fic:
        while True:
            my_object_line = fic.readline().split()
            if len(my_object_line) == 0:
                break
            # print(my_object_line)
            predecessor_list = []
            if len(my_object_line) > 2:
                predecessor_list = my_object_line[2].split(",")
            # print(predecessor_list)
            my_object = MyObject(my_object_line[0], my_object_line[1], predecessor_list)
            object_list.append(my_object)
    return object_list


list_object = read_from_file("example.txt")
calculate_rank(list_object)
print("critic path: [node_id, rank]: ", calculate_critic_path(list_object))

