from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from getpass import getpass
from re import search
import sys
from time import gmtime, strftime
from os.path import basename

import deb_handler


@task
def install_mysql():
    """ Installs mysql. """

    # if not installed
    if search('un', run('dpkg-query -l mysql-server| cut -d " " -f1')):
        # mysql password workaround
        # http://www.muhuk.com/2010/05/how-to-install-mysql-with-fabric/
        while True:
            mysql_password = getpass(
                'Please enter MySQL root password: ')
            mysql_password_confirmation = getpass(
                'Please confirm your password: ')
            if mysql_password == mysql_password_confirmation:
                break
            else:
                print "Passwords don't match"

        # get mysql-server version available
        mysql_version = run('aptitude show mysql-server| grep Version | '
            'cut -d "." -f2')
        # insert the given password into the debconf database
        sudo('echo "mysql-server-5.%s mysql-server/root_password password '
            '%s" | debconf-set-selections' % (mysql_version, 
                                                mysql_password))
        sudo('echo "mysql-server-5.%s mysql-server/root_password_again '
                'password %s" | debconf-set-selections' % (mysql_version,
                                                        mysql_password))
        # install the package
        deb_handler.install('mysql-server')


@task
def migrate():
    """ Migrates database to the latest south migration """
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('python manage.py migrate --no-initial-data')


@task
def query(sql, db="", mysql_user='root', mysql_pass=""):
    if type(sql) is list:
        sql = " ".join(sql)
    run('mysql --user=%s --password=%s -e "%s" %s' % (mysql_user, mysql_pass, sql, db))


@task
def create_user(user, password, root_pass):
    sql = []
    sql.append("GRANT USAGE ON *.* TO '%s'@'localhost';" % (user))
    sql.append("DROP USER %s@localhost;" % user)
    sql.append("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';" % (user, password))
    sql.append("FLUSH PRIVILEGES;")
    query(sql=sql, db="mysql", mysql_user="root", mysql_pass=root_pass)


@task
def grant_db(name, owner, root_pass):
    sql = []
    sql.append("GRANT USAGE ON %s.* TO '%s'@'localhost';" % (name, owner))
    sql.append("GRANT ALL ON %s.* TO '$dbuser'@'localhost' WITH GRANT OPTION;" % name)
    sql.append("FLUSH PRIVILEGES;")
    query(sql=sql, db="mysql", mysql_user="root", mysql_pass=root_pass)


@task
def create_db(name, root_pass, owner=None):
    sql = []
    sql.append("CREATE DATABASE %s;" % name)
    query(sql=sql, db="mysql", mysql_user="root", mysql_pass=root_pass)
    if owner is not None:
        grant_db(name, owner, root_pass)


@task
def drop_db(name, root_pass):
    sql = []
    sql.append("DROP DATABASE IF EXISTS %s;" % name)
    query(sql=sql, db="mysql", mysql_user="root", mysql_pass=root_pass)


@task
def drop_user(user, root_pass):
    if user == "":
        raise Exception("Must provide a valid username")

    sql = []
    sql.append("GRANT USAGE ON *.* TO '%s'@'localhost';" % (user))
    sql.append("DROP USER %s@localhost;" % user)
    sql.append("FLUSH PRIVILEGES;")
    query(sql=sql, db="mysql", mysql_user="root", mysql_pass=root_pass)


@task
def dump_db(name, mysql_user, mysql_pass):
    # generating dump file name
    dumps_folder = "db_dumps"
    cmd = "mkdir -p %s" % dumps_folder
    run(cmd)
    branch_name = basename(env.branch)
    dump_name = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    dump_name = "%s/%s-%s.sql" % (dumps_folder, branch_name, dump_name)

    # dump into db_dumps/<dump_name>
    cmd = "mysqldump --add-drop-database -u%s -p%s %s > '%s'"
    cmd %= (mysql_user, mysql_pass, name, dump_name)
    run(cmd)

    # compressing dump
    cmd = "zip '%s.zip' '%s'" % (dump_name, dump_name)
    run(cmd)

    # removing raw dump
    cmd = "rm '%s'" % dump_name
    run(cmd)

    return dump_name


@task
def flush_db(name, mysql_user, mysql_pass):
    query = ("Are you sure you want to flush the database?"
        " Type in the host to confirm")

    selected = run(query)
    if selected != env.host:
        print "%s != %s... aborting database flush" % (selected, env.host)
        sys.exit(1);

    dump_db(name, mysql_user, mysql_pass)
    cmd = ("mysqldump -u%s -p%s --add-drop-table --no-data %s "
            "| grep ^DROP | mysql -u%s -p%s %s")
    cmd %= (mysql_user, mysql_pass, name,
            mysql_user, mysql_pass, name)
    run(cmd)
