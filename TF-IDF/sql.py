#!coding=utf-8

import sqlite3

class sql_db:
	def __init__(self):
		self.db=sqlite3.connect("./test.db")  ##连接库，若没有则创建
		self.cur=self.db.cursor()
	
	def create_table(self):
		self.cur.execute("""create table ci_num (name varchar(100) UNIQUE,number varchar(100))""")  ##创建表

	def insert_db(self,**kwargs):
		tables=str(kwargs['table'])
		name=str(kwargs['name'])
		num=str(kwargs['num'])
	
		self.cur.execute("insert into '"+tables+"' values('"+name+"','"+num+"')")    ##执行插入语句
		self.db.commit()   ##提交修改

	def search_db(self,**kwargs):
		tables=kwargs['table']
		name=kwargs['name']

		self.cur.execute("select * from '"+tables+"' where name= '"+name+"'" )    ##查询
		return self.cur.fetchall()

	def update_db(self,**kwargs):  ##更新
		tables=kwargs['table']
		name=kwargs['name']
		num=str(kwargs['num'])

		self.cur.execute("update '"+tables+"' set number='"+num+"' where name = '"+name+"'") ##修改
		self.db.commit()

	def delete_db(self,**kwargs):  ##删除
		tables=kwargs['table']

		self.cur.execute("delete from '"+tables+"'")  ##删除
		self.db.commit()

	def close(self):
		self.cur.close()
		self.db.close()



# if __name__=="__main__":
# 	cur=sql_db()
# 	# cur.create_table()
# 	cur.search_db(table='ci_num')
# 	# cur.delete_db(table='ci_num')


