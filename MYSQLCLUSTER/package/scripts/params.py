"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management.libraries.functions.default import default
from resource_management import *

config = Script.get_config()

# cluster info
mgm_host = config['clusterHostInfo']['mgm_hosts'][0]

# cluster conf
config_ini_template = config['configurations']['cluster-config']['content']
slave_config_template = config['configurations']['node-config']['content']

# mgm node
mgm_pid_file = "/var/run/mgm.pid"

# sql node
mysql_root_password = "Rootss-12345"

# path
mgm_config_path = "/var/lib/mysql-cluster"
ndb_data_path = "/usr/local/mysql/data"
sql_node_pid_path = "/var/run/mysqld/"
slave_node_config_path = "/etc"

stop_mgm_ndb_cmd = "ndb_mgm -e shutdown"
stop_sql_node_cmd = "service mysql stop"

hostname = None
if config.has_key('hostname'):
    hostname = config['hostname']
sql_node_pid_file_path = "/var/lib/mysql/{0}.pid".format(hostname)