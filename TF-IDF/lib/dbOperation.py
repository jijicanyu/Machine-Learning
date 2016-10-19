import rethinkdb as r
import hashlib
import json

'''
doc ={
     "id":
	 "NAME": "ni",
     "NUM":"1000",
	  }
'''

class dbOperation():
    def __init__(self):
        self.conn = r.connect(host="172.16.1.2",port=28015)
       # r.db_list().contains('Atlas').do(lambda databaseExists: r.branch(databaseExists, 0 ,r.db_create('Atlas'))).run(self.conn)
       # r.db('Atlas').table_create('DomainTable').run(self.conn)
        #r.db('Atlas').contains('DomainTable').do(lambda exists : r.branch( exists, 0,  r.db('Atlas').table_create('DomainTable'))).run(self.conn)
        self.table = r.db('Atlas').table("WordSearchCount")

    def Insert(self,document):
        dicthash=hashlib.md5(json.dumps(document['NAME'])).hexdigest()
        document["id"]=dicthash
        document.pop('NAME',None)
        return self.table.insert(document, conflict="update").run(self.conn)

    def queryWord(self,word):
        f=self.table.filter({'NAME':word}).run(self.conn)
        content=[]
        for i in f:
            content.append(i['NUM'])
        return content


# cur=dbOperation()
# a=cur.queryWord("1")
# print a
# print type(a)




