#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const previewPath = path.join(__dirname, "..", "preview.html");
const html = fs.readFileSync(previewPath, "utf8");
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  resources: "usable",
  url: "file://" + previewPath,
});
const { window } = dom;

function fail(message) {
  console.error("FAIL:", message);
  process.exit(1);
}

setTimeout(() => {
  const doc = window.document;
  const sidebarSlot = doc.querySelector('[data-ad-slot="sidebar"]');
  const bottomSlot = doc.querySelector('[data-ad-slot="article-bottom"]');
  const sidebarIns = sidebarSlot && sidebarSlot.querySelector("ins.adsbygoogle");
  const bottomIns = bottomSlot && bottomSlot.querySelector("ins.adsbygoogle");
  const sidebarLabel = sidebarSlot && sidebarSlot.querySelector(":scope > .ad-label");
  const bottomLabel = bottomSlot && bottomSlot.querySelector(":scope > .ad-label");

  if (!sidebarIns) fail("sidebar slot should contain ins.adsbygoogle in place");
  if (!bottomIns) fail("article-bottom slot should contain ins.adsbygoogle in place");
  if (!sidebarLabel || sidebarLabel.textContent.trim() !== "AD") fail("sidebar should keep an AD label");
  if (!bottomLabel || bottomLabel.textContent.trim() !== "AD") fail("article-bottom should keep an AD label");
  if (sidebarSlot.hidden || sidebarSlot.classList.contains("is-hidden")) fail("sidebar slot should stay visible as placeholder");
  if (bottomSlot.hidden || bottomSlot.classList.contains("is-hidden")) fail("article-bottom slot should stay visible as placeholder");
  if (sidebarSlot.classList.contains("is-filled")) fail("unfilled sidebar should not look filled");
  if (bottomSlot.classList.contains("is-filled")) fail("unfilled article-bottom should not look filled");

  const hiddenLiveAds = doc.querySelectorAll("#ad-sources ins.adsbygoogle, #ad-sidebar ins.adsbygoogle, #ad-article-bottom ins.adsbygoogle");
  if (hiddenLiveAds.length) fail("sidebar/bottom ads should not live in hidden #ad-sources");

  console.log("OK: in-place ads stay visible as placeholders until filled");
  process.exit(0);
}, 80);
