import psycopg2
import re
import Crypto
import Revision

connectionStr   = "host='127.0.0.1' dbname='modSlicer' user='postgres' password='hamham123'"
connection      = psycopg2.connect(connectionStr)
cursor          = connection.cursor()

class Database:
    def databaseSliceCheck(self, sliceName ):
        cursor.execute("SELECT slicename FROM slicedict WHERE slicename = E'" + re.escape(sliceName) + "';" )
        rows = cursor.fetchall()
        connection.commit()
        return rows

    def databaseSimSlicenameCheck(self, sliceName ):
        cursor.execute("SELECT slicename FROM slicedict WHERE slicename LIKE E'%" + re.escape(sliceName) + "%';")
        rows = cursor.fetchall()
        connection.commit()
        return rows
    
    def databaseUpdate(self, resultDict, authorId):
        for key, value in resultDict.items():
            if re.escape(key) != "":
                res = Database.databaseModuleCheck(re.escape(key))
                if res == list():
                    try:
                        cr                  = Crypto.Crypto
                        rev                 = Revision.Revision
                        param               = value[0]
                        source              = value[3]
                        actualRevisionId    = rev.computeRevision(key, source)
                        shaSum              = cr.shaHashing( re.escape(key+source) )
                        importListing       = value[4]
                        sliceLanguage       = "py"  # TODO: Language analyzing by Filename
                        
                        cursor.execute("INSERT INTO slicedict (slicename, parameters, authorId, actualRevisionId, shaSum) VALUES (E'" + re.escape(key) + "', '" + re.escape(param) + "', '" + re.escape(authorId) + "', '" + re.escape(actualRevisionId) + "', '" + re.escape(shaSum) + "');")
                        cursor.execute("SELECT sliceId FROM slicedict WHERE sliceName = E'" + re.escape(key) + "' AND actualRevisionId = E'" + re.escape( actualRevisionId ) + "';")
                        sliceId = cursor.fetchall()
                        connection.commit()
                        
                        cursor.execute("INSERT INTO slicerev ( sliceId, revisionId, revision, authorId ) VALUES (" + re.escape(sliceId) + ", E'" + re.escape(actualRevisionId) + "', 1, E'" + re.escape(authorId) + "');") # revision = 1 'cuz first commit
                        cursor.execute("INSERT INTO importdict ( sliceId, revisionId, importListing ) VALUES (" + re.escape(sliceId) + ", E'" + re.escape(actualRevisionId) + "', E'" + re.escape(importListing) + "');")
                        cursor.execute("INSERT INTO slicesrc (sliceId, revisionId, authorid, source, sliceLanguage, sourceHash) VALUES (E'" + re.escape(sliceId) + "', E'"+re.escape(actualRevisionId)+"',E'" + re.escape(authorId) + "', E'" + re.escape(source) + "', E'" + re.escape(sliceLanguage) + "',E'"+ re.escape(cr.shaHashing(source)) +"');")
                        connection.commit()
                        
                        # TODO:
                        # For-loop for sliceTags
                        # "INSERT INTO slicetags ( sliceId, sliceTag ) VALUES (" + re.escape(sliceId) + ", E'" + re.escape(sliceTag) + ");"
                        
                        # TODO:
                        # Get all authors, chain em, store in sliceDoc (maybe deprecated 'cuz we are the only authors :O)
                        # "INSERT INTO sliceDoc ( sliceId, revisionId, documentation, dependencyflag, authorid ) VALUES (" + re.escape( sliceId ) + ", E'" + re.escape( revisionId ) + "', E'" + re.escape( documentation ) + "', E'" + re.escape( dependencyFlag ) + "', E'" + re.escape(authorId) + "');"
                        # "INSERT INTO sliceLang ( sliceId, sliceLanguage ) VALUES ( " + sliceId + ", E'" + sliceLanguage + "');"
                        # "INSERT INTO slicePatterncontainer ( sliceName, sliceId, sliceLanguage, chimaeraGroupPrint, revisionId ) VALUES (E'" + re.escape( sliceName ) + "', " + re.escape(sliceId) + ", E'" + re.escape( sliceLang ) + "', E'" + chimaeraGroupPrint + "', E'" + re.escape( revisionId ) + ");"
                        # "INSERT INTO sliceTimestamps ( sliceId, timestamp, revisionId, revision, authorId ) VALUES ( " + re.escape( sliceId ) + ", E'" + re.escape( timestamp ) + "', E'" + re.escape( revisionId ) + "', " + re.escape( revision ) + ", E'" + authorId + "' );"
                        
                    finally:
                        print "Stored Function \"" + re.escape(key) + "\" in Database."
                    
                elif res != list():
                    print "Module with the same name (" + re.escape(key) + ") already exists, sorry!"
                else:
                    print "Key>\t" + re.escape(key) + "\nValue>\t"+ re.escape(value)
            # GOGOGO!!
            connection.commit()
            key     = ""
            value   = ""
            # TODO: Create Revisionfeature and add hashing
            
    def revisionCheck(self, modName):
        cursor.execute("SELECT revisionId, revision FROM moduleSrc WHERE modulename = '" + re.escape(modName) + "';")
        rows = cursor.fetchall()
        
        connection.commit()
        if rows != list():
            revisions = dict()
            for row in rows:
                revisions[row[0]] = row[1]
            return revisions
    return dict()

    def updRevision(self, sliceName, revisionId, revision):
        cursor.execute("UPDATE moduleSrc SET revisionId = '" + re.escape(revisionId) + "', revision = " + re.escape(revision) + " WHERE modulename = '" + re.escape(sliceName) + "';")
        connection.commit()
