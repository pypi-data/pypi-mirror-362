import os
from openai import OpenAI
import asyncio
import tiktoken
import pickle

from .agent_tools import split_stream_into_speech_chunks
from .local_semantic_db import local_semantic_db
from .local_sql_db import local_sql_db
from .basic_web_scraping import basic_web_scrape, contains_url, extract_urls


os.environ["TOKENIZERS_PARALLELISM"] = "false"


class ChatAgent:
    def __init__(self, name="Agent", api_key=None, model="gpt-3.5-turbo", messages=None, token_limit=4096, summary_size=500):
        self.name=name
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.messages = messages if messages is not None else []
        self.token_limit = token_limit
        self.enc = tiktoken.encoding_for_model(self.model)
        self.primary_directive = None
        self.summary_size = summary_size
        self.semantic_db = None
        self.sql_db = None
        self._initialize_databases()

    def _initialize_databases(self):
        """
        Initializes the semantic and SQL databases.
        This method is called upon instantiation and after unpickling.
        """
        self.semantic_db = local_semantic_db(
            persist_directory=f"{self.name}_data/{self.name}_semantic_db", 
            collection_name=f"{self.name}_general"
        )
        self.sql_db = local_sql_db(f"{self.name}_data/{self.name}_sql_db")


    def set_primary_directive(self, system_prompt=None):
        if system_prompt is None and self.primary_directive is not None:
            system_prompt = self.primary_directive
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
            self.primary_directive = system_prompt

    def count_tokens(self):
        num_tokens = 0
        for message in self.messages:
            num_tokens += len(self.enc.encode(message["content"]))
        return num_tokens

    def is_within_token_limit(self, token_limit=None):
        if token_limit is None:
            token_limit = self.token_limit
        current_token_count = self.count_tokens()
        return current_token_count <= token_limit

    def tokens_left(self):
        t = self.count_tokens()
        return int(self.token_limit) - int(t)

    def extract_messages_content(self):
        return ' '.join(entry['content'] for entry in self.messages if 'content' in entry)

    def len_of_messages(self):
        return len(self.extract_messages_content().split(" "))

    def add_context(self, system_prompt=None):
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def refresh(self):
        summary = self.summarize_current_conversation()
        self.messages = []
        self.set_primary_directive()
        self.add_context("In a previous conversation, the following was discussed ... " + str(summary))

    def chat(self, user_message, stream=False, speech_ready=False, logs=False):
        tokens_used_user = len(self.enc.encode(user_message))
        current_token_count = self.count_tokens()
        if logs:
            print("CURRENT TOKENS USED:", current_token_count)
            print("MAX TOKENS:", self.token_limit)

        if current_token_count + tokens_used_user > self.token_limit:
            self.refresh()
            if logs:
                print("ABOUT TO GO OVER TOKEN LIMIT")
                print("CONVERSATION WAS REFRESHED")

        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})

        if stream:
            def stream_generator():
                assistant_reply = ""
                response_stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=True
                )
                for chunk in response_stream:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        piece = chunk.choices[0].delta.content
                        assistant_reply += piece
                        yield piece
                # Finalize assistant response in conversation history
                self.messages.append({"role": "assistant", "content": assistant_reply})

            if speech_ready:
                return split_stream_into_speech_chunks(stream_generator())
            else:
                return stream_generator()


        else:
            # Standard full response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            ai_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": ai_message})
            return ai_message

    def print_stream(self, stream_generator):
        for chunk in stream_generator:
            print(chunk, end="", flush=True)



    async def chat_async(self, user_message, stream=False):
        # Use asyncio.to_thread to run the synchronous side_message method asynchronously
        response = await asyncio.to_thread(lambda: self.chat(user_message,stream=stream))
        return response  # side_message already returns the content

    def get_conversation_history(self):
        # Returns the entire conversation history
        return self.messages


    def side_message(self, prompt, use_context = False):
        # get side message that will not affect overall conversation or be added to conversation history
        temp_messages = []
        if use_context:
            temp_messages = self.messages.copy()
        temp_messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(model=self.model,
                                                       messages=temp_messages)
        return response.choices[0].message.content


    async def side_message_async(self, prompt, use_context=False):
        # Use asyncio.to_thread to run the synchronous side_message method asynchronously
        response = await asyncio.to_thread(lambda: self.side_message(prompt, use_context))
        return response  # side_message already returns the content


    def summarize_current_conversation(self,in_max_n_words=None):
        if in_max_n_words is None:
            in_max_n_words = self.summary_size
        q = """
        Summarize the entire conversation we have had in in_max_n_words
        words or less.
        """
        q = q.replace("in_max_n_words",str(in_max_n_words))
        return self.side_message(q, use_context=True)


    def __repr__(self):
        repr_str = (
            f"ChatAgent(api_key='{self.api_key}', "
            f"model='{self.model}', "
            f"token_limit={self.token_limit}, "
            f"messages={repr(self.messages)}, "
            f"summary_size={repr(self.summary_size)})"
        )
        return repr_str

    def repr_no_key(self):
        repr_str = (
            f"ChatAgent(api_key=None, "
            f"model='{self.model}', "
            f"token_limit={self.token_limit}, "
            f"messages={repr(self.messages)}, "
            f"summary_size={repr(self.summary_size)})"
        )
        return repr_str

    def save_as_txt(self, filename):
        if ".txt" not in filename:
            filename = filename+".txt"
        with open(filename, 'w') as myfile: 
            content = repr(self)
            myfile.write(content)

    def load_from_txt(self, filename):
        repr_str=None
        with open(filename, 'r') as myfile: 
            repr_str = myfile.read()
        new_instance = eval(repr_str)
        attributes = [
            attr
            for attr in dir(new_instance)
            if not callable(getattr(new_instance, attr)) and not attr.startswith("__")
        ]
        for attr in attributes:
            setattr(self, attr, getattr(new_instance, attr))

    def save_as_pickle(self, filename):
        temp_client = self.client  # Temporarily store the OpenAI client
        self.client = None  # Remove the client before pickling
        if ".pickle" not in filename:
            filename = filename + ".pickle"
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        self.client = temp_client  # Restore the client after pickling

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as file:
            loaded_instance = pickle.load(file)
        # Update current instance's attributes (excluding special methods)
        attributes = [
            attr
            for attr in dir(loaded_instance)
            if not callable(getattr(loaded_instance, attr)) and not attr.startswith("__")
        ]
        for attr in attributes:
            setattr(self, attr, getattr(loaded_instance, attr))
        # Reinitialize the OpenAI client
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)


    def semantically_contextualize(self, message, semantic_top_k=1, semantic_where=None, semantic_contextualize_prompt=None):

        context = self.semantic_db.query(message, top_k=semantic_top_k, where=semantic_where)
        context_text = []
        for d in context:
            context_text.append(d["text"])
        context = " ... ".join(context_text)

        # Include semantic context if applicable
        if context is not None:
            print("semantically_contextualize: context added")
            if semantic_contextualize_prompt is None:
                self.add_context("This information may be relevant to the conversation ... " + str(context))
            else:
                self.add_context(str(semantic_contextualize_prompt) + " ... " + str(context))
        else:
            print("semantically_contextualize: No context added")


    def upload_document(self, doc_path, doc_name=None, max_sentences_per_chunk=5, metadata=None):
        if doc_name is None:
            doc_name = os.path.basename(doc_path)   
        with open(doc_path, "r") as file:
            doc = file.read()
        if metadata is None:
            metadata = {"doc_name":doc_name}
        self.semantic_db.insert_in_chunks(doc, metadata=metadata, max_sentences_per_chunk=max_sentences_per_chunk)


    def discuss_document(self, semantic_query, doc_name=None, semantic_where=None, semantic_top_k=5, semantic_contextualize_prompt=None):
        if semantic_where is None and doc_name is None:
            raise ValueError("Must include either doc_name or semantic_where")
        if semantic_where is None and doc_name is not None:
            semantic_where = {"doc_name":doc_name}
        self.semantically_contextualize(semantic_query, semantic_top_k=semantic_top_k,
         semantic_where=semantic_where,
          semantic_contextualize_prompt=semantic_contextualize_prompt)








