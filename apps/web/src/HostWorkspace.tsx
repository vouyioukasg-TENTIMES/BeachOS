import { useEffect, useRef, useState } from 'react';

import {
  getVenueContext,
  openVenue,
  type OpeningReport,
  type VenueContext,
  VenueOpeningApiError,
} from './venueOpeningApi';

type OpeningAction =
  | { status: 'idle' }
  | { status: 'confirming' }
  | { status: 'processing' }
  | { status: 'error'; message: string }
  | { status: 'success' };

export type HostWorkspaceState =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; context: VenueContext; opening: OpeningAction };

interface HostWorkspaceViewProps {
  state: HostWorkspaceState;
  onRetry: () => void;
  onRequestOpen: () => void;
  onConfirmOpen: () => void;
  onCancelOpen: () => void;
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'long',
    timeZone: 'UTC',
  }).format(new Date(`${value}T00:00:00Z`));
}

function formatTime(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value));
}

function OpeningReportView({ report }: { report: OpeningReport }) {
  return (
    <section className="workspace-panel report" aria-labelledby="opening-report-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Official record</p>
          <h2 id="opening-report-title">Opening Report</h2>
        </div>
        <span className="status-chip open">Venue open</span>
      </div>
      <dl className="report-summary">
        <div>
          <dt>Business date</dt>
          <dd>{formatDate(report.business_date)}</dd>
        </div>
        <div>
          <dt>Opening time</dt>
          <dd>{formatTime(report.opened_at)}</dd>
        </div>
        <div>
          <dt>Host</dt>
          <dd>{report.host_id}</dd>
        </div>
        <div>
          <dt>Departments ready</dt>
          <dd>{report.department_readiness.length}</dd>
        </div>
      </dl>
      <div className="report-readiness">
        <h3>Readiness at opening</h3>
        <div className="report-departments">
          {report.department_readiness.map((department) => (
            <div className="report-department" key={department.department_id}>
              <span>{department.department_id}</span>
              <strong>{department.status}</strong>
            </div>
          ))}
        </div>
      </div>
      <p className="report-footnote">
        {report.delays.length === 0 && report.blocking_issues.length === 0
          ? 'No delays or blocking issues were recorded at opening.'
          : `${report.delays.length} delay record${
              report.delays.length === 1 ? '' : 's'
            } and ${report.blocking_issues.length} blocking issue${
              report.blocking_issues.length === 1 ? '' : 's'
            } are preserved in this report.`}
      </p>
    </section>
  );
}

