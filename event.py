class event:
    def __init__(self, data):
        self.plain = data
        self.course = data[1].strip("SUMMARY:")

    def __str__(self):
        return self.course

    def __repr__(self):
        return str(self)
