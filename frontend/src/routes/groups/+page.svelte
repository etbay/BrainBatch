<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    const BACKEND = 'http://localhost:8000';

    let groups = [];
    let loading = true;
    let error = '';
    let newGroupName = '';

    const token = () => localStorage.getItem('authToken');

    async function loadGroups() {
        loading = true; error = '';
        try {
            const res = await fetch(`${BACKEND}/api/groups/`, {
                headers: { Authorization: `Token ${token()}` }
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Failed to load groups');
            groups = data;
        } catch (e) { error = e.message; }
        finally { loading = false; }
    }

    async function createGroup() {
        if (!newGroupName.trim()) return;
        const res = await fetch(`${BACKEND}/api/groups/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Authorization: `Token ${token()}` },
            body: JSON.stringify({ name: newGroupName.trim() })
        });
        const data = await res.json();
        if (!res.ok) { error = data.error || 'Failed to create'; return; }
        goto(`/groups/${data.id}`);
    }

    onMount(loadGroups);
</script>

<h1>Your Groups</h1>
{#if error}<p style="color:red">{error}</p>{/if}
{#if loading}<p>Loading…</p>{/if}

<div style="margin: 0.5rem 0;">
    <input placeholder="New group name" bind:value={newGroupName} />
    <button on:click={createGroup}>Create</button>
</div>

<ul>
    {#each groups as g}
        <li><a href={`/groups/${g.id}`}>{g.name}</a> <small>({g.member_count} members)</small></li>
    {/each}
</ul>