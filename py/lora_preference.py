from typing import TypedDict
import os
import json
from pathlib import Path
import folder_paths

class LoraPreference(TypedDict):
    activation_text: str
    preferred_weight: str
    lora_name: str

def try_find_lora_config(lora_name: str):
  
    try:
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
            p = Path(config_full_path)
            config_json = json.loads(p.read_text(encoding="utf-8"))
            activation_text= ''
            preferred_weight = 1.0
            
            #A111 style config
            if 'activation text' in config_json:
                activation_text = config_json['activation text']
            elif 'activationText' in config_json:
                 activation_text = config_json['activationText']

            #A111 style config
            if 'preferred weight' in config_json:
                if config_json['preferred weight'] != 0:
                    preferred_weight = config_json['preferred weight']
            elif 'preferredWeight' in config_json:
                if config_json['preferredWeight'] != 0:
                    preferred_weight = config_json['preferredWeight']
            pref = LoraPreference(activation_text=activation_text, preferred_weight=preferred_weight, lora_name=lora_name)
            return pref

        else:
            return None
    except:
        return None
