class Reader:
    def sourceReader(self, filename ):
        sourceCode = list()
        fileobj = open(filename, "r")
        for item in fileobj.readlines():
            if item.find("#def") == -1:
                sourceCode.append(item)
        return sourceCode