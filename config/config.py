class Config:
    prompt_for_llm = """
        You are an advanced AI model tasked with extracting structured financial data from an image. The image provided is a page from a financial document, such as a balance sheet, income statement, or other tabular financial data.

        Your goal is to extract the relevant data and output it as a structured Python Dictionary. The Dictionary should follow this format:

        {
            "data_point_1": "value_1",
            "data_point_2": "value_2",
            ...
        }

        Guidelines:
        1. Use the text visible in the image to extract data.
        2. Identify and include key financial data points such as:
        - Revenue, expenses, profit/loss.
        - Assets, liabilities, equity.
        - Ratios or other calculated metrics, if applicable.
        3. If a data point is found but its value is unclear, set its value to `null`.
        4. If a data point is not present in the image, omit it from the JSON.
        5. Ensure that numerical values are properly formatted as numbers (e.g., integers, floats) without extraneous characters like commas.

        Respond only with the JSON output, no additional explanation or text.

        Input image: [Attach the image of the financial document]
    """
    
    API_KEY = "AIzaSyCM0bRwKpTcXXrIWYYojil92uj7dt3_yM0"
