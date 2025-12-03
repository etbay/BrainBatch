import { writable } from 'svelte/store';

export const auth = writable({
    userId: null,
    isLoggedIn: false
});
