# svllm

Create a OpenAI-Compatible API Server for your LLM.

## Usage

## Install

```
$ pip install svllm
```

## Prepare

svllm provided following HTTP APIs:

* chat: `/v1/chat/completions`
* complete: `/v1/completions`
* embed: `/v1/embeddings`
* models: `/v1/models`

You only need to implement the `chat`, `complete`, `embed` function (or part of them).

Set `__model__`, `__owner__` for these functions can affect `/v1/models` API.

See `src/protocol.py` for more information.

Then you can use svllm in the following two ways:

### CLI

If you have a `demo.py` file that implements a `chat` function, you can start it like this:

~~~bash
$ svllm --chat demo:chat
$ svllm-cli # client
~~~

Run `svllm --help` and `svllm-cli --help` for more information.

### Library

You can also use svllm as a library. (also see `demo.py`)

~~~python
import uvicorn
import svllm

if __name__ == '__main__':
    svllm.set_chat(svllm.examples.chat)
    svllm.set_complete(svllm.examples.complete)
    svllm.set_embed(svllm.examples.embed)

    app = svllm.create_app()
    uvicorn.run(app, host='0.0.0.0', port=5261)
~~~
