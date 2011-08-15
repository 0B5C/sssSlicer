# TODO: Syntaxanalyze for more programming languages
# NOTE: We could analyze the filetype to get the language. After that we 
#       get some regex from a regex module or something similiar.

# TODO: Catalogize whole classes
# Note: Maybe in next release

class Slicer(object):
    
    # Scans for the programming language
    def languageScanner(self, filename):
        ind0        = filename.find(".")
        length      = len(filename)
        filetype    = filename[ind0+1:length]
        return filetype
    
    # Scans for all members
    # TODO: What happens with members?
    # Note: Analyze of sourcecode, if a function uses a Member we should insert it in
    #       an extra databasetable with the relationinformation.
    def memberScanner(self, sourceCode):
        pass
    
    # Scans for Authortag etc.
    # TODO: get Author Tag etc ( and ''' ''' Comments)
    # NOTE: So we have to filter every scriptfile for their standardtags, maybe we could work
    #       with some Regexmagic
    def sourceTagScanner(self, sourceCode):
        pass
    
    # Scans for Slicetags
    # TODO: Class Tagging and flagging
    #        Flag is a sha 256 sum of the headclass.. if there are
    #        dependencys in the mod it flags every dependent function with the
    #        shasum and an autoinkrement (per dependency group)
    #        Tagging: Maybe we can create an own statement for that for example:
    #~slicetag: module, slicer, example Tag, common
    #        This we could place at the bottom of every function
    #        If no tags are listed we ask user for tags
    def sliceTagScanner(self, sliceSource):
        pass
    
    ##########################################################################
    # Returns dictionary which contains a list.. Structure:
    # modName                  = Name of function
    # startLine/endLine        = First and last line number of function
    # resultSource             = Source between first an last line
    #
    #    { modName, resList[parameters, startindex, endindex, sourcecode, importListing] }
    ##
    
    def findDefinition(self, sourceCode ):
        # TODO: Filter for mainclass
        # TODO: Filter for comments
    
        # Init some vars
        functionDict    =   dict()
        preResList      =   list()
        srcString       =   ""
        params          =   ""
        functionName    =   ""
        lineCounter     =   1
        startIndex      =   0
        found           =   False
    
        # for every line in our sourcecode:
        for item in sourceCode:
            found = False
            # try to find the definition clause
            val = item.find("def")
            valChk = item.find("):\n")
            valMain = item.find("if __name__ == \'__main__\':")
        
            if valMain != -1:
                print "Found Main, skipping! ("+"if __name__ == \'__main__\':"+")"
            # if we got a definition in the string set found True and reset params
            elif val != -1 and valChk != -1:
                srcString   =   ""
                found       =   True
                params      =   ""
            
                # cut definition<WHITESPACE>
                subFunctionName = item[4:]
            
                # get parameter
                ind0 = subFunctionName.find("(")
                ind1 = subFunctionName.find("):")
                params = subFunctionName[ind0+1:ind1]
            
                # get name
                ind0 = subFunctionName.find("(")
                functionName = subFunctionName[0:ind0]
                startIndex = lineCounter
                
                # TODO: get importListing
                importListing = ""
            
            # if we haven't got the clause and the found var was set to true:
            if found == False:
                # get source
                    srcString += item
                    if item.find("\t\n") == -1:
                        preResList.append(params)
                        preResList.append(startIndex)
                        preResList.append(lineCounter)
                        preResList.append(srcString)
                        preResList.append(importListing)
            # set found to false
            lineCounter += 1
            functionDict[functionName] = preResList
            preResList = list()
        
        return functionDict