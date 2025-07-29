import { BehaviorSubject, Observable, distinctUntilChanged, map } from 'rxjs';
import { IPendingDiff } from '../types';

export interface IDiffStateChange {
  cellId: string;
  approved: boolean | undefined;
  notebookPath?: string | null;
}

export interface IDiffState {
  pendingDiffs: Map<string, IPendingDiff>;
  allDiffsResolved: boolean;
  notebookPath?: string | null;
}

/**
 * RxJS-based service for managing diff state across the application
 */
export class DiffStateService {
  private static instance: DiffStateService | null = null;

  private _diffState$ = new BehaviorSubject<IDiffState>({
    pendingDiffs: new Map(),
    allDiffsResolved: false,
    notebookPath: null
  });

  private constructor() {}

  /**
   * Get the singleton instance
   */
  public static getInstance(): DiffStateService {
    if (!DiffStateService.instance) {
      DiffStateService.instance = new DiffStateService();
    }
    return DiffStateService.instance;
  }

  /**
   * Observable for all diff state changes
   */
  public get diffState$(): Observable<IDiffState> {
    return this._diffState$.asObservable();
  }

  /**
   * Observable for specific cell state changes
   */
  public getCellStateChanges$(
    cellId: string
  ): Observable<IDiffStateChange | null> {
    return this._diffState$.pipe(
      map(state => {
        const diff = state.pendingDiffs.get(cellId);
        if (!diff) return null;

        return {
          cellId,
          approved: diff.approved,
          notebookPath: state.notebookPath
        };
      }),
      distinctUntilChanged(
        (prev, curr) => JSON.stringify(prev) === JSON.stringify(curr)
      )
    );
  }

  /**
   * Observable for when all diffs are resolved
   */
  public get allDiffsResolved$(): Observable<{ notebookPath?: string | null }> {
    return this._diffState$.pipe(
      map(state => ({
        allDiffsResolved: state.allDiffsResolved,
        notebookPath: state.notebookPath
      })),
      distinctUntilChanged(
        (prev, curr) =>
          prev.allDiffsResolved === curr.allDiffsResolved &&
          prev.notebookPath === curr.notebookPath
      ),
      map(state => ({ notebookPath: state.notebookPath }))
    );
  }

  /**
   * Observable for pending diffs for a specific notebook
   */
  public getPendingDiffsForNotebook$(
    notebookPath?: string | null
  ): Observable<IPendingDiff[]> {
    return this._diffState$.pipe(
      map(state => {
        const diffs: IPendingDiff[] = [];
        for (const [, diff] of state.pendingDiffs) {
          if (!notebookPath || diff.notebookPath === notebookPath) {
            diffs.push(diff);
          }
        }
        return diffs;
      }),
      distinctUntilChanged(
        (prev, curr) => JSON.stringify(prev) === JSON.stringify(curr)
      )
    );
  }

  /**
   * Get current state value
   */
  public getCurrentState(): IDiffState {
    return this._diffState$.value;
  }

  /**
   * Update the entire pending diffs map
   */
  public updatePendingDiffs(
    pendingDiffs: Map<string, IPendingDiff>,
    notebookPath?: string | null
  ): void {
    const currentState = this._diffState$.value;
    const allResolved = this.checkIfAllDiffsResolved(
      pendingDiffs,
      notebookPath
    );

    this._diffState$.next({
      ...currentState,
      pendingDiffs,
      allDiffsResolved: allResolved,
      notebookPath
    });
  }

  /**
   * Update a specific diff state
   */
  public updateDiffState(
    cellId: string,
    approved: boolean | undefined,
    notebookPath?: string | null
  ): void {
    const currentState = this._diffState$.value;
    const newPendingDiffs = new Map(currentState.pendingDiffs);

    const existingDiff = newPendingDiffs.get(cellId);
    if (existingDiff) {
      newPendingDiffs.set(cellId, {
        ...existingDiff,
        approved,
        userDecision:
          existingDiff.userDecision ||
          (approved === true
            ? 'approved'
            : approved === false
              ? 'rejected'
              : null)
      });
    }

    const allResolved = this.checkIfAllDiffsResolved(
      newPendingDiffs,
      notebookPath
    );

    this._diffState$.next({
      ...currentState,
      pendingDiffs: newPendingDiffs,
      allDiffsResolved: allResolved,
      notebookPath: notebookPath ?? currentState.notebookPath
    });
  }

