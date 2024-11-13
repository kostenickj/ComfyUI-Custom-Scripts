from typing import List
from server import PromptServer
from aiohttp import web
import os
import folder_paths
from .lora_preference import try_find_lora_config, LoraPreference

dir = os.path.abspath(os.path.join(__file__, "../../user"))
if not os.path.exists(dir):
    os.mkdir(dir)
file = os.path.join(dir, "autocomplete.txt")

@PromptServer.instance.routes.get("/pysssss/autocomplete")
async def get_autocomplete(request):
    if os.path.isfile(file):
        return web.FileResponse(file)
    return web.Response(status=404)


@PromptServer.instance.routes.post("/pysssss/autocomplete")
async def update_autocomplete(request):
    with open(file, "w", encoding="utf-8") as f:
        f.write(await request.text())
    return web.Response(status=200)


@PromptServer.instance.routes.get("/pysssss/loras")
async def get_loras(request):
    loras = folder_paths.get_filename_list("loras")
    ret: List[LoraPreference] = []
    for lora in loras:
        name = os.path.splitext(lora)[0]
        maybe_config = try_find_lora_config(lora)
        if maybe_config:
            ret.append(maybe_config)
        else:
            ret.append(LoraPreference(activation_text='', lora_name=name, preferred_weight=1.0))
    return web.json_response(ret)
