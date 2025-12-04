export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.svg","robots.txt"]),
	mimeTypes: {".svg":"image/svg+xml",".txt":"text/plain"},
	_: {
		client: {start:"_app/immutable/entry/start.b6j6cirY.js",app:"_app/immutable/entry/app.BVBxbdFh.js",imports:["_app/immutable/entry/start.b6j6cirY.js","_app/immutable/chunks/BbPlUrqJ.js","_app/immutable/chunks/BGfPQn0W.js","_app/immutable/chunks/C7H14__D.js","_app/immutable/chunks/CqFkhK-z.js","_app/immutable/chunks/Doj5kpS1.js","_app/immutable/entry/app.BVBxbdFh.js","_app/immutable/chunks/C7H14__D.js","_app/immutable/chunks/CqFkhK-z.js","_app/immutable/chunks/Doj5kpS1.js","_app/immutable/chunks/DsnmJJEf.js","_app/immutable/chunks/BGfPQn0W.js","_app/immutable/chunks/-RQBovE-.js","_app/immutable/chunks/WavmjKSR.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/4.js')),
			__memo(() => import('./nodes/5.js')),
			__memo(() => import('./nodes/6.js')),
			__memo(() => import('./nodes/7.js')),
			__memo(() => import('./nodes/8.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/canvas",
				pattern: /^\/canvas\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/createaccount",
				pattern: /^\/createaccount\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/login",
				pattern: /^\/login\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			},
			{
				id: "/profile",
				pattern: /^\/profile\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 5 },
				endpoint: null
			},
			{
				id: "/sverdle",
				pattern: /^\/sverdle\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 6 },
				endpoint: null
			}
		],
		prerendered_routes: new Set(["/","/about","/sverdle/how-to-play"]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

export const prerendered = new Set(["/","/about","/sverdle/how-to-play"]);

export const base = "";