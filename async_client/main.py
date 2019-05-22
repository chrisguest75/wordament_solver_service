#!/usr/bin/env python3
import os
import logging
import asyncio
import aiohttp
import aiofiles
import json

MAX_WORD_LOAD = 1000

# read a file and despatch a 100 lines at a time to wordament.  
async def create_dictionary(session, base_url: str, name:str): 
    url = f"{base_url}/dictionary/{name}"
    logging.debug(f"create_dictionary {url}")
    async with session.post(url, data="[]", headers={'content-type': 'application/json'}) as response:
        response_json = await response.json()
        return response.status, response_json


async def add_to_dictionary(session, base_url: str, name:str, words):
    url = f"{base_url}/dictionary/{name}"
    logging.debug(f"add_to_dictionary {url}")
    async with session.put(url, data=json.dumps(words), headers={'content-type': 'application/json'}) as response:
        response_json = await response.json()
        return response.status, response_json


async def build_dictionary(session, base_url: str, name:str):
    async with aiofiles.open("../test_data/words_alpha.txt") as f:
        lines = []
        async for line in f:
            lines.append(line.strip())
            if (len(lines) == MAX_WORD_LOAD):
                response = await add_to_dictionary(session, base_url, name, lines)    
                logging.debug("building dictionary response {}".format(response))
                lines = []

        if len(lines) > 0: 
            response = await add_to_dictionary(session, base_url, name, lines)    
            logging.debug("building dictionary response {}".format(response))


async def solve(session, base_url: str, grid: str, name:str):
    url = (f"{base_url}/puzzle/solve/{grid}?dictionary_id={name}")
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json


async def dictionary_stat(session, base_url: str, name:str):
    url = f"{base_url}/dictionary/{name}"
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json

async def dictionary_names(session, base_url: str):
    url = f"{base_url}/dictionary"
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json

async def main(base_url: str):
    # We use only one session
    async with aiohttp.ClientSession() as session:
        while True:
            response = await dictionary_names(session, base_url)
            logging.info(response)             

            name = input("Dictionary name (quit):")
            if name.lower() == "quit":
                break
            response = await dictionary_stat(session, base_url, name)
            logging.info(response) 
            if response[0] != 200 or response[1]["num_of_words"] < 370103:
                response = await create_dictionary(session, base_url, name)
                logging.info(response)
                response = await build_dictionary(session, base_url, name)
                logging.info(response)

            # grid = 'GLNTSRAWRPHSEOPS'
            grid = input("Enter grid or (quit) - examples 'GLNTSRAWRPHSEOPS':")
            if grid.lower() == "quit":
                break
            else:
                response = await solve(session, base_url, grid, name)
                logging.info(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Hello")

    base_url = "http://localhost:8000/api"
    if 'SERVER_URL' in os.environ:
        base_url = os.environ['SERVER_URL']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(base_url))
