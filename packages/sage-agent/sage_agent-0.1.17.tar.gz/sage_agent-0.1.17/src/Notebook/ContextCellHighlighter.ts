import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { NotebookContextManager } from './NotebookContextManager';
import { Cell } from '@jupyterlab/cells';
import { NotebookTools } from './NotebookTools';
import { NotebookDiffTools } from './NotebookDiffTools';

/**
 * Service that highlights cells that are in context
 * and provides UI to add/remove cells from context and quick generation
 */
export class ContextCellHighlighter {
  private notebookTracker: INotebookTracker;
  private notebookContextManager: NotebookContextManager;
  private notebookTools: NotebookTools;
  private highlightedCells: Map<string, Set<string>> = new Map(); // Map of notebook path to set of highlighted cell IDs
  private chatContainerRef: any = null; // Reference to chat container for updates
  private cellHistory: Map<string, string[]> = new Map(); // Map of cell tracking ID to array of content versions for undo
  private onPromptSubmit: (
    cell: Cell,
    prompt: string,
    mode: 'edit_selection' | 'edit_full_cell' | 'quick_question'
  ) => Promise<boolean>; // Callback for prompt submission

  constructor(
    notebookTracker: INotebookTracker,
    notebookContextManager: NotebookContextManager,
    notebookTools: NotebookTools,
    onPromptSubmit: (
      cell: Cell,
      prompt: string,
      mode: 'edit_selection' | 'edit_full_cell' | 'quick_question'
    ) => Promise<boolean>
  ) {
    this.notebookTracker = notebookTracker;
    this.notebookContextManager = notebookContextManager;
    this.notebookTools = notebookTools;
    this.onPromptSubmit = onPromptSubmit; // Store the callback

    // Add CSS for context highlighting
    this.addContextHighlightCSS();

    this.setupListeners();
  }

  private async handlePromptSubmit(
    cell: Cell,
    prompt: string,
    mode: 'edit_selection' | 'edit_full_cell' | 'quick_question'
  ) {
    if (prompt.trim()) {
      const inputContainer = <HTMLInputElement>(
        cell.node.querySelector('.sage-ai-prompt-input')
      );
      const errorMessage = <HTMLElement>(
        cell.node.querySelector('.sage-ai-quick-gen-prompt-error-message')
      );
      const submitButton = <HTMLButtonElement>(
        cell.node.querySelector('.sage-ai-quick-gen-submit')
      );
      const undoButton = <HTMLButtonElement>(
        cell.node.querySelector('.sage-ai-quick-gen-undo')
      );
      const loader = <HTMLElement>(
        cell.node.querySelector('.sage-ai-blob-loader')
      );

      // Get cell tracking ID for history
      const metadata: any = cell.model.sharedModel.getMetadata() || {};
      const trackingId = metadata.cell_tracker?.trackingId;

      // Save current content before making changes
      const originalContent = cell.model.sharedModel.getSource();
      if (trackingId) {
        if (!this.cellHistory.has(trackingId)) {
          this.cellHistory.set(trackingId, []);
        }
        this.cellHistory.get(trackingId)!.push(originalContent);
      }

      loader.style.display = 'block';
      submitButton.disabled = true;
      inputContainer.disabled = true;
      if (undoButton) undoButton.disabled = true;

      const successResult = await this.onPromptSubmit(cell, prompt, mode);

      loader.style.display = 'none';
      submitButton.disabled = false;
      inputContainer.disabled = false;

      if (successResult) {
        inputContainer.value = '';
        errorMessage.classList.add(
          'sage-ai-quick-gen-prompt-error-message-hidden'
        );

        // Get the new content after AI modification
        const newContent = cell.model.sharedModel.getSource();

        // Show diff view if content has changed
        if (originalContent !== newContent) {
          this.showDiffView(cell, originalContent, newContent);
        }

        // Update undo button state
        this.updateUndoButtonState(cell);
      } else {
        errorMessage.classList.remove(
          'sage-ai-quick-gen-prompt-error-message-hidden'
        );
        // Keep undo button disabled on failure
        if (undoButton) {
          undoButton.disabled = true;
        }
      }
    }
  }

