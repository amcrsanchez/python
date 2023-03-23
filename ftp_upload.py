import sys
import getopt
import os.path, os
from ftplib import FTP, error_perm

def init(argv):
    arg_path = ""
    arg_host = ""
    arg_port = ""
    arg_user = ""
    arg_password = ""
    arg_help = ("{0} "
                "--path <directory or file> "
                "--host <ftp_host> "
                "-p <port> " 
                "-u <user> "
                "--pwd <password>").format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], 
        "hp:u:",
        ["help","port=","host=","path=","user=","pwd="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            sys.exit(2)
        elif opt in ["--path"]:
            arg_path = arg
        elif opt in ["--host"]:
            arg_host = arg
        elif opt in ["-p", "--port"]:
            arg_port = arg
        elif opt in ["-u", "--user"]:
            arg_user = arg
        elif opt in ["--pwd"]:
            arg_password = arg

    ftp = ftpConnection(arg_host, int(arg_port), arg_user, arg_password)

    placeFiles(ftp, arg_path)

def placeFiles(ftp, path):
    basename = os.path.basename(path)
    if(os.path.isdir(path)):
        try:
            ftp.mkd(basename)
        except error_perm as e:
            if not e.args[0].startswith("550"):
                raise

        ftp.cwd(basename)
        for name in os.listdir(path):
            placeFiles(ftp, os.path.join(path, name))
        
        ftp.cwd("..")
    else:
        ftp.storbinary('STOR ' + basename, open(path, 'rb'))


def ftpConnection(host, port, user, password):
    try:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(user, password)
    except:
        print("An error ocurred trying to connect ftp")
    return ftp

if __name__ == "__main__":
    init(sys.argv)
