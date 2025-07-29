from fastloop import FastLoop, LoopContext, LoopEvent


class MockClient:
    def transcribe(self, message: str):
        return message + " - from the server"


app = FastLoop(name="basic-chat-demo")


class AppContext(LoopContext):
    client: MockClient | None = None


async def load_client(context: LoopContext):
    print("Loading client...")
    context.client = MockClient()


@app.event("user_message")
class UserMessage(LoopEvent):
    msg: str


@app.event("agent_message")
class AgentMessage(LoopEvent):
    msg: str


@app.loop(
    name="chat",
    start_event=UserMessage,
    on_loop_start=load_client,
)
async def basic_chat(context: AppContext):
    user_message = await context.wait_for(
        UserMessage, timeout=1.0, raise_on_timeout=False
    )
    if not user_message:
        print("No user message")
        return

    await context.emit(AgentMessage(msg="Ack: " + user_message.msg))


if __name__ == "__main__":
    app.run(port=8111)
