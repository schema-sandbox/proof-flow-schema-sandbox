import { useState } from "react";
import type {
  ClaimAtomRecord,
  EvidenceCardRecord,
  ResearchStateSnapshot,
  TransitionProposalRecord,
} from "../api";
import type { SupportedLanguage, ControlPlaneTranslations } from "../i18n";

type ControlPlaneProps = {
  researchState: ResearchStateSnapshot | null;
  transitionProposals: TransitionProposalRecord[];
  claimAtoms: ClaimAtomRecord[];
  evidenceCards: EvidenceCardRecord[];
  lang: SupportedLanguage;
  t: ControlPlaneTranslations;
};

export function ControlPlane({
  researchState,
  transitionProposals,
  claimAtoms,
  evidenceCards,
  lang,
  t,
}: ControlPlaneProps) {
  const [openProposalId, setOpenProposalId] = useState<string | null>(null);
  const proposal =
    transitionProposals.find((item) => item.proposal_id === openProposalId) ??
    null;

  return (
    <section className="control-plane-panel" aria-label={t.ariaLabel}>
      <div className="section-heading">
        <div>
          <h3>{t.heading}</h3>
          <span>
            {t.meta(
              researchState?.revision ?? "—",
              transitionProposals.length,
              claimAtoms.length,
              evidenceCards.length,
            )}
          </span>
        </div>
        <span className="control-plane-note">{t.statusNote}</span>
      </div>
      <div className="plane-grid">
        {(["operational", "epistemic", "claim", "artifact"] as const).map((plane) => (
          <article key={plane} className="plane-card">
            <span>{plane}</span>
            <strong>{Object.keys(researchState?.[plane] ?? {}).length}</strong>
            <small>{t.planeCards[plane].desc}</small>
          </article>
        ))}
      </div>
      {transitionProposals.length > 0 && (
        <div className="proposal-strip">
          {transitionProposals
            .slice(-4)
            .reverse()
            .map((item) => (
              <button
                key={item.proposal_id}
                type="button"
                className={`proposal-chip proposal-status ${item.status.toLowerCase()}`}
                onClick={() => setOpenProposalId(item.proposal_id)}
                title={t.viewProposalDetails}
              >
                {item.status} · {item.trigger_class}
              </button>
            ))}
        </div>
      )}
      {proposal && (
        <details className="proposal-detail" open>
          <summary>
            {t.proposalSummary(proposal.proposal_id.slice(0, 8), proposal.status)}
          </summary>
          <p>
            {t.proposalMeta(
              proposal.trigger_class,
              new Date(proposal.created_at).toLocaleString(lang === "en" ? "en-US" : "zh-CN"),
              proposal.next_obligation_refs.length,
              proposal.handoff_refs.length,
            )}
          </p>
          <pre>{JSON.stringify(proposal.accepted_delta, null, 2)}</pre>
        </details>
      )}
      {(claimAtoms.length > 0 || evidenceCards.length > 0) && (
        <details className="claim-evidence">
          <summary>
            {t.claimEvidenceSummary(claimAtoms.length, evidenceCards.length)}
          </summary>
          <ul className="claim-list">
            {claimAtoms.map((claim) => (
              <li key={claim.claim_id}>
                <strong>
                  {claim.state} · {claim.source_class}
                </strong>
                <p>{claim.statement}</p>
                <small>{t.openObligations(claim.open_obligation_refs.length)}</small>
              </li>
            ))}
          </ul>
          <ul className="evidence-list">
            {evidenceCards.map((card) => (
              <li key={card.card_id}>
                <strong>{card.card_id.slice(0, 10)}…</strong>
                <span>
                  {Object.entries(card.dimensions)
                    .map(([dimension, value]) => `${dimension}:${value.status}`)
                    .join(" · ")}
                </span>
              </li>
            ))}
          </ul>
        </details>
      )}
    </section>
  );
}