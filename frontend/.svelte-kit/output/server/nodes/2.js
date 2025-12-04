import * as universal from '../entries/pages/_page.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+page.js";
export const imports = ["_app/immutable/nodes/2.BYrfZG1w.js","_app/immutable/chunks/DsnmJJEf.js","_app/immutable/chunks/BBk6bQQc.js","_app/immutable/chunks/C7H14__D.js","_app/immutable/chunks/Doj5kpS1.js","_app/immutable/chunks/CoNfMqP3.js","_app/immutable/chunks/CqFkhK-z.js","_app/immutable/chunks/BRzKQYUk.js"];
export const stylesheets = ["_app/immutable/assets/2.C7W8Uifw.css"];
export const fonts = [];
