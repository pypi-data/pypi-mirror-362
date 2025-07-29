from urllib.parse import urlparse, parse_qs

def _extract_google_analytics_tags(request):
	parsed_url = urlparse(request.url)
	params = parse_qs(parsed_url.query)
	param_dict = {}
	for key, value in params.items():
		param_dict[key] = value[0] if len(value) == 1 else value
	return param_dict


class TagManagers:
	def __init__(self):
		self.urls = {
			"https://analytics.google.com/g/collect" : _extract_google_analytics_tags
		}

	def keys(self):
		return self.urls.keys()

	def extend(self, url, handler):
		self.urls[url] = handler

	def __getitem__(self, value):
		return self.urls[value]


TAGGING_URLS = TagManagers()