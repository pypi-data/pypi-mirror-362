import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import {
  ICommandPalette,
  IToolbarWidgetRegistry,
  WidgetTracker
} from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ToolService } from './Services/ToolService';
import { ConfigService, IConfig } from './Config/ConfigService';
import { NotebookTools } from './Notebook/NotebookTools';
import { ActionHistory } from './Chat/ActionHistory';
import { NotebookDiffManager } from './Notebook/NotebookDiffManager';
import { CellTrackingService } from './CellTrackingService';
import { TrackingIDUtility } from './TrackingIDUtility';
import { NotebookChatContainer } from './Notebook/NotebookChatContainer';
import { NotebookContextManager } from './Notebook/NotebookContextManager';
import { addIcon } from '@jupyterlab/ui-components';
import { ContextCellHighlighter } from './Notebook/ContextCellHighlighter';
import { AppStateService } from './AppState';
import { NotebookSettingsContainer } from './NotebookSettingsContainer';
import { AnthropicService } from './Services/AnthropicService';
import { Widget } from '@lumino/widgets';
import { PlanStateDisplay } from './Components/PlanStateDisplay';
import { WaitingUserReplyBoxManager } from './Notebook/WaitingUserReplyBoxManager';
import { registerCommands } from './commands';
import { registerEvalCommands } from './eval_commands';
import { IThemeManager } from '@jupyterlab/apputils';
import { NotebookDiffTools } from './Notebook/NotebookDiffTools';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { ListModel } from '@jupyterlab/extensionmanager';
import { CachingService, SETTING_KEYS } from './utils/caching';
import { StateDBCachingService } from './utils/stateDBCaching';
import { IStateDB } from '@jupyterlab/statedb';

// TypeScript interfaces for edit_selection operations
interface EditOperation {
  line: number;
  action: 'KEEP' | 'MODIFY' | 'REMOVE' | 'INSERT';
  content: string;
}

interface EditSelectionResponse {
  operations: EditOperation[];
}

const THEME_FLAG_KEY = 'darkThemeApplied';

/**
 * Initialization data for the sage-ai extension.
 */
