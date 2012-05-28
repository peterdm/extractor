# Case-sensitive exact matcher for sorted term file:  Binary Search O(log N)

class Searcher:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.f.seek(0,2)
        self.length = self.f.tell()
        
    def __contains__(self, string):
        low = 0
        high = self.length
        while low < high:
            mid = (low+high)//2
            p = mid
            while p >= 0:
                self.f.seek(p)
                if self.f.read(1) == '\n': break
                p -= 1
            if p < 0: self.f.seek(0)
            line = self.f.readline()
#            print '--', mid, line

            if line.strip() == string:
                return True  # Found
            elif line < string:
                low = mid+1
            else:
                high = mid

        return False

