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

import commands
import os
from resource_management import *
from resource_management.core.logger import Logger


class mysql_service:
    """Provide MYSQL service tools

    """

    def create_expect_sh(self, env):
        """Create execExpect.sh file in /etc/mysql

        :param env:
        :return:
        """
        import params
        Logger.info('create execExpect.sh in /etc/mysql')
        File(os.path.join(params.mysql_config_path,'execExpect.sh'),
             owner = 'root',
             group = 'root',
             mode = 0777,
             content = Template("execExpect.sh.j2")
             )

    def executeCmd(self, cmd):
        """Execute given command, return (status, output)

        :param cmd:
        :return:
        """
        Logger.info("exec command: {0}".format(cmd))
        (status, output) = commands.getstatusoutput(cmd)
        return (status, output)

    def server_not_running(self):
        """Judge mysql server is running or not

        :return: True if is running, else False
        """
        cmd = "service mysqld status"
        (status, output) = self.executeCmd(cmd)
        Logger.error("mysql_server_not_running,status={0},output={1}".format(status, output))
        if status != 0: # die or wrong -> not running
            return True
        else:
            return False

    def get_init_root_pwd(self):
        """Get mysql server initial root random password

        :return:
        """
        Logger.info("get sql node initial root random password")
        root_pwd_cmd = "grep \"The random password set\" /root/.mysql_secret"
        (status, output) = commands.getstatusoutput(root_pwd_cmd)
        results = output.split(' ')
        Logger.info(results[-1])
        return results[-1]

