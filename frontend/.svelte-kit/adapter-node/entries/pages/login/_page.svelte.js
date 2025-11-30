import "clsx";
function _page($$payload) {
  $$payload.out.push(`<div class="login-container svelte-1x05zx6"><h1 class="svelte-1x05zx6">Log in to BrainBatch</h1> <p class="svelte-1x05zx6">Don't have an account yet? <a href="/createaccount">Create one!</a></p> <form class="svelte-1x05zx6"><div class="form-field svelte-1x05zx6"><label for="username" class="svelte-1x05zx6">Username:</label> <input type="text" name="username" id="username" required class="svelte-1x05zx6"/></div> <div class="form-field svelte-1x05zx6"><label for="password" class="svelte-1x05zx6">Password:</label> <input type="password" name="password" id="password" required class="svelte-1x05zx6"/></div> <input type="submit" value="Log in" class="svelte-1x05zx6"/></form></div>`);
}
export {
  _page as default
};