  /**
   * Show diff view for a cell after AI modification
   */
  private showDiffView(
    cell: Cell,
    originalContent: string,
    newContent: string
  ): void {
    const inputContainer = <HTMLInputElement>(
      cell.node.querySelector('.sage-ai-prompt-input')
    );

    try {
      inputContainer.disabled = true;

      // Generate HTML diff using NotebookDiffTools
      const htmlDiff = NotebookDiffTools.generateHtmlDiff(
        originalContent,
        newContent,
        true
      );

      const editorSourceArea = <HTMLElement>(
        cell.node.querySelector('.cm-editor')
      );
      if (editorSourceArea) {
        editorSourceArea.classList.add('sage-ai-hide-editor');
      }

      // Create overlay container for the diff
      const overlayElement = document.createElement('div');
      overlayElement.className =
        'jp-DiffOverlay sage-ai-quick-gen-diff-overlay';
      overlayElement.style.minHeight = '40px';
      overlayElement.style.top = '0';
      overlayElement.style.left = '0';
      overlayElement.style.width = '100%';
      overlayElement.style.height = '100%';
      overlayElement.style.zIndex = '100';
      overlayElement.style.backgroundColor = 'var(--jp-layout-color0)';
      overlayElement.style.border = '2px solid #4CAF50';
      overlayElement.style.borderRadius = '4px';
      overlayElement.innerHTML = htmlDiff;

      // Add data attributes to identify this overlay
      overlayElement.dataset.cellId = cell.model.id;
      overlayElement.dataset.diffType = 'quick_gen';

      // Find the editor area
      const editorArea = cell.node.querySelector(
        '.jp-InputArea-editor'
      ) as HTMLElement;
      if (editorArea) {
        // Check if item has position set
        const itemPosition = window.getComputedStyle(editorArea).position;
        if (itemPosition === 'static') {
          editorArea.style.position = 'relative';
        }

        // Remove any existing diff overlays for this cell
        const existingOverlay = editorArea.querySelector(
          '.sage-ai-quick-gen-diff-overlay'
        );
        if (existingOverlay) {
          existingOverlay.remove();
        }

        // Append the overlay to the editor area
        editorArea.appendChild(overlayElement);

        // Add approve and reject buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.style.position = 'absolute';
        buttonContainer.style.top = '8px';
        buttonContainer.style.right = '8px';
        buttonContainer.style.zIndex = '101';
        buttonContainer.style.display = 'flex';
        buttonContainer.style.gap = '8px';

        const approveButton = document.createElement('button');
        approveButton.className = 'sage-ai-diff-approve-button';
        approveButton.innerHTML = '✓ Approve';
        approveButton.style.background = '#4CAF50';
        approveButton.style.color = 'white';
        approveButton.style.border = 'none';
        approveButton.style.borderRadius = '4px';
        approveButton.style.padding = '6px 12px';
        approveButton.style.cursor = 'pointer';
        approveButton.style.fontSize = '12px';
        approveButton.style.fontWeight = 'bold';

        const rejectButton = document.createElement('button');
        rejectButton.className = 'sage-ai-diff-reject-button';
        rejectButton.innerHTML = '✕ Reject';
        rejectButton.style.background = '#f44336';
        rejectButton.style.color = 'white';
        rejectButton.style.border = 'none';
        rejectButton.style.borderRadius = '4px';
        rejectButton.style.padding = '6px 12px';
        rejectButton.style.cursor = 'pointer';
        rejectButton.style.fontSize = '12px';
        rejectButton.style.fontWeight = 'bold';

        approveButton.addEventListener('click', () => {
          // Keep the new content (already applied by AI)
          overlayElement.remove();
          buttonContainer.remove();
          editorSourceArea.classList.remove('sage-ai-hide-editor');
          inputContainer.disabled = false;
        });

        rejectButton.addEventListener('click', () => {
          // Revert to original content
          cell.model.sharedModel.setSource(originalContent);
          overlayElement.remove();
          buttonContainer.remove();
          editorSourceArea.classList.remove('sage-ai-hide-editor');
          inputContainer.disabled = false;
        });

        buttonContainer.appendChild(approveButton);
        buttonContainer.appendChild(rejectButton);
        overlayElement.appendChild(buttonContainer);
      }
    } catch (error) {
      console.error('Error showing diff view:', error);
      inputContainer.disabled = false;
    }
  }

  /**
   * Set the chat container reference for updates
   */
  public setChatContainer(container: any): void {
    this.chatContainerRef = container;
  }

