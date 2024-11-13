from typing import List, TypedDict
from server import PromptServer
from aiohttp import web
import os
import json
from pathlib import Path
import folder_paths

dir = os.path.abspath(os.path.join(__file__, "../../user"))
if not os.path.exists(dir):
    os.mkdir(dir)
file = os.path.join(dir, "autocomplete.txt")

#TODO, clean this up and move it to a different file...

class LoraPreference(TypedDict):
    activation_text: str
    preferred_weight: str
    lora_name: str

def try_find_lora_config(lora_name: str):
  
    file_path = None

    possible_paths = folder_paths.get_folder_paths('loras')
    for p in possible_paths:
        check_path = os.path.join(p, lora_name)
        if os.path.isfile(check_path):
            file_path = check_path
            break

    if not file_path:
        return None
    
    file_path_no_ext = os.path.splitext(file_path)[0]
    config_full_path = file_path_no_ext + '.json'

    if os.path.isfile(config_full_path):
        #
        p = Path(config_full_path)
        config_json = json.loads(p.read_text(encoding="utf-8"))
        activation_text= ''
        preferred_weight = 1.0
        if 'activation text' in config_json:
            activation_text = config_json['activation text']
        if 'preferred weight' in config_json:
            if config_json['preferred weight'] != 0:
                preferred_weight = config_json['preferred weight']
        pref = LoraPreference(activation_text=activation_text, preferred_weight=preferred_weight, lora_name=lora_name)
        return pref

    else:
        return None

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
