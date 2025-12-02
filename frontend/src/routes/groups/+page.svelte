<script>
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    let groups = [];
    let loading = true;
    let error = '';
    let newGroupName = '';

    async function loadGroups() {
        if (!$auth.userId)
        {
            console.error('Error: No user logged in');
            loading = false;
            return;
        }

        loading = true;
        error = '';

        try {
            const res = await fetch('http://127.0.0.1:5000/groups/get_all_groups', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: $auth.userId })
            });
            const response = await res.json();
            console.log('Groups data:', response);
            if (!res.ok) throw new Error(response.error || 'Failed to load groups');
            groups = Array.isArray(response.data) ? response.data : [response.data];
        } catch (e) {
            console.error('Error:', e);
            error = e.message;
        } finally {
            loading = false;
        }
    }

    async function createGroup() {
        if (!$auth.userId)
        {
            console.error('Error: No user logged in');
            return;
        }

        if (!newGroupName.trim()) return;
        const res = await fetch('http://127.0.0.1:5000/groups/new_group', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                group_name: newGroupName.trim(),
                creator_id: $auth.userId
            })
        });
        const data = await res.json();
        if (!res.ok) {
            error = data.error || 'Failed to create';
            return;
        }
        console.log('Group created:', data);
        await loadGroups();
    }

    onMount(loadGroups);
</script>

<h1>Your Groups</h1>
{#if error}<p style="color:red">{error}</p>{/if}

<div style="margin: 0.5rem 0;">
    <input placeholder="New group name" bind:value={newGroupName} />
    <button on:click={createGroup}>Create</button>
</div>

{#if loading}
    <p>Loading…</p>
{:else}
    <ul>
        {#each groups as g}
            <li><a href={'/groups/${g.id}'}>{g.name}</a></li>
        {:else}
            <p>No groups found. Create one to get started!</p>
        {/each}
    </ul>
{/if}