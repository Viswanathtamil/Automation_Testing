class VysfinPaginator:
    index = None
    has_next = None
    has_previous = None
    limit = 10

    def __init__(self):
        pass

    def __init__(self, data_list, index, limit):
        length = len(data_list)
        self.index = index
        self.limit = limit
        if index <= 1:
            self.has_previous = False
        else:
            self.has_previous = True
        if length > self.limit:
            self.has_next = True
        else:
            self.has_next = False

    def set_index(self, index):
        self.index = index

    def set_has_next(self, has_next):
        self.has_next = has_next

    def set_has_previous(self, has_previous):
        self.has_previous = has_previous

    def set_limit(self, limit):
        self.limit = limit

    def get_index(self):
        return self.index

    def get_has_next(self):
        return self.has_next

    def get_has_previous(self):
        return self.has_previous

    def get_limit(self):
        return self.limit