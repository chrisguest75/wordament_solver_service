
import logging
import asyncio
import aiohttp
import aiofiles
import json

logger = logging.getLogger("solver_client")

class solver_client():
    def __init__(self, session, base_url: str, max_words_per_insert = 1000):
        self.session = session
        self.base_url = base_url
        self.max_words_per_insert = max_words_per_insert


    async def create_dictionary(self, name:str): 
        """ Create an empty dictionary on the server 
        """
        url = f"{self.base_url}/dictionary/{name}"
        logger.debug(f"create_dictionary {url}")
        async with self.session.post(url, data="[]", headers={'content-type': 'application/json'}) as response:
            response_json = await response.json()
            return response.status, response_json


    async def add_to_dictionary(self, name:str, words):
        """ Add an array of words to the dictionary
        """
        url = f"{self.base_url}/dictionary/{name}"
        logger.debug(f"add_to_dictionary {url}")
        async with self.session.put(url, data=json.dumps(words), headers={'content-type': 'application/json'}) as response:
            response_json = await response.json()
            return response.status, response_json


    async def build_dictionary(self, filename: str, name:str):
        """ Build the dictionary using asynchronous tasks. 
        NOTE: It only despatches one request at a time.   
        """
        async with aiofiles.open(filename) as f:
            lines = []
            count = 0 
            async for line in f:
                lines.append(line.strip())
                if (len(lines) == self.max_words_per_insert):
                    task = asyncio.create_task(self.add_to_dictionary(name, lines))
                    logger.debug(f"insert {len(lines)} into {name} line number {count} - wait on task - {id(task)}")
                    response = await task     
                    logger.debug("building dictionary response {}".format(response))
                    count += len(lines)
                    lines = []

            # do remaining words
            if len(lines) > 0: 
                task = asyncio.create_task(self.add_to_dictionary(name, lines))    
                logger.debug(f"insert {len(lines)} into {name} line number {count} - wait on task - {id(task)}")
                response = await task   
                logger.debug(f"dictionary response {response}")
                count += len(lines)


    async def solve(self, grid: str, name:str):
        """ Solve the grid with the named dictionary 
        """
        url = (f"{self.base_url}/puzzle/solve/{grid}?dictionary_id={name}")
        async with self.session.get(url) as response:
            response_json = await response.json()
            return response.status, response_json


    async def get_health(self):
        """ Get health endpoint 
        """
        url = f"{self.base_url}/health"
        async with self.session.get(url) as response:
            response_json = await response.json()
            return response.status, response_json


    async def dictionary_stat(self, name:str):
        """ Get statistics for the dictionary 
        """
        url = f"{self.base_url}/dictionary/{name}"
        async with self.session.get(url) as response:
            response_json = await response.json()
            return response.status, response_json

    async def dictionary_names(self):
        """ Get the names of the dictionaries stored on the server    
        """
        url = f"{self.base_url}/dictionary"
        async with self.session.get(url) as response:
            response_json = await response.json()
            return response.status, response_json
