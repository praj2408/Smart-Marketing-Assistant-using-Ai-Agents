import os
from exa_py import Exa
from langchain.agents import tool

class ExaSearchToolSet():
    
    @tool
    def search(query:str):
        """Search for a webpage based on the query.
        
        Args:
            query (str): The search query string.
        
        Returns:
            list: A list of search results.
        """
        return ExaSearchToolSet._exa().search(f"{query}", use_autoprompt=True, num_results=3)
    
    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        
        The URL passed in should be a URL returned from 'search'.
        
        Args:
            url (str): The URL to find similar pages for.
        
        Returns:
            list: A list of similar search results.
        """
        return ExaSearchToolSet._exa().find_similar(url, num_results=3)
    
    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage.
        
        The ids must be passed in as a list, a list of ids returned from 'search'.
        
        Args:
            ids (str): The IDs of the search results to get contents for.
        
        Returns:
            str: The content of the webpages concatenated and truncated to 1000 characters each.
        """
        # print("ids from params:",ids)
        # Evaluate the string representation of the list of IDs
        ids = eval(ids)
        # print("eval ids:",ids)
        
        # Get the contents of the webpages
        contents = str(ExaSearchToolSet._exa().get_contents(ids))
        print("contents:",contents)

        # Split the contents by 'URL:' and truncate each content to 1000 characters
        contents = contents.split("URL:")
        contents= [content[:1000] for content in contents]
        return "\n\n".join(contents)
    
    def tools():
        return [
            ExaSearchToolSet.search,
            ExaSearchToolSet.find_similar,
            ExaSearchToolSet.get_contents
        ]
    
    def _exa():
        """Initialize and return an instance of the Exa class.
        
        Returns:
            Exa: An instance of the Exa class initialized with the API key from environment variables.
        """
        return Exa(api_key=os.environ.get('EXA_API_KEY'))
            