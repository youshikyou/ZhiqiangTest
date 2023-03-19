import pickle, os
from transformers import GPT2TokenizerFast
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ChatHistory:

    @staticmethod
    def to_file(file_path, data):
        # Make sure the directory for the file exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                print(f"Error creating directory: {e}")
                return

        # Serialize the chat history object to bytes
        try:
            with open(file_path, 'wb') as f:
                f.write(pickle.dumps(data))
        except IOError as e:
            print(f"Error writing to file: {e}")

    @staticmethod
    def from_file(file_path):

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
            # Deserialize the chat history object from bytes
                chat_history = pickle.loads(f.read())
        else:
            chat_history = []
        
        return chat_history
    """
    @staticmethod
    def limit_chat_history(data, token_limit=800):
        # Initialize the GPT2 tokenizer
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        #tokenizer = GPT2TokenizerFast.from_pretrained("/gpt2_tokenizer")
        # Calculate the total token count of the list
        token_count = sum(len(tokenizer.encode(x['content'])) for x in data)
        print("==============")
        print("token是多少")
        print(token_count)
        # Calculate the number of pairs to remove
        pairs_to_remove = 0
        while token_count > token_limit and pairs_to_remove < len(data) // 2:
            pair_token_count = len(tokenizer.encode(data[pairs_to_remove * 2]['content'])) \
                               + len(tokenizer.encode(data[pairs_to_remove * 2 + 1]['content']))
            token_count -= pair_token_count
            pairs_to_remove += 1

        # Slice the list to get the limited data
        limited_data = data[pairs_to_remove * 2:]
        print("留下数据是")
        print(limited_data)
        print("==============")
        return limited_data
    """
    @staticmethod
    async def limit_chat_history(data, token_limit=800):
        # Initialize the GPT2 tokenizer
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Construct the absolute path of the tokenizer folder
        tokenizer_path = os.path.join(current_dir, "gpt2_tokenizer")
        tokenizer = GPT2TokenizerFast.from_pretrained(tokenizer_path)
        loop = asyncio.get_event_loop()

        # Run the tokenization and processing in a separate thread to avoid blocking
        limited_data = await loop.run_in_executor(None, ChatHistory._limit_chat_history_sync, data, token_limit,tokenizer)

        return limited_data

    @staticmethod
    def _limit_chat_history_sync(data, token_limit, tokenizer):
        # Calculate the total token count of the list
        token_count = sum(len(tokenizer.encode(x['content'])) for x in data)

        print("==============")
        print("token是多少")
        print(token_count)
        # Calculate the number of pairs to remove
        pairs_to_remove = 0
        while token_count > token_limit and pairs_to_remove < len(data) // 2:
            pair_token_count = len(tokenizer.encode(data[pairs_to_remove * 2]['content'])) \
                               + len(tokenizer.encode(data[pairs_to_remove * 2 + 1]['content']))
            token_count -= pair_token_count
            pairs_to_remove += 1

        # Slice the list to get the limited data
        limited_data = data[pairs_to_remove * 2:]
        print("留下数据是")
        print(limited_data)
        print("==============")

        return limited_data


