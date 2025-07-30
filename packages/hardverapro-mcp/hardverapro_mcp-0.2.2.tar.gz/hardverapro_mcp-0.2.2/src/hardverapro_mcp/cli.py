from scraper import categories, search, fetch
import gradio as gr

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
    raw = search(query,offset=offset,category=category)
    return [[r["title"], r["price"], r["link"]] for r in raw]

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



iface_search = gr.Interface(
    fn=hardverapro_search,
    inputs=[
        gr.Textbox(label="Search query"),
        gr.Number(label="Offset (e.g. 100, 200)", value=0),
        gr.Dropdown(choices=categories, value="All"),
        ],
    outputs=gr.Dataframe(headers=["title", "price", "link"], type="array"),
    title="HardverApró Search"
)

iface_fetch = gr.Interface(
    fn=hardverapro_fetch,
    inputs=gr.Textbox(label="URL"),
    outputs=gr.JSON(),
    title="HardverApró Fetch"
)

tabbed_interface = gr.TabbedInterface(
    [iface_search, iface_fetch],
)



def main():
    tabbed_interface.launch(mcp_server=True)

if __name__ == "__main__":
    main()