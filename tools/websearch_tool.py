class WebSearchTool:
    def __init__(self):
        pass

    def search(self, args):
        # In production, call Bing / Google / custom search API
        q = args.get('q','')
        return [{"title":"Result 1","snippet":"This is a mocked result about "+q, "url":"https://example.com"}]