  /**
   * Handle undo functionality for a cell
   */
  private handleUndo(cell: Cell): void {
    const metadata: any = cell.model.sharedModel.getMetadata() || {};
    const trackingId = metadata.cell_tracker?.trackingId;

    if (trackingId && this.cellHistory.has(trackingId)) {
      const history = this.cellHistory.get(trackingId);
      if (history && history.length > 0) {
        // Get the most recent previous version
        const previousContent = history.pop()!;
        cell.model.sharedModel.setSource(previousContent);

        // Update undo button state
        this.updateUndoButtonState(cell);

        // Remove from history if empty
        if (history.length === 0) {
          this.cellHistory.delete(trackingId);
        }
      }
    }
  }

  /**
   * Clear history for a specific cell
   */
  private clearCellHistory(trackingId: string): void {
    this.cellHistory.delete(trackingId);
  }

  /**
   * Get the number of undo steps available for a cell
   */
  private getUndoStepsAvailable(trackingId: string): number {
    const history = this.cellHistory.get(trackingId);
    return history ? history.length : 0;
  }

  /**
   * Update undo button tooltip and state
   */
  private updateUndoButtonState(cell: Cell): void {
    const metadata: any = cell.model.sharedModel.getMetadata() || {};
    const trackingId = metadata.cell_tracker?.trackingId;
    const undoButton = <HTMLButtonElement>(
      cell.node.querySelector('.sage-ai-quick-gen-undo')
    );

    if (undoButton && trackingId) {
      const stepsAvailable = this.getUndoStepsAvailable(trackingId);
      undoButton.disabled = stepsAvailable === 0;
      undoButton.title =
        stepsAvailable > 0
          ? `Undo AI changes (${stepsAvailable} step${stepsAvailable > 1 ? 's' : ''} available)`
          : 'No AI changes to undo';
    }
  }

  /**
   * Set up event listeners for notebook changes
   */
  private setupListeners(): void {
    // Listen for active notebook changes
    this.notebookTracker.currentChanged.connect((_, notebook) => {
      if (notebook) {
        // Apply highlighting to the newly active notebook
        this.highlightContextCells(notebook);

        // Listen for changes in cells
        notebook.model?.cells.changed.connect(() => {
          this.refreshHighlighting(notebook);
        });
      }
    });

    // Initial highlight for the current notebook
    if (this.notebookTracker.currentWidget) {
      this.highlightContextCells(this.notebookTracker.currentWidget);
    }
  }

  /**
   * Refresh highlighting for a notebook
   */
  public refreshHighlighting(notebook: NotebookPanel): void {
    // Clear existing highlights for this notebook
    const notebookPath = notebook.context.path;
    this.highlightedCells.delete(notebookPath);

    // Apply highlighting again
    this.highlightContextCells(notebook);
  }

