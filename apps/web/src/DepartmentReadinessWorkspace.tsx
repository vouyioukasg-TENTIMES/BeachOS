import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';

import {
  declareDepartmentReadiness,
  getDepartmentOwnerContext,
  readinessRequiresReason,
  type DepartmentOwnerContext,
  type ReadinessStatus,
} from './departmentReadinessApi';
import { VenueOpeningApiError } from './venueOpeningApi';

type WorkspaceState =
  | { status: 'identify' }
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; context: DepartmentOwnerContext };

interface Props {
  venueId: string;
}

function message(error: unknown): string {
  return error instanceof VenueOpeningApiError
    ? error.message
    : 'BeachOS could not confirm the current readiness state.';
}

export function DepartmentReadinessWorkspace({ venueId }: Props) {
  const [actorId, setActorId] = useState('');
  const [identifiedActor, setIdentifiedActor] = useState<string | null>(null);
  const [state, setState] = useState<WorkspaceState>({ status: 'identify' });
  const [status, setStatus] = useState<ReadinessStatus>('READY');
  const [reason, setReason] = useState('');
  const [comment, setComment] = useState('');
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [selectedDepartmentId, setSelectedDepartmentId] = useState<string | null>(null);

  useEffect(() => {
    if (!identifiedActor) return;
    const controller = new AbortController();
    setState({ status: 'loading' });
    void getDepartmentOwnerContext(venueId, identifiedActor, controller.signal)
      .then((context) => setState({ status: 'ready', context }))
      .catch((error: unknown) => {
        if (!controller.signal.aborted) setState({ status: 'error', message: message(error) });
      });
    return () => controller.abort();
  }, [identifiedActor, venueId]);

  function identify(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalized = actorId.trim();
    if (normalized) setIdentifiedActor(normalized);
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (state.status !== 'ready' || !identifiedActor) return;
    const department =
      state.context.departments.find((item) => item.department_id === selectedDepartmentId) ??
      state.context.departments[0];
    if (!department) return;
    setSaveError(null);
    setSaved(false);
    setSaving(true);
    try {
      await declareDepartmentReadiness({
        venueId,
        departmentId: department.department_id,
        actorId: identifiedActor,
        status,
        reason: status === 'READY' ? null : reason.trim() || null,
        comment: comment.trim() || null,
      });
      const context = await getDepartmentOwnerContext(venueId, identifiedActor);
      setState({ status: 'ready', context });
      setSaved(true);
      setReason('');
      setComment('');
    } catch (error: unknown) {
      setSaveError(message(error));
    } finally {
      setSaving(false);
    }
  }

  if (state.status === 'identify') {
    return (
      <main className="page-shell">
        <div className="centered-state">
          <form className="state-card owner-identification" onSubmit={identify}>
            <p className="eyebrow">Department Readiness</p>
            <h1>Identify yourself</h1>
            <p>Enter your staff identifier to see only the department assigned to you.</p>
            <label htmlFor="staff-identifier">Staff identifier</label>
            <input
              id="staff-identifier"
              value={actorId}
              onChange={(event) => setActorId(event.target.value)}
              autoComplete="username"
              required
            />
            <button className="primary-action" type="submit" disabled={!actorId.trim()}>
              Continue
            </button>
          </form>
        </div>
      </main>
    );
  }

  if (state.status === 'loading') {
    return (
      <main className="page-shell centered-state">
        <section className="state-card" role="status">
          <span className="spinner" aria-hidden="true" />
          <h1>Confirming your department</h1>
          <p>BeachOS is retrieving the current declaration.</p>
        </section>
      </main>
    );
  }

  if (state.status === 'error') {
    return (
      <main className="page-shell centered-state">
        <section className="state-card" role="alert">
          <h1>Department unavailable</h1>
          <p>{state.message}</p>
          <button
            className="secondary-action"
            type="button"
            onClick={() => setState({ status: 'identify' })}
          >
            Use another identity
          </button>
        </section>
      </main>
    );
  }

  const department =
    state.context.departments.find((item) => item.department_id === selectedDepartmentId) ??
    state.context.departments[0];
  if (!department) return null;
  const requiresReason = readinessRequiresReason(status);
  const current = department.current_readiness;

  return (
    <main className="page-shell">
      <header className="product-header">
        <span className="wordmark">BeachOS</span>
        <span>Department Readiness</span>
      </header>
      <div className="page-content readiness-owner-page">
        <p className="eyebrow">{state.context.venue_name}</p>
        <h1>{department.name}</h1>
        <p className="lede">Declare the department's current opening readiness.</p>

        {state.context.departments.length > 1 && (
          <label className="department-selector">
            Your department
            <select
              value={department.department_id}
              onChange={(event) => {
                setSelectedDepartmentId(event.target.value);
                setSaved(false);
                setSaveError(null);
              }}
            >
              {state.context.departments.map((item) => (
                <option value={item.department_id} key={item.department_id}>
                  {item.name}
                </option>
              ))}
            </select>
          </label>
        )}

        {state.context.opening_status === 'OPEN' ? (
          <section className="workspace-panel" role="status">
            <h2>The Venue is open</h2>
            <p>Opening readiness can no longer be changed for this Business Date.</p>
          </section>
        ) : (
          <form className="workspace-panel readiness-form" onSubmit={(event) => void submit(event)}>
            <fieldset disabled={saving}>
              <legend>Current status</legend>
              <div className="readiness-options">
                {(['READY', 'NOT READY', 'BLOCKED'] as const).map((option) => (
                  <label key={option}>
                    <input
                      type="radio"
                      name="readiness-status"
                      value={option}
                      checked={status === option}
                      onChange={() => setStatus(option)}
                    />
                    {option}
                  </label>
                ))}
              </div>
              {requiresReason && (
                <label>
                  Reason
                  <textarea
                    value={reason}
                    onChange={(event) => setReason(event.target.value)}
                    required
                  />
                </label>
              )}
              <label>
                Comment <span>(optional)</span>
                <textarea value={comment} onChange={(event) => setComment(event.target.value)} />
              </label>
              {saveError && (
                <p className="error-message" role="alert">
                  {saveError}
                </p>
              )}
              {saved && (
                <p className="success-message" role="status">
                  Readiness declaration saved.
                </p>
              )}
              <button
                className="primary-action"
                type="submit"
                disabled={saving || (requiresReason && !reason.trim())}
              >
                {saving ? 'Saving…' : current ? 'Update declaration' : 'Save declaration'}
              </button>
            </fieldset>
          </form>
        )}

        <section className="workspace-panel declaration-history" aria-labelledby="history-title">
          <h2 id="history-title">Declaration history</h2>
          {state.context.declaration_history.filter(
            (item) => item.department_id === department.department_id,
          ).length === 0 ? (
            <p>No declaration has been made for this Business Date.</p>
          ) : (
            <ol>
              {state.context.declaration_history
                .filter((item) => item.department_id === department.department_id)
                .map((item, index) => (
                  <li key={`${item.declared_at}-${index}`}>
                    <strong>{item.status}</strong>
                    {item.reason && <span> — {item.reason}</span>}
                    {item.comment && <p>{item.comment}</p>}
                    <time dateTime={item.declared_at}>
                      {new Date(item.declared_at).toLocaleString()}
                    </time>
                  </li>
                ))}
            </ol>
          )}
        </section>
      </div>
    </main>
  );
}
