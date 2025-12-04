import adapter from '@sveltejs/adapter-node';

// Deploy the app by running `npm run build`. Then, start the server with `node build`.

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter()
	}
};

export default config;