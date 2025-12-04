import "clsx";
import { d as attr, c as pop, p as push } from "../../chunks/index2.js";
import { p as page } from "../../chunks/index3.js";
const github = "data:image/svg+xml,%3csvg%20width='98'%20height='96'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20fill-rule='evenodd'%20clip-rule='evenodd'%20d='M48.854%200C21.839%200%200%2022%200%2049.217c0%2021.756%2013.993%2040.172%2033.405%2046.69%202.427.49%203.316-1.059%203.316-2.362%200-1.141-.08-5.052-.08-9.127-13.59%202.934-16.42-5.867-16.42-5.867-2.184-5.704-5.42-7.17-5.42-7.17-4.448-3.015.324-3.015.324-3.015%204.934.326%207.523%205.052%207.523%205.052%204.367%207.496%2011.404%205.378%2014.235%204.074.404-3.178%201.699-5.378%203.074-6.6-10.839-1.141-22.243-5.378-22.243-24.283%200-5.378%201.94-9.778%205.014-13.2-.485-1.222-2.184-6.275.486-13.038%200%200%204.125-1.304%2013.426%205.052a46.97%2046.97%200%200%201%2012.214-1.63c4.125%200%208.33.571%2012.213%201.63%209.302-6.356%2013.427-5.052%2013.427-5.052%202.67%206.763.97%2011.816.485%2013.038%203.155%203.422%205.015%207.822%205.015%2013.2%200%2018.905-11.404%2023.06-22.324%2024.283%201.78%201.548%203.316%204.481%203.316%209.126%200%206.6-.08%2011.897-.08%2013.526%200%201.304.89%202.853%203.316%202.364%2019.412-6.52%2033.405-24.935%2033.405-46.691C97.707%2022%2075.788%200%2048.854%200z'%20fill='%2324292f'/%3e%3c/svg%3e";
function Header($$payload, $$props) {
  push();
  $$payload.out.push(`<header class="svelte-vny38x"><div class="corner svelte-vny38x"><a href="/" class="svelte-vny38x">BrainBatch</a></div> <nav class="svelte-vny38x"><svg viewBox="0 0 2 3" aria-hidden="true" class="svelte-vny38x"><path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z" class="svelte-vny38x"></path></svg> <ul class="svelte-vny38x"><li${attr("aria-current", page.url.pathname === "/" ? "page" : void 0)} class="svelte-vny38x"><a href="/" class="svelte-vny38x">Home</a></li> <li${attr("aria-current", page.url.pathname === "/login" ? "page" : void 0)} class="svelte-vny38x"><a href="/login" class="svelte-vny38x">Log in</a></li> <li${attr("aria-current", page.url.pathname === "/createaccount" ? "page" : void 0)} class="svelte-vny38x"><a href="/createaccount" class="svelte-vny38x">Create Account</a></li> <li${attr("aria-current", page.url.pathname === "/canvas" ? "page" : void 0)} class="svelte-vny38x"><a href="/canvas" class="svelte-vny38x">Canvas</a></li> <li${attr("aria-current", page.url.pathname === "/profile" ? "page" : void 0)} class="svelte-vny38x"><a href="/profile" class="svelte-vny38x">Profile</a></li></ul> <svg viewBox="0 0 2 3" aria-hidden="true" class="svelte-vny38x"><path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" class="svelte-vny38x"></path></svg></nav> <div class="corner svelte-vny38x"><a href="https://github.com/etbay/BrainBatch" class="svelte-vny38x"><img${attr("src", github)} alt="GitHub" class="svelte-vny38x"/></a></div></header>`);
  pop();
}
function _layout($$payload, $$props) {
  let { children } = $$props;
  $$payload.out.push(`<div class="app svelte-12qhfyh">`);
  Header($$payload);
  $$payload.out.push(`<!----> <main class="svelte-12qhfyh">`);
  children($$payload);
  $$payload.out.push(`<!----></main> <footer class="svelte-12qhfyh"><p>visit <a href="https://svelte.dev/docs/kit" class="svelte-12qhfyh">svelte.dev/docs/kit</a> to learn about SvelteKit</p></footer></div>`);
}
export {
  _layout as default
};
