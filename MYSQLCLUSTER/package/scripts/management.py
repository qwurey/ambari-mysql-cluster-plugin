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

class Management(Script):

    def install(self, env):
        Logger.info("install mysql cluster management")
        import params
        env.set_params(params)
        # remove_mysql_cmd = "yum remove mysql -y"
        # Execute(remove_mysql_cmd,
        #         user='root'
        #         )
        remove_mysql_lib_cmd = "rpm -e --nodeps mysql-libs-5.1.71-1.el6.x86_64 >/dev/null 2>&1"
        Execute(remove_mysql_lib_cmd,
                user='root'
                )
        install_server_cmd = "yum -y install MySQL-Cluster-server-gpl-7.4.11-1.el6.x86_64"
        Execute(install_server_cmd,
                user='root'
                )
        # create mgm config dir
        Directory(params.mgm_config_path,
                  owner='root',
                  group='root',
                  recursive=True
                  )
        # create cluster config
        Logger.info('create config.ini in /var/lib/mysql-cluster')
        File(format("{mgm_config_path}/config.ini"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.config_ini_template)
             )
        Execute('ndb_mgmd -f /var/lib/mysql-cluster/config.ini --initial  >/dev/null 2>&1', logoutput = True)
        # create pid file
        pid_cmd = "pgrep -o -f ^ndb_mgmd.* > {0}".format(params.mgm_pid_file)
        Execute(pid_cmd,
                logoutput=True)


    def configure(self, env):
        Logger.info("config mgm node")
        import params
        env.set_params(params)
        File(format("{mgm_config_path}/config.ini"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.config_ini_template)
             )


    def start(self, env):
        Logger.info("start mgm node")
        import params
        env.set_params(params)
        self.configure(env)
        Execute('ndb_mgmd -f /var/lib/mysql-cluster/config.ini  >/dev/null 2>&1', logoutput = True)
        pid_cmd = "pgrep -o -f ^ndb_mgmd.* > {0}".format(params.mgm_pid_file)
        Execute(pid_cmd,
                logoutput=True)

    def stop(self, env):
        Logger.info("stop mgm node")
        import params
        env.set_params(params)
        Execute(params.stop_mgm_ndb_cmd, logoutput = True)
        File(params.mgm_pid_file, action = 'delete')


    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.mgm_pid_file)


    def uninstall(self, env):
        Logger.info("uninstall mgm node")

if __name__ == "__main__":
    Management().execute()