  public updateDiffStateResult(cellId: string, runResult: any): void {
    const currentState = this._diffState$.value;
    const newPendingDiffs = new Map(currentState.pendingDiffs);

    const existingDiff = newPendingDiffs.get(cellId);
    if (existingDiff) {
      newPendingDiffs.set(cellId, {
        ...existingDiff,
        runResult
      });
    }

    const allResolved = this.checkIfAllDiffsResolved(
      newPendingDiffs,
      newPendingDiffs.get(cellId)?.notebookPath || currentState.notebookPath
    );

    this._diffState$.next({
      ...currentState,
      allDiffsResolved: allResolved,
      pendingDiffs: newPendingDiffs
    });
  }

  /**
   * Update a specific diff state to "run" (approve and execute immediately)
   */
  public updateDiffStateToRun(
    cellId: string,
    notebookPath?: string | null
  ): void {
    const currentState = this._diffState$.value;
    const newPendingDiffs = new Map(currentState.pendingDiffs);

    const existingDiff = newPendingDiffs.get(cellId);
    if (existingDiff) {
      newPendingDiffs.set(cellId, {
        ...existingDiff,
        approved: true,
        userDecision: 'run'
      });
    }

    this._diffState$.next({
      ...currentState,
      pendingDiffs: newPendingDiffs,
      notebookPath: notebookPath ?? currentState.notebookPath
    });
  }

  /**
   * Add a new pending diff
   */
  public addPendingDiff(cellId: string, diff: IPendingDiff): void {
    const currentState = this._diffState$.value;
    const newPendingDiffs = new Map(currentState.pendingDiffs);
    newPendingDiffs.set(cellId, diff);

    const allResolved = this.checkIfAllDiffsResolved(
      newPendingDiffs,
      diff.notebookPath
    );

    this._diffState$.next({
      ...currentState,
      pendingDiffs: newPendingDiffs,
      allDiffsResolved: allResolved,
      notebookPath: diff.notebookPath ?? currentState.notebookPath
    });
  }

  /**
   * Remove a pending diff
   */
  public removePendingDiff(cellId: string, notebookPath?: string | null): void {
    const currentState = this._diffState$.value;
    const newPendingDiffs = new Map(currentState.pendingDiffs);
    newPendingDiffs.delete(cellId);

    const allResolved = this.checkIfAllDiffsResolved(
      newPendingDiffs,
      notebookPath
    );

    this._diffState$.next({
      ...currentState,
      pendingDiffs: newPendingDiffs,
      allDiffsResolved: allResolved,
      notebookPath: notebookPath ?? currentState.notebookPath
    });
  }

  /**
   * Clear all pending diffs
   */
  public clearAllDiffs(notebookPath?: string | null): void {
    const currentState = this._diffState$.value;
    let newPendingDiffs: Map<string, IPendingDiff>;

    if (notebookPath) {
      // Clear only diffs for specific notebook
      newPendingDiffs = new Map();
      for (const [cellId, diff] of currentState.pendingDiffs) {
        if (diff.notebookPath !== notebookPath) {
          newPendingDiffs.set(cellId, diff);
        }
      }
    } else {
      // Clear all diffs
      newPendingDiffs = new Map();
    }

    this._diffState$.next({
      ...currentState,
      pendingDiffs: newPendingDiffs,
      allDiffsResolved: newPendingDiffs.size === 0,
      notebookPath: notebookPath ?? currentState.notebookPath
    });
  }

  /**
   * Set current notebook path
   */
  public setNotebookPath(notebookPath: string | null): void {
    const currentState = this._diffState$.value;
    this._diffState$.next({
      ...currentState,
      notebookPath
    });
  }

  /**
   * Get count of pending diffs for a specific notebook
   */
  public getPendingDiffCount(notebookPath?: string | null): number {
    const currentState = this._diffState$.value;
    let count = 0;

    for (const [, diff] of currentState.pendingDiffs) {
      if (!notebookPath || diff.notebookPath === notebookPath) {
        if (!diff.userDecision) count++;
      }
    }

    return count;
  }

  /**
   * Get count of approved diffs for a specific notebook
   */
  public getApprovedDiffCount(notebookPath?: string | null): number {
    const currentState = this._diffState$.value;
    let count = 0;

    for (const [, diff] of currentState.pendingDiffs) {
      if (
        (!notebookPath || diff.notebookPath === notebookPath) &&
        (diff.approved === true ||
          diff.userDecision === 'approved' ||
          diff.userDecision === 'run')
      ) {
        count++;
      }
    }

    return count;
  }

