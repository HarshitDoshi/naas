from .types import t_asset
from .manager import Manager
import os


class Assets:
    naas = None
    role = t_asset

    def __init__(self):
        self.manager = Manager()
        self.list = self.manager.list_prod
        self.clear = self.manager.clear_prod
        self.get = self.manager.get_prod
        self.get_output = self.manager.get_output
        self.clear_output = self.manager.clear_output

    def current_raw(self):
        json_data = self.manager.get_naas()
        for item in json_data:
            if item["type"] == self.role:
                print(item)

    def currents(self, raw=False):
        json_data = self.manager.get_naas()
        if raw:
            for item in json_data:
                if item["type"] == self.role:
                    print(item)
        else:
            for item in json_data:
                kind = None
                if item["type"] == self.role:
                    kind = f"gettable with this url {self.manager.proxy_url('assets', item['value'])}"
                    print(f"File ==> {item['path']} is {kind}")

    def add(self, path=None, params={}, debug=False, force=False):
        current_file = self.manager.get_path(path)
        if current_file is None:
            print("Missing file path in prod mode")
            return
        prod_path = self.manager.get_prod_path(current_file)
        token = self.manager.get_value(prod_path, self.role)
        if token is None or force is True:
            token = os.urandom(30).hex()
        url = self.manager.proxy_url(self.role, token)
        if not self.manager.notebook_path() and force is False:
            print("No add done you are in already in naas folder\n")
            return url
        # "path", "type", "params", "value", "status"
        self.manager.add_prod(
            {"type": self.role, "path": current_file, "params": params, "value": token},
            debug,
        )
        print("👌 Well done! Your Assets has been sent to production folder.\n")
        print(f"🔗 You can access this assets remotely with: {url} \n")
        self.manager.copy_url(url)
        print('PS: to remove the "Assets" feature, just replace .add by .delete')
        return url

    def delete(self, path=None, all=False, debug=False):
        if not self.manager.notebook_path():
            print("No delete done you are in already in naas folder\n")
            return
        current_file = self.manager.get_path(path)
        self.manager.del_prod({"type": self.role, "path": current_file}, debug)
        print("🗑 Done! Your Assets has been remove from production folder.\n")
        if all is True:
            self.clear(path)

    def help(self):
        print(f"=== {type(self).__name__} === \n")
        print(
            f".add(path, params) => add path to the prod {type(self).__name__} server\n"
        )
        print(
            f".delete(path) => delete path to the prod {type(self).__name__} server\n"
        )
        print(
            ".clear(path, histonumber) => clear history, history number and path are optionel, \
                if you don't provide them it will erase full history of current file \n"
        )
        print(
            ".list(path) => list history, of a path or if not provided the current file \n"
        )
        print(
            ".get(path, histonumber) => get prod file, of a path or if not provided the current file \n"
        )
        print(f".currents() => get current list of {type(self).__name__} prod file\n")
        print(
            f".current(raw=True) => get json current list of {type(self).__name__} prod file\n"
        )