  /**
   * Add the CSS for context highlighting
   */
  private addContextHighlightCSS(): void {
    const style = document.createElement('style');
    style.id = 'sage-ai-context-highlight-style';
    style.textContent = `
      .sage-ai-in-context-cell {
        position: relative;
      }
      .sage-ai-cell-id-label {
        position: absolute;
        right: 8px;
        top: -8px;
        transform: translateY(-50%);
        background: #f2f7fd;
        color: #1976d2;
        border: 1px solid #dce5f2;
        border-radius: 4px;
        font-size: 10px;
        padding: 2px 6px;
        z-index: 101;
        pointer-events: none;
      }
      
      .sage-ai-context-indicator {
        position: absolute;
        left: -24px;
        top: 0;
        bottom: 0;
        width: 4px;
        background-color: #4CAF50;
        border-radius: 2px;
      }
      
      .sage-ai-context-badge {
        position: absolute;
        left: -80px;
        top: 50%;
        transform: translateY(-50%);
        background-color: #4CAF50;
        color: white;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 10px;
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s;
      }
      
      .sage-ai-in-context-cell:hover .sage-ai-context-badge {
        opacity: 1;
      }
      
      .sage-ai-context-buttons {
        position: absolute;
        top: 0px;
        left: 78px;
        transform: translateY(-100%);
        display: flex;
        gap: 8px;
        opacity: 1;
        z-index: 100;
      }
      
      .sage-ai-add-button, .sage-ai-remove-button {
        padding: 2px 8px;
        font-size: 10px;
        border-radius: 4px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
      }
      
      .sage-ai-add-button {
        background-color: #f2f7fd;
        color: #1976d2;
        border: 1px solid #dce5f2;
      }
      
      .sage-ai-add-button:hover {
        background-color: #e1f0ff;
        border-color: #a9c6e9;
      }
      
      .sage-ai-remove-button {
        background-color: #ffebee;
        color: #e53935;
        border: 1px solid #ffcdd2;
      }
      
      .sage-ai-remove-button:hover {
        background-color: #ffcdd2;
        border-color: #ef9a9a;
      }

      .sage-ai-quick-generation {
        display: flex;
        align-items: center;
        border: 0;
        cursor: pointer;
        font-size: 10px;
        background-color: #f2f7fd;
        color: #1976d2;
        border: 1px solid #dce5f2;
      }
      
      .sage-ai-quick-generation:hover {
        background-color: #e1f0ff;
        border-color: #a9c6e9;
      }

      .sage-ai-quick-generation-hidden {
        display: none !important;
      }
      
      .sage-ai-quick-gen-prompt-container {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        gap: 4px;
        flex: 1;
        padding: 6px;
      }

      .sage-ai-quick-gen-prompt-input-container {
        display: flex;
        flex-direction: column;
        gap: 4px;
        flex: 1;
      }

      .sage-ai-quick-gen-prompt-error-message {
        color: #f1625f;
        font-size: var(--jp-ui-font-size0);
        position: absolute;
        top: 29px;
        left: 91px;
      }

      .sage-ai-quick-gen-prompt-error-message-hidden {
        display: none;
      }

      .sage-ai-prompt-input {
        padding: 4px;
        margin: 0;
        min-height: 20px;
        width: 100%;
        border: 0;
        background-color: transparent;
        outline: 0;
      }

      .sage-ai-quick-gen-submit {
        background: transparent;
        border: 0;
        padding: 0;
        margin: 0;
      }

      .sage-ai-quick-gen-undo {
        background: transparent;
        border: 0;
        padding: 0;
        margin: 0;
        cursor: pointer;
        opacity: 0.5;
        transition: opacity 0.2s;
      }

      .sage-ai-quick-gen-undo:enabled {
        opacity: 1;
        cursor: pointer;
      }

      .sage-ai-quick-gen-undo:disabled {
        opacity: 0.3;
        cursor: not-allowed;
      }

      .sage-ai-quick-gen-cancel {
        color: #e7e7e7;
        font-size: 14px;
        cursor: pointer;
        line-height: 0;
      }

      .sage-ai-quick-gen-container {
        display: flex;
        flex-direction: column;
        flex: 1;
        border: var(--jp-border-width) solid var(--jp-cell-editor-border-color);
        background-color: var(--neutral-stroke-active);
      }

      .sage-ai-quick-gen-active .jp-InputArea-editor {
        border-top: var(--jp-border-width) solid var(--jp-cell-editor-border-color) !important; /* Use !important to override */
        border-left: 0 !important;
        border-right: 0 !important;
        border-bottom: 0 !important;
      }

      .sage-ai-quick-gen-active .jp-Toolbar {
        top: 39px !important; /* Use !important to override */
      }

      /* Reset toolbar position when quick gen is not active */
      .jp-Cell:not(.sage-ai-quick-gen-active) .jp-Toolbar {
          top: 0 !important; /* Ensure it resets */
      }

      .sage-ai-placeholder-quick-gen {
        color: #828282;
        position: absolute;
        bottom: 12px;
        left: 84px;
      }

      .sage-ai-placeholder-quick-gen-hidden {
        display: none;
      }

      .sage-ai-placeholder-quick-gen-button {
        display: inline-flex;
        align-items: center;
        gap: 2px;
        color: #1976D2 !important;
      }

      .sage-ai-placeholder-quick-gen-button:hover {
        cursor: pointer;
        color: rgb(19, 93, 167) !important;
      }

      .sage-ai-placeholder-quick-gen-button:hover svg {
        cursor: pointer;
        fill: rgb(19, 93, 167) !important;
      }
      
      .sage-ai-plan-label {
        border-color: #12ff00 !important;
      }

      .sage-ai-quick-gen-diff-overlay {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: opacity 0.3s ease;
      }

      .sage-ai-quick-gen-diff-overlay:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
      }

      .sage-ai-diff-approve-button:hover {
        background: #45a049 !important;
        transform: scale(1.05);
        transition: all 0.2s ease;
      }

      .sage-ai-diff-reject-button:hover {
        background: #d32f2f !important;
        transform: scale(1.05);
        transition: all 0.2s ease;
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Highlight cells that are in context for a specific notebook
   */
  private highlightContextCells(notebook: NotebookPanel): void {
    const notebookPath = notebook.context.path;
    if (!notebookPath) return;

    // Get all context cells for this notebook
    const contextCells =
      this.notebookContextManager.getContextCells(notebookPath);

    // Create a set to track highlighted cells
    const highlightedSet = new Set<string>();
    this.highlightedCells.set(notebookPath, highlightedSet);

    // Apply highlighting to each cell in the context
    for (const contextCell of contextCells) {
      // Find the cell based on its ID
      const cellId = contextCell.trackingId || contextCell.cellId;
      const cellInfo = this.notebookTools.findCellByAnyId(cellId, notebookPath);

      if (cellInfo) {
        this.highlightCell(cellInfo.cell, true);
        highlightedSet.add(cellId);
      }
    }

    // Add context buttons to all cells
    this.addContextButtonsToAllCells(notebook);
  }

  /**
   * Add context buttons to all cells in a notebook
   */
  public addContextButtonsToAllCells(notebook: NotebookPanel): void {
    const cells = notebook.content.widgets;
    const notebookPath = notebook.context.path;

    for (let i = 0; i < cells.length; i++) {
      const cell = cells[i];

      // Get tracking ID from metadata
      const metadata: any = cell.model.sharedModel.getMetadata() || {};
      const trackingId = metadata.cell_tracker?.trackingId;

      // Remove existing cell id label if any
      const existingIdLabel = cell.node.querySelector('.sage-ai-cell-id-label');
      if (existingIdLabel) existingIdLabel.remove();
      if (trackingId) {
        // Add cell id label to the right
        const idLabel = document.createElement('div');
        idLabel.setAttribute('sage-ai-cell-id', trackingId);
        idLabel.className = 'sage-ai-cell-id-label';
        if (trackingId === 'planning_cell')
          idLabel.className += ' sage-ai-plan-label';
        idLabel.textContent = trackingId;
        cell.node.appendChild(idLabel);

        // Check if this cell is in context
        const isInContext = this.notebookContextManager.isCellInContext(
          notebookPath,
          trackingId
        );

        // Add appropriate buttons based on context status
        this.addContextButtonsToCell(
          cell,
          trackingId,
          notebookPath,
          isInContext
        );
      }
    }
  }

  /**
   * Add context buttons to a single cell
   */
  private addContextButtonsToCell(
    cell: Cell,
    trackingId: string,
    notebookPath: string,
    isInContext: boolean
  ): void {
    // Remove existing buttons if any
    const existingButtons = cell.node.querySelector('.sage-ai-context-buttons');
    if (existingButtons) {
      existingButtons.remove();
    }

    // Create buttons container
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'sage-ai-context-buttons';

    if (isInContext) {
      // Create remove button if in context
      const removeButton = document.createElement('button');
      removeButton.className = 'sage-ai-remove-button';
      removeButton.textContent = 'Remove from Chat';
      removeButton.addEventListener('click', e => {
        e.stopPropagation();
        e.preventDefault();

        // Remove from context
        this.notebookContextManager.removeCellFromContext(
          notebookPath,
          trackingId
        );

        // Update the cell UI
        this.highlightCell(cell, false); // Immediately remove highlighting
        this.refreshHighlighting(this.notebookTracker.currentWidget!);

        // Update chat UI context counter
        if (this.chatContainerRef && !this.chatContainerRef.isDisposed) {
          this.chatContainerRef.onCellRemovedFromContext(
            notebookPath,
            trackingId
          );
        }
      });
      buttonsContainer.appendChild(removeButton);

      // Add the in-context class using classList
      cell.node.classList.add('sage-ai-in-context-cell');
    } else {
      // Create add button if not in context
      const addButton = document.createElement('button');
      addButton.className = 'sage-ai-add-button';
      addButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" height="12" width="12" viewBox="0 0 24 24">
          <path fill="#1976d2" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6z"/>
        </svg>
        Add to Context
      `;
      addButton.addEventListener('click', e => {
        e.stopPropagation();
        e.preventDefault();

        // Get cell content and metadata
        const cellContent = cell.model.sharedModel.getSource();
        const cellType = cell.model.type;

        // Add to context
        this.notebookContextManager.addCellToContext(
          notebookPath,
          trackingId,
          trackingId,
          cellContent,
          cellType
        );

        // Update the cell UI
        this.refreshHighlighting(this.notebookTracker.currentWidget!);

        // Update chat UI context counter
        if (this.chatContainerRef && !this.chatContainerRef.isDisposed) {
          this.chatContainerRef.onCellAddedToContext(notebookPath, trackingId);
        }
      });

      buttonsContainer.appendChild(addButton);

      // Remove the in-context class using classList
      cell.node.classList.remove('sage-ai-in-context-cell');
    }

