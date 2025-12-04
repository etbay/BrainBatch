

export const index = 5;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/createaccount/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/5.DMhMQCN4.js","_app/immutable/chunks/DsnmJJEf.js","_app/immutable/chunks/BBk6bQQc.js","_app/immutable/chunks/C7H14__D.js"];
export const stylesheets = ["_app/immutable/assets/5.Dfarygw0.css"];
export const fonts = [];
