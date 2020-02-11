import requests
import shutil
import zipfile
import os


def checkpathexists(path: str) -> bool:
    return os.path.exists(path)


def deletedir(path: str):
    print("deleting directory: {}".format(path))
    return shutil.rmtree(path)


def deletefile(path: str):
    print("deleting file: {}".format(path))
    return os.remove(path)


def download_wordpress():
    print("Wordpress download initiating...")
    if checkpathexists("wordpress.zip"):
        delete = input("should I delete your wordpress zip file?: y/n     ")
        if delete == "y":
            deletefile("wordpress.zip")
        else:
            print("the script failed, because you won't let me delete stuff. hmpf.")
            exit()
    url = "https://wordpress.org/latest.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open("wordpress.zip", "wb") as f:
            shutil.copyfileobj(r.raw, f)
    print("Wordpress download completed...")
    return


def unzip_wordpress():
    print("Wordpress unziping initiating...")
    if checkpathexists("wordpress"):
        delete = input("should I delete your wordpress folder?: y/n     ")
        if delete == "y":
            deletedir("wordpress")
        else:
            print("the script failed, because you won't let me delete stuff. hmpf.")
            exit()
    with zipfile.ZipFile("wordpress.zip", "r") as zip_ref:
        zip_ref.extractall(".")
    print("Unziping wordpress file completed....")
    return


def duplicate_file(source, destination):
    shutil.copyfile(source, destination)
    print("Copying file {} to {} was successful...".format(soure, destination))
    return


def replace_line_in_source(findstr, replacement, filepath):
    with open(filepath, "rt") as f:
        data = f.read()
        data = data.replace(findstr, replacement)
        f.close()
        with open(filepath, "wt") as fw:
            fw.write(data)
            fw.close()
    print("The line {} was replaced with {} in file {}".format(
        findstr, replacement, filepath))
    return


def fill_wp_config():
    config = {
        "define( 'DB_NAME', 'database_name_here' )": {"field": "DB_NAME", "replacement": "database_name_here"},
        "define( 'DB_USER', 'username_here' )":  {"field": "DB_USER", "replacement": "username_here"},
        "define( 'DB_PASSWORD', 'password_here' )":  {"field": "DB_PASSWORD", "replacement": "password_here"},
        "define( 'DB_HOST', 'localhost' )":  {"field": "DB_HOST", "replacement": "localhost"},
        "define( 'DB_CHARSET', 'utf8' )":  {"field": "DB_CHARSET", "replacement": "utf8"},
        "define( 'DB_COLLATE', '' )":  {"field": "DB_COLLATE", "replacement": ""}
    }

    for key in config:
        definition = config[key]
        field = definition["field"]
        replacement = definition["replacement"]
        user_replacement = input(
            "Please type in the replacement for [" + field + "]  or press ENTER to type nothing:     ")
        if user_replacement and len(user_replacement) > 0:
            definition["replacement"] = user_replacement
        r = definition["replacement"]
        valid_replacement = "define( '{}', '{}' )".format(field, r)
        replace_line_in_source(key, valid_replacement,
                               "wordpress/wp-config.php")
    print("All fields replaced")
    return


def start():
    download_wordpress()
    unzip_wordpress()
    duplicate_file("wordpress/wp-config-sample.php", "wordpress/wp-config.php")
    fill_wp_config()


start()
