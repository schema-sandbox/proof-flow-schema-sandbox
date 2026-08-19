import type { AuthGateTranslations } from "../i18n";

type AuthGateProps = {
  apiKeyDraft: string;
  setApiKeyDraft: (value: string) => void;
  onConnect: () => void;
  message?: string;
  t?: AuthGateTranslations;
};

export function AuthGate({ apiKeyDraft, setApiKeyDraft, onConnect, message, t }: AuthGateProps) {
  return (
    <div className="auth-box">
      <h3>{t?.title ?? "API Authentication"}</h3>
      <p>{message ?? t?.defaultDesc ?? "Production mode requires an API key. Keys are saved only in this browser session."}</p>
      <input
        aria-label="API key"
        type="password"
        value={apiKeyDraft}
        onChange={(event) => setApiKeyDraft(event.target.value)}
        placeholder={t?.placeholder ?? "Enter one key from PROOFFLOW_API_KEYS"}
        onKeyDown={(event) => {
          if (event.key === "Enter" && apiKeyDraft.trim()) onConnect();
        }}
      />
      <button disabled={!apiKeyDraft.trim()} onClick={onConnect}>
        {t?.connectButton ?? "Connect API"}
      </button>
    </div>
  );
}