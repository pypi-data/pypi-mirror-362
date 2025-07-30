/**
 * Class to handle the mention dropdown functionality in the chat input
 */
import { Contents, KernelMessage } from '@jupyterlab/services';
// Remove textarea-caret import since it doesn't work with contentEditable
import { ToolService } from '../Services/ToolService';

export interface MentionContext {
  type: 'rules' | 'data' | 'variable' | 'cell';
  id: string;
  name: string;
  content?: string;
  description?: string;
}

const VARIABLE_TYPE_BLACKLIST = [
  'module',
  'type',
  'function',
  'ZMQExitAutocall',
  'method'
];

const VARIABLE_NAME_BLACKLIST = ['In', 'Out'];

export class ChatMentionDropdown {
  private dropdownElement: HTMLDivElement;
  private chatInput: HTMLElement; // Changed from HTMLTextAreaElement to HTMLElement
  private toolService: ToolService;
  private isVisible: boolean = false;
  private mentionTrigger: string = '@';
  private currentMentionStart: number = -1;
  private currentMentionText: string = '';
  private contentManager: Contents.IManager;
  private onContextSelected: ((context: MentionContext) => void) | null = null;

  // Navigation state
  private currentView: 'categories' | 'items' = 'categories';
  private selectedCategory: string | null = null;
  private selectedIndex: number = 0;

  // Categories and their items
  private categories = [
    {
      id: 'rules',
      name: 'Rules',
      icon: '📄',
      description: 'Reusable prompt templates'
    },
    {
      id: 'data',
      name: 'Data',
      icon: '📊',
      description: 'Dataset references and info'
    },
    {
      id: 'variables',
      name: 'Variables',
      icon: '🔤',
      description: 'Code variables and values'
    },
    {
      id: 'cells',
      name: 'Cells',
      icon: '📝',
      description: 'Notebook cell references'
    }
  ];

  private contextItems: Map<string, MentionContext[]> = new Map();

  constructor(
    chatInput: HTMLElement, // Changed from HTMLTextAreaElement to HTMLElement
    parentElement: HTMLElement,
    contentManager: Contents.IManager,
    toolService: ToolService
  ) {
    this.chatInput = chatInput;
    this.contentManager = contentManager;
    this.toolService = toolService;

    // Create dropdown element
    this.dropdownElement = document.createElement('div');
    this.dropdownElement.className = 'sage-ai-mention-dropdown';
    parentElement.appendChild(this.dropdownElement);

    // Set up event listeners
    this.setupEventListeners();

    // Initialize context items for each category
    this.initializeContextItems();
  }

  /**
   * Set a callback to be invoked when a context item is selected
   */
  public setContextSelectedCallback(
    callback: (context: MentionContext) => void
  ): void {
    this.onContextSelected = callback;
  }

  /**
   * Initialize context items for each category
   */
  private async initializeContextItems(): Promise<void> {
    // Initialize empty maps for each category
    this.contextItems.set('rules', []);
    this.contextItems.set('data', [
      {
        type: 'data',
        id: 'demo-dataset',
        name: 'demo-dataset',
        description: 'Sample dataset for demonstration',
        content: 'This is a demo dataset context'
      }
    ]);
    this.contextItems.set('variables', [
      {
        type: 'variable',
        id: 'demo-var',
        name: 'demo_variable',
        description: 'Sample variable for demonstration',
        content: 'x = 42  # Demo variable'
      }
    ]);
    this.contextItems.set('cells', [
      {
        type: 'cell',
        id: 'demo-cell',
        name: 'Cell 1',
        description: 'Sample cell for demonstration',
        content: 'print("Hello from demo cell")'
      }
    ]);

    console.log(
      'All context items after initialization:',
      Array.from(this.contextItems.entries())
    ); // Debug log
  }

  private async loadDatasets(): Promise<void> {
    try {
      const datasets = await this.contentManager.get('./data');
      console.log('Loaded datasets:', datasets); // Debug log

      if (datasets.content && Array.isArray(datasets.content)) {
        const datasetContexts: MentionContext[] = await Promise.all(
          datasets.content
            .filter(file => file.type === 'file')
            .map(async file => {
              // remove everything from the last dot to the end (e.g. ".json", ".csv", ".txt", etc.)
              const name = file.name.replace(/\.[^/.]+$/, '');

              const content = await this.contentManager.get(
                './data/' + file.name
              );

              const contentString = `${content.content}`;

              return {
                type: 'data' as const,
                id: file.path,
                name,
                description: 'Dataset file',
                content: contentString.slice(0, 1000)
              };
            })
        );

        this.contextItems.set('data', datasetContexts);
      }
    } catch (error) {
      console.error('Error loading datasets:', error);
      this.contextItems.set('data', []);
    }
  }

