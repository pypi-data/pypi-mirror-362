from scraper import categories, search, fetch
from mcp import cli

def hardverapro_search(query: str,offset: int = 0, category: str = "All")-> list:
    """
    Search HardverApró listings with the given query and extract relevant results.
    They usually include listins of people seaching for the given product. 
    The list returns the first 100 results (if any). This can be offset by the offset parameter
    Args:
        query (str): The search term to use in the HardverApró listings
        offset (int, optional): The pagination offset. Defaults to 0.

    Returns:
        list[dict]: A list of dictionaries, each containing:
            - 'title' (str): The title of the listing
            - 'price' (str): The price listed
            - 'link' (str): A full URL to the listing
    """
    return search(query,offset=offset,category=category)

def hardverapro_fetch(url: str) -> dict:
    """
    Fetch a listing from HardverApró
    Args:
        url (str): A full URL to the listing

    Returns:
        dict: A dictionary containing:
            - 'title' (str): The title of the listing
            - 'price' (str): The price listed
            - 'description' (str): The description of the listing
            - 'img' (str): A full URL to the image
    """
    return fetch(url)

def main():
    mcp_cli = cli.MCP()
    mcp_cli.expose(hardverapro_search)
    mcp_cli.expose(hardverapro_fetch)
    mcp_cli.run()

if __name__ == "__main__":
    main()