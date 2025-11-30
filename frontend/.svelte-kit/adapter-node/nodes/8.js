import * as server from '../entries/pages/sverdle/_page.server.js';

export const index = 8;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/sverdle/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/sverdle/+page.server.js";
export const imports = ["_app/immutable/nodes/8.DzwdUfgw.js","_app/immutable/chunks/DsnmJJEf.js","_app/immutable/chunks/C7H14__D.js","_app/immutable/chunks/CqFkhK-z.js","_app/immutable/chunks/Doj5kpS1.js","_app/immutable/chunks/-RQBovE-.js","_app/immutable/chunks/CD2-qF9y.js","_app/immutable/chunks/CoNfMqP3.js","_app/immutable/chunks/BRzKQYUk.js","_app/immutable/chunks/WavmjKSR.js","_app/immutable/chunks/BbPlUrqJ.js","_app/immutable/chunks/BGfPQn0W.js"];
export const stylesheets = ["_app/immutable/assets/8.DM6DEHdi.css"];
export const fonts = [];
