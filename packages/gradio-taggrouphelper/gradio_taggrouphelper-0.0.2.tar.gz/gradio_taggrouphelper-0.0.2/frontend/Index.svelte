<script lang="ts">	
	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";

	export let value: Record<string, string[]> = {};		
	export let target_textbox_id: string;
	export let separator: string = ", ";
	export let label: string;
	export let visible: boolean = true;
	export let elem_id: string = "";
	export let elem_classes: string[] = [];
	export let container: boolean = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{ clear_status: LoadingStatus; }>;

	let groupVisibility: Record<string, boolean> = {};

	const tagColors = ["#d8b4fe", "#bbf7d0", "#fde047", "#fca5a5", "#93c5fd"];

	$: {
		if (value) {
			for (const groupName in value) {
				if (groupVisibility[groupName] === undefined) {
					groupVisibility[groupName] = true;
				}
			}
		}
	}

	function toggleGroup(groupName: string) {
		groupVisibility[groupName] = !groupVisibility[groupName];
	}

	function addTagToPrompt(tag: string) {
		if (!target_textbox_id) {
			console.error("TagGroupHelper: `target_textbox_id` prop is not set.");
			return;
		}

		const targetTextarea = document.querySelector<HTMLTextAreaElement>(
			`#${target_textbox_id} textarea`
		);

		if (!targetTextarea) {
			console.error(`TagGroupHelper: Could not find textarea with id: #${target_textbox_id} textarea`);
			return;
		}
		
		let currentValue = targetTextarea.value;
		
		if (currentValue === "") {
			targetTextarea.value = tag;
		} else {
			if (currentValue.endsWith(separator) || currentValue.endsWith(" ")) {
				targetTextarea.value = `${currentValue}${tag}`;
			} else {
				targetTextarea.value = `${currentValue}${separator}${tag}`;
			}
		}

		targetTextarea.dispatchEvent(new Event('input', { bubbles: true }));
	}
</script>

<!-- The main structure uses the standard Gradio <Block> component. -->
<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	{#if label}
		<span class="label">{label}</span>
	{/if}
	<div class="container">
		<!-- We iterate over the 'value' prop, which contains our tag groups -->
		{#if value}
			{#each Object.entries(value) as [groupName, tags]}
				<div class="group">
					<button class="group-header" on:click={() => toggleGroup(groupName)}>
						<span class="group-title">{groupName}</span>
						<span class="group-toggle-icon">{groupVisibility[groupName] ? '−' : '+'}</span>
					</button>

					{#if groupVisibility[groupName]}
						<div class="tags-container">
							<!-- Apply background color dynamically to each tag -->
							{#each tags as tag, i}
								<button 
									class="tag-button"
									style="background-color: {tagColors[i % tagColors.length]};"
									on:click={() => addTagToPrompt(tag)}
								>
									{tag}
								</button>
							{/each}
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>
</Block>

<style>	
	.container {
		border: 1px solid var(--border-color-primary);
		border-radius: var(--radius-lg);
		padding: 8px;
		background: var(--background-fill-secondary);
	}
	.label {
		display: block;
		margin-bottom: 8px;
		font-size: 14px;
		color: var(--body-text-color-subdued);
		font-weight: 600;
	}
	.group {
		margin-bottom: 8px;
	}
	.group:last-child {
		margin-bottom: 0;
	}
	
	.group-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		padding: 8px 12px;				
		background-color: var(--neutral-100, #f3f4f6); 				
		color: var(--neutral-700, #374151);
		border: 1px solid var(--border-color-primary);
		border-radius: var(--radius-md);
		text-align: left;
		cursor: pointer;
		font-size: 1rem; 
		transition: background-color 0.2s;
	}
	.group-header:hover {		
		background-color: var(--neutral-200, #e5e7eb);
	}

	.group-title {
		font-weight: 600;
	}
	.group-toggle-icon {
		font-size: 1.2rem;
		font-weight: bold;
	}
	.tags-container {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		padding: 12px 8px;
	}
	.tag-button {
		padding: 4px 10px;
		border: 1px solid #d1d5db;
		border-radius: 12px;
		font-size: 0.875rem;
		cursor: pointer;
		transition: filter 0.2s;
		color: #1f2937;
	}
	.tag-button:hover {
		filter: brightness(0.95);
	}
</style>