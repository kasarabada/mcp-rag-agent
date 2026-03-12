class MCPContext:

    def __init__(self):

        self.history = []

        self.system_prompt = """
You are an AI assistant.

Use retrieved documents when answering questions.
If the answer is not in the documents, say you don't know.
"""

    def add_turn(self, user, assistant):

        self.history.append({
            "user": user,
            "assistant": assistant
        })

    def get_context(self):

        text = self.system_prompt + "\n"

        for turn in self.history:

            text += f"\nUser: {turn['user']}\nAssistant: {turn['assistant']}\n"

        return text