    const quickGen = cell.node.querySelector('.sage-ai-quick-gen-container');
    if (!quickGen) {
      const generateWithSageButton = document.createElement('button');
      generateWithSageButton.className = 'sage-ai-quick-generation';
      generateWithSageButton.innerHTML = STAR_ICON;
      generateWithSageButton.append('Generate with Sage');
      buttonsContainer.appendChild(generateWithSageButton);

      if (!cell.model.sharedModel.source) {
        generateWithSageButton.classList.add('sage-ai-quick-generation-hidden');
      }

      // Add click event listener to the Generate with Sage button
      generateWithSageButton.addEventListener('click', () => {
        const isBoxOpened = cell.node.querySelector(
          '.sage-ai-quick-gen-prompt-container'
        );
        if (isBoxOpened) return;

        // Hide the buttons container
        generateWithSageButton.classList.add('sage-ai-quick-generation-hidden');

        // Create and style the textarea
        const quickGenContainer = document.createElement('div');
        quickGenContainer.className = 'sage-ai-quick-gen-prompt-container';

        // Create the select element
        const modeSelect = document.createElement('select');
        modeSelect.style.display = 'none';
        modeSelect.style.border = '0';
        modeSelect.style.backgroundColor = 'transparent';
        modeSelect.style.fontSize = 'var(--jp-ui-font-size1)';
        modeSelect.style.color = 'var(--jp-ui-font-color2)';
        modeSelect.id = 'sage-ai-auto-run-mode-select';
        modeSelect.className = 'sage-ai-auto-run-mode-checkbox';

        const loader = document.createElement('div');
        loader.className = 'sage-ai-blob-loader';
        loader.style.display = 'none';

        // Create the options
        const editSelectedCodeOption = document.createElement('option');
        editSelectedCodeOption.value = 'edit_selection';
        editSelectedCodeOption.textContent = 'Edit selection';

        const editFullCellOption = document.createElement('option');
        editFullCellOption.value = 'edit_full_cell';
        editFullCellOption.textContent = 'Edit full cell';

        const dontAskOption = document.createElement('option');
        dontAskOption.value = 'quick_question';
        dontAskOption.textContent = 'Quick question';

        // Set default selection
        modeSelect.value = 'edit_selection';

        modeSelect.appendChild(editSelectedCodeOption);
        modeSelect.appendChild(editFullCellOption);
        modeSelect.appendChild(dontAskOption);

        const inputContainer = document.createElement('div');
        inputContainer.className = 'sage-ai-quick-gen-prompt-input-container';

        const promptInput = document.createElement('input');
        promptInput.className = 'sage-ai-prompt-input';
        promptInput.placeholder = 'Prompt this cell with Sage';

        const errorMessage = document.createElement('span');
        errorMessage.className =
          'sage-ai-quick-gen-prompt-error-message sage-ai-quick-gen-prompt-error-message-hidden';
        errorMessage.textContent =
          'An unexpected error occurred, please try again.';

        inputContainer.append(promptInput, errorMessage);

        const cancelQuickGen = document.createElement('span');
        cancelQuickGen.className = 'sage-ai-quick-gen-cancel';
        cancelQuickGen.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px" viewBox="0 0 24 24">
          <path fill="#e7e7e7" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
      `;

        cancelQuickGen.addEventListener('click', () => {
          container.remove();
          cellInputArea?.appendChild(cellInputAreaEditor);
          buttonsContainer.classList.remove('sage-ai-buttons-hidden');
          cell.node.classList.remove('sage-ai-quick-gen-active');

          if (cell.model.sharedModel.source) {
            generateWithSageButton.classList.remove(
              'sage-ai-quick-generation-hidden'
            );
          }
        });

        const undoButton = document.createElement('button');
        undoButton.className = 'sage-ai-quick-gen-undo';
        undoButton.disabled = true; // Initially disabled
        undoButton.innerHTML = UNDO_ICON;
        undoButton.title = 'Undo AI changes';
        undoButton.addEventListener('click', () => {
          this.handleUndo(cell);
        });

        const submitButton = document.createElement('button');
        submitButton.className = 'sage-ai-quick-gen-submit';
        submitButton.style.cursor = 'pointer';
        submitButton.innerHTML =
          '<svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#e7e7e7"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g clip-path="url(#clip0_429_11126)"> <path d="M9 4.00018H19V18.0002C19 19.1048 18.1046 20.0002 17 20.0002H9" stroke="#e7e7e7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M12 15.0002L15 12.0002M15 12.0002L12 9.00018M15 12.0002H5" stroke="#e7e7e7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path> </g> <defs> <clipPath id="clip0_429_11126"> <rect width="24" height="24" fill="white"></rect> </clipPath> </defs> </g></svg>';

        submitButton.addEventListener('click', () => {
          void this.handlePromptSubmit(
            cell,
            promptInput.value,
            'edit_full_cell'
            // modeSelect.value as
            //   | 'edit_selection'
            //   | 'edit_full_cell'
            //   | 'quick_question'
          );
        });

        quickGenContainer.innerHTML = STAR_ICON;
        quickGenContainer.append(
          inputContainer,
          modeSelect,
          loader,
          undoButton,
          submitButton,
          cancelQuickGen
        );

        const container = document.createElement('div');
        container.className = 'sage-ai-quick-gen-container';

        const cellInputAreaEditor = <HTMLElement>(
          cell.node.querySelector('.jp-InputArea-editor')
        );
        if (!cellInputAreaEditor)
          throw "Unexpected error: Couldn't find the cell input area editor element";

        container.append(quickGenContainer, cellInputAreaEditor);

        const cellInputArea = cell.node.querySelector('.jp-InputArea');
        if (!cellInputArea)
          throw "Unexpected error: Couldn't find the cell input area element";

        cellInputArea.appendChild(container);

        // Add class to cell node to activate toolbar and editor styles
        cell.node.classList.add('sage-ai-quick-gen-active');

        // Focus the textarea
        promptInput.focus();

        // Add keydown listener for submission
        promptInput.addEventListener('keydown', event => {
          // Submit on Enter (without Shift)
          if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent newline
            void this.handlePromptSubmit(
              cell,
              promptInput.value,
              'edit_full_cell'
              // modeSelect.value as
              //   | 'edit_selection'
              //   | 'edit_full_cell'
              //   | 'quick_question'
            );
          }
        });
      });
    }

    // Add keydown listener to trigger quick generation on Cmd+K
    cell.node.addEventListener('keydown', event => {
      // Check if the cell is focused and Cmd+K is pressed
      if (
        cell.node.classList.contains('jp-mod-active') &&
        (event.metaKey || event.ctrlKey) &&
        event.key === 'k'
      ) {
        event.preventDefault(); // Prevent default browser shortcut

        // Find the generate button and trigger its click event
        const generateButton = cell.node.querySelector(
          '.sage-ai-quick-generation'
        ) as HTMLButtonElement;
        if (
          generateButton &&
          !generateButton.classList.contains('sage-ai-quick-generation-hidden')
        ) {
          generateButton.click();
        }
      }
    });

    try {
      this.createCellPlaceholder(cell);
      this.cellPlaceholderListener(cell);
    } catch (e) {
      console.error(`Couldn't setup placeholder: ${e}`);
    }

    // Add buttons to cell
    cell.node.appendChild(buttonsContainer);
  }

  private cellPlaceholderListener(cell: Cell) {
    cell.model.contentChanged.connect(ev => {
      const sageEditButton = cell.node.querySelector(
        '.sage-ai-quick-generation'
      );
      const hasContent = ev.sharedModel.source;
      const placeholder = <HTMLElement>(
        cell.node.querySelector('.sage-ai-placeholder-quick-gen')
      );
      const isPlaceholderHidden = placeholder?.classList.contains(
        'sage-ai-placeholder-quick-gen-hidden'
      );

      if (!hasContent && isPlaceholderHidden) {
        placeholder?.classList.remove('sage-ai-placeholder-quick-gen-hidden');
        sageEditButton?.classList.add('sage-ai-quick-generation-hidden');
        return;
      }

      if (hasContent) {
        placeholder?.classList.add('sage-ai-placeholder-quick-gen-hidden');
        sageEditButton?.classList.remove('sage-ai-quick-generation-hidden');
        return;
      }
    });
  }

  private createCellPlaceholder(cell: Cell) {
    const placeholder = cell.node.querySelector(
      '.sage-ai-placeholder-quick-gen'
    );
    if (placeholder) return;

    const placeholderQuickGen = document.createElement('span');
    placeholderQuickGen.className = 'sage-ai-placeholder-quick-gen';
    if (cell.model.sharedModel.source) {
      placeholderQuickGen.classList.add('sage-ai-placeholder-quick-gen-hidden');
    }
    const quickGenButton = document.createElement('a');
    quickGenButton.className = 'sage-ai-placeholder-quick-gen-button';
    quickGenButton.textContent = 'Generate with Sage';
    quickGenButton.innerHTML += STAR_ICON;
    placeholderQuickGen.textContent = 'Start coding or ';
    placeholderQuickGen.append(quickGenButton);

    quickGenButton.addEventListener('click', ev => {
      ev.stopPropagation();
      const generateWithSageButton = <HTMLElement>(
        cell.node.querySelector('.sage-ai-quick-generation')
      );
      const isOpen = cell.node.querySelector(
        '.sage-ai-quick-gen-prompt-container'
      );
      if (generateWithSageButton && !isOpen) {
        generateWithSageButton.click();
      }
    });

    placeholderQuickGen.addEventListener('click', () => {
      const editor = <HTMLElement>cell.node.querySelector('.cm-content');
      editor?.focus();
    });

    cell.node.append(placeholderQuickGen);
  }

  /**
   * Highlight a cell to indicate it's in context
   */
  private highlightCell(cell: Cell, isInContext: boolean): void {
    // Remove existing highlighting
    cell.node.classList.remove('sage-ai-in-context-cell');
    const existingIndicator = cell.node.querySelector(
      '.sage-ai-context-indicator'
    );
    if (existingIndicator) {
      existingIndicator.remove();
    }

    const existingBadge = cell.node.querySelector('.sage-ai-context-badge');
    if (existingBadge) {
      existingBadge.remove();
    }

    if (isInContext) {
      // Add the highlighting class
      cell.node.classList.add('sage-ai-in-context-cell');

      // Create and add the indicator
      const indicator = document.createElement('div');
      indicator.className = 'sage-ai-context-indicator';
      cell.node.appendChild(indicator);

      // Create and add the badge
      const badge = document.createElement('div');
      badge.className = 'sage-ai-context-badge';
      badge.textContent = 'In Context';
      cell.node.appendChild(badge);
    }
  }
}

const STAR_ICON = `
      <svg fill="#1976d2" width="14px" height="14px" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
      // <title></title><g data-name="Layer 2" id="Layer_2">
      // <path d="M18,11a1,1,0,0,1-1,1,5,5,0,0,0-5,5,1,1,0,0,1-2,0,5,5,0,0,0-5-5,1,1,0,0,1,0-2,5,5,0,0,0,5-5,1,1,0,0,1,2,0,5,5,0,0,0,5,5A1,1,0,0,1,18,11Z"></path>
      // <path d="M19,24a1,1,0,0,1-1,1,2,2,0,0,0-2,2,1,1,0,0,1-2,0,2,2,0,0,0-2-2,1,1,0,0,1,0-2,2,2,0,0,0,2-2,1,1,0,0,1,2,0,2,2,0,0,0,2,2A1,1,0,0,1,19,24Z"></path><path d="M28,17a1,1,0,0,1-1,1,4,4,0,0,0-4,4,1,1,0,0,1-2,0,4,4,0,0,0-4-4,1,1,0,0,1,0-2,4,4,0,0,0,4-4,1,1,0,0,1,2,0,4,4,0,0,0,4,4A1,1,0,0,1,28,17Z"></path></g></svg>
    `;

const UNDO_ICON = `
      <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#e7e7e7">
        <path d="M3 7v6h6" stroke="#e7e7e7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13" stroke="#e7e7e7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `;
