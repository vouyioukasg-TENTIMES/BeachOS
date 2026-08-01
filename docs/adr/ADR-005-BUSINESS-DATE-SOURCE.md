# ADR-005 — Business Date Source

## Status

Proposed recommendation. This ADR is not accepted.

## Context

A Business Date is the Venue operating day to which activity belongs. Its boundary
may differ from midnight. Venue Opening, reports, uniqueness, operational timers,
and later financial work require every server instance and device to agree on the
same Business Date.

The exact rollover rule remains a Product Owner decision for each Venue. The
Application Layer already obtains Business Date through an interface rather than
accepting it as device authority.

## Problem

The platform needs an authoritative method for deriving Business Date that remains
correct across timezones, daylight-saving changes, restarts, multiple application
instances, and late-night operation.

## Options

1. **Server-derived Venue policy.** Combine authoritative time with the Venue’s
   approved IANA timezone and configured local rollover rule.
2. **Calendar date at midnight UTC.** Use the universal calendar date for every
   Venue.
3. **Calendar date at local midnight.** Use each Venue’s local calendar date with no
   configurable rollover.
4. **Client-provided Business Date.** Trust the tablet, phone, or desktop selection
   or clock.
5. **Manual daily activation.** Require an authorized person to select the Business
   Date directly.

## Recommended Option

Derive Business Date centrally from authoritative server time and a Venue-owned
policy containing an approved IANA timezone and approved local rollover time.
Expose the result through the Application-owned `BusinessDateProvider` interface.

Persist enough policy identity or historical context to explain how permanent
records received their Business Date. Reject protected operations when the Venue
policy is missing or cannot be evaluated safely. Do not select a default rollover
time in engineering; it requires Product Owner approval.

## Advantages

- All devices and server instances use one business rule.
- Supports hospitality work that continues after local midnight.
- IANA timezone rules handle historical and future daylight-saving changes better
  than fixed offsets.
- Keeps device clocks and user selection from becoming authoritative.
- Allows Venue-specific operation in a multi-venue platform.

## Disadvantages

- Requires Venue timezone and rollover configuration.
- Daylight-saving transitions and policy changes need explicit tests.
- Historical explanation becomes more complex if a Venue changes its policy.
- A missing or invalid policy must block sensitive operations.

## Risks

- An incorrect configured timezone or rollover assigns activity to the wrong day.
- Different deployed versions of timezone data could disagree.
- A policy change might silently reinterpret old records if history is not
  preserved.
- Ambiguous local times during daylight-saving changes could be mishandled.
- Treating local midnight as an implicit default would create an unapproved
  business rule.

## Future Impact

All future modules should request Business Date from the same Application port and
store the resolved value with permanent records. Multi-period days, exceptional
events, or manual correction require separate Product Owner decisions. Cross-Venue
reporting must retain each Venue’s original Business Date meaning rather than
recalculate history from current policy.
