<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { tick } from 'svelte';
    const BACKEND = 'http://localhost:8000';

    let group = null, messages = [];
    let next_before = null, has_more = false;
    let error = '', loading = true, loadingOlder = false;
    let content = '';
    let listEl;

    const token = () => localStorage.getItem('authToken');
    const gid = () => Number($page.params.id);

    async function loadGroup() {
        const res = await fetch(`${BACKEND}/api/groups/${gid()}/`, {
            headers: { Authorization: `Token ${token()}` }
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to load group');
        group = data;
    }

    async function loadLatest() {
        const res = await fetch(`${BACKEND}/api/groups/${gid()}/messages/?limit=25`, {
            headers: { Authorization: `Token ${token()}` }
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to load messages');
        messages = data.messages;
        next_before = data.next_before;
        has_more = data.has_more;
        await tick();
        if (listEl) listEl.scrollTop = listEl.scrollHeight;
    }

    async function loadOlder() {
        if (!has_more || loadingOlder) return;
        loadingOlder = true;
        const prevHeight = listEl?.scrollHeight ?? 0;
        const res = await fetch(`${BACKEND}/api/groups/${gid()}/messages/?limit=25&before=${encodeURIComponent(next_before)}`, {
            headers: { Authorization: `Token ${token()}` }
        });
        const data = await res.json();
        if (res.ok) {
            messages = [...data.messages, ...messages];
            has_more = data.has_more;
            next_before = data.next_before;
            await tick();
            if (listEl) listEl.scrollTop = listEl.scrollHeight - prevHeight;
        } else {
            error = data.error || 'Failed to load older';
        }
        loadingOlder = false;
    }

    async function sendMessage() {
        const text = content.trim();
        if (!text) return;
        const res = await fetch(`${BACKEND}/api/groups/${gid()}/messages/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Authorization: `Token ${token()}` },
            body: JSON.stringify({ content: text })
        });
        const data = await res.json();
        if (!res.ok) { error = data.error || 'Failed to send'; return; }
        messages = [...messages, data];
        content = '';
        await tick();
        if (listEl) listEl.scrollTop = listEl.scrollHeight;
    }

    function onScroll() {
        if (listEl?.scrollTop <= 0) loadOlder();
    }

    onMount(async () => {
        try {
            await loadGroup();
            await loadLatest();
        } catch (e) { error = e.message; }
        finally { loading = false; }
    });
</script>

{#if error}<p style="color:red">{error}</p>{/if}
{#if loading}<p>Loading…</p>{/if}

{#if group}
    <h2>{group.name}</h2>
    <div bind:this={listEl} on:scroll={onScroll} style="height:60vh; overflow:auto; border:1px solid #ddd; padding:8px; background:#fff;">
        {#if has_more}
            <div style="text-align:center; color:#666; padding:4px 0;">
                {loadingOlder ? 'Loading…' : 'Scroll up for earlier messages'}
            </div>
        {/if}
        {#each messages as m}
            <div style="margin:6px 0;">
                <strong>{m.username}</strong>
                <span style="color:#888; font-size:.8em;"> {new Date(m.created_at).toLocaleString()}</span>
                <div>{m.content}</div>
            </div>
        {/each}
    </div>
    <div style="margin-top:8px; display:flex; gap:8px;">
        <input style="flex:1" bind:value={content} placeholder="Type a message…" on:keydown={(e)=>e.key==='Enter'&&sendMessage()} />
        <button on:click={sendMessage}>Send</button>
    </div>
{/if}