
export function MockXHR(settings) {
	let
		response = settings.content,
		json = null;
	if (typeof response === 'string') {
		try {
			json = JSON.parse(response);
		}
		catch (e) {}
	}
	if (typeof response === 'object') {
		response = JSON.stringify(response);
	}
	const result = {
		open: jest.fn(),
		send: jest.fn(),
		setRequestHeader: jest.fn(),
		getResponseHeader: jest.fn((header) => {
			const headers = {
				'content-type': settings.contentType === undefined ? 'application/json' : settings.contentType
			};
			return headers[header];
		}),
		readyState: settings.readyState || 4,
		responseText: response || JSON.stringify({
			status: settings.status || 'success'
		}),
		statusText: settings.statusText || 'OK'
	};
	if (json) {
		result.responseJSON = json;
	}
	return result;
}
