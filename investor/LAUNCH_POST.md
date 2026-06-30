# Launch post — understated, evidence-led

## Short version (for X / LinkedIn / Hacker News "Show")

**Show: an OpenAI-compatible LLM gateway that returns a signed, verifiable receipt with every answer**

Most AI systems can't prove their own decisions. We built one that can.

`szl-router` is a sovereign, OpenAI-compatible gateway. Point any OpenAI client at it, and every response carries a signed receipt — which model served it, on whose hardware, at what tier — that you can verify independently with standard tools (`cosign`-compatible ECDSA-P256). Alter one byte and verification fails. No signing key? The receipt is honestly marked *unsigned* — never a false "verified."

Run it yourself:

```
docker run -p 8000:8000 -e GROQ_API_KEY=... ghcr.io/szl-holdings/szl-router:latest
```

Then `POST /v1/receipt/verify`, or tamper with a receipt and watch it fail.

Public data only. Runs on your own hardware. 33 public repos, passing CI. We'd rather you verify than trust us.

→ github.com/szl-holdings/szl-router

---

## Notes on tone (why it's written this way)

- **No adjectives doing the work.** No "revolutionary," "game-changing," "the future of." The claim is concrete and checkable; that's the persuasion.
- **The call to action is "verify," not "believe."** For a trust product, inviting scrutiny *is* the pitch. Skeptical engineers respect that and amplify it.
- **One product, one capability.** We lead with the single thing nobody else has (a verifiable per-decision receipt) and one way to experience it (`docker run`). No feature dump.
- **Traction stated plainly, only if true.** 12,400+ dataset downloads and live demos are facts; we state them once, without spin.

## Where to post (in order of fit)
1. **Hacker News** — "Show HN: An OpenAI-compatible gateway that signs a verifiable receipt for every answer." The HN crowd rewards run-it-yourself and honesty about limits.
2. **A short technical blog post** ("Why every AI decision should come with a receipt") cross-posted to the GitHub org and LinkedIn.
3. **The killinchu dataset page** — it already has 12,400+ downloads; add a one-line pointer from there to szl-router to convert existing attention.
