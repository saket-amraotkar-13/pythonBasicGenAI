##Add custom tool which can be integrated whole scheme of things to perfom task in org which is independept of online tools

from langchain_core.tools import tool

### tool is decorator (just like annotations in CAP/CDS) - define doc string to instrcut langgraph when to use this tool by instructing input/output types as doc string
@tool
def my_custom_tool(input: str) -> str:
    """
        This is a custom tool that pcrocess input string.

        Args:
            query: The input string to process

        Returns:

            the Pceossed output string
    """

    ##implement custiom logic for tool
    return f"Process: {input}"

    @tool
    def update_vendor_data(vendor_id: str, data: dict) -> str:

        """
            This is Custom tool for vendor data.

            Args:
                vendor_id: vendor ID to update
                data: new data for vendor 

            Returns:
                A confirmation message indicating ststus of update vendor data
        """

        return f"{vendor_id} updated Vendor Data {data} "