  private async loadCells(): Promise<void> {
    console.log('Loading cells... ======================');
    const notebook = this.toolService.getCurrentNotebook();
    if (!notebook) {
      console.warn('No notebook available');
      return;
    }
    const cellContexts: MentionContext[] = [];
    const cells = notebook.widget.model.cells as any;

    for (const cell of cells) {
      console.log('Cell:', cell); // Debug log
      console.log('Cell metadata:', cell.metadata); // Debug log

      const tracker = cell.metadata.cell_tracker;
      if (tracker) {
        cellContexts.push({
          type: 'cell',
          id: tracker.trackingId,
          name: tracker.trackingId,
          description: '',
          content: cell.sharedModel.getSource()
        });
      }
    }

    this.contextItems.set('cells', cellContexts);

    console.log('CELL LOADING, cells:', cells); // Debug log
  }

  private async loadVariables(): Promise<void> {
    console.log('Loading variables... ======================');
    const kernel = this.toolService.getCurrentNotebook()?.kernel;
    if (!kernel) {
      console.warn('No kernel available');
      return;
    }

    // This Python snippet builds a dict of { varName: { type: ..., value: ... } }
    // and prints it as one JSON string.
    const code = `
      import json
      
      def to_jsonable(v):
          # Primitive types → leave as-is
          if isinstance(v, (int, float, str, bool, type(None))):
              return v
          # Lists/tuples → recursively convert
          if isinstance(v, (list, tuple)):
              return [to_jsonable(x) for x in v]
          # Dicts → recursively convert
          if isinstance(v, dict):
              return {k: to_jsonable(val) for k, val in v.items()}
          # Fallback → string repr
          return repr(v)
      
      data = {
          name: {
              "type": type(val).__name__,
              "value": to_jsonable(val)
          }
          for name, val in globals().items()
          if not name.startswith('_')
      }
      
      # Print as a single JSON blob
      print(json.dumps(data))
      `;

    // Buffer to accumulate the printed JSON
    let buffer = '';

    // Send execute request
    const future = kernel.requestExecute({ code });

    future.onIOPub = (msg: KernelMessage.IIOPubMessage) => {
      const msgType = msg.header.msg_type;
      if (msgType === 'stream') {
        // stdout comes in as a stream msg
        const text = (msg as KernelMessage.IStreamMsg).content.text;
        buffer += text;
      } else if (msgType === 'error') {
        // handle any Python exceptions
        const err = (msg as KernelMessage.IErrorMsg).content;
        console.error('Error fetching variables:', err.ename, err.evalue);
      }
    };

    future.done.then(() => {
      // Once execution is finished, try to parse the accumulated buffer
      try {
        const varsWithTypes = JSON.parse(buffer);
        console.log('Variables with types and values:', varsWithTypes);
        const variableContexts: MentionContext[] = [];
        for (const varName of Object.keys(varsWithTypes)) {
          if (VARIABLE_NAME_BLACKLIST.includes(varName)) continue;
          if (VARIABLE_TYPE_BLACKLIST.includes(varsWithTypes[varName].type))
            continue;

          variableContexts.push({
            type: 'variable',
            id: varName,
            name: varName,
            description: varsWithTypes[varName].type,
            content: varsWithTypes[varName].value
          });
        }
        this.contextItems.set('variables', variableContexts);
      } catch (e) {
        console.error('Failed to parse JSON output:', buffer, e);
      }
    });
  }

  private async loadTemplateFiles(): Promise<void> {
    try {
      const files = await this.contentManager.get('./templates');

      if (files.content && Array.isArray(files.content)) {
        const templateContexts: MentionContext[] = files.content
          .filter(
            file => file.type === 'file' && file.name !== 'rule.example.md'
          )
          .map(file => {
            const displayName = file.name
              .replace(/^rule\./, '')
              .replace(/\.md$/, '');

            return {
              type: 'rules' as const,
              id: file.path,
              name: displayName,
              description: 'Rule file'
            };
          });

        this.contextItems.set('rules', templateContexts);
      }
    } catch (error) {
      console.error('Error loading template files:', error);
      this.contextItems.set('rules', []);
    }
  }

