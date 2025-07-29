import mysql.connector

class MysqlStorage():
	def __init__(self, user="",password="",host="",port=3306,database="",connexion=None,auth_plugin='mysql_native_password'):
		super(MysqlStorage, self).__init__()
		self.connexion = connexion
		self.credentials = {
			"user":user,
			"password":password,
			"host":host,
			"port":port,
			"database":database,
			"auth_plugin":auth_plugin
		}

	def connect(self,force=False):
		if(self.connexion is not None and not force):
			return self.connexion
		self.connexion = mysql.connector.connect(**self.credentials)
		return self.connexion
	
	def close(self):
		if self.connexion is None:
			return
		self.connexion.close()
		self.connexion = None

	def cursor(self):
		try:
			return self.connect().cursor()
		except:
			return self.connect(force=True).cursor()

	def executeAndCommit(self,query):
		cursor = self.cursor()
		try:
			cursor.execute(query)
			self.connexion.commit()
		finally:
			try:
				cursor.close()
			except ReferenceError:
				pass
			self.close()
		return cursor

	def getOne(self,query):
		cursor=self.cursor()
		self.connexion.commit()
		try:
			query=(query)
			cursor.execute(query)
			result = cursor.fetchone()
			columns = cursor.column_names
		finally:
			try:
				cursor.close()
			except ReferenceError:
				pass
		if result is not None:
			return {col:result[i] for i,col in enumerate(columns)}
		self.close()

	def getMany(self,query):
		cursor=self.cursor()
		try:
			cursor.execute(query)
			columns = cursor.column_names
			for row in cursor.fetchall():
				yield {col:row[i] for i,col in enumerate(columns)}
		finally:
			try:
				cursor.close()
			except ReferenceError:
				pass
			self.close()

	def searchMany(self,select,condition=None,orderby=None,skip=None,limit=None):
		query = select
		if condition is not None:
			query += f' WHERE {condition}'
		if orderby is not None:
			query += f' ORDER BY {orderby}'
		if limit is not None:
			query += f' LIMIT {limit}'
			if skip is not None:
				query += f' OFFSET {skip}'
		for row in self.getMany(query):
			yield row
	
