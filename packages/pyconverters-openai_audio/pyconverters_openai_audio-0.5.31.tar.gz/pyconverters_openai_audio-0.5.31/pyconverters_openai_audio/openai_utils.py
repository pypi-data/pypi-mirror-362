import os
from logging import Logger

import requests
from openai import OpenAI
from openai.lib.azure import AzureOpenAI
from strenum import StrEnum

logger = Logger("pymultirole")


def audio_list_models(prefix, **kwargs):
    def sort_by_created(x):
        if 'created' in x:
            return x['created']
        elif 'created_at' in x:
            return x['created_at']
        elif 'deprecated' in x:
            return x['deprecated'] or 9999999999
        else:
            return x.id

    models = []
    client = set_openai(prefix)
    if prefix.startswith("DEEPINFRA"):
        deepinfra_url = client.base_url
        deepinfra_models = {}
        public_models_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/models/list"
        response = requests.get(public_models_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp, key=sort_by_created, reverse=True)
            mods = list(
                {m['model_name'] for m in mods if m['type'] == 'automatic-speech-recognition'})
            deepinfra_models.update({m: m for m in mods})

        private_models_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/models/private/list"
        response = requests.get(private_models_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp, key=sort_by_created, reverse=True)
            mods = list(
                {m['model_name'] for m in mods if m['type'] == 'automatic-speech-recognition'})
            deepinfra_models.update({m: m for m in mods})

        deployed_models_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/deploy/list/"
        response = requests.get(deployed_models_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp, key=sort_by_created, reverse=True)
            mods = list(
                {m['model_name'] for m in mods if m['task'] == 'text-generation' and m['status'] == 'running'})
            deepinfra_models.update({m: m for m in mods})
        models = list(deepinfra_models.keys())
    return models


def set_openai(prefix):
    if prefix.startswith("AZURE"):
        client = AzureOpenAI(
            # This is the default and can be omitted
            api_key=os.getenv(prefix + "OPENAI_API_KEY"),
            azure_endpoint=os.getenv(prefix + "OPENAI_API_BASE", None),
            api_version=os.getenv(prefix + "OPENAI_API_VERSION", None),
            azure_deployment=os.getenv(prefix + "OPENAI_DEPLOYMENT_ID", None)
        )
    else:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.getenv(prefix + "OPENAI_API_KEY"),
            base_url=os.getenv(prefix + "OPENAI_API_BASE", None)
        )
    return client


NO_DEPLOYED_MODELS = 'no deployed models - check API key'


def create_asr_model_enum(name, prefix="", key=lambda m: m):
    audio_models = []
    default_audio_model = None
    try:
        audio_models = [m for m in audio_list_models(prefix) if key(m)]
        if audio_models:
            default_audio_model = audio_models[0]
    except BaseException:
        logger.warning("Can't list models from endpoint", exc_info=True)

    if len(audio_models) == 0:
        audio_models = [NO_DEPLOYED_MODELS]
    models = [("".join([c if c.isalnum() else "_" for c in m]), m) for m in audio_models]
    model_enum = StrEnum(name, dict(models))
    default_audio_model = model_enum(default_audio_model) if default_audio_model is not None else None
    return model_enum, default_audio_model
