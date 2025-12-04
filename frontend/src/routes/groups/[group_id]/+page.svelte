<script>
    import { onMount, onDestroy } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import { page } from '$app/stores';
    import { tick } from 'svelte';
    import { goto } from '$app/navigation';
    const BACKEND = 'https://api.brainbatch.xyz';

    let group = null;
    let messages = [];
    let error = '';
    let loading = true;
    let sending = false;
    let content = '';
    let listEl;
    let pollingInterval;

    const token = () => localStorage.getItem('authToken');
    const gid = () => $page.params.group_id;

    let userCache = {};

    async function verifyLogin() {
        if (!$auth.isLoggedIn)
        {
            goto('/login');
            return;
        }

        await loadGroup();
        await loadMessages();
    }

    async function loadGroup() {
        try {
            const res = await fetch(`${BACKEND}/groups/get_group`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: gid() }) 
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Failed to load group');
            group = data.data; 
        } catch (e) {
            console.error('Error:', e);
            error = e.message;
        }
    }

    async function loadMessages() {
        try {
            const res = await fetch(`${BACKEND}/groups/get_group`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: gid() }) 
            });
            const data = await res.json();
            console.log('Backend response:', data);

            if (!res.ok || !data.data || !Array.isArray(data.data) || data.data.length === 0) {
                throw new Error(data.error || 'Invalid response from backend');
            }

            const groupData = data.data[0];
            if (groupData.chat_areas && groupData.chat_areas.length > 0) {
                messages = groupData.chat_areas[0].messages || []; 
            } else {
                messages = [];
            }

            for (const message of messages) {
                if (message.sender_id && !userCache[message.sender_id]) {
                    userCache[message.sender_id] = await fetchUsername(message.sender_id);
                }
            }

            await tick();
            if (listEl) listEl.scrollTop = listEl.scrollHeight;
        } catch (e) {
            console.error('Error in loadMessages:', e);
            error = e.message;
        }
    }

    async function updateMessages() {
        try {
            await tick();
            if (listEl) {
                listEl.scrollTop = listEl.scrollHeight;
            }
        } catch (e) {
            console.error('Error updating messages:', e);
        }
    }

    async function fetchUsername(senderId) {
        try {
            const res = await fetch(`${BACKEND}/users/get_user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: senderId })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Failed to fetch username');
            return data.data[0].username; 
        } catch (e) {
            console.error('Error fetching username for sender_id:', senderId, e);
            return 'Unknown User'; 
        }
    }    

    async function sendMessage() {
        const text = content.trim();
        if (!text) return;

        sending = true;
        const newMessage = {
            sender_id: $auth.userId,
            contents: text
        };

        content = ''; 

        await tick(); 
        if (listEl) listEl.scrollTop = listEl.scrollHeight; 

        try {
            const res = await fetch(`${BACKEND}/groups/send_message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    group_id: gid(),
                    chat_area_name: 'General',
                    message: text,
                    sender_id: $auth.userId
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Failed to send message');

            if (!userCache[$auth.userId]) {
                userCache[$auth.userId] = await fetchUsername($auth.userId);
            }
        } catch (e) {
            console.error('Error:', e);
            error = e.message;

            messages = messages.filter((m) => m !== newMessage);
            await tick(); 
        } finally {
            sending = false;
        }
    }

    // check for new messages every 5 seconds
    function startPolling() {
        pollingInterval = setInterval(async () => {
            try {
                await loadMessages(); 
            } catch (e) {
                console.error('Error during polling:', e);
            }
        }, 5000); 
    }

    onMount(async () => {
        loading = true;
        try {
            await verifyLogin();
            startPolling();
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    });

    onDestroy(() => {
        console.log('onDestroy called'); // Debugging
        if (pollingInterval) {
            clearInterval(pollingInterval); // Clear the polling interval
            console.log('Polling interval cleared'); // Debugging
            pollingInterval = null; // Reset the interval variable
        }
    });
</script>

{#if error}<p style="color:red">{error}</p>{/if}
{#if loading}<p>Loading…</p>{/if}

{#if group}
    <h2>{group.name}</h2>
    <div bind:this={listEl} style="height:60vh; overflow:auto; border:1px solid #ddd; padding:8px; background:#fff;">
        {#if messages.length === 0}
            <p style="text-align: center; color: #888;">No messages yet. Start the conversation!</p>
        {/if}
        {#each messages as m}
            <div style="margin:6px 0;">
                <strong>{userCache[m.sender_id] || 'Unknown User'}</strong>
                <div>{m.contents}</div>
            </div>
        {/each}
    </div>
    <div style="margin-top:8px; display:flex; gap:8px;">
        <input style="flex:1" bind:value={content} placeholder="Type a message…" on:keydown={(e) => e.key === 'Enter' && sendMessage()} />
        <button on:click={sendMessage}>Send</button>
    </div>
    {#if sending}
        <div style="color: #888; font-size: 0.9em;">Sending...</div>
    {/if}
{/if}