from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client


class InfluxStorage(object):
	"""docstring for InfluxStorage"""
	def __init__(self, host="127.0.0.1", port=8086, bucket=None, token=None, org=None):
		super(InfluxStorage, self).__init__()
		self.client = influxdb_client.InfluxDBClient(
		    url=f"{host}:{port}",
		    token=token,
		    org=org
		)
		self.org = org

	def point(self,measurement,tags=None,fields=None):
		if tags is None:
			tags = []
		if fields is None:
			fields = []
		p = influxdb_client.Point(measurement)
		for tag in tags:
			if tag[1] is None:
				continue
			p = p.tag(tag[0],tag[1])
		for field in fields:
			if field[1] is None:
				continue
			p = p.field(field[0],field[1])
		return p

	def write(self,bucket,point):
		wa = self.client.write_api(write_options=SYNCHRONOUS)
		wa.write(bucket=bucket,org=self.org,record=point)
		wa.close()
		return point

	def getOne(self,bucket,range_,condition=None,skip=None,orderby=None):
		qa = self.client.query_api()
		query = f"""
			from(bucket:"{bucket}")
			|> range(start: {range_})\
			|> filter(fn: (r) => {condition})
			|> first()
		"""

	def getMany(self,bucket,range_,fields=None,condition=None,skip=None,orderby=None,limit=None,selectors=None,aggregations=None):
		qa = self.client.query_api()
		query = f"""from(bucket:"{bucket}")\
			|> range(start: {range_}) """
		if condition is None:
			if fields is None:
				query += f"""|> filter(fn: (r) => {condition}) """
			else:
				query += f"""|> filter(fn: (r) => {condition} and r._field =~ /{'|'.join(fields)}/)\
				|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")"""
		elif fields is not None:
			query += f"""|> filter(fn: (r) => r._field =~ /{'|'.join(fields)}/)\
			|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")"""

		if selectors is None:
			selectors = []
		for selector in selectors:
			query += f"""|> filter(fn: (r) => {select})"""

		if aggregations is None:
			aggregations = []
		for aggregation in aggregations:
			query += f"""|> {aggregation}"""
		for r in qa.query_stream(org=self.org,query=query.strip()):
			yield r

	def streamQuery(self,query):
		qa = self.client.query_api()
		for r in qa.query_stream(org=self.org,query=query.strip()):
			yield r