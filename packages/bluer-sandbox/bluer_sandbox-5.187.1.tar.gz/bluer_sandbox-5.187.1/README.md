# 🌀 bluer-sandbox

🌀 A sandbox for ideas and experiments.

## installation

```bash
pip install bluer-sandbox
```

## aliases

[@assets](./bluer_sandbox/docs/aliases/assets.md), 
[@docker](./bluer_sandbox/docs/aliases/docker.md), 
[@notebooks](./bluer_sandbox/docs/aliases/notebooks.md), 
[@offline_llm](./bluer_sandbox/docs/aliases/offline_llm.md).

```mermaid
graph LR

    arvancloud_ssh["@arvan<br>ssh"]


    assets_publish["@assets<br>publish<br>extensions=png+txt,push<br>&lt;object-name&gt;"]


    docker_browse["@docker<br>browse"]

    docker_build["@docker<br>build"]

    docker_clear["@docker<br>clear"]

    docker_eval["@docker<br>eval -<br>&lt;command-line&gt;"]

    docker_push["@docker<br>push"]

    docker_run["@docker<br>run"]

    docker_seed["@docker<br>seed"]


    notebooks_build["@notebooks<br>build<br>&lt;notebook-name&gt;"]

    notebooks_code["@notebooks<br>code<br>&lt;notebook-name&gt;"]
    
    notebooks_connect["@notebooks<br>connect<br>ip=&lt;ip-address&gt;"]

    notebooks_create["@notebooks<br>create<br>&lt;notebook-name&gt;"]

    notebooks_host["@notebooks<br>host"]

    notebooks_open["@notebooks<br>open<br>&lt;notebook-name&gt;"]


    offline_llm_build["@offline_llm<br>build"]

    offline_llm_model_download["@offline_llm<br>model<br>download"]

    offline_llm_prompt["@offline_llm<br>prompt -<br>&lt;prompt&gt;<br>&lt;object-name&gt;"]

    speedtest["@speedtest"]

    object["📂 object"]:::folder
    prompt["🗣️ prompt"]:::folder
    notebook["📘 notebook"]:::folder
    ip_address["🛜 <ip-address>"]:::folder
    docker_image["📂 docker image"]:::folder
    docker_com["🕸️ docker.com"]:::folder
    command_line["🗣️ <command-line>"]:::folder
    clipboard["📋 clipboard"]:::folder
    llm["🧠 llm"]:::folder
    llama_cpp["🛠️ llama_cpp"]:::folder
    arvancloud_machine["🖥️ arvancloud"]:::folder


    ip_address --> arvancloud_ssh
    arvancloud_ssh --> arvancloud_machine


    object --> assets_publish


    docker_seed["@docker<br>seed"]

    docker_browse --> docker_com

    docker_build --> docker_image

    docker_clear

    command_line --> docker_eval
    docker_image --> docker_eval

    docker_image --> docker_push 
    docker_push --> docker_com

    docker_image --> docker_run

    docker_seed --> clipboard


    notebook --> notebooks_build

    notebook --> notebooks_code

    ip_address --> notebooks_connect

    notebooks_host --> ip_address

    notebooks_create --> notebook

    notebook --> notebooks_open


    offline_llm_build --> llama_cpp

    offline_llm_model_download --> llm

    prompt --> offline_llm_prompt
    llama_cpp --> offline_llm_prompt
    llm --> offline_llm_prompt
    offline_llm_prompt --> object
```

|   |   |
| --- | --- |
| [`arvancloud`](./bluer_sandbox/docs/arvancloud.md) [![image](https://github.com/kamangir/assets/blob/main/arvancloud/arvancloud.png?raw=true)](./bluer_sandbox/docs/arvancloud.md) tools to work with [arvancloud](https://arvancloud.ir/). | [`offline LLM`](./bluer_sandbox/docs/offline_llm.md) [![image](https://user-images.githubusercontent.com/1991296/230134379-7181e485-c521-4d23-a0d6-f7b3b61ba524.png)](./bluer_sandbox/docs/offline_llm.md) using [llama.cpp](https://github.com/ggerganov/llama.cpp). |

---

> 🌀 [`blue-sandbox`](https://github.com/kamangir/blue-sandbox) for the [Global South](https://github.com/kamangir/bluer-south).

---


[![pylint](https://github.com/kamangir/bluer-sandbox/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/bluer-sandbox/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/bluer-sandbox/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/bluer-sandbox/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/bluer-sandbox/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/bluer-sandbox/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/bluer-sandbox.svg)](https://pypi.org/project/bluer-sandbox/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/bluer-sandbox)](https://pypistats.org/packages/bluer-sandbox)

built by 🌀 [`bluer README`](https://github.com/kamangir/bluer-objects/tree/main/bluer_objects/README), based on 🌀 [`bluer_sandbox-5.187.1`](https://github.com/kamangir/bluer-sandbox).
