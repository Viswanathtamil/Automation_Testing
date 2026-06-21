class VysfinPage:
    index = None
    offset = None
    limit =10
    query_limit = 10

    def __init__(self, index):
        self.index = index
        self.offset = (index-1)* 10
        self.limit = (index)* 10

    def __init__(self, index, limit):
        self.index = index
        self.limit = limit * index
        self.offset = (index - 1) * 10
        #print('page start')
        #print(self.index)
        #print(self.limit)
        #print(self.offset)
        #print('page ends')

    def get_index(self):
        return self.index

    def get_offset(self):
        return self.offset

    def get_limit(self):
        return self.limit

    def get_query_limit(self):
        return self.limit+1

    def get_data_limit(self):
        return self.limit -1

class VysfinPage1:
    index = None
    offset = None
    limit =None
    query_limit = 10

    def __init__(self, index):
        self.index = index
        self.offset = (index-1)* 10
        self.limit = (index)* 10

    def __init__(self, index, limit):
        self.index = index
        self.limit = limit * index
        self.offset = (index - 1) * 10
        # self.query_limit = limit
        #print('page start')
        #print(self.index)
        #print(self.limit)
        #print(self.offset)
        #print('page ends')

    def get_index(self):
        return self.index

    def get_offset(self):
        return self.offset

    def get_limit(self):
        return self.limit

    def get_query_limit(self):
        return self.limit + 1
    def get_data_limit(self):
        return self.limit -1

###PROOFING
class VysfinPage2:
    index = None
    offset = None
    limit =10
    query_limit = 10

    def __init__(self, index):
        self.index = index
        self.offset = (index-1)* 10
        self.limit = (index)* 10

    def __init__(self, index, limit):
        self.index = index
        self.limit = limit * index
        self.offset = (index - 1) * limit
        #print('page start')
        #print(self.index)
        #print(self.limit)
        #print(self.offset)
        #print('page ends')

    def get_index(self):
        return self.index

    def get_offset(self):
        return self.offset

    def get_limit(self):
        return self.limit

    def get_query_limit(self):
        return self.limit

    def get_data_limit(self):
        return self.limit -1

class VysfinPage_FA:
    index = None
    offset = None
    limit =10
    query_limit = 10
    def __init__(self, index, limit):
        self.index = index
        self.limit = limit * index
        self.offset = (index - 1) * limit

    def get_index(self):
        return self.index

    def get_offset(self):
        return self.offset

    def get_limit(self):
        return self.limit

    def get_query_limit(self):
        return self.limit+1

    def get_data_limit(self):
        return self.limit -1


class Rmu_VysfinPage:
    index = None
    offset = None
    limit =10
    query_limit = 10

    def __init__(self, index):
        self.index = index
        self.offset = (index-1)* 10
        self.limit = (index)* 10

    def __init__(self, index, limit):
        self.index = index
        self.limit = limit * index
        self.offset = (index - 1) * 50
        #print('page start')
        #print(self.index)
        #print(self.limit)
        #print(self.offset)
        #print('page ends')

    def get_index(self):
        return self.index

    def get_offset(self):
        return self.offset

    def get_limit(self):
        return self.limit

    def get_query_limit(self):
        return self.limit+1

    def get_data_limit(self):
        return self.limit -1

class VysfinPagefive:
    index = None
    offset = None
    limit = 5
    query_limit = 5

    def __init__(self, index):
        self.index = index
        self.offset = (index-1)* 5
        self.limit = (index)* 5

    def __init__(self, index, limit):
        self.index = index
        self.limit = limit * index
        self.offset = (index - 1) * 5
        #print('page start')
        #print(self.index)
        #print(self.limit)
        #print(self.offset)
        #print('page ends')

    def get_index(self):
        return self.index

    def get_offset(self):
        return self.offset

    def get_limit(self):
        return self.limit

    def get_query_limit(self):
        return self.limit+1

    def get_data_limit(self):
        return self.limit -1