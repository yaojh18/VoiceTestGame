"""django的mysql做的不行，这里用别人的mysql库"""

import pymysql
pymysql.version_info = (1, 4, 0, "final", 0)
pymysql.install_as_MySQLdb()
