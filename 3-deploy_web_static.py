from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['142.44.167.228', '144.217.246.195']
env.user = 'your_username'  # Update with your actual username

def do_pack():
    """Generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(f"Error occurred while creating archive: {e}")
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        print(f"Archive {archive_path} not found.")
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Error occurred during deployment: {e}")
        return False

def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False