  /**
   * Set up event listeners for detecting @ mentions and handling selection
   */
  private setupEventListeners(): void {
    // Listen for input to detect @ character and filter dropdown
    this.chatInput.addEventListener('input', this.handleInput);

    // Listen for keydown to handle navigation and selection
    this.chatInput.addEventListener('keydown', this.handleKeyDown);

    // Close dropdown when clicking outside
    document.addEventListener('click', event => {
      if (
        !this.dropdownElement.contains(event.target as Node) &&
        event.target !== this.chatInput
      ) {
        this.hideDropdown();
      }
    });

    // Handle clicks on dropdown items
    this.dropdownElement.addEventListener('click', this.handleDropdownClick);
  }

  /**
   * Handle input events to detect @ mentions and update dropdown
   */
  private handleInput = (event: Event): void => {
    const cursorPosition = this.getSelectionStart();
    const inputValue = this.getInputValue();

    // Check if we're currently in a mention context
    if (this.isVisible) {
      // Check if cursor moved outside of the current mention
      if (
        cursorPosition < this.currentMentionStart ||
        !inputValue
          .substring(this.currentMentionStart, cursorPosition)
          .startsWith(this.mentionTrigger)
      ) {
        this.hideDropdown();
        return;
      }

      // Update the current mention text
      this.currentMentionText = inputValue.substring(
        this.currentMentionStart + 1,
        cursorPosition
      );
      this.renderDropdown(this.currentMentionText);
      return;
    }

    // Look for a new mention
    if (inputValue.charAt(cursorPosition - 1) === this.mentionTrigger) {
      // Found a new mention
      this.currentMentionStart = cursorPosition - 1;
      this.currentMentionText = '';
      this.showDropdown();
    }
  };

  /**
   * Get the current selection start position
   */
  private getSelectionStart(): number {
    if (this.isTextArea()) {
      return (this.chatInput as HTMLTextAreaElement).selectionStart || 0;
    } else {
      // Handle contentEditable div
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return 0;

      const range = selection.getRangeAt(0);
      const preCaretRange = range.cloneRange();
      preCaretRange.selectNodeContents(this.chatInput);
      preCaretRange.setEnd(range.startContainer, range.startOffset);

      return preCaretRange.toString().length;
    }
  }

  /**
   * Get the current input value
   */
  private getInputValue(): string {
    if (this.isTextArea()) {
      return (this.chatInput as HTMLTextAreaElement).value || '';
    } else {
      return this.chatInput.textContent || '';
    }
  }

  /**
   * Set the input value
   */
  private setInputValue(value: string): void {
    if (this.isTextArea()) {
      (this.chatInput as HTMLTextAreaElement).value = value;
    } else {
      this.chatInput.textContent = value;
    }
  }

  /**
   * Set selection range
   */
  private setSelectionRange(start: number, end: number): void {
    if (this.isTextArea()) {
      const textarea = this.chatInput as HTMLTextAreaElement;
      textarea.setSelectionRange(start, end);
    } else {
      // Handle contentEditable div
      const selection = window.getSelection();
      if (!selection) return;

      const range = this.createRangeFromOffsets(start, end);
      if (range) {
        selection.removeAllRanges();
        selection.addRange(range);
      }
    }
  }

  /**
   * Create a range from character offsets for contentEditable elements
   */
  private createRangeFromOffsets(
    startOffset: number,
    endOffset: number
  ): Range | null {
    const walker = document.createTreeWalker(
      this.chatInput,
      NodeFilter.SHOW_TEXT
    );

    let currentOffset = 0;
    let startNode: Node | null = null;
    let startPos = 0;
    let endNode: Node | null = null;
    let endPos = 0;

    while (walker.nextNode()) {
      const node = walker.currentNode;
      const nodeLength = node.textContent?.length || 0;

      if (!startNode && currentOffset + nodeLength >= startOffset) {
        startNode = node;
        startPos = startOffset - currentOffset;
      }

      if (currentOffset + nodeLength >= endOffset) {
        endNode = node;
        endPos = endOffset - currentOffset;
        break;
      }

      currentOffset += nodeLength;
    }

    if (startNode && endNode) {
      const range = document.createRange();
      range.setStart(
        startNode,
        Math.min(startPos, startNode.textContent?.length || 0)
      );
      range.setEnd(endNode, Math.min(endPos, endNode.textContent?.length || 0));
      return range;
    }

    return null;
  }

