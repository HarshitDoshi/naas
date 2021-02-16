from naas.runner.env_var import n_env
import urllib.parse
import requests
import os

__jup_def_set_workspace = "/etc/naas/set_workspace.json"
__jup_load_workspace = "jupyter lab workspaces import "
__github_starter_repo = "jupyter-naas/starters"
__github_api_url = "https://api.github.com/repos/{REPO}/git/trees/main"
__github_base_url = "https://github.com/{REPO}/blob/main/"


def download_file(url):
    raw_target = url
    if "github.com" in raw_target:
        raw_target = raw_target.replace(
            "https://github.com/", "https://raw.githubusercontent.com/"
        )
        raw_target = raw_target.replace("/blob/", "/")
    r = requests.get(raw_target)

    file_name = raw_target.split("/")[-1]
    file_name = urllib.parse.unquote(file_name)

    with open(file_name, "wb") as f:
        f.write(r.content)
    return file_name


def __wp_set_for_open(url):
    try:
        filename_full = url.split("/")[-1]
        filename_num = filename_full.split(".")[0]
        filename = filename_num.split("__")[1]
        new_wp = os.path.join(n_env.path_naas_folder, f"{filename}_workspace.json")
        if not os.path.exists(new_wp):
            old_filename = download_file(url)
            os.system(f"mv {old_filename} {filename}.ipynb")
            with open(__jup_def_set_workspace, "r") as fh:
                content_wp = fh.read()
                new_content_wp = content_wp.replace("{NB_NAME}", filename)
                with open(new_wp, "w+") as f:
                    f.write(new_content_wp)
            os.system(f"{__jup_load_workspace} {new_wp}")
    except Exception as e:
        print("Cannot config jupyter workspace", e)


def __get_onboarding_list():
    url = __github_api_url.replace("{REPO}", __github_starter_repo)
    url_list = []
    try:
        r = requests.get(url)
        data = r.json()
        for ff in data.get("tree"):
            path = ff.get("path")
            if not path.startswith(".") and path.endswith(".ipynb"):
                base = __github_base_url.replace("{REPO}", __github_starter_repo)
                good_url = f"{base}{path}"
                url_list.append(good_url)
    except Exception as e:
        print("__get_onboarding_list", e)
    return url_list


def init_onborading():
    #  jupyter lab workspaces import file_name.json
    try:
        if os.path.exists(n_env.custom_path):
            print("In Naas Docker machine")
            file_list = __get_onboarding_list()
            for url in file_list:
                try:
                    __wp_set_for_open(url)
                except Exception as e:
                    print("error for", url, e)
    except Exception as e:
        print("Cannot config jupyter", e)