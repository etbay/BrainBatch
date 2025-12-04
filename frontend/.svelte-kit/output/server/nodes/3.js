import * as universal from '../entries/pages/about/_page.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/about/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/about/+page.js";
export const imports = ["_app/immutable/nodes/3.BIhyhADm.js","_app/immutable/chunks/Dnx749Jq.js","_app/immutable/chunks/C7H14__D.js","_app/immutable/chunks/DsnmJJEf.js","_app/immutable/chunks/BBk6bQQc.js","_app/immutable/chunks/Doj5kpS1.js"];
export const stylesheets = [];
export const fonts = [];
