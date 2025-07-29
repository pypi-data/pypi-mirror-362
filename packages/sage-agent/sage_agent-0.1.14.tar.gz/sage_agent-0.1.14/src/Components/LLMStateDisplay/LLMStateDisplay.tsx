import * as React from 'react';
import { Widget } from '@lumino/widgets';
import { ReactWidget } from '@jupyterlab/ui-components';
import { AppStateService } from '../../AppState';
import { LLMStateContent } from './LLMStateContent';
import { ILLMState, LLMDisplayState } from './types';
import { IPendingDiff } from '../../types';
import { diffStateService } from '../../Services/DiffStateService';
import { Subscription } from 'rxjs';

/**
 * Component for displaying LLM processing state above the chat input
 */
export class LLMStateDisplay extends ReactWidget {
  private _state: ILLMState;
  private subscriptions: Subscription[] = [];

  constructor() {
    super();
    this._state = {
      isVisible: false,
      state: LLMDisplayState.IDLE,
      text: ''
    };
    this.addClass('sage-ai-llm-state-widget');
    this.addClass('hidden');
    this.setupDiffStateSubscriptions();
  }

  /**
   * Set up RxJS subscriptions for diff state changes
   */
  private setupDiffStateSubscriptions(): void {
    // Subscribe to diff state changes to auto-update the display
    const diffStateSub = diffStateService.diffState$.subscribe(diffState => {
      // If we're in diff mode and diffs change, update the display
      if (this._state.state === LLMDisplayState.DIFF) {
        const diffs = Array.from(diffState.pendingDiffs.values());
        this._state = {
          ...this._state,
          diffs
        };
        this.update();
      }
    });
    this.subscriptions.push(diffStateSub);

    // Subscribe to allDiffsResolved changes to automatically hide when complete
    const allResolvedSub = diffStateService.allDiffsResolved$.subscribe(
      ({ notebookPath }) => {
        const currentState = diffStateService.getCurrentState();
        const hasAnyDiffs = currentState.pendingDiffs.size > 0;

        // If all diffs are resolved and no pending diffs remain, hide the display
        if (!hasAnyDiffs && this._state.state === LLMDisplayState.DIFF) {
          this.hide();
        }
      }
    );
    this.subscriptions.push(allResolvedSub);
  }

  /**
   * Clean up subscriptions
   */
  public dispose(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.subscriptions = [];
    super.dispose();
  }

  /**
   * Render the React component
   */
  render(): JSX.Element {
    this.handleIsVisibleChanges(this._state.isVisible);

    return (
      <LLMStateContent
        isVisible={this._state.isVisible}
        state={this._state.state}
        text={this._state.text}
        toolName={this._state.toolName}
        diffs={this._state.diffs}
        waitingForUser={this._state.waitingForUser}
        isRunContext={this._state.isRunContext}
        onRunClick={this._state.onRunClick}
        onRejectClick={this._state.onRejectClick}
      />
    );
  }

  private handleIsVisibleChanges(isVisible: boolean): void {
    if (isVisible) {
      this.removeClass('hidden');
    } else {
      this.addClass('hidden');
    }
  }

  /**
   * Show the LLM state in generating mode
   * @param text The status text to display
   * @param waitingForUser
   */
  public show(text: string = 'Generating...', waitingForUser?: boolean): void {
    this._state = {
      isVisible: true,
      state: LLMDisplayState.GENERATING,
      text,
      waitingForUser
    };
    this.update();
  }

  /**
   * Show the LLM state in using tool mode with approval buttons
   * @param text Optional custom status text
   * @param onRunClick Optional callback for run action (for notebook-run_cell tool)
   * @param onRejectClick Optional callback for reject action (for notebook-run_cell tool)
   */
  public showRunCellTool(
    onRunClick?: () => void,
    onRejectClick?: () => void
  ): void {
    this._state = {
      isVisible: true,
      state: LLMDisplayState.USING_TOOL,
      text: '',
      toolName: 'notebook-run_cell',
      onRunClick,
      onRejectClick
    };
    this.update();
  }

