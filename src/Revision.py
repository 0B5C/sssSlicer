'''
Created on 10.08.2011

@author: obscurity
'''

import Crypto
import re
import Database

class Revision:
    def chgRevision(self, sliceName, revisionId, revision):
        pass
    
    def computeRevision(self, sliceName, sliceSrc):
        # query Database for revision
        db = Database.Database
        rev = db.revisionCheck(sliceName)
        if rev == dict():
            db.updRevision( sliceName, Revision.fingerprintRevision(sliceName, sliceSrc, 1) )
        elif rev != dict() and rev != list():
            returnMe= 0
            tmpNumb = 0
            for item in rev.items():
                tmpNumb = item
                if tmpNumb >= returnMe:
                    returnMe = tmpNumb
            print str(returnMe)
            revision = int(returnMe)+1
            db.updRevision( sliceName, Revision.fingerprintRevision(sliceName, sliceSrc, revision), revision)
        # if no revision is available do a fingerprint with revisionNumber as 1
        #     call addRevision with params
        # if revision is available get revisionNumber and increment it by 1, after that do fingerprint
        #     call chgRevision with params
        pass
    
    def fingerprintRevision(self, sliceName, sliceSrc, revisionNumber):
        fingerprint     = ""
        cr              = Crypto.Crypto
        computeString   = re.escape(sliceName+sliceSrc+str(revisionNumber))
        try:
            fingerprint = cr.shaHashing(computeString)
        finally:
            if fingerprint != "":
                return fingerprint