  /**
   * Check if the input is a textarea
   */
  private isTextArea(): boolean {
    return this.chatInput.tagName.toLowerCase() === 'textarea';
  }

  /**
   * Get caret coordinates for positioning the dropdown
   */
  private getCaretCoordinates(): { top: number; left: number; height: number } {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      return { top: 0, left: 0, height: 20 };
    }

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    const elementRect = this.chatInput.getBoundingClientRect();

    return {
      top: rect.top - elementRect.top,
      left: rect.left - elementRect.left,
      height: rect.height || 20
    };
  }

  /**
   * Position the dropdown relative to the current cursor position
   */
  private positionDropdown(): void {
    if (!this.isVisible) return;

    const coords = this.getCaretCoordinates();
    console.log('Caret coordinates:', coords); // Debug log

    let top = coords.top;
    let left = coords.left;

    // Invalid
    if (left < 0) return;
    if (top < 0) return;

    this.dropdownElement.style.position = 'fixed'; // Changed to fixed for better positioning
    this.dropdownElement.style.left = `${left}px`;
    this.dropdownElement.style.zIndex = '9999';
    this.dropdownElement.style.maxHeight = '300px';
    this.dropdownElement.style.transform = 'translateY(-100%) translateY(-8px)';
    this.dropdownElement.style.marginBottom = '12px';

    // Adjust if overflowing viewport
    const rect = this.dropdownElement.getBoundingClientRect();

    // amount overflowing bottom
    const overflowY = rect.bottom - window.innerHeight;
    if (overflowY + 30 > 0) {
      this.dropdownElement.style.maxHeight = `${this.dropdownElement.clientHeight - (overflowY + 30)}px`;
    }

    // amount overflowing right
    const overflowX = rect.right - window.innerWidth;
    if (overflowX + 20 > 0) {
      this.dropdownElement.style.left = `${left - this.dropdownElement.clientWidth - 64}px`;
    }
  }

  /**
   * Render the dropdown based on current view and search text
   */
  private renderDropdown(searchText: string): void {
    this.dropdownElement.innerHTML = '';

    if (this.currentView === 'categories') {
      // If there's search text, show matching items first
      if (searchText && searchText.length > 0) {
        const hasMatchingItems = this.renderMatchingItems(searchText);
        
        // Only show categories if we don't have good matches or search is very short
        if (!hasMatchingItems || searchText.length < 2) {
          // Add a separator if we have matching items
          if (hasMatchingItems) {
            const separator = document.createElement('div');
            separator.className = 'sage-ai-mention-separator';
            separator.textContent = 'Categories';
            this.dropdownElement.appendChild(separator);
          }
          this.renderCategories();
        }
      } else {
        // No search text, just show categories
        this.renderCategories();
      }
    } else if (this.currentView === 'items' && this.selectedCategory) {
      // Show items in the category with filtering if there's search text
      this.renderCategoryItems(this.selectedCategory, searchText);
    }

    // Reset to first item and highlight it
    this.selectedIndex = 0;
    this.highlightItem(this.selectedIndex);
    this.positionDropdown();
  }

  /**
   * Calculate a relevance score for an item based on search text
   */
  private calculateRelevanceScore(item: MentionContext, searchText: string): number {
    const itemName = item.name.toLowerCase();
    const search = searchText.toLowerCase();
    
    if (!search) return 0;
    
    // Exact match gets highest score
    if (itemName === search) return 1000;
    
    // Starts with search text gets high score
    if (itemName.startsWith(search)) return 900;
    
    // Word boundary match (after space, underscore, etc.)
    const wordBoundaryRegex = new RegExp(`\\b${search}`, 'i');
    if (wordBoundaryRegex.test(itemName)) return 800;
    
    // Contains search text gets medium score
    if (itemName.includes(search)) return 700;
    
    // Fuzzy match - calculate based on character matches in order
    let fuzzyScore = 0;
    let searchIndex = 0;
    for (let i = 0; i < itemName.length && searchIndex < search.length; i++) {
      if (itemName[i] === search[searchIndex]) {
        fuzzyScore += 10;
        searchIndex++;
      }
    }
    
    // Only return fuzzy score if we matched all search characters
    if (searchIndex === search.length) {
      return 500 + fuzzyScore;
    }
    
    return 0;
  }

  /**
   * Render items that match the search text across all categories
   * @returns true if matching items were found and rendered, false otherwise
   */
  private renderMatchingItems(searchText: string): boolean {
    const matchingItems: Array<{item: MentionContext, score: number}> = [];

    // Collect matching items from all categories with scores
    for (const [categoryId, items] of this.contextItems.entries()) {
      for (const item of items) {
        const score = this.calculateRelevanceScore(item, searchText);
        if (score > 0) {
          matchingItems.push({item, score});
        }
      }
    }

    // Sort by score (highest first), then by name
    matchingItems.sort((a, b) => {
      if (a.score !== b.score) {
        return b.score - a.score;
      }
      return a.item.name.localeCompare(b.item.name);
    });

    if (matchingItems.length > 0) {
      // Limit to maximum 5 matching items for better selection
      matchingItems.slice(0, 5).forEach(({item}) => {
        const itemElement = document.createElement('div');
        itemElement.className =
          'sage-ai-mention-item sage-ai-mention-subcategory';
        itemElement.setAttribute('data-id', item.id);
        itemElement.setAttribute('data-type', item.type);
        itemElement.setAttribute(
          'data-category',
          this.getCategoryForType(item.type)
        );

        const iconElement = document.createElement('span');
        iconElement.className = 'sage-ai-mention-item-icon';
        iconElement.textContent = this.getIconForType(item.type);

        const textContainer = document.createElement('div');
        textContainer.style.flex = '1';

        const textElement = document.createElement('div');
        textElement.className = 'sage-ai-mention-item-text';
        textElement.textContent = item.name;

        textContainer.appendChild(textElement);

        if (item.description) {
          const descElement = document.createElement('div');
          descElement.className = 'sage-ai-mention-item-description';
          descElement.textContent = item.description;
          textContainer.appendChild(descElement);
        }

        itemElement.appendChild(iconElement);
        itemElement.appendChild(textContainer);
        this.dropdownElement.appendChild(itemElement);
      });
      
      return true;
    }
    
    return false;
  }

  /**
   * Get category ID for a given item type
   */
  private getCategoryForType(type: string): string {
    switch (type) {
      case 'rules':
        return 'rules';
      case 'data':
        return 'data';
      case 'variable':
        return 'variables';
      case 'cell':
        return 'cells';
      default:
        return '';
    }
  }

  /**
   * Render the categories view
   */
  private renderCategories(): void {
    this.categories.forEach(category => {
      const itemElement = document.createElement('div');
      itemElement.className =
        'sage-ai-mention-item sage-ai-mention-category-main';
      itemElement.setAttribute('data-category', category.id);

      const iconElement = document.createElement('span');
      iconElement.className = 'sage-ai-mention-item-icon';
      iconElement.textContent = category.icon;

      const textContainer = document.createElement('div');
      textContainer.style.flex = '1';

      const textElement = document.createElement('div');
      textElement.className = 'sage-ai-mention-item-text';
      textElement.textContent = category.name;

      textContainer.appendChild(textElement);

      itemElement.appendChild(iconElement);
      itemElement.appendChild(textContainer);
      this.dropdownElement.appendChild(itemElement);
    });
  }

  /**
   * Render items for a specific category
   */
  private renderCategoryItems(categoryId: string, searchText: string = ''): void {
    // Add back button
    const backButton = document.createElement('div');
    backButton.className = 'sage-ai-mention-back-button';
    backButton.innerHTML = '← Back to Categories';
    this.dropdownElement.appendChild(backButton);

    const items = this.contextItems.get(categoryId) || [];
    console.log(`Rendering items for category ${categoryId}:`, items); // Debug log

    if (items.length === 0) {
      const emptyElement = document.createElement('div');
      emptyElement.className = 'sage-ai-mention-empty';

      let emptyMessage = 'No items found';
      switch (categoryId) {
        case 'data':
          emptyMessage =
            'No datasets available. Add datasets to reference them here.';
          break;
        case 'variables':
          emptyMessage =
            'No variables available. Define variables in your notebook to reference them here.';
          break;
        case 'cells':
          emptyMessage =
            'No cells available. Create cells in your notebook to reference them here.';
          break;
        case 'rules':
          emptyMessage =
            'No rules available. Create template files in the templates/ directory.';
          break;
      }

      emptyElement.textContent = emptyMessage;
      this.dropdownElement.appendChild(emptyElement);
      return;
    }

    // Filter and sort items based on search text
    let displayItems = items;
    if (searchText) {
      const matchingItems: Array<{item: MentionContext, score: number}> = [];
      
      for (const item of items) {
        const score = this.calculateRelevanceScore(item, searchText);
        if (score > 0) {
          matchingItems.push({item, score});
        }
      }
      
      // Sort by score (highest first)
      matchingItems.sort((a, b) => {
        if (a.score !== b.score) {
          return b.score - a.score;
        }
        return a.item.name.localeCompare(b.item.name);
      });
      
      displayItems = matchingItems.map(({item}) => item);
    }

    // Show filtered/sorted items
    displayItems.forEach(item => {
      const itemElement = document.createElement('div');
      itemElement.className =
        'sage-ai-mention-item sage-ai-mention-subcategory';
      itemElement.setAttribute('data-id', item.id);
      itemElement.setAttribute('data-type', item.type);

      const iconElement = document.createElement('span');
      iconElement.className = 'sage-ai-mention-item-icon';
      iconElement.textContent = this.getIconForType(item.type);

      const textContainer = document.createElement('div');
      textContainer.style.flex = '1';

      const textElement = document.createElement('div');
      textElement.className = 'sage-ai-mention-item-text';
      textElement.textContent = item.name;

      textContainer.appendChild(textElement);

      if (item.description) {
        const descElement = document.createElement('div');
        descElement.className = 'sage-ai-mention-item-description';
        descElement.textContent = item.description;
        textContainer.appendChild(descElement);
      }

      itemElement.appendChild(iconElement);
      itemElement.appendChild(textContainer);
      this.dropdownElement.appendChild(itemElement);
    });
  }

  /**
   * Get icon for context type
   */
  private getIconForType(type: string): string {
    switch (type) {
      case 'rules':
        return '📄';
      case 'data':
        return '📊';
      case 'variable':
        return '🔤';
      case 'cell':
        return '📝';
      default:
        return '❓';
    }
  }

  /**
   * Handle clicks on dropdown items
   */
  private handleDropdownClick = (event: Event): void => {
    event.preventDefault();
    event.stopPropagation();

    const target = event.target as Element;

    // Handle back button
    if (target.closest('.sage-ai-mention-back-button')) {
      this.currentView = 'categories';
      this.selectedCategory = null;
      this.renderDropdown(this.currentMentionText);
      this.positionDropdown();
      return;
    }

    // Handle category selection
    const categoryItem = target.closest('.sage-ai-mention-category-main');
    if (categoryItem) {
      const categoryId = categoryItem.getAttribute('data-category');
      if (categoryId) {
        this.selectedCategory = categoryId;
        this.currentView = 'items';
        this.renderDropdown(this.currentMentionText); // Pass current search text
        this.positionDropdown(); // Reposition after content change
      }
      return;
    }

    // Handle item selection
    const mentionItem = target.closest('.sage-ai-mention-subcategory');
    if (mentionItem) {
      const itemId = mentionItem.getAttribute('data-id');
      const categoryId = mentionItem.getAttribute('data-category');

      if (itemId) {
        // If we're selecting from the matching items section and have a category
        if (this.currentView === 'categories' && categoryId) {
          this.selectedCategory = categoryId;
        }

        this.selectItem(itemId);
      }
    }
  };

  /**
   * Highlight a specific item in the dropdown
   */
  private highlightItem(index: number): void {
    // Remove active class from all items
    const items = this.dropdownElement.querySelectorAll(
      '.sage-ai-mention-item, .sage-ai-mention-subcategory, .sage-ai-mention-back-button'
    );
    items.forEach(item => item.classList.remove('active'));

    // Add active class to the specified item
    if (items.length > 0 && index >= 0 && index < items.length) {
      items[index].classList.add('active');

      // Scroll to the item if needed
      const itemElement = items[index] as HTMLElement;
      const dropdownRect = this.dropdownElement.getBoundingClientRect();
      const itemRect = itemElement.getBoundingClientRect();

      if (itemRect.bottom > dropdownRect.bottom) {
        this.dropdownElement.scrollTop += itemRect.bottom - dropdownRect.bottom;
      } else if (itemRect.top < dropdownRect.top) {
        this.dropdownElement.scrollTop -= dropdownRect.top - itemRect.top;
      }
    }
  }

  /**
   * Select an item from the dropdown and insert it into the input
   */
  private async selectItem(itemId: string): Promise<void> {
    // Find the selected item
    const categoryItems = this.contextItems.get(this.selectedCategory!) || [];
    const selectedItem = categoryItems.find(item => item.id === itemId);

    if (!selectedItem) return;

    // Replace the mention with the selected item
    const beforeMention = this.getInputValue().substring(
      0,
      this.currentMentionStart
    );
    const afterMention = this.getInputValue().substring(
      this.getSelectionStart()
    );

    // Format: @{item name}
    const replacement = `@${selectedItem.name} `;

    // Update the input value
    this.setInputValue(beforeMention + replacement + afterMention);

    // Set cursor position after the inserted mention
    const newCursorPosition = this.currentMentionStart + replacement.length;
    this.setSelectionRange(newCursorPosition, newCursorPosition);

    // Hide the dropdown
    this.hideDropdown();

    // Focus the input
    this.chatInput.focus();

    // Load content if needed and invoke callback
    if (this.onContextSelected) {
      let contextWithContent = { ...selectedItem };

      if (selectedItem.type === 'rules' && !selectedItem.content) {
        contextWithContent.content = await this.loadTemplateContent(
          selectedItem.id
        );
      }

      this.onContextSelected(contextWithContent);
    }
  }

  /**
   * Load the content of a template file
   */
  public async loadTemplateContent(filePath: string): Promise<string> {
    try {
      const file = await this.contentManager.get(filePath, { content: true });
      if (file.content) {
        return typeof file.content === 'string'
          ? file.content
          : JSON.stringify(file.content);
      }
      return '';
    } catch (error) {
      console.error(`Error loading template file ${filePath}:`, error);
      return '';
    }
  }

  /**
   * Show the dropdown
   */
  async showDropdown() {
    this.isVisible = true;
    this.currentView = 'categories';
    this.selectedCategory = null;
    this.selectedIndex = 0;
    this.dropdownElement.classList.add('visible');

    // Load templates
    await this.loadTemplateFiles();
    await this.loadDatasets();
    await this.loadVariables();
    await this.loadCells();

    this.positionDropdown();
    this.renderDropdown('');
  }

  /**
   * Hide the dropdown
   */
  hideDropdown(): void {
    this.isVisible = false;
    this.dropdownElement.classList.remove('visible');
    this.currentMentionStart = -1;
    this.currentMentionText = '';
    this.currentView = 'categories';
    this.selectedCategory = null;
  }

  /**
   * Handle keydown events for navigation and selection
   */
  private handleKeyDown = (event: KeyboardEvent): void => {
    if (!this.isVisible) return;

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        this.navigateDropdown('down');
        break;
      case 'ArrowUp':
        event.preventDefault();
        this.navigateDropdown('up');
        break;
      case 'Tab':
        event.preventDefault();
        this.selectCurrentItem();
        break;
      case 'Enter':
        event.preventDefault();
        this.selectCurrentItem();
        break;
      case 'Escape':
        event.preventDefault();
        this.hideDropdown();
        break;
    }
  };

  /**
   * Navigate through dropdown items
   */
  private navigateDropdown(direction: 'up' | 'down'): void {
    const items = this.dropdownElement.querySelectorAll(
      '.sage-ai-mention-item, .sage-ai-mention-subcategory, .sage-ai-mention-back-button'
    );

    if (items.length === 0) return;

    if (direction === 'down') {
      this.selectedIndex = (this.selectedIndex + 1) % items.length;
    } else {
      this.selectedIndex = this.selectedIndex <= 0 ? items.length - 1 : this.selectedIndex - 1;
    }

    this.highlightItem(this.selectedIndex);
  }

  /**
   * Select the currently highlighted item
   */
  private selectCurrentItem(): void {
    const items = this.dropdownElement.querySelectorAll(
      '.sage-ai-mention-item, .sage-ai-mention-subcategory, .sage-ai-mention-back-button'
    );

    if (items.length === 0 || this.selectedIndex < 0 || this.selectedIndex >= items.length) {
      return;
    }

    const selectedElement = items[this.selectedIndex] as HTMLElement;

    // Handle back button
    if (selectedElement.classList.contains('sage-ai-mention-back-button')) {
      this.currentView = 'categories';
      this.selectedCategory = null;
      this.selectedIndex = 0;
      this.renderDropdown(this.currentMentionText);
      this.positionDropdown();
      return;
    }

    // Handle category selection
    if (selectedElement.classList.contains('sage-ai-mention-category-main')) {
      const categoryId = selectedElement.getAttribute('data-category');
      if (categoryId) {
        this.selectedCategory = categoryId;
        this.currentView = 'items';
        this.selectedIndex = 0;
        this.renderDropdown(this.currentMentionText);
        this.positionDropdown();
      }
      return;
    }

    // Handle item selection
    if (selectedElement.classList.contains('sage-ai-mention-subcategory')) {
      const itemId = selectedElement.getAttribute('data-id');
      const categoryId = selectedElement.getAttribute('data-category');

      if (itemId) {
        // If we're selecting from the matching items section and have a category
        if (this.currentView === 'categories' && categoryId) {
          this.selectedCategory = categoryId;
        }

        this.selectItem(itemId);
      }
    }
  }

  /**
   * Trigger selection of the currently highlighted item (public method)
   */
  public selectHighlightedItem(): void {
    this.selectCurrentItem();
  }

  /**
   * Get the best matching item for autocomplete
   */
  public getBestMatch(): string | null {
    if (!this.isVisible) return null;

    // If we have items and a selected index, use the currently highlighted item
    const items = this.dropdownElement.querySelectorAll(
      '.sage-ai-mention-subcategory'
    );

    if (items.length > 0 && this.selectedIndex >= 0) {
      // Find the subcategory item at the selected index
      const allItems = this.dropdownElement.querySelectorAll(
        '.sage-ai-mention-item, .sage-ai-mention-subcategory, .sage-ai-mention-back-button'
      );
      
      if (allItems[this.selectedIndex] && allItems[this.selectedIndex].classList.contains('sage-ai-mention-subcategory')) {
        const itemId = allItems[this.selectedIndex].getAttribute('data-id');
        if (itemId) {
          // Find the item by ID
          for (const [categoryId, categoryItems] of this.contextItems.entries()) {
            const item = categoryItems.find(item => item.id === itemId);
            if (item) return item.name;
          }
        }
      }
    }

    // Fallback: find best match based on search text
    if (!this.currentMentionText) {
      // No search text, try to get the first available item
      for (const [categoryId, items] of this.contextItems.entries()) {
        if (items.length > 0) return items[0].name;
      }
      return null;
    }

    // Get all available items with scores based on current view
    const matchingItems: Array<{item: MentionContext, score: number}> = [];

    if (this.currentView === 'categories') {
      // Check for direct matches in items across all categories
      for (const [categoryId, items] of this.contextItems.entries()) {
        for (const item of items) {
          const score = this.calculateRelevanceScore(item, this.currentMentionText);
          if (score > 0) {
            matchingItems.push({item, score});
          }
        }
      }
    } else if (this.currentView === 'items' && this.selectedCategory) {
      const items = this.contextItems.get(this.selectedCategory) || [];
      for (const item of items) {
        const score = this.calculateRelevanceScore(item, this.currentMentionText);
        if (score > 0) {
          matchingItems.push({item, score});
        }
      }
    }

    // Sort by score (highest first)
    matchingItems.sort((a, b) => {
      if (a.score !== b.score) {
        return b.score - a.score;
      }
      return a.item.name.localeCompare(b.item.name);
    });
    
    return matchingItems.length > 0 ? matchingItems[0].item.name : null;
  }

  /**
   * Check if dropdown is visible (public method)
   */
  public getIsVisible(): boolean {
    return this.isVisible;
  }
}
