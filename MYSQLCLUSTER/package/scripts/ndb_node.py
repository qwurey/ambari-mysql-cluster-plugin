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

from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
from mysql_service import *

class NDB(Script):

    def install(self, env):
        import params
        env.set_params(params)
        Logger.info("install mysql cluster server")
        # remove_mysql_cmd = "yum remove mysql -y"
        # Execute(remove_mysql_cmd,
        #         user='root'
        #         )
        remove_mysql_lib_cmd = "rpm -e --nodeps mysql-libs-5.1.71-1.el6.x86_64  >/dev/null 2>&1"
        Execute(remove_mysql_lib_cmd,
                user='root'
                )
        install_server_cmd = "yum -y install MySQL-Cluster-server-gpl-7.4.11-1.el6.x86_64"
        Execute(install_server_cmd,
                user='root'
                )
        # create ndb_data_path
        Directory(params.ndb_data_path,
                  owner='root',
                  group='root',
                  recursive=True
                  )
        # create my.cnf
        Logger.info('create my.cnf in /etc/')
        File(format("{slave_node_config_path}/my.cnf"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.slave_config_template)
             )
        Execute("ndbd --initial",
                user='root'
                )


    def configure(self, env):
        Logger.info("config ndb node")
        import params
        env.set_params(params)


    def start(self, env):
        Logger.info("start ndb node")
        import params
        env.set_params(params)
        Execute("ndbd",
                user='root'
                )


    def status(self, env):
        import params
        env.set_params(params)


    def stop(self, env):
        Logger.info("stop ndb node")
        import params
        env.set_params(params)


    def uninstall(self, env):
        Logger.info("uninstall ndb node")

if __name__ == "__main__":
    NDB().execute()
