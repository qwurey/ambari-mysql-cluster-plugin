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

class SQLNODE(Script):

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
        Logger.info("install mysql cluster client")
        install_client_cmd = "yum -y install MySQL-Cluster-client-gpl-7.4.11-1.el6.x86_64"
        Execute(install_client_cmd,
                user='root'
                )
        # create my.cnf
        Logger.info('create my.cnf in /etc/')
        File(format("{slave_node_config_path}/my.cnf"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.slave_config_template)
             )
        self.configure(env)
        self.start(env)
        # change root password
        # get init root pwd
        init_root_pwd = mysql_service().get_init_root_pwd()
        if '\'' in init_root_pwd:
            init_root_pwd.replace('\'', '\'"\'"\'')
        Logger.info(init_root_pwd)
        # run sh to change root init_root_password to mysql_root_password
        run_sh_cmd = "mysqladmin -u root -p'{0}' password '{1}' ".format(init_root_pwd, params.mysql_root_password)
        Logger.info(run_sh_cmd)
        Execute(run_sh_cmd,
                user='root'
                )
        # allow root user remote connection
        allow_remote_connec_cmd = "mysql -uroot -p{0} -e \"use mysql; update user set host = '%' where user = 'root' and host = 'localhost'; flush privileges;\"".format(params.mysql_root_password)
        Logger.info(allow_remote_connec_cmd)
        Execute(allow_remote_connec_cmd,
                user='root'
                )

    def configure(self, env):
        Logger.info("config sql node")
        import params
        env.set_params(params)

    def start(self, env):
        Logger.info("start sql node")
        import params
        env.set_params(params)
        Execute("mysqld_safe >/dev/null 2>&1 &",
                user='root'
                )

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.sql_node_pid_file_path)

    def stop(self, env):
        Logger.info("stop sql node")
        import params
        env.set_params(params)
        Execute(params.stop_sql_node_cmd,
                user='root'
                )

    def uninstall(self, env):
        Logger.info("uninstall sql node")

if __name__ == "__main__":
    SQLNODE().execute()
