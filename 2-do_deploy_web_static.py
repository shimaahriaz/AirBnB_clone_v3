#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['142.44.167.228', '144.217.246.195']
remote_path = "/data/web_static/releases"


def do_deploy(archive_path):
    """
    Distribute archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Extracting file name and folder name without extension
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Creating directory for the release
        run('mkdir -p {}/{}'.format(remote_path, folder_name))

        # Unpacking the archive into the folder
        run('tar -xzf /tmp/{} -C {}/{}'.format(file_name, remote_path, folder_name))

        # Deleting the archive from the /tmp/ directory
        run('rm /tmp/{}'.format(file_name))

        # Moving the contents of web_static to the current release folder
        run('mv {}/{}/web_static/* {}/{}/'.format(remote_path, folder_name, remote_path, folder_name))

        # Removing the web_static folder
        run('rm -rf {}/{}/web_static'.format(remote_path, folder_name))

        # Updating the symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s {}/{}/ /data/web_static/current'.format(remote_path, folder_name))

        return True
    except Exception as e:
        print(e)
        return False