if __name__ == "__main__":




    # 1. initialize agent
    OPENAI_API_KEY = "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"
    agent = ChatAgent(name="Tomatio", api_key=OPENAI_API_KEY)

    # 2. (optional) purge semantic database for fresh start
    agent.semantic_db.purge_collection();

    # 3. upload txt document of your choosing in chunks of 5 sentences to the semantic database
    doc_name = "docs/AliceInWonderland.txt"
    agent.upload_document(doc_name, max_sentences_per_chunk=5)

    # 4. do a semantic search for 5 relevent passages to a semantic_query and add it to the context window of the agent
    semantic_query = "Interactions between Alice and the Mad Hatter"
    semantic_contextualize_prompt = f"These are some passages from {doc_name} that should be considered"
    agent.discuss_document(semantic_query, doc_name="AliceInWonderland.txt", semantic_top_k=5, semantic_contextualize_prompt=semantic_contextualize_prompt)

    # 5. start the chat with a question about the uploaded content.
    message = "Tell me about the relationship between Alice and the Mad Hatter. Use examples from the provided passages"
    response_stream = agent.chat(message)
    print("\n")
    print(f"You: {message}")
    print(agent.name, end=": ")
    agent.print_stream(response_stream)

    print("\n")
    print("Continue to basic chat...")
    print("\n")

    while message not in ["bye","goodbye","exit","quit"]:
        message = input("You: ")
        response_stream = agent.chat(message)
        print(agent.name, end=": ")
        agent.print_stream(response_stream)
        print("\n")




























