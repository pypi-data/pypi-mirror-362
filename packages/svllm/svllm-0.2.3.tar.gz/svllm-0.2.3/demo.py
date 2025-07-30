import uvicorn
import src.svllm as svllm

if __name__ == '__main__':
    svllm.set_chat(svllm.examples.chat)
    svllm.set_complete(svllm.examples.complete)
    svllm.set_embed(svllm.examples.embed)

    app = svllm.create_app()
    uvicorn.run(app, host='0.0.0.0', port=5261)