  /**
   * Get count of rejected diffs for a specific notebook
   */
  public getRejectedDiffCount(notebookPath?: string | null): number {
    const currentState = this._diffState$.value;
    let count = 0;

    for (const [, diff] of currentState.pendingDiffs) {
      if (
        (!notebookPath || diff.notebookPath === notebookPath) &&
        (diff.approved === false || diff.userDecision === 'rejected')
      ) {
        count++;
      }
    }

    return count;
  }

  /**
   * Check if all diffs are approved for a specific notebook
   */
  public areAllDiffsApproved(notebookPath?: string | null): boolean {
    const currentState = this._diffState$.value;
    const relevantDiffs: IPendingDiff[] = [];

    for (const [, diff] of currentState.pendingDiffs) {
      if (!notebookPath || diff.notebookPath === notebookPath) {
        relevantDiffs.push(diff);
      }
    }

    if (relevantDiffs.length === 0) {
      return true; // No diffs means all are "approved"
    }

    return relevantDiffs.every(
      diff =>
        diff.approved === true ||
        diff.userDecision === 'approved' ||
        diff.userDecision === 'run'
    );
  }

  /**
   * Check if all diffs are rejected for a specific notebook
   */
  public areAllDiffsRejected(notebookPath?: string | null): boolean {
    const currentState = this._diffState$.value;
    const relevantDiffs: IPendingDiff[] = [];

    for (const [, diff] of currentState.pendingDiffs) {
      if (!notebookPath || diff.notebookPath === notebookPath) {
        relevantDiffs.push(diff);
      }
    }

    if (relevantDiffs.length === 0) {
      return false; // No diffs means none are rejected
    }

    return relevantDiffs.every(
      diff => diff.approved === false || diff.userDecision === 'rejected'
    );
  }

  /**
   * Observable for diff count changes for a specific notebook
   */
  public getDiffCountChanges$(
    notebookPath?: string | null
  ): Observable<number> {
    return this._diffState$.pipe(
      map(state => {
        let count = 0;
        for (const [, diff] of state.pendingDiffs) {
          if (!notebookPath || diff.notebookPath === notebookPath) {
            count++;
          }
        }
        return count;
      }),
      distinctUntilChanged()
    );
  }

  /**
   * Observable for approval status changes for a specific notebook
   */
  public getApprovalStatusChanges$(notebookPath?: string | null): Observable<{
    pending: number;
    approved: number;
    rejected: number;
    allResolved: boolean;
  }> {
    return this._diffState$.pipe(
      map(state => {
        let pending = 0;
        let approved = 0;
        let rejected = 0;

        for (const [, diff] of state.pendingDiffs) {
          if (!notebookPath || diff.notebookPath === notebookPath) {
            if (
              diff.approved === true ||
              diff.userDecision === 'approved' ||
              diff.userDecision === 'run'
            ) {
              approved++;
            } else if (
              diff.approved === false ||
              diff.userDecision === 'rejected'
            ) {
              rejected++;
            } else {
              pending++;
            }
          }
        }

        const total = pending + approved + rejected;
        return {
          pending,
          approved,
          rejected,
          allResolved: total > 0 && pending === 0
        };
      }),
      distinctUntilChanged(
        (prev, curr) => JSON.stringify(prev) === JSON.stringify(curr)
      )
    );
  }

  /**
   * Check if all diffs are resolved for a specific notebook or globally
   */
  private checkIfAllDiffsResolved(
    pendingDiffs: Map<string, IPendingDiff>,
    notebookPath?: string | null
  ): boolean {
    let relevantDiffs: IPendingDiff[] = [];

    for (const [, diff] of pendingDiffs) {
      if (!notebookPath || diff.notebookPath === notebookPath) {
        relevantDiffs.push(diff);
      }
    }

    if (relevantDiffs.length === 0) {
      return true;
    }

    for (const diff of relevantDiffs) {
      if (diff.userDecision === 'run' && !diff.runResult) return false;
    }

    return relevantDiffs.every(
      diff =>
        diff.approved !== undefined ||
        diff.userDecision === 'approved' ||
        diff.userDecision === 'rejected' ||
        diff.userDecision === 'run'
    );
  }
}

// Export singleton instance for easy access
export const diffStateService = DiffStateService.getInstance();
