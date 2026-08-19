import type { SupportedLanguage } from "./i18n";

/** Display labels for API enums in English and Chinese. Values stay English on the wire. */

const ROUTE_STATE_ZH: Record<string, string> = {
  SEED: "种子",
  ACTIVE: "进行中",
  CHALLENGED: "被挑战",
  CONDITIONAL: "有条件",
  DORMANT: "休眠",
  REVIVED: "已复活",
  BRIDGE_RESULT: "桥接结果",
  SUPERSEDED: "已被替代",
  COMPLETED: "完成",
};

const ROUTE_STATE_EN: Record<string, string> = {
  SEED: "Seed",
  ACTIVE: "Active",
  CHALLENGED: "Challenged",
  CONDITIONAL: "Conditional",
  DORMANT: "Dormant",
  REVIVED: "Revived",
  BRIDGE_RESULT: "Bridge Result",
  SUPERSEDED: "Superseded",
  COMPLETED: "Completed",
};

const BRANCH_STATE_ZH: Record<string, string> = {
  ...ROUTE_STATE_ZH,
  COMPLETED: "完成",
};

const BRANCH_STATE_EN: Record<string, string> = {
  ...ROUTE_STATE_EN,
  COMPLETED: "Completed",
};

const CHALLENGE_TYPE_ZH: Record<string, string> = {
  OBJECTION: "异议",
  COUNTEREXAMPLE_SEARCH: "反例搜索",
  SOURCE_CHECK: "来源核查",
  QUANTIFIER_CHECK: "量词检查",
  FORMALIZATION_TEST: "形式化检验",
  COMPUTATIONAL_TEST: "计算检验",
  BOUNDARY_CASE: "边界情形",
  OTHER: "其他",
};

const CHALLENGE_TYPE_EN: Record<string, string> = {
  OBJECTION: "Objection",
  COUNTEREXAMPLE_SEARCH: "Counterexample Search",
  SOURCE_CHECK: "Source Check",
  QUANTIFIER_CHECK: "Quantifier Check",
  FORMALIZATION_TEST: "Formalization Test",
  COMPUTATIONAL_TEST: "Computational Test",
  BOUNDARY_CASE: "Boundary Case",
  OTHER: "Other",
};

const CHALLENGE_STATUS_ZH: Record<string, string> = {
  OPEN: "开放",
  RESOLVED: "已解决",
  DISMISSED: "已驳回",
  IN_PROGRESS: "处理中",
};

const CHALLENGE_STATUS_EN: Record<string, string> = {
  OPEN: "Open",
  RESOLVED: "Resolved",
  DISMISSED: "Dismissed",
  IN_PROGRESS: "In Progress",
};

const NOTE_TYPE_ZH: Record<string, string> = {
  GENERAL: "一般",
  INTUITION: "直觉",
  DEFINITION: "定义",
  COUNTEREXAMPLE: "反例",
  ROUTE_PRIORITY: "路线优先级",
  SIMPLIFICATION_GOAL: "简化目标",
  REDIRECT: "转向",
};

const NOTE_TYPE_EN: Record<string, string> = {
  GENERAL: "General",
  INTUITION: "Intuition",
  DEFINITION: "Definition",
  COUNTEREXAMPLE: "Counterexample",
  ROUTE_PRIORITY: "Route Priority",
  SIMPLIFICATION_GOAL: "Simplification Goal",
  REDIRECT: "Redirect",
};

const ARTIFACT_TYPE_ZH: Record<string, string> = {
  OTHER: "其他",
  TEXT: "文本",
  IMAGE: "图像",
  HAND_DRAWING: "手绘草图",
  CODE: "代码",
  GRAPH: "图",
  COUNTEREXAMPLE: "反例",
  PROOF_SOURCE: "证明源",
};

const ARTIFACT_TYPE_EN: Record<string, string> = {
  OTHER: "Other",
  TEXT: "Text",
  IMAGE: "Image",
  HAND_DRAWING: "Freehand Sketch",
  CODE: "Code",
  GRAPH: "Graph",
  COUNTEREXAMPLE: "Counterexample",
  PROOF_SOURCE: "Proof Source",
};

const KIND_ZH: Record<string, string> = {
  route: "路线",
  branch: "分支",
  challenge: "挑战",
  bridge: "桥接",
};

const KIND_EN: Record<string, string> = {
  route: "Route",
  branch: "Branch",
  challenge: "Challenge",
  bridge: "Bridge",
};

function formatRaw(val: string): string {
  return val
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/(^\w|\s\w)/g, (m) => m.toUpperCase());
}

function lookup(table: Record<string, string>, value: string, lang: SupportedLanguage): string {
  if (!value) return value;
  if (lang === "en") {
    return table[value] ?? formatRaw(value);
  }
  return table[value] ?? value.replaceAll("_", " ");
}

export function labelRouteState(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? ROUTE_STATE_EN : ROUTE_STATE_ZH, value, lang);
}

export function labelBranchState(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? BRANCH_STATE_EN : BRANCH_STATE_ZH, value, lang);
}

export function labelChallengeType(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? CHALLENGE_TYPE_EN : CHALLENGE_TYPE_ZH, value, lang);
}

export function labelChallengeStatus(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? CHALLENGE_STATUS_EN : CHALLENGE_STATUS_ZH, value, lang);
}

export function labelNoteType(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? NOTE_TYPE_EN : NOTE_TYPE_ZH, value, lang);
}

export function labelArtifactType(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? ARTIFACT_TYPE_EN : ARTIFACT_TYPE_ZH, value, lang);
}

export function labelKind(value: string, lang: SupportedLanguage = "zh"): string {
  return lookup(lang === "en" ? KIND_EN : KIND_ZH, value, lang);
}

export function labelEnum(value: string, lang: SupportedLanguage = "zh"): string {
  if (!value) return value;
  if (lang === "en") {
    return (
      ROUTE_STATE_EN[value] ??
      CHALLENGE_TYPE_EN[value] ??
      CHALLENGE_STATUS_EN[value] ??
      NOTE_TYPE_EN[value] ??
      ARTIFACT_TYPE_EN[value] ??
      formatRaw(value)
    );
  }
  return (
    ROUTE_STATE_ZH[value] ??
    CHALLENGE_TYPE_ZH[value] ??
    CHALLENGE_STATUS_ZH[value] ??
    NOTE_TYPE_ZH[value] ??
    ARTIFACT_TYPE_ZH[value] ??
    value.replaceAll("_", " ")
  );
}
