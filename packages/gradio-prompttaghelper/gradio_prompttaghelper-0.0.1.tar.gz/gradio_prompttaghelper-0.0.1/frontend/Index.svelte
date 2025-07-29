<script lang="ts">
	// --- IMPORTS ---
	// Standard Gradio imports for component structure and compatibility.
	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";

	// --- PROPS from Python Backend ---
	// The `value` prop receives our dictionary of tag groups.
	export let value: Record<string, string[]> = {};
	
	// The ID of the Textbox we need to update.
	export let target_textbox_id: string;

	// Standard Gradio props for visibility, labeling, etc.
	export let label: string;
	export let visible: boolean = true;
	export let elem_id: string = "";
	export let elem_classes: string[] = [];
	export let container: boolean = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{ clear_status: LoadingStatus; }>;

	// --- INTERNAL STATE ---
	// A dictionary to track which groups are open or collapsed.
	let groupVisibility: Record<string, boolean> = {};

	// Color palette for the tags: lilac, green, yellow, red, blue.
	const tagColors = ["#d8b4fe", "#bbf7d0", "#fde047", "#fca5a5", "#93c5fd"];

	// This reactive block runs whenever `value` (our tag groups) changes.
	// It initializes all groups to be open by default.
	$: {
		if (value) {
			for (const groupName in value) {
				if (groupVisibility[groupName] === undefined) {
					groupVisibility[groupName] = true;
				}
			}
		}
	}

	// --- FUNCTIONS ---
	function toggleGroup(groupName: string) {
		groupVisibility[groupName] = !groupVisibility[groupName];
	}

	function addTagToPrompt(tag: string) {
		if (!target_textbox_id) {
			console.error("PromptTagHelper: `target_textbox_id` prop is not set.");
			return;
		}

		// Find the actual <textarea> element inside the Gradio Textbox component.
		const targetTextarea = document.querySelector<HTMLTextAreaElement>(
			`#${target_textbox_id} textarea`
		);

		if (!targetTextarea) {
			console.error(`PromptTagHelper: Could not find textarea with id: #${target_textbox_id} textarea`);
			return;
		}
		
		let currentValue = targetTextarea.value.trim();

		// Intelligent logic for appending the tag with proper comma spacing.
		if (currentValue === "" || currentValue.endsWith(",")) {
			// If the field is empty or already ends with a comma,
			// add the tag. If it ends with a comma, add a space first.
			targetTextarea.value = currentValue.endsWith(",")
				? `${currentValue} ${tag}`
				: tag;
		} else {
			// If the field has text, append a comma, a space, and the new tag.
			targetTextarea.value = `${currentValue}, ${tag}`;
		}

		// ** CRITICAL STEP **
		// Programmatically dispatch an 'input' event on the target textarea.
		// This notifies Gradio that the value has changed, so any other
		// event listeners on that textbox will be triggered correctly.
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

	<!-- Our custom UI for displaying and interacting with tags -->
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
	/* Styles for our custom component UI */
	.container {
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		padding: 8px;
		background: #f9fafb;
	}
	.label {
		display: block;
		margin-bottom: 8px;
		font-size: 14px;
		color: #374151;
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
		background-color: #f3f4f6;
		border: 1px solid #e5e7eb;
		border-radius: 6px;
		text-align: left;
		cursor: pointer;
		font-size: 1rem;
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
		color: #1f2937; /* Ensure dark text for readability on light backgrounds */
	}
	.tag-button:hover {
		/* Slightly darken any background color on hover for visual feedback */
		filter: brightness(0.95);
	}
</style>