export const plugin: JupyterFrontEndPlugin<void> = {
  id: 'sage-agent:plugin',
  description: 'Sage AI - Your AI Data Partner',
  autoStart: true,
  requires: [INotebookTracker, ICommandPalette, IThemeManager, IStateDB],
  optional: [ISettingRegistry, IToolbarWidgetRegistry],
  activate: (
    app: JupyterFrontEnd,
    notebooks: INotebookTracker,
    palette: ICommandPalette,
    themeManager: IThemeManager,
    db: IStateDB,
    settingRegistry: ISettingRegistry | null,
    toolbarRegistry: IToolbarWidgetRegistry | null
  ) => {
    console.log('JupyterLab extension sage-agent is activated!');

    // Initialize the caching service with settings registry
    CachingService.initialize(settingRegistry);

    // Initialize the state database caching service for chat histories
    StateDBCachingService.initialize(db);

    const moveToChatHistory = async () => {
      console.log('MOVING ALL SETTINGS TO THE STATE DB');
      const oldHistories = await CachingService.getSetting(
        SETTING_KEYS.CHAT_HISTORIES,
        {}
      );
      if (oldHistories && Object.keys(oldHistories).length > 0) {
        await StateDBCachingService.setValue(
          SETTING_KEYS.CHAT_HISTORIES,
          oldHistories
        );
        console.log('SUCCESSFULLY MOVED ALL SETTINGS TO THE STATE DB');

        await CachingService.setSetting(SETTING_KEYS.CHAT_HISTORIES, {});
      }
    };

    moveToChatHistory();

    // Store settings registry in AppState
    AppStateService.setSettingsRegistry(settingRegistry);

    const loadSettingsRegistry = async () => {
      if (!settingRegistry) return;
      const settings = await settingRegistry.load(plugin.id);
    };

    const serviceManager = app.serviceManager;

    const extensions = new ListModel(serviceManager as any);

    // Store extensions in AppState for UpdateBanner to use
    AppStateService.setExtensions(extensions);

    const contentManager = app.serviceManager.contents;

    // Replace localStorage with settings registry for theme flag
    const checkAndSetTheme = async () => {
      const alreadySet = await CachingService.getBooleanSetting(
        SETTING_KEYS.DARK_THEME_APPLIED,
        false
      );
      if (!alreadySet) {
        console.log('Setting theme to JupyterLab Dark (first time)');
        themeManager.setTheme('JupyterLab Dark');
        await CachingService.setBooleanSetting(
          SETTING_KEYS.DARK_THEME_APPLIED,
          true
        );
      }
    };
    checkAndSetTheme();

    // Ensure 'templates' directory exists and create 'rule.default.md' if missing
    const ensureTemplatesDirAndFile = async () => {
      try {
        // Check if 'templates' directory exists
        let dirExists = false;
        try {
          const dir = await contentManager.get('templates');
          dirExists = dir.type === 'directory';
        } catch (e) {
          dirExists = false;
        }
        if (!dirExists) {
          // Create untitled directory, then rename to 'templates'
          const untitledDir = await contentManager.newUntitled({
            type: 'directory',
            path: ''
          });
          await contentManager.rename(untitledDir.path, 'templates');
          console.log("Created 'templates' directory.");
        }
        // Check if 'rule.default.md' exists
        let fileExists = false;
        try {
          await contentManager.get('templates/rule.example.md');
          fileExists = true;
        } catch (e) {
          fileExists = false;
        }
        if (!fileExists) {
          await contentManager.save('templates/rule.example.md', {
            type: 'file',
            format: 'text',
            content:
              '# EXAMPLE TEMPLATE FILE\n' +
              '\n' +
              '# Description: \n' +
              'When called, look into the requested function or codeblock and see if you find any parallelizale code. You can use the following embarringly parallel code template to speed up those function computations\n' +
              '\n' +
              '# Code:\n' +
              '```python\n' +
              'from joblib import Parallel, delayed\n' +
              '\n' +
              'def run_in_batches(fn_name):\n' +
              '    tickers = get_sp500_tickers()\n' +
              '    \n' +
              '    # Process in smaller batches to control memory usage\n' +
              '    results = Parallel(\n' +
              '        n_jobs=-1, \n' +
              '        batch_size=10,  # Process 10 items per batch\n' +
              "        backend='multiprocessing'\n" +
              '    )(delayed(test_ticket)(ticker) for ticker in tickers)\n' +
              '    \n' +
              '    return dict(zip(tickers, results))\n' +
              '```'
          });
          console.log(
            "Created 'templates/rule.default.md' with placeholder content."
          );
        }
      } catch (err) {
        console.error(
          'Error ensuring templates directory and rule.default.md:',
          err
        );
      }
    };
    ensureTemplatesDirAndFile();

    // Load settings if available
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('Loaded settings for sage-agent');
          const defaultService = settings.get('defaultService')
            .composite as string;
          // Store the default service in ConfigService
          if (defaultService) {
            ConfigService.setActiveModelType(defaultService);
          }

          // Watch for setting changes
          settings.changed.connect(() => {
            const newDefaultService = settings.get('defaultService')
              .composite as string;
            ConfigService.setActiveModelType(newDefaultService);
            console.log(`Default service changed to ${newDefaultService}`);
          });
        })
        .catch(error => {
          console.error('Failed to load settings for sage-agent', error);
        });
    }

    // Create a shared ToolService instance that has access to the notebook context
    const toolService = new ToolService();

    const planStateDisplay = new PlanStateDisplay();
    const waitingUserReplyBoxManager = new WaitingUserReplyBoxManager();

    // Set the notebook tracker in the tool service
    toolService.setNotebookTracker(notebooks, waitingUserReplyBoxManager);

    // Set the content manager in the tool service
    toolService.setContentManager(contentManager);

    // Initialize NotebookContextManager with the shared tool service
    const notebookContextManager = new NotebookContextManager(toolService);

    // Set the context manager in the tool service
    toolService.setContextManager(notebookContextManager);

    // Initialize action history
    const actionHistory = new ActionHistory();

    // Initialize NotebookTools
    const notebookTools = new NotebookTools(
      notebooks,
      waitingUserReplyBoxManager
    );

    // Initialize the AppState with core services
    AppStateService.initializeCoreServices(
      toolService,
      notebooks,
      notebookTools,
      notebookContextManager,
      contentManager,
      settingRegistry
    );

    // Initialize managers in AppState
    AppStateService.initializeManagers(
      planStateDisplay,
      waitingUserReplyBoxManager
    );

    // Initialize additional services
    AppStateService.initializeAdditionalServices(
      actionHistory,
      new CellTrackingService(notebookTools, notebooks),
      new TrackingIDUtility(notebooks),
      new ContextCellHighlighter(
        notebooks,
        notebookContextManager,
        notebookTools,
        async (
          cell,
          promptText,
          mode: 'edit_selection' | 'edit_full_cell' | 'quick_question'
        ): Promise<boolean> => {
          // This is the callback executed when a prompt is submitted from the quick generation input
          console.log(
            'Prompt submitted for cell',
            (cell as any).model?.id || cell.id,
            'in mode',
            mode,
            ':',
            promptText
          );

          // Get the cell ID (use tracking ID if available, fallback to model.id or id)
          const cellId =
            (cell as any).model?.sharedModel.getMetadata()?.cell_tracker
              ?.trackingId ||
            (cell as any).model?.id ||
            (cell as any).id ||
            '[unknown]';

          if (cellId === '[unknown]') {
            console.error(
              'Could not determine cell ID for prompt submission.',
              cell
            );
            return false;
          }

          const activeCell = notebooks.activeCell;
          if (!activeCell) {
            console.warn('No active cell');
            return false;
          }

          const editor = activeCell.editor;
          const selection = editor?.getSelection();
          const selectedText = editor?.model.sharedModel.source.substring(
            editor.getOffsetAt(selection?.start || { line: 0, column: 0 }),
            editor.getOffsetAt(selection?.end || { line: 0, column: 0 })
          );

          // For edit_selection, get the selected line range
          const startLine = selection?.start?.line || 0;
          const endLine = selection?.end?.line || 0;
          const cellLines = editor?.model.sharedModel.source.split('\n') || [];
          const selectedLines = cellLines.slice(startLine, endLine + 1);

          const config = AppStateService.getConfig();

          // Determine which config section to use based on mode
          let modeConfig;
          let modeLabel;
          switch (mode) {
            case 'edit_selection':
              modeConfig = config.edit_selection;
              modeLabel = 'edit_selection';
              break;
            case 'edit_full_cell':
              modeConfig = config.edit_full_cell;
              modeLabel = 'edit_full_cell';
              break;
            case 'quick_question':
              modeConfig = config.quick_question;
              modeLabel = 'quick_question';
              break;
            default:
              // fallback to quick_edit as a default
              modeConfig = config.quick_edit;
              modeLabel = 'quick_edit';
          }

          const systemPrompt = modeConfig.system_prompt;

          // Use ephemeral API call instead of chatbox for faster response
          try {
            const targetCell = notebookTools.findCellByTrackingId(cellId);
            const cellContent = targetCell?.cell.model.sharedModel.getSource();
            const previousCellContent = notebookTools
              .findCellByIndex((targetCell?.index || 0) - 1)
              ?.cell?.model?.sharedModel.getSource();

            // Compose enhanced context messages based on mode
            let contextMessage = '';

            if (mode === 'edit_selection') {
              if (selectedText && selectedText.trim()) {
                // Create line-numbered cell content for the selection range
                const selectionRangeLines = selectedLines
                  .map((line, index) => {
                    const lineNum = index + 1;
                    return `${lineNum.toString().padStart(3, ' ')}: ${line}`;
                  })
                  .join('\n');

                contextMessage = `${promptText}

EDIT SELECTION MODE: Edit the selected lines (${startLine + 1}-${endLine + 1}) using structured operations.

SELECTED LINES TO EDIT (${startLine + 1}-${endLine + 1}):
\`\`\`
${selectionRangeLines}
\`\`\`

Return a JSON object with operations for each line in the selection range. Use KEEP, MODIFY, REMOVE, or INSERT actions.`;
              } else {
                contextMessage = `${promptText}
                      EDIT SELECTION MODE: No text is currently selected. 

                      COMPLETE CELL CONTENT:
                      \`\`\`
                      ${cellContent}
                      \`\`\`

                      Please select specific code before using edit selection mode, or use edit full cell mode instead.`;
              }
            } else if (mode === 'edit_full_cell') {
              contextMessage = `${promptText}
                  EDIT FULL CELL MODE: Edit and improve the complete cell.

                  CELL TO EDIT:
                  \`\`\`
                  ${cellContent}
                  \`\`\`

                  PREVIOUS CELL CONTENT:
                  \`\`\`
                  ${previousCellContent}
                  \`\`\`

                  Return only the fully edited cell. Apply your quantitative expertise to improve the code.`;
            } else if (mode === 'quick_question') {
              contextMessage = `${promptText}
                    QUICK QUESTION MODE: Answer the question without generating any code.

                    ${
                      selectedText && selectedText.trim()
                        ? `SELECTED CODE REFERENCE:
                    \`\`\`
                    ${selectedText}
                    \`\`\`

                    `
                        : ''
                    }CELL CONTENT FOR REFERENCE:
                    \`\`\`
                    ${cellContent}
                    \`\`\`

                    Provide explanations and insights only. Do not generate any code.`;
            }

            const chatService = AppStateService.getChatService();

            // Handle streaming based on mode
            if (mode === 'edit_selection') {
              // For edit_selection, use structured JSON operations
              const targetCell = notebookTools.findCellByTrackingId(cellId);
              if (!targetCell) {
                throw new Error(`Could not find cell with ID ${cellId}`);
              }

              const response = await chatService.sendEphemeralMessage(
                contextMessage,
                systemPrompt,
                'claude-3-5-haiku-latest'
              );

              // Parse the JSON response
              try {
                let jsonResponse: EditSelectionResponse | null = null;
                if (response.includes('```json')) {
                  const jsonMatch = response.match(/```json\s*([\s\S]*?)```/);
                  if (jsonMatch) {
                    jsonResponse = JSON.parse(jsonMatch[1].trim());
                  }
                } else if (response.includes('```')) {
                  const jsonMatch = response.match(/```\s*([\s\S]*?)```/);
                  if (jsonMatch) {
                    jsonResponse = JSON.parse(jsonMatch[1].trim());
                  }
                } else {
                  jsonResponse = JSON.parse(response.trim());
                }

                if (
                  jsonResponse &&
                  jsonResponse.operations &&
                  Array.isArray(jsonResponse.operations)
                ) {
                  // Apply the operations to the cell
                  const updatedCellLines = [...cellLines];
                  let lineOffset = 0; // Track line shifts due to INSERT/REMOVE operations

                  // Sort operations by line number to process in order
                  const sortedOperations = jsonResponse.operations.sort(
                    (a: EditOperation, b: EditOperation) => a.line - b.line
                  );

                  for (const operation of sortedOperations) {
                    const actualLineIndex =
                      startLine + operation.line - 1 + lineOffset;

                    switch (operation.action) {
                      case 'KEEP':
                        // Do nothing - line stays as is
                        break;
                      case 'MODIFY':
                        if (actualLineIndex < updatedCellLines.length) {
                          updatedCellLines[actualLineIndex] = operation.content;
                        }
                        break;
                      case 'REMOVE':
                        if (actualLineIndex < updatedCellLines.length) {
                          updatedCellLines.splice(actualLineIndex, 1);
                          lineOffset--; // Adjust for removed line
                        }
                        break;
                      case 'INSERT':
                        if (actualLineIndex <= updatedCellLines.length) {
                          updatedCellLines.splice(
                            actualLineIndex,
                            0,
                            operation.content
                          );
                          lineOffset++; // Adjust for inserted line
                        }
                        break;
                      default:
                        console.warn(
                          `Unknown operation action: ${operation.action}`
                        );
                    }
                  }

                  // Apply the changes
                  targetCell.cell.model.sharedModel.setSource(
                    updatedCellLines.join('\n')
                  );
                  console.log(
                    `Applied edit_selection operations to lines ${startLine + 1}-${endLine + 1} in cell ${cellId}`
                  );
                } else {
                  throw new Error('Invalid JSON response structure');
                }
              } catch (error) {
                console.error(
                  'Failed to parse edit_selection response:',
                  error
                );
                console.error('Raw response:', response);
                alert(
                  `Error processing edit_selection: Invalid response format. Please try again.`
                );
                return false;
              }
            } else if (mode === 'edit_full_cell') {
              // For edit_full_cell, keep the original behavior
              const targetCell = notebookTools.findCellByTrackingId(cellId);
              if (!targetCell) {
                throw new Error(`Could not find cell with ID ${cellId}`);
              }

              let accumulatedResponse = '';
              let codeContent = '';
              let isInCodeBlock = false;
              let codeBlockStartPattern = /```(?:python|py)?\s*/i;
              let codeBlockEndPattern = /```/;

              const response = await chatService.sendEphemeralMessage(
                contextMessage,
                systemPrompt,
                'claude-3-5-haiku-latest',
                (textChunk: string) => {
                  accumulatedResponse += textChunk;

                  // Handle code extraction for streaming
                  if (!isInCodeBlock) {
                    const startMatch = accumulatedResponse.match(
                      codeBlockStartPattern
                    );
                    if (startMatch) {
                      isInCodeBlock = true;
                      // Remove everything up to and including the code block start (and any language specifier)
                      codeContent = accumulatedResponse.substring(
                        accumulatedResponse.indexOf(startMatch[0]) +
                          startMatch[0].length
                      );
                      // Remove any leading 'python' or 'py' line if present
                      codeContent = codeContent.replace(
                        /^\s*(python|py)\s*\n?/i,
                        ''
                      );
                    } else {
                      // Not in code block, just accumulate
                      codeContent = accumulatedResponse;
                    }
                  } else {
                    // Already in code block
                    if (codeBlockEndPattern.test(textChunk)) {
                      isInCodeBlock = false;
                      // Remove trailing ```
                      const endIndex = codeContent.lastIndexOf('```');
                      if (endIndex !== -1) {
                        codeContent = codeContent.substring(0, endIndex);
                      }
                      // Remove any trailing 'python' or 'py' line if present
                      codeContent = codeContent.replace(
                        /^\s*(python|py)\s*\n?/i,
                        ''
                      );
                    } else {
                      codeContent += textChunk;
                    }
                  }

                  // Create progressive transformation effect
                  if (codeContent.includes('\n')) {
                    const newCodeLines = codeContent.split('\n');

                    // Progressive replacement: mix old and new code
                    const displayLines = [...cellLines];

                    // Replace lines progressively based on how much new content we have
                    const linesToReplace = Math.min(
                      newCodeLines.length,
                      cellLines.length
                    );

                    for (let i = 0; i < linesToReplace; i++) {
                      if (newCodeLines[i] !== undefined) {
                        displayLines[i] = newCodeLines[i];
                      }
                    }

                    // If new code has more lines than original, add them
                    if (newCodeLines.length > cellLines.length) {
                      for (
                        let i = cellLines.length;
                        i < newCodeLines.length;
                        i++
                      ) {
                        if (newCodeLines[i] !== undefined) {
                          displayLines.push(newCodeLines[i]);
                        }
                      }
                    }

                    // Update cell with the progressive transformation
                    targetCell.cell.model.sharedModel.setSource(
                      displayLines.join('\n')
                    );
                  } else if (
                    codeContent.trim() &&
                    !codeContent.includes('\n')
                  ) {
                    // Handle single line updates by replacing first line progressively
                    const displayLines = [...cellLines];
                    if (displayLines.length > 0) {
                      displayLines[0] = codeContent.trim();
                    } else {
                      displayLines.push(codeContent.trim());
                    }
                    targetCell.cell.model.sharedModel.setSource(
                      displayLines.join('\n')
                    );
                  }
                }
              );

              // Final cleanup and application for full cell mode
              let finalCode = codeContent.trim();
              if (!finalCode && response.trim()) {
                if (response.includes('```')) {
                  const codeMatch = response.match(
                    /```(?:python|py)?\s*([\s\S]*?)```/i
                  );
                  if (codeMatch) {
                    finalCode = codeMatch[1]
                      .replace(/^\s*(python|py)\s*\n?/i, '')
                      .trim();
                  }
                } else {
                  finalCode = response.trim();
                }
              } else if (finalCode) {
                // Remove any leading/trailing code block markers and 'python' lines
                finalCode = finalCode
                  .replace(/^```(?:python|py)?\s*/i, '')
                  .replace(/```$/, '')
                  .replace(/^\s*(python|py)\s*\n?/i, '')
                  .trim();
              }

              // Always commit the last codeContent to the cell, even if not updated in the last chunk
              if (finalCode) {
                targetCell.cell.model.sharedModel.setSource(finalCode);
                console.log(
                  `Applied edit_full_cell response to cell ${cellId} with progressive transformation`
                );
              }
            } else if (mode === 'quick_question') {
              // For questions, create a temporary notification area
              let responseText = '';
              const notificationId = `question-response-${Date.now()}`;

              // Create a simple notification element
              const notification = document.createElement('div');
              notification.id = notificationId;
              notification.style.cssText = `
                  position: fixed;
                  top: 20px;
                  right: 20px;
                  max-width: 400px;
                  padding: 16px;
                  background: var(--jp-layout-color1);
                  border: 1px solid var(--jp-border-color1);
                  border-radius: 8px;
                  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                  z-index: 10000;
                  font-family: var(--jp-ui-font-family);
                  font-size: var(--jp-ui-font-size1);
                  color: var(--jp-ui-font-color1);
                  white-space: pre-wrap;
                  overflow-wrap: break-word;
                `;
              notification.innerHTML =
                '<strong>AI Response:</strong><br/><span class="response-content">Thinking...</span>';
              document.body.appendChild(notification);

              const responseContent = notification.querySelector(
                '.response-content'
              ) as HTMLElement;

              const response = await chatService.sendEphemeralMessage(
                contextMessage,
                systemPrompt,
                'claude-3-5-haiku-latest',
                (textChunk: string) => {
                  responseText += textChunk;
                  if (responseContent) {
                    responseContent.textContent = responseText;
                  }
                }
              );

              // Auto-remove notification after 10 seconds
              setTimeout(() => {
                const element = document.getElementById(notificationId);
                if (element) {
                  element.remove();
                }
              }, 10000);

              console.log(`Quick Question Response:`, response);
            }

            console.log(
              `Ephemeral ${modeLabel} request completed using Haiku model.`
            );

            return true;
          } catch (error) {
            const errorMessage =
              error instanceof Error ? error.message : String(error);
            console.error(`Failed to process: ${errorMessage}`, error);
            return false;
          }
        }
      )
    );

    // Initialize CellTrackingService - now retrieved from AppState
    const cellTrackingService = AppStateService.getCellTrackingService();

    // Initialize ContextCellHighlighter - now retrieved from AppState
    const contextCellHighlighter = AppStateService.getContextCellHighlighter();

    // Initialize NotebookDiffManager
    const diffManager = new NotebookDiffManager(notebookTools, actionHistory);

    // Update AppState with the diff manager
    AppStateService.setState({ notebookDiffManager: diffManager });

    // Initialize diff2html theme detection
    NotebookDiffTools.initializeThemeDetection();

    // Set up automatic refresh of diff displays when theme changes
    NotebookDiffTools.onThemeChange(() => {
      NotebookDiffTools.refreshAllDiffDisplays();
    });

    // Set up notebook tracking to provide the active notebook widget to the diffManager
    notebooks.currentChanged.connect((_, notebook) => {
      if (notebook) {
        let oldPath = notebook.context.path;

        notebook.context.pathChanged.connect((_, path) => {
          if (oldPath !== path) {
            diffManager.setNotebookPath(path);

            const chatContainer = AppStateService.getChatContainerSafe();
            chatContainer?.updateNotebookPath(oldPath, path);

            oldPath = path;
          }
        });

        diffManager.setNotebookWidget(notebook);
        // Initialize tracking metadata for existing cells
        cellTrackingService.initializeExistingCells();

        // Update the context for this notebook path
        if (notebook.context.path) {
          notebookContextManager.getContext(notebook.context.path);
        }

        // Update the chat widget with the new notebook path
        AppStateService.switchChatContainerToNotebook(notebook.context.path);
      }
    });

    // Initialize the tracking ID utility - now retrieved from AppState
    const trackingIDUtility = AppStateService.getTrackingIDUtility();

    // Create the widget tracker
    const tracker = new WidgetTracker<Widget>({
      namespace: 'sage-ai-widgets'
    });

    // Initialize the containers
    let settingsContainer: NotebookSettingsContainer | undefined;

    const initializeChatContainer = () => {
      // Get existing chat container from AppState
      const existingChatContainer = AppStateService.getState().chatContainer;

      // Create a new chat container
      const createContainer = () => {
        // Pass the shared tool service, diff manager, and notebook context manager to the container
        const newContainer = new NotebookChatContainer(
          toolService,
          notebookContextManager
        );
        tracker.add(newContainer);

        // Add the container to the right side panel
        app.shell.add(newContainer, 'right', { rank: 1000 });

        // If there's a current notebook, set its path
        if (notebooks.currentWidget) {
          newContainer.switchToNotebook(notebooks.currentWidget.context.path);
        }

        // Store in AppState
        AppStateService.setChatContainer(newContainer);

        return newContainer;
      };

      if (!existingChatContainer || existingChatContainer.isDisposed) {
        const chatContainer = createContainer();

        // Set the chat container reference in the context cell highlighter
        contextCellHighlighter.setChatContainer(chatContainer);

        return chatContainer;
      }

      return existingChatContainer;
    };

    const initializeSettingsContainer = () => {
      // Create a new settings container
      const createContainer = () => {
        // Pass the shared tool service, diff manager, and notebook context manager to the container
        const newContainer = new NotebookSettingsContainer(
          toolService,
          diffManager,
          notebookContextManager
        );
        tracker.add(newContainer);

        // Add the container to the right side panel
        app.shell.add(newContainer, 'right', { rank: 1001 });

        return newContainer;
      };

      if (!settingsContainer || settingsContainer.isDisposed) {
        settingsContainer = createContainer();
      }

      return settingsContainer;
    };

    // Initialize both containers
    initializeChatContainer();
    settingsContainer = initializeSettingsContainer();

    // Set up notebook tracking to switch to the active notebook
    notebooks.currentChanged.connect((_, notebook) => {
      if (notebook) {
        // Fix for old notebooks having undeletable first cells
        if (notebook.model && notebook.model.cells.length > 0) {
          notebook.model.cells.get(0).setMetadata('deletable', true);
        }

        diffManager.setNotebookWidget(notebook);
        diffManager.setNotebookPath(notebook.context.path);
        // Initialize tracking metadata for existing cells
        cellTrackingService.initializeExistingCells();

        // Update the context for this notebook path
        if (notebook.context.path) {
          notebookContextManager.getContext(notebook.context.path);
        }

        // Update both containers with the new notebook path
        const chatContainer = AppStateService.getState().chatContainer;
        if (chatContainer && !chatContainer.isDisposed) {
          chatContainer.switchToNotebook(notebook.context.path);
        }

        const planCell = notebookTools.getPlanCell(notebook.context.path);

        if (planCell) {
          const currentStep =
            (planCell.model.sharedModel.getMetadata().custom as any)
              ?.current_step_string || '';
          const nextStep =
            (planCell.model.sharedModel.getMetadata().custom as any)
              ?.next_step_string || '';
          const source = planCell.model.sharedModel.getSource() || '';

          console.log('Updating step floating box', currentStep, nextStep);

          void AppStateService.getPlanStateDisplay().updatePlan(
            currentStep,
            nextStep,
            source,
            false
          );
        } else if (!planCell) {
          void AppStateService.getPlanStateDisplay().updatePlan(
            undefined,
            undefined,
            undefined
          );
        }

        notebook?.model?.cells.changed.connect(() => {
          // Update the context cell highlighting when cells change
          trackingIDUtility.fixTrackingIDs(notebook.context.path);
          contextCellHighlighter.refreshHighlighting(notebook);

          const planCell = notebookTools.getPlanCell(notebook.context.path);

          if (planCell) {
            const currentStep =
              (planCell.model.sharedModel.getMetadata().custom as any)
                ?.current_step_string || '';
            const nextStep =
              (planCell.model.sharedModel.getMetadata().custom as any)
                ?.next_step_string || '';
            const source = planCell.model.sharedModel.getSource() || '';

            console.log('Updating step floating box', currentStep, nextStep);

            void AppStateService.getPlanStateDisplay().updatePlan(
              currentStep,
              nextStep,
              source,
              false
            );
          } else if (!planCell) {
            void AppStateService.getPlanStateDisplay().updatePlan(
              undefined,
              undefined,
              undefined
            );
          }

          if (notebook.model?.cells) {
            for (const cell of notebook.model.cells) {
              cell.metadataChanged.connect(() => {
                // Refresh the context cell highlighting when metadata changes
                contextCellHighlighter.refreshHighlighting(notebook);
              });
            }
          }
        });
      }
    });

    // Register all commands
    registerCommands(app, palette);
    registerEvalCommands(app, palette);

    // Set up notebook tracking to update button state
    notebooks.activeCellChanged.connect((_, cell) => {
      if (cell) {
        // Get the current notebook path
        const notebookPath = notebooks.currentWidget?.context.path;
        if (!notebookPath) return;

        // Check if the cell has tracking ID metadata
        const metadata = cell.model.sharedModel.getMetadata() || {};
        let trackingId = '';

        if (
          metadata &&
          typeof metadata === 'object' &&
          'cell_tracker' in metadata &&
          metadata.cell_tracker &&
          typeof metadata.cell_tracker === 'object' &&
          'trackingId' in metadata.cell_tracker
        ) {
          trackingId = String(metadata.cell_tracker.trackingId);
        }

        // Update the button state based on whether this cell is in context
        const isInContext = trackingId
          ? notebookContextManager.isCellInContext(notebookPath, trackingId)
          : notebookContextManager.isCellInContext(notebookPath, cell.model.id);

        // Find the button
        const buttonNode = document.querySelector(
          '.jp-ToolbarButtonComponent[data-command="sage-ai-add-to-context"]'
        );
        if (buttonNode) {
          if (isInContext) {
            // Set to "Remove from Chat" state
            buttonNode.classList.add('in-context');

            const icon = buttonNode.querySelector('.jp-icon3');
            if (icon) {
              // Create a minus icon
              const minusIcon =
                '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="currentColor" d="M5 13v-2h14v2z"/></svg>';
              icon.innerHTML = minusIcon;
            }

            const textSpan = buttonNode.querySelector('.button-text');
            if (textSpan) {
              textSpan.textContent = 'Remove from Chat';
            }
          } else {
            // Set to "Add to Chat" state
            buttonNode.classList.remove('in-context');

            const icon = buttonNode.querySelector('.jp-icon3');
            if (icon) {
              icon.innerHTML = addIcon.svgstr;
            }

            const textSpan = buttonNode.querySelector('.button-text');
            if (textSpan) {
              textSpan.textContent = 'Add to Context';
            }
          }
        }
      }
    });

    const { commands } = app;

    const commandId = 'sage-agent:log-selected-code';
    palette.addItem({ command: commandId, category: 'Sage AI' });
    app.commands.addKeyBinding({
      command: commandId,
      keys: ['Accel Shift K'],
      selector: '.jp-Notebook.jp-mod-editMode' // only trigger in edit mode
    });

    commands.addCommand(commandId, {
      label: 'Log Selected Code',
      execute: () => {
        const current = tracker.currentWidget;
        if (!current) {
          console.warn('No active notebook');
          return;
        }

        const activeCell = notebooks.activeCell;
        if (!activeCell) {
          console.warn('No active cell');
          return;
        }

        const editor = activeCell.editor;
        const selection = editor?.getSelection();
        if (selection) {
          console.log('Selection:', selection);
        } else {
          console.log('No selection');
        }

        const selectedText = editor?.model.sharedModel.source.substring(
          editor.getOffsetAt(selection?.start || { line: 0, column: 0 }),
          editor.getOffsetAt(selection?.end || { line: 0, column: 0 })
        );

        if (selectedText) {
          console.log('Selected text:', selectedText);
        } else {
          console.log('No text selected');
        }
      }
    });

    // Initialize the chat widget
    initializeChatContainer();
    initializeSettingsContainer();
  },
  deactivate: () => {
    console.log('JupyterLab extension sage-agent is deactivated!');
    // Cleanup theme detection
    NotebookDiffTools.cleanupThemeDetection();
  }
};
