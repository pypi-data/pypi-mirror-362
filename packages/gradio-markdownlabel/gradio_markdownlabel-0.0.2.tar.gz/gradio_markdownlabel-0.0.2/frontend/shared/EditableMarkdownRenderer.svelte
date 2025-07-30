<script lang="ts">
	import { marked } from 'marked';
	import { createEventDispatcher } from 'svelte';
	import type { SelectData } from '@gradio/utils';
	import { Copy } from '@gradio/icons';

	export let markdown_content: string = '';
	export let highlights: Array<{
		term?: string;
		position?: number[];
		title: string;
		content: string;
		category: string;
		color: string;
	}> = [];
	export let show_side_panel: boolean = true;
	export let panel_width: string = '300px';
	export let interactive: boolean = false;
	export let edit_mode: string = 'split'; // 'split', 'tabs', 'overlay'
	export let show_preview: boolean = true;
	export const markdown_editor: string = 'textarea';

	const dispatch = createEventDispatcher<{
		select: SelectData;
		change: { markdown_content: string; highlights: any[] };
		edit: { markdown_content: string; highlights: any[] };
		save: { markdown_content: string; highlights: any[] };
		cancel: { markdown_content: string; highlights: any[] };
	}>();

	let selectedHighlight: typeof highlights[0] | null = null;
	let processedHtml: string = '';
	let panelContent: string = '';
	let isEditing: boolean = false;
	let editingContent: string = '';
	let originalContent: string = '';
	let currentTab: 'edit' | 'preview' | 'highlights' = 'edit';

	// Track original state for cancel functionality
	$: {
		if (!isEditing) {
			originalContent = markdown_content;
		}
	}

	// Process markdown and apply highlighting
	$: {
		const contentToRender = isEditing && edit_mode === 'split' && show_preview ? editingContent : markdown_content;
		if (contentToRender) {
			processMarkdown(contentToRender);
		}
	}

	// Process panel content
	$: {
		if (selectedHighlight) {
			processPanelContent();
		}
	}

	async function processMarkdown(contentToRender: string) {
		// First, parse the markdown to HTML
		let html = await marked(contentToRender);
		
		// Separate position-based and term-based highlights
		const positionHighlights = highlights.filter(h => h.position && h.position.length === 2);
		const termHighlights = highlights.filter(h => h.term && h.term.trim());
		
		// Apply term-based highlights to the HTML first
		termHighlights.forEach(highlight => {
			if (highlight.term && highlight.term.trim()) {
				const index = highlights.indexOf(highlight);
				const regex = new RegExp(`\\b${escapeRegex(highlight.term)}\\b`, 'gi');
				html = html.replace(regex, (match: string) => {
					const color = highlight.color || '#e3f2fd';
					return `<span class="highlight-term" 
								data-index="${index}" 
								data-term="${highlight.term}"
								style="background-color: ${color}; cursor: pointer; padding: 2px 4px; border-radius: 3px; transition: all 0.2s;"
								role="button" 
								tabindex="0" 
								aria-label="Highlighted term: ${highlight.term}">
							${match}
						</span>`;
				});
			}
		});
		
		// Apply position-based highlights to the HTML
		// Convert position-based highlights to term-based for simplicity and reliability
		positionHighlights.forEach(highlight => {
			const [start, end] = highlight.position!;
			if (start >= 0 && end <= contentToRender.length && start < end) {
				const targetText = contentToRender.substring(start, end);
				const color = highlight.color || '#e3f2fd';
				const index = highlights.indexOf(highlight);
				
				// Escape the target text for regex and handle multiline/whitespace
				const escapedText = escapeRegex(targetText).replace(/\s+/g, '\\s+');
				
				// Create a regex that only matches text content (not inside HTML tags)
				const textRegex = new RegExp(`\\b${escapedText}\\b`, 'gi');
				
				// Apply the highlight - this will work like term-based highlighting
				// but using the exact text from the position
				html = html.replace(textRegex, (match: string) => {
					return `<span class="highlight-position" 
								data-index="${index}" 
								data-text="${encodeURIComponent(targetText)}"
								style="background-color: ${color}; cursor: pointer; padding: 2px 4px; border-radius: 3px; transition: all 0.2s;"
								role="button" 
								tabindex="0" 
								aria-label="Highlighted text: ${targetText.replace(/"/g, '&quot;')}">
							${match}
						</span>`;
				});
			}
		});
		
		processedHtml = html;
	}

	async function processPanelContent() {
		if (selectedHighlight) {
			panelContent = await marked(selectedHighlight.content || 'No additional information available.');
		}
	}

	function escapeRegex(string: string): string {
		return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
	}

	function handleTermClick(event: Event) {
		const target = event.target as HTMLElement;
		if (target.classList.contains('highlight-term') || target.classList.contains('highlight-position')) {
			const index = parseInt(target.dataset.index || '0');
			const highlight = highlights[index];
			if (highlight) {
				selectedHighlight = highlight;
				dispatch('select', {
					index,
					value: highlight
				});
			}
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		const target = event.target as HTMLElement;
		if ((event.key === 'Enter' || event.key === ' ') && 
			(target.classList.contains('highlight-term') || target.classList.contains('highlight-position'))) {
			event.preventDefault();
			handleTermClick(event);
		}
	}

	function closeSidePanel() {
		selectedHighlight = null;
	}

	function startEditing() {
		isEditing = true;
		editingContent = markdown_content;
		originalContent = markdown_content;
		dispatch('edit', { markdown_content, highlights });
	}

	function saveChanges() {
		markdown_content = editingContent;
		isEditing = false;
		dispatch('save', { markdown_content, highlights });
		// Only dispatch change event on explicit save
		dispatch('change', { markdown_content, highlights });
	}

	function cancelEditing() {
		editingContent = originalContent;
		isEditing = false;
		dispatch('cancel', { markdown_content: originalContent, highlights });
	}

	function handleTextareaInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		editingContent = target.value;
		// Don't dispatch change events in real-time to avoid loops
		// Changes will be dispatched only on save
	}

	function setTab(tab: typeof currentTab) {
		currentTab = tab;
	}

	async function copyToClipboard() {
		try {
			const contentToCopy = isEditing ? editingContent : markdown_content;
			if (navigator.clipboard && window.isSecureContext) {
				await navigator.clipboard.writeText(contentToCopy);
			} else {
				// Fallback for older browsers or non-secure contexts
				const textArea = document.createElement('textarea');
				textArea.value = contentToCopy;
				textArea.style.position = 'fixed';
				textArea.style.left = '-999999px';
				textArea.style.top = '-999999px';
				document.body.appendChild(textArea);
				textArea.focus();
				textArea.select();
				document.execCommand('copy');
				textArea.remove();
			}
		} catch (err) {
			console.error('Failed to copy text: ', err);
		}
	}
