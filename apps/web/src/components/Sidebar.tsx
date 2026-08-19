import { useState, type FormEvent } from "react";
import type { ProjectSummary } from "../api";
import type { SupportedLanguage, SidebarTranslations } from "../i18n";

type SidebarProps = {
  projects: ProjectSummary[];
  activeProjectId?: string;
  version?: string;
  busy: boolean;
  lang: SupportedLanguage;
  onLanguageChange: (lang: SupportedLanguage) => void;
  t: SidebarTranslations;
  onOpen: (id: string) => void;
  onCreate: (title: string, problem: string, notes: string) => Promise<boolean>;
};

export function Sidebar({
  projects,
  activeProjectId,
  version,
  busy,
  lang,
  onLanguageChange,
  t,
  onOpen,
  onCreate,
}: SidebarProps) {
  const [title, setTitle] = useState("");
  const [problem, setProblem] = useState("");
  const [notes, setNotes] = useState("");
  const [creating, setCreating] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim() || !problem.trim()) return;
    setCreating(true);
    try {
      await onCreate(title.trim(), problem.trim(), notes.trim());
      setTitle("");
      setProblem("");
      setNotes("");
    } finally {
      setCreating(false);
    }
  }

  return (
    <aside className="project-sidebar" aria-label={t.ariaLabel}>
      <div className="brand-block">
        <span className="brand-mark" aria-hidden="true">
          PF
        </span>
        <div className="brand-title-area">
          <h1>ProofFlow</h1>
          <p>{t.brandSubtitle}{version ? ` · ${version}` : ""}</p>
        </div>
      </div>

      <div className="lang-switcher-bar">
        <span className="lang-switcher-label">{t.langSwitcher}:</span>
        <div className="lang-toggle-group" role="group" aria-label="Language selection">
          <button
            type="button"
            className={`lang-btn ${lang === "en" ? "active" : ""}`}
            onClick={() => onLanguageChange("en")}
            aria-pressed={lang === "en"}
          >
            English
          </button>
          <button
            type="button"
            className={`lang-btn ${lang === "zh" ? "active" : ""}`}
            onClick={() => onLanguageChange("zh")}
            aria-pressed={lang === "zh"}
          >
            中文
          </button>
        </div>
      </div>

      <p className="constitution">{t.constitution}</p>

      <nav className="project-list" aria-label={t.researchProjects}>
        {projects.map((item) => (
          <button
            className={activeProjectId === item.project_id ? "active" : ""}
            key={item.project_id}
            disabled={busy}
            onClick={() => onOpen(item.project_id)}
          >
            <strong>{item.title}</strong>
            <span>{item.project_status.join(" / ")}</span>
          </button>
        ))}
        {!busy && projects.length === 0 && (
          <div className="empty-copy">{t.emptyCopy}</div>
        )}
      </nav>

      <form
        className="create-project"
        onSubmit={(event) => void submit(event)}
      >
        <strong>{t.newProject}</strong>
        <input
          aria-label={t.projectTitleAria}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder={t.projectTitlePlaceholder}
          required
        />
        <textarea
          aria-label={t.originalProblemAria}
          value={problem}
          onChange={(event) => setProblem(event.target.value)}
          placeholder={t.originalProblemPlaceholder}
          rows={3}
          required
        />
        <input
          aria-label={t.notesAria}
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
          placeholder={t.notesPlaceholder}
        />
        <button disabled={creating || busy} type="submit">
          {creating ? t.creatingButton : t.createButton}
        </button>
      </form>

      <div className="sidebar-rule">{t.sidebarRule}</div>
      <a className="workbench-link" href={`/prototype/${activeProjectId ? `?project=${activeProjectId}` : ""}`}>
        {t.workbenchLink}
      </a>
    </aside>
  );
}