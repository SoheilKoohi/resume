# Skills

Vendored Claude Code skills for resume and job-search work. They load
automatically in this repo.

| Source | Skills | License |
| --- | --- | --- |
| [varunr89/resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill) @ `9a4a0f2` | `resume-tailoring` | MIT (c) 2025 Varun Ramesh |
| [Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills) @ `74ae19e` | the other 22 | MIT (c) 2026 Resume Skills |

Vendored on 2026-08-20. Each skill directory keeps its upstream `LICENSE`.

`resume-tailoring` also ships its companion references
(`branching-questions.md`, `matching-strategies.md`, `multi-job-workflow.md`,
`research-prompts.md`); they live next to `SKILL.md` because the skill loads
them by bare filename.

## Note on this repo

These skills expect resumes as Markdown. The source of truth here is
`Soheil_Koohi_CV.yaml`. Use `rendercv_output/Soheil_Koohi_CV.md` (produced by
`make build`) as the Markdown input, and apply any accepted wording back into
the YAML — never edit the generated Markdown as if it were the original.

## Refresh

Re-clone upstream and copy `SKILL.md` files over the directories above.