</script>

<div class="markdown-container" class:editing={isEditing} class:with-panel={show_side_panel && selectedHighlight}>
	<!-- View Mode Controls -->
	{#if !isEditing}
		<div class="edit-controls">
			{#if interactive}
				<button class="edit-btn" on:click={startEditing}>
					✏️ Edit
				</button>
			{/if}
			<button class="copy-btn" on:click={copyToClipboard} aria-label="Copy" aria-roledescription="Copy text">
				<Copy />
			</button>
		</div>
	{/if}

	{#if isEditing}
		<div class="edit-controls">
			<button class="save-btn" on:click={saveChanges}>
				💾 Save
			</button>
			<button class="cancel-btn" on:click={cancelEditing}>
				❌ Cancel
			</button>
			
			{#if edit_mode === 'tabs'}
				<div class="tab-controls">
					<button 
						class="tab-btn" 
						class:active={currentTab === 'edit'}
						on:click={() => setTab('edit')}
					>
						Edit
					</button>
					<button 
						class="tab-btn" 
						class:active={currentTab === 'preview'}
						on:click={() => setTab('preview')}
					>
						Preview
					</button>
					<button class="copy-btn" on:click={copyToClipboard} aria-label="Copy" aria-roledescription="Copy text">
						<Copy />
					</button>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Content Area -->
	<div class="content-area" class:split-mode={edit_mode === 'split' && isEditing}>
		{#if isEditing}
			{#if edit_mode === 'split'}
				<!-- Split Mode: Editor and Preview Side by Side -->
				<div class="editor-section">
					<div class="editor-header">
						<h4>Markdown Editor</h4>
						<button class="copy-btn" on:click={copyToClipboard} aria-label="Copy" aria-roledescription="Copy text">
							<Copy />
						</button>
					</div>
					<textarea
						class="markdown-editor"
						bind:value={editingContent}
						on:input={handleTextareaInput}
						placeholder="Enter your markdown content..."
						spellcheck="false"
					></textarea>
				</div>
				
				{#if show_preview}
					<div class="preview-section">
						<div class="preview-header">
							<h4>Live Preview</h4>
						</div>
						<div class="markdown-content preview" on:click={handleTermClick} on:keydown={handleKeydown} role="document" aria-label="Markdown preview with interactive highlights">
							{@html processedHtml}
						</div>
					</div>
				{/if}
			{:else if edit_mode === 'tabs'}
				<!-- Tab Mode: Switch between Edit and Preview -->
				<div class="tab-content">
					{#if currentTab === 'edit'}
						<textarea
							class="markdown-editor fullwidth"
							bind:value={editingContent}
							on:input={handleTextareaInput}
							placeholder="Enter your markdown content..."
							spellcheck="false"
						></textarea>
					{:else if currentTab === 'preview'}
						<div class="markdown-content preview" on:click={handleTermClick} on:keydown={handleKeydown} role="document" aria-label="Markdown preview with interactive highlights">
							{@html processedHtml}
						</div>
					{/if}
				</div>
			{/if}
		{:else}
			<!-- View Mode: Regular markdown display -->
			<div class="markdown-content" on:click={handleTermClick} on:keydown={handleKeydown} role="document" aria-label="Markdown content with interactive highlights">
				{@html processedHtml}
			</div>
		{/if}
	</div>
	
	<!-- Side Panel (same as before) -->
	{#if show_side_panel && selectedHighlight}
		<div class="side-panel" style="width: {panel_width}">
			<div class="panel-header">
				<h3>{selectedHighlight.title || selectedHighlight.term || 'Highlighted Text'}</h3>
				<button class="close-btn" on:click={closeSidePanel}>×</button>
			</div>
			<div class="panel-content">
				{#if selectedHighlight.category}
					<div class="category-badge" style="background-color: {selectedHighlight.color || '#e3f2fd'}">
						{selectedHighlight.category}
					</div>
				{/if}
				<div class="content-text">
					{@html panelContent}
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.markdown-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		position: relative;
		transition: all 0.3s ease;
	}

	.edit-controls {
		display: flex;
		gap: var(--spacing-sm);
		padding: var(--spacing-sm);
		background: var(--background-fill-secondary);
		border-bottom: 1px solid var(--border-color-primary);
		align-items: center;
	}

	.edit-btn, .save-btn, .cancel-btn {
		padding: var(--size-1) var(--size-2);
		border: 1px solid var(--border-color-primary);
		border-radius: var(--radius-sm);
		background: var(--background-fill-primary);
		cursor: pointer;
		font-size: var(--text-sm);
		transition: all 0.2s;
	}

	.edit-btn:hover {
		background: var(--background-fill-secondary);
	}

	.save-btn {
		background: var(--color-accent);
		color: white;
		border-color: var(--color-accent);
	}

	.save-btn:hover {
		opacity: 0.9;
	}

	.cancel-btn {
		background: var(--color-red-500);
		color: white;
		border-color: var(--color-red-500);
	}

	.cancel-btn:hover {
		opacity: 0.9;
	}

	.tab-controls {
		display: flex;
		gap: 2px;
		margin-left: auto;
	}

	.tab-btn {
		padding: var(--size-1) var(--size-3);
		border: 1px solid var(--border-color-primary);
		background: var(--background-fill-primary);
		cursor: pointer;
		font-size: var(--text-sm);
		border-radius: var(--radius-sm) var(--radius-sm) 0 0;
		transition: all 0.2s;
	}

	.tab-btn.active {
		background: var(--background-fill-secondary);
		border-bottom-color: var(--background-fill-secondary);
	}

	.tab-btn:hover:not(.active) {
		background: var(--background-fill-secondary);
		opacity: 0.7;
	}

	.copy-btn {
		padding: var(--size-1);
		border: 1px solid var(--border-color-primary);
		border-radius: var(--radius-sm);
		background: var(--background-fill-primary);
		cursor: pointer;
		transition: all 0.2s;
		margin-left: var(--spacing-sm);
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--body-text-color);
	}

	.copy-btn:hover {
		background: var(--background-fill-secondary);
		transform: scale(1.05);
	}

	.copy-btn:active {
		transform: scale(0.95);
	}


	.content-area {
		flex: 1;
		display: flex;
		overflow: hidden;
	}

	.content-area.split-mode {
		flex-direction: row;
	}

	.editor-section, .preview-section {
		flex: 1;
		display: flex;
		flex-direction: column;
		border-right: 1px solid var(--border-color-primary);
	}

	.preview-section {
		border-right: none;
		border-left: 1px solid var(--border-color-primary);
	}

	.editor-header, .preview-header {
		padding: var(--size-2);
		background: var(--background-fill-secondary);
		border-bottom: 1px solid var(--border-color-primary);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.editor-header h4, .preview-header h4 {
		margin: 0;
		font-size: var(--text-sm);
		font-weight: var(--weight-semibold);
		color: var(--body-text-color);
	}

	.markdown-editor {
		flex: 1;
		width: 100%;
		padding: var(--size-3);
		border: none;
		resize: none;
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		line-height: 1.5;
		background: var(--background-fill-primary);
		color: var(--body-text-color);
		outline: none;
	}

	.markdown-editor.fullwidth {
		height: 400px;
	}

	.tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.markdown-content {
		flex: 1;
		padding: var(--block-padding);
		overflow-y: auto;
		transition: margin-right 0.3s ease;
	}

	.markdown-content.preview {
		background: var(--background-fill-primary);
	}

	.with-panel .markdown-content {
		margin-right: var(--spacing-md);
	}

	.side-panel {
		position: fixed;
		top: 0;
		right: 0;
		height: 100vh;
		background: var(--background-fill-primary);
		border-left: 1px solid var(--border-color-primary);
		box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
		z-index: 1000;
		overflow-y: auto;
		transform: translateX(0);
		transition: transform 0.3s ease;
	}

	.panel-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--size-4);
		border-bottom: 1px solid var(--border-color-primary);
		background: var(--background-fill-secondary);
	}

	.panel-header h3 {
		margin: 0;
		font-size: var(--text-lg);
		font-weight: var(--weight-semibold);
		color: var(--body-text-color);
	}

	.close-btn {
		background: none;
		border: none;
		font-size: var(--text-xl);
		cursor: pointer;
		color: var(--body-text-color);
		padding: var(--size-1);
		border-radius: var(--radius-sm);
		transition: background-color 0.2s;
	}

	.close-btn:hover {
		background-color: var(--background-fill-primary);
	}

	.panel-content {
		padding: var(--size-4);
	}

	.category-badge {
		display: inline-block;
		padding: var(--size-1) var(--size-2);
		border-radius: var(--radius-full);
		font-size: var(--text-sm);
		font-weight: var(--weight-medium);
		margin-bottom: var(--size-3);
		color: var(--body-text-color);
	}

	.content-text {
		line-height: 1.6;
		color: var(--body-text-color);
	}

	/* Markdown styling (same as before) */
	.markdown-content :global(h1) {
		font-size: var(--text-2xl);
		font-weight: var(--weight-bold);
		margin: var(--size-4) 0 var(--size-2) 0;
		color: var(--body-text-color);
	}

	.markdown-content :global(h2) {
		font-size: var(--text-xl);
		font-weight: var(--weight-semibold);
		margin: var(--size-3) 0 var(--size-2) 0;
		color: var(--body-text-color);
	}

	.markdown-content :global(h3) {
		font-size: var(--text-lg);
		font-weight: var(--weight-medium);
		margin: var(--size-3) 0 var(--size-1) 0;
		color: var(--body-text-color);
	}

	.markdown-content :global(p) {
		margin: var(--size-2) 0;
		line-height: 1.6;
		color: var(--body-text-color);
	}

	.markdown-content :global(strong) {
		font-weight: var(--weight-bold);
	}

	.markdown-content :global(em) {
		font-style: italic;
	}

	.markdown-content :global(ul), .markdown-content :global(ol) {
		margin: var(--size-2) 0;
		padding-left: var(--size-4);
		color: var(--body-text-color);
	}

	.markdown-content :global(li) {
		margin: var(--size-1) 0;
	}

	.markdown-content :global(code) {
		background-color: var(--background-fill-secondary);
		padding: var(--size-1);
		border-radius: var(--radius-sm);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
	}

	.markdown-content :global(pre) {
		background-color: var(--background-fill-secondary);
		padding: var(--size-3);
		border-radius: var(--radius-md);
		overflow-x: auto;
		margin: var(--size-2) 0;
	}

	.markdown-content :global(pre code) {
		background: none;
		padding: 0;
	}

	.markdown-content :global(.highlight-term:hover),
	.markdown-content :global(.highlight-position:hover),
	.markdown-content :global(.highlight-term:focus),
	.markdown-content :global(.highlight-position:focus) {
		opacity: 0.8;
		transform: scale(1.02);
		outline: 2px solid var(--color-accent);
		outline-offset: 1px;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.side-panel {
			width: 100% !important;
		}
		
		.with-panel .markdown-content {
			margin-right: 0;
		}

		.content-area.split-mode {
			flex-direction: column;
		}

		.editor-section, .preview-section {
			border-right: none;
			border-bottom: 1px solid var(--border-color-primary);
		}

		.preview-section {
			border-left: none;
			border-top: 1px solid var(--border-color-primary);
		}
	}
</style>