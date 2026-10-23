// Rafla Design enquiry handler.
// Static files are served by the assets binding; only /api/* reaches this code.
// Recipients come from the ENQUIRY_TO secret (comma-separated, must be verified
// destination addresses in Cloudflare Email Routing). Mail is sent from info@rafladesign.com.
import { EmailMessage } from "cloudflare:email";

const FROM = "info@rafladesign.com";
const ORIGINS = ["https://rafladesign.com", "https://www.rafladesign.com"];

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

const clean = (v, max) => String(v ?? "").replace(/[\r\u0000]/g, "").trim().slice(0, max);
const oneLine = (v, max) => clean(v, max).replace(/\n+/g, " ");
const b64 = (str) => {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
};
const wrap = (s) => s.replace(/(.{76})/g, "$1\r\n");

function buildMime({ to, subject, replyTo, text }) {
  const headers = [
    `From: Rafla Design website <${FROM}>`,
    `To: ${to}`,
    replyTo ? `Reply-To: ${replyTo}` : null,
    `Subject: =?UTF-8?B?${b64(subject)}?=`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@rafladesign.com>`,
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="UTF-8"',
    "Content-Transfer-Encoding: base64",
  ].filter(Boolean);
  return headers.join("\r\n") + "\r\n\r\n" + wrap(b64(text)) + "\r\n";
}

async function handleEnquiry(request, env) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);

  const origin = request.headers.get("origin");
  if (origin && !ORIGINS.includes(origin) && !/\.workers\.dev$/.test(new URL(origin).hostname)) {
    return json({ ok: false, error: "origin" }, 403);
  }

  let form;
  try { form = await request.formData(); } catch { return json({ ok: false, error: "bad" }, 400); }

  // Honeypot: real people never fill this in. Pretend success so bots move on.
  if (clean(form.get("botcheck"), 50)) return json({ ok: true });

  const name = oneLine(form.get("name"), 120);
  const phone = oneLine(form.get("phone"), 40);
  const email = oneLine(form.get("email"), 160);
  const suburb = oneLine(form.get("suburb"), 80);
  const type = oneLine(form.get("project_type"), 80);
  const message = clean(form.get("message"), 3000);

  if (!name) return json({ ok: false, error: "name" }, 400);
  if (!phone && !email) return json({ ok: false, error: "contact" }, 400);
  const emailOk = /^[^\s@<>,;]+@[^\s@<>,;]+\.[^\s@<>,;]+$/.test(email);
  if (email && !emailOk) return json({ ok: false, error: "email" }, 400);

  const recipients = String(env.ENQUIRY_TO || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (!recipients.length) return json({ ok: false, error: "not-configured" }, 500);

  const subject = `New enquiry: ${name}${type ? " (" + type + ")" : ""}`;
  const text = [
    "New enquiry from rafladesign.com",
    "",
    `Name: ${name}`,
    `Phone: ${phone || "-"}`,
    `Email: ${email || "-"}`,
    `Property suburb: ${suburb || "-"}`,
    `Project: ${type || "-"}`,
    "",
    "Message:",
    message || "-",
    "",
    `Sent ${new Date().toISOString()}`,
  ].join("\r\n");

  let sent = 0;
  for (const to of recipients) {
    try {
      const raw = buildMime({ to, subject, replyTo: emailOk ? email : "", text });
      await env.EMAIL.send(new EmailMessage(FROM, to, raw));
      sent++;
    } catch (err) {
      console.error("send failed", to, String(err));
    }
  }
  return sent ? json({ ok: true }) : json({ ok: false, error: "send" }, 502);
}

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    // Old WordPress site was hit by casino spam under /projects/* and /blog/page/*.
    // 410 Gone tells Google to drop them faster than a 404.
    if (pathname.startsWith("/projects/") || pathname.startsWith("/blog/page/"))
      return new Response("Gone", { status: 410, headers: { "content-type": "text/plain", "x-robots-tag": "noindex" } });
    if (pathname === "/api/enquiry") return handleEnquiry(request, env);
    if (pathname.startsWith("/api/")) return json({ ok: false }, 404);
    return env.ASSETS.fetch(request);
  },
};