  /**
   * Show the LLM state in using tool mode
   * @param toolName The name of the tool being used
   * @param text Optional custom status text
   * @param onRunClick Optional callback for run action (for notebook-run_cell tool)
   * @param onRejectClick Optional callback for reject action (for notebook-run_cell tool)
   */
  public showTool(toolName: string, text?: string): void {
    this._state = {
      isVisible: true,
      state: LLMDisplayState.USING_TOOL,
      text: text || '',
      toolName
    };
    this.update();
  }

  /**
   * Show the diff state with pending diffs using DiffStateService
   * @param notebookPath Optional path to filter diffs for a specific notebook
   * @param isRunContext
   */
  public showDiffsWithManager(
    notebookPath?: string,
    isRunContext?: boolean
  ): void {
    try {
      // Get diffs from the RxJS service instead of NotebookDiffManager
      const currentState = diffStateService.getCurrentState();
      const diffs = Array.from(currentState.pendingDiffs.values()).filter(
        diff => !notebookPath || diff.notebookPath === notebookPath
      );

      if (diffs.length === 0) {
        this.hide();
        return;
      }

      this._state = {
        isVisible: true,
        state: LLMDisplayState.DIFF,
        text: '',
        diffs,
        isRunContext: isRunContext || false
      };
      this.update();
    } catch (error) {
      console.warn('Could not show diffs with manager:', error);
      this.hide();
    }
  }

  /**
   * Hide the LLM state display and set to idle
   */
  public hide(): void {
    this._state = {
      isVisible: false,
      state: LLMDisplayState.IDLE,
      text: '',
      waitingForUser: false
    };

    const planComponent = document.getElementsByClassName(
      'sage-ai-plan-state-widget'
    );
    const planWidget = planComponent.item(0);
    if (planWidget) {
      planWidget.className += ' no-state-open';
    }

    this.update();
  }

  /**
   * Update the status text without changing visibility (only for generating/tool states)
   * @param text The new status text
   */
  public updateText(text: string): void {
    if (
      !this._state.isVisible ||
      (this._state.state !== LLMDisplayState.GENERATING &&
        this._state.state !== LLMDisplayState.USING_TOOL)
    ) {
      return;
    }

    this._state = {
      ...this._state,
      text
    };
    this.update();
  }

  /**
   * Update the tool name for using tool state
   * @param toolName The new tool name
   */
  public updateToolName(toolName: string): void {
    if (
      !this._state.isVisible ||
      this._state.state !== LLMDisplayState.USING_TOOL
    ) {
      return;
    }

    this._state = {
      ...this._state,
      toolName
    };
    this.update();
  }

  /**
   * Public method to show pending diffs
   * @param notebookPath Optional path to filter diffs for a specific notebook
   */
  public showPendingDiffs(
    notebookPath?: string | null,
    isRunContext?: boolean
  ): void {
    this.showDiffsWithManager(notebookPath || undefined, isRunContext);
  }

  /**
   * Public method to hide pending diffs
   */
  public hidePendingDiffs(): void {
    this.hide();
  }

  /**
   * Public method to check if there are pending diffs to show
   * @param notebookPath Optional path to filter diffs for a specific notebook
   * @returns Boolean indicating if there are pending diffs
   */
  public hasPendingDiffs(notebookPath?: string | null): boolean {
    try {
      const currentState = diffStateService.getCurrentState();
      const diffs = Array.from(currentState.pendingDiffs.values()).filter(
        diff => !notebookPath || diff.notebookPath === notebookPath
      );
      return diffs.length > 0;
    } catch (error) {
      console.warn('Could not check pending diffs:', error);
      return false;
    }
  }

  /**
   * Get the current state
   */
  public getCurrentState(): LLMDisplayState {
    return this._state.state;
  }

  /**
   * Check if currently in diff state
   */
  public isDiffState(): boolean {
    return this._state.state === LLMDisplayState.DIFF;
  }

  /**
   * Check if currently in using tool state
   */
  public isUsingToolState(): boolean {
    return this._state.state === LLMDisplayState.USING_TOOL;
  }

  /**
   * Get the widget for adding to layout (for backwards compatibility)
   */
  public getWidget(): Widget {
    return this;
  }
}