export function HostWorkspaceView({
  state,
  onRetry,
  onRequestOpen,
  onConfirmOpen,
  onCancelOpen,
}: HostWorkspaceViewProps) {
  if (state.status === 'loading') {
    return (
      <main className="page-shell">
        <header className="product-header">
          <span className="wordmark">BeachOS</span>
          <span>Host Workspace</span>
        </header>
        <div className="centered-state state-area">
          <section className="state-card loading-card" role="status" aria-live="polite">
            <span className="spinner large-spinner" aria-hidden="true" />
            <div>
              <p className="eyebrow">Authoritative status</p>
              <h1>Loading Host Workspace</h1>
              <p>BeachOS is confirming the current Venue and Business Date.</p>
            </div>
            <div className="loading-placeholder" aria-hidden="true">
              <span />
              <span />
              <span />
            </div>
          </section>
        </div>
      </main>
    );
  }

  if (state.status === 'error') {
    return (
      <main className="page-shell">
        <header className="product-header">
          <a className="wordmark" href="/" aria-label="BeachOS home">
            BeachOS
          </a>
          <span>Host Workspace</span>
        </header>
        <div className="centered-state state-area">
          <section className="state-card error-state-card" role="alert">
            <span className="state-symbol" aria-hidden="true">
              !
            </span>
            <p className="eyebrow">Current state unavailable</p>
            <h1>Host Workspace could not load</h1>
            <p>{state.message}</p>
            <p className="state-guidance">
              OPEN VENUE is unavailable until current information is confirmed. Continue manual
              coordination and try again.
            </p>
            <button className="primary-action" type="button" onClick={onRetry}>
              Try again
            </button>
          </section>
        </div>
      </main>
    );
  }

  const { context, opening } = state;
  const isOpen = context.opening_status === 'OPEN';
  const hasDepartments = context.department_readiness.length > 0;
  const isOperationallyReady = hasDepartments && context.outstanding_departments.length === 0;
  const canOpen = !isOpen && isOperationallyReady;
  const isProcessing = opening.status === 'processing';
  const readyDepartmentCount =
    context.department_readiness.length - context.outstanding_departments.length;

  return (
    <main className="page-shell">
      <header className="product-header">
        <a className="wordmark" href="/" aria-label="BeachOS home">
          BeachOS
        </a>
        <span>Host Workspace</span>
      </header>

      <div className="workspace-content">
        <section className="workspace-hero" aria-labelledby="workspace-title">
          <div>
            <p className="eyebrow">Current Venue</p>
            <h1 id="workspace-title">{context.venue_name}</h1>
            <p className="lede">{formatDate(context.business_date)}</p>
          </div>
          <span className={`venue-status ${isOpen ? 'open' : 'closed'}`}>
            {isOpen ? 'Venue open' : 'Venue closed'}
          </span>
        </section>

        <section
          className={`operational-readiness-card ${isOperationallyReady ? 'ready' : 'not-ready'}`}
          aria-labelledby="operational-readiness-title"
        >
          <div className="readiness-decision">
            <p className="eyebrow">Operational Readiness</p>
            <div className="decision-verdict">
              <span className="decision-mark" aria-hidden="true">
                {isOperationallyReady ? '✓' : '!'}
              </span>
              <div>
                <strong>{isOperationallyReady ? 'READY' : 'NOT READY'}</strong>
                <h2 id="operational-readiness-title">
                  {isOpen
                    ? 'The Venue is open'
                    : canOpen
                      ? 'You can safely open the Venue'
                      : 'The Venue cannot open yet'}
                </h2>
              </div>
            </div>
            <p className="decision-explanation">
              {isOpen
                ? 'The official operational start is confirmed for this Business Date.'
                : canOpen
                  ? `All ${context.department_readiness.length} mandatory departments are READY.`
                  : `${context.outstanding_departments.length} mandatory department${
                      context.outstanding_departments.length === 1 ? '' : 's'
                    } must be resolved before opening.`}
            </p>
          </div>

          <dl className="readiness-facts">
            <div>
              <dt>Opening status</dt>
              <dd>{isOpen ? 'OPEN' : 'CLOSED'}</dd>
            </div>
            <div>
              <dt>Blocking items</dt>
              <dd>{context.outstanding_departments.length}</dd>
            </div>
            <div>
              <dt>Attention</dt>
              <dd>{context.attention_queue.length}</dd>
            </div>
            <div>
              <dt>Estimated readiness</dt>
              <dd>
                Not available
                <small>No approved estimate</small>
              </dd>
            </div>
          </dl>

          <div className="readiness-progress">
            <div>
              <span>Department readiness</span>
              <strong>
                {readyDepartmentCount} of {context.department_readiness.length} ready
              </strong>
            </div>
            <div
              className="progress-track"
              role="progressbar"
              aria-label="Department readiness"
              aria-valuemin={0}
              aria-valuemax={context.department_readiness.length}
              aria-valuenow={readyDepartmentCount}
            >
              <span
                style={{
                  width:
                    context.department_readiness.length === 0
                      ? '0%'
                      : `${(readyDepartmentCount / context.department_readiness.length) * 100}%`,
                }}
              />
            </div>
          </div>

          {!isOpen ? (
            <div className="readiness-action">
              <div>
                <strong>{canOpen ? 'Opening is available' : 'Opening is unavailable'}</strong>
                <p>
                  {canOpen
                    ? 'Review the supporting details below, then confirm the official opening.'
                    : 'Resolve every outstanding department shown below before continuing.'}
                </p>
              </div>
              <button
                className="primary-action"
                type="button"
                disabled={!canOpen || isProcessing}
                onClick={onRequestOpen}
              >
                {isProcessing ? 'Opening…' : 'Open Venue'}
              </button>
              {isProcessing ? (
                <div className="opening-progress" role="status" aria-live="polite">
                  <span className="spinner" aria-hidden="true" />
                  <span>
                    <strong>Opening is being confirmed</strong>
                    Do not repeat the action.
                  </span>
                </div>
              ) : null}
            </div>
          ) : null}
        </section>

        {opening.status === 'success' ? (
          <section className="message success-message" role="status" aria-live="polite">
            <span className="success-mark" aria-hidden="true">
              ✓
            </span>
            <span>
              <strong>Venue opened successfully</strong>
              The official operational start has been recorded.
            </span>
          </section>
        ) : null}

        {opening.status === 'error' ? (
          <section className="message error-message" role="alert">
            <span>
              <strong>Venue was not opened</strong>
              {opening.message}
            </span>
          </section>
        ) : null}

        <div className="workspace-grid">
          <aside className="workspace-panel attention-panel" aria-labelledby="attention-title">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Confirmed facts</p>
                <h2 id="attention-title">Attention Queue</h2>
                <p className="panel-description">Current matters that require Host awareness.</p>
              </div>
              <span className="panel-count" aria-label={`${context.attention_queue.length} items`}>
                {context.attention_queue.length}
              </span>
            </div>
            {context.attention_queue.length === 0 ? (
              <div className="empty-state">
                <span className="empty-state-mark" aria-hidden="true">
                  ✓
                </span>
                <div>
                  <strong>No confirmed action required</strong>
                  <p>
                    Continue normal operational observation. This does not mean the operation is
                    perfect.
                  </p>
                </div>
              </div>
            ) : (
              <div className="attention-list">
                {context.attention_queue.map((item) => (
                  <article className={`attention-item ${item.importance}`} key={item.code}>
                    <div className="attention-meta">
                      <span>{item.importance === 'CRITICAL' ? 'Critical' : 'Action required'}</span>
                      {item.department_id ? <small>{item.department_id}</small> : null}
                    </div>
                    <p>{item.message}</p>
                  </article>
                ))}
              </div>
            )}
          </aside>

          <section className="workspace-panel readiness-panel" aria-labelledby="readiness-title">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Opening readiness</p>
                <h2 id="readiness-title">Departments</h2>
                <p className="panel-description">
                  Latest declaration from each responsible department.
                </p>
              </div>
              <span className="panel-count">
                {context.department_readiness.length - context.outstanding_departments.length} /{' '}
                {context.department_readiness.length} ready
              </span>
            </div>
            {context.department_readiness.length === 0 ? (
              <div className="empty-state department-empty-state">
                <span className="empty-state-mark warning" aria-hidden="true">
                  !
                </span>
                <div>
                  <strong>Opening setup is incomplete</strong>
                  <p>No mandatory departments are available for this Business Date.</p>
                </div>
              </div>
            ) : (
              <div className="workspace-departments">
                {context.department_readiness.map((department) => {
                  const readiness = department.current_readiness;
                  const status = readiness?.status ?? 'PENDING';
                  return (
                    <article className="workspace-department" key={department.department_id}>
                      <div className="department-copy">
                        <h3>{department.name}</h3>
                        <p>
                          <span>Responsible person</span>
                          {department.responsible_person_id}
                        </p>
                        {readiness ? (
                          <p>
                            <span>Declared</span>
                            {formatTime(readiness.declared_at)}
                          </p>
                        ) : (
                          <p className="pending-copy">Waiting for a readiness declaration.</p>
                        )}
                        {readiness?.reason ? (
                          <p className="department-reason">
                            <span>Reason</span>
                            {readiness.reason}
                          </p>
                        ) : null}
                        {readiness?.comment ? (
                          <p className="department-comment">
                            <span>Comment</span>
                            {readiness.comment}
                          </p>
                        ) : null}
                      </div>
                      <span
                        className={`readiness-status ${status.replaceAll(' ', '-')}`}
                        aria-label={`${department.name}: ${status}`}
                      >
                        {status}
                      </span>
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        </div>

        {isOpen && context.opening_report ? (
          <OpeningReportView report={context.opening_report} />
        ) : null}
      </div>

      {opening.status === 'confirming' ? (
        <div className="dialog-backdrop">
          <dialog className="confirmation-dialog" open aria-labelledby="confirmation-title">
            <p className="eyebrow">Confirm opening</p>
            <h2 id="confirmation-title">Open {context.venue_name}?</h2>
            <p>
              Confirm only after reviewing the current readiness above. This creates the official
              operational start for the Business Date.
            </p>
            <dl className="confirmation-summary">
              <div>
                <dt>Venue</dt>
                <dd>{context.venue_name}</dd>
              </div>
              <div>
                <dt>Business date</dt>
                <dd>{formatDate(context.business_date)}</dd>
              </div>
              <div>
                <dt>Departments</dt>
                <dd>{context.department_readiness.length} ready</dd>
              </div>
            </dl>
            <div className="dialog-actions">
              <button className="secondary-action" type="button" onClick={onCancelOpen}>
                Cancel
              </button>
              <button className="primary-action" type="button" onClick={onConfirmOpen}>
                Confirm Open Venue
              </button>
            </div>
          </dialog>
        </div>
      ) : null}
    </main>
  );
}

export function HostWorkspace({ venueId }: { venueId: string }) {
  const [state, setState] = useState<HostWorkspaceState>({ status: 'loading' });
  const loadController = useRef<AbortController | null>(null);

  async function loadContext(): Promise<void> {
    loadController.current?.abort();
    const controller = new AbortController();
    loadController.current = controller;
    setState({ status: 'loading' });
    try {
      const context = await getVenueContext(venueId, controller.signal);
      setState({ status: 'ready', context, opening: { status: 'idle' } });
    } catch (error) {
      if (controller.signal.aborted) return;
      setState({
        status: 'error',
        message:
          error instanceof VenueOpeningApiError
            ? error.message
            : 'BeachOS could not confirm the current Venue state. Check the connection.',
      });
    }
  }

  useEffect(() => {
    void loadContext();
    return () => loadController.current?.abort();
    // The Venue identity is the complete load scope.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [venueId]);

  async function handleOpen(): Promise<void> {
    if (state.status !== 'ready' || state.opening.status === 'processing') return;
    setState({ ...state, opening: { status: 'processing' } });
    try {
      const result = await openVenue(venueId);
      setState({
        status: 'ready',
        context: {
          ...state.context,
          opening_status: 'OPEN',
          opening_report: result.report,
          outstanding_departments: [],
          attention_queue: [],
        },
        opening: { status: 'success' },
      });
    } catch (error) {
      setState({
        ...state,
        opening: {
          status: 'error',
          message:
            error instanceof VenueOpeningApiError
              ? error.message
              : 'BeachOS could not confirm the opening. Check the connection and try again.',
        },
      });
    }
  }

  function updateOpening(opening: OpeningAction): void {
    setState((current) => (current.status === 'ready' ? { ...current, opening } : current));
  }

  return (
    <HostWorkspaceView
      state={state}
      onRetry={() => void loadContext()}
      onRequestOpen={() => updateOpening({ status: 'confirming' })}
      onConfirmOpen={() => void handleOpen()}
      onCancelOpen={() => updateOpening({ status: 'idle' })}
    />
  );
}
