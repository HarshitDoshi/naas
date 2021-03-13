from notebook.services.contents.filemanager import FileContentsManager as FCM
from naas.onboarding import download_file, wp_set_for_open_filebrowser
from sanic.response import redirect, json
from sanic.views import HTTPMethodView
from naas.runner.env_var import n_env
from naas.types import t_downloader
import traceback
import uuid


class DownloaderController(HTTPMethodView):
    __logger = None

    def __init__(self, logger, *args, **kwargs):
        super(DownloaderController, self).__init__(*args, **kwargs)
        self.__logger = logger

    async def get(self, request):
        uid = str(uuid.uuid4())
        url = str(request.args.get("url", None))
        mode_api = request.args.get("api", None)
        file_name = str(request.args.get("name", None))
        redirect_to = f"{n_env.user_url}/lab"
        if url is None and file_name is None:
            return json({"status": "fail"})
        if url is None:
            try:
                file_name = f"{file_name}.ipynb"
                FCM().new(path=file_name)
            except Exception as e:
                tb = traceback.format_exc()
                self.__logger.error(
                    {"id": uid, "type": t_downloader, "status": "send", "filepath": url}
                )
                return json({"status": e, "tb": str(tb)})
        else:
            try:
                file_name = download_file(url, file_name)
                self.__logger.info(
                    {"id": uid, "type": t_downloader, "status": "send", "filepath": url}
                )
            except Exception as e:
                tb = traceback.format_exc()
                self.__logger.error(
                    {"id": uid, "type": t_downloader, "status": "send", "filepath": url}
                )
                return json({"status": e, "tb": str(tb)})
        wp_set_for_open_filebrowser(file_name)
        if mode_api is None:
            return redirect(redirect_to)
        else:
            return json({"status": "ok"})
