# ambari-mysql-cluster-plugin

This plugin is used to install, deploy and manage mysql cluster by ambari.

The version of mysql cluster is 7.4.11 and the version of ambari is 2.1.2.

# Installation instructions

You need to supplement the cluster-config before install it using ambari-web.

The configuration of [ndbd] and [mysqld] is indispensable. Other configuration is optional.

NOTE 1: The testing operation system is CentOS-6.5 and the environment is clean which means no mysql-related rpms installed before.

NOTE 2: It lacks comprehensive test coverage. Of course contributions are welcome to make its more stable and useful.

