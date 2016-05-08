# Ambari service plugin: ambari-mysql-cluster-plugin

This plugin is aimed at installing, deploying and managing mysql cluster by ambari.

<br>
<br>
##### NOTE 1: The testing operation system is CentOS-6.5 and the environment is clean which means no mysql-related rpms installed before excepts original mysql-libs-5.1.71-1.el6.x86_64 installed in CentOS-6.5 in advance by default.

##### NOTE 2: It lacks comprehensive test coverage. Of course contributions are welcome to make its more stable and useful.

## Version

The version of mysql cluster is 7.4.11 and the version of ambari is 2.1.2.

## Installation instructions

#### Before installing

Put `MYSQLCLUSTER` in the correspnding stack.

Then you need to revise the related stack's role_command_order.json.

Add this:

```
    "SQLNODE-INSTALL": ["NDB-INSTALL"],
    "NDB-INSTALL": ["MGM-INSTALL"],
    "SQLNODE-START": ["NDB-START"],
    "NDB-START": ["MGM-START"],
    "MGM-STOP": ["NDB-STOP"],
    "NDB-STOP": ["SQLNODE-STOP"]
```

#### During installing

You need to supplement the cluster-config using ambari-web.

The configuration of [ndbd] and [mysqld] is indispensable. Other configuration is optional.





