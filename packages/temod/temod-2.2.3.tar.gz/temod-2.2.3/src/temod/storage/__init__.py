from temod.base import Entity, Join, Cluster
from .mysql import *

REGISTRED_STORAGES = {
	"mysql":{
		Entity: MysqlEntityStorage,
		Join: MysqlJoinStorage,
		Cluster: MysqlClusterStorage
